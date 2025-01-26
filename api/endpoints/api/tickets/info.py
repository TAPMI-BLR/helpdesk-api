from uuid import UUID
from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.category_executor import CategoryExecutor
from api.mayim.message_executor import MessageExecutor
from api.mayim.severity_executor import SeverityExecutor
from api.mayim.sla_executor import SLAExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.mayim.user_executor import UserExecutor
from api.models.db.populated.full_ticket import FullTicket
from api.models.enums import MessageType
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.ticket_update_form import TicketUpdateForm


class TicketInfo(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, ticket_id: UUID):
        executor = Mayim.get(TicketExecutor)
        try:
            ticket = await executor.get_ticket_by_id(ticket_id, require_full=True)
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

    @validate(form=TicketUpdateForm, body_argument="form")
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def post(
        self,
        request: Request,
        jwt_data: JWT_Data,
        ticket_id: UUID,
        form: TicketUpdateForm,
    ):
        ticket_executor = Mayim.get(TicketExecutor)
        user_executor = Mayim.get(UserExecutor)
        message_executor = Mayim.get(MessageExecutor)
        sla_executor = Mayim.get(SLAExecutor)
        severity_executor = Mayim.get(SeverityExecutor)
        category_executor = Mayim.get(CategoryExecutor)

        # Check if the ticket exists
        try:
            ticket: FullTicket = await ticket_executor.get_ticket_by_id(
                ticket_id, require_full=True
            )
        except RecordNotFound:
            return json(
                {"error": "Not Found", "message": "The requested ticket was not found"},
                status=404,
            )

        # Ensure that something has been changed
        if (
            not form.subcategory_id
            and not form.assignee_id
            and not form.severity_id
            and not form.sla_id
        ):
            return json(
                {
                    "error": "Bad Request",
                    "message": "No changes were requested for this ticket",
                },
                status=400,
            )

        # Only allow one change at a time
        if (
            (
                form.subcategory_id
                and (form.assignee_id or form.severity_id or form.sla_id)
            )
            or (
                form.assignee_id
                and (form.subcategory_id or form.severity_id or form.sla_id)
            )
            or (
                form.severity_id
                and (form.subcategory_id or form.assignee_id or form.sla_id)
            )
            or (
                form.sla_id
                and (form.subcategory_id or form.assignee_id or form.severity_id)
            )
        ):
            return json(
                {
                    "error": "Bad Request",
                    "message": "Only one change is allowed at a time",
                },
                status=400,
            )

        # Update ticket category
        if (
            str(ticket.user.id) == jwt_data.uuid
            or jwt_data.is_support()
            or jwt_data.is_admin()
        ) and form.subcategory_id:
            try:
                new_category = await category_executor.get_subcategory_by_id(
                    form.subcategory_id
                )
            except RecordNotFound:
                return json(
                    {
                        "error": "Not Found",
                        "message": "The requested category was not found",
                    },
                    status=404,
                )

            if new_category.id == ticket.subcategory.id:
                return json(
                    {
                        "error": "Bad Request",
                        "message": "The requested category is already assigned to this ticket",
                    },
                    status=400,
                )

            await ticket_executor.update_ticket_subcategory(ticket.id, new_category.id)
            await message_executor.create_text_message(
                ticket_id=ticket.id,
                user_id=jwt_data.uuid,
                message=f"Ticket category has been updated to {new_category.name} by {jwt_data.name}",
                message_type=MessageType.SYSTEM,
            )

            return json({"status": "success"})

        if jwt_data.is_support() or jwt_data.is_admin():
            # Update ticket severity
            if form.severity_id:
                try:
                    new_severity = await severity_executor.get_severity_by_id(
                        form.severity_id
                    )
                except RecordNotFound:
                    return json(
                        {
                            "error": "Not Found",
                            "message": "The requested severity was not found",
                        },
                        status=404,
                    )

                if new_severity.id == ticket.severity.id:
                    return json(
                        {
                            "error": "Bad Request",
                            "message": "The requested severity is already assigned to this ticket",
                        },
                        status=400,
                    )

                await ticket_executor.update_ticket_severity(ticket.id, new_severity.id)
                await message_executor.create_text_message(
                    ticket_id=ticket.id,
                    user_id=jwt_data.uuid,
                    message=f"Ticket severity has been updated to {new_severity.name} by {jwt_data.name}",
                    message_type=MessageType.SYSTEM,
                )

                return json({"status": "success"})
            # Update ticket SLA
            if form.sla_id:
                try:
                    new_sla = await sla_executor.get_sla_by_id(form.sla_id)
                except RecordNotFound:
                    return json(
                        {
                            "error": "Not Found",
                            "message": "The requested SLA was not found",
                        },
                        status=404,
                    )

                if new_sla.id == ticket.sla.id:
                    return json(
                        {
                            "error": "Bad Request",
                            "message": "The requested SLA is already assigned to this ticket",
                        },
                        status=400,
                    )

                await ticket_executor.update_ticket_sla(ticket.id, new_sla.id)
                await message_executor.create_text_message(
                    ticket_id=ticket.id,
                    user_id=jwt_data.uuid,
                    message=f"Ticket SLA has been updated to {new_sla.name} by {jwt_data.name}",
                    message_type=MessageType.SYSTEM,
                )

                return json({"status": "success"})
            # Update ticket assignee
            if form.assignee_id:
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

                await ticket_executor.update_ticket_assignee(ticket.id, new_assignee.id)
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
                "message": "You do not have permission to update this property",
            },
            status=403,
        )
