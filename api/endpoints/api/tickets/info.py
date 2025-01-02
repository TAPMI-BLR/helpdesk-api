from uuid import UUID
from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.message_executor import MessageExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.mayim.user_executor import UserExecutor
from api.models.enums import MessageType
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.ticket_assignee_form import TicketAssigneeForm


class TicketInfo(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, ticket_id: UUID):
        executor = Mayim.get(TicketExecutor)
        try:
            ticket = await executor.get_full_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {"error": "Not Found", "message": "The requested ticket was not found"},
                status=404,
            )

        if (
            str(ticket.user.id) == jwt_data.uuid
            or jwt_data.is_support()
            or jwt_data.is_admin()
        ):
            return json({"status": "success", "ticket": ticket.to_dict()})

        return json(
            {
                "error": "Forbidden",
                "message": "You do not have permission to view this ticket",
            },
            status=403,
        )

    @validate(form=TicketAssigneeForm, body_argument="form")
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def post(
        self,
        request: Request,
        jwt_data: JWT_Data,
        ticket_id: UUID,
        form: TicketAssigneeForm,
    ):
        ticket_executor = Mayim.get(TicketExecutor)
        user_executor = Mayim.get(UserExecutor)
        message_executor = Mayim.get(MessageExecutor)
        try:
            ticket = await ticket_executor.get_full_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {"error": "Not Found", "message": "The requested ticket was not found"},
                status=404,
            )

        if jwt_data.is_support() or jwt_data.is_admin():
            try:
                new_assignee = await user_executor.get_user_by_id(form.assignee_id)
            except RecordNotFound:
                return json(
                    {
                        "error": "Not Found",
                        "message": "The requested assignee was not found",
                    },
                    status=404,
                )

            if not new_assignee.is_team or not new_assignee.is_sys_admin:
                return json(
                    {
                        "error": "Bad Request",
                        "message": "The requested assignee is not a support team member",
                    },
                    status=400,
                )
            if new_assignee.id == ticket.assignee.id:
                return json(
                    {
                        "error": "Bad Request",
                        "message": "The requested assignee is already assigned to this ticket",
                    },
                    status=400,
                )
            if ticket.assignee.is_sys_admin and not jwt_data.is_admin():
                return json(
                    {
                        "error": "Forbidden",
                        "message": "You cannot reassign a ticket from an admin",
                    },
                    status=403,
                )

            await ticket_executor.update_ticket_assignee(ticket, new_assignee)
            await message_executor.create_text_message(
                ticket_id=ticket.id,
                user_id=jwt_data.uuid,
                message=f"Ticket has been reassigned to {new_assignee.name} by {jwt_data.name}",
                message_type=MessageType.SYSTEM,
            )
            return json({"status": "success"})

        return json(
            {
                "error": "Forbidden",
                "message": "You do not have permission to update this ticket",
            },
            status=403,
        )
