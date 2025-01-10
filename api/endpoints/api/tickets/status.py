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
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.ticket_status_form import TicketStatusForm
from api.models.enums import (
    MessageType,
    TicketResolution,
    TicketStatus as TicketStatusEnum,
)


class TicketStatus(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, ticket_id: UUID):
        executor = Mayim.get(TicketExecutor)
        try:
            ticket = await executor.get_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {"error": "Not Found", "message": "The requested ticket was not found"},
                status=404,
            )
        if (
            str(ticket.user_id) == jwt_data.uuid
            or jwt_data.is_support()
            or jwt_data.is_admin()
        ):
            return json(
                {
                    "status": "success",
                    "created_at": str(ticket.created_at),
                    "resolution_status": ticket.resolution_status,
                    "ticket_status": ticket.ticket_status,
                    "closed_at": str(ticket.closed_at) if ticket.closed_at else None,
                }
            )

        return json(
            {
                "error": "Forbidden",
                "message": "You do not have permission to view this ticket",
            },
            status=403,
        )

    @validate(form=TicketStatusForm, body_argument="form")
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def post(
        self,
        request: Request,
        jwt_data: JWT_Data,
        ticket_id: UUID,
        form: TicketStatusForm,
    ):
        ticket_executor = Mayim.get(TicketExecutor)
        message_executor = Mayim.get(MessageExecutor)
        try:
            ticket = await ticket_executor.get_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {"error": "Not Found", "message": "The requested ticket was not found"},
                status=404,
            )
        if (
            ticket.user_id == jwt_data.uuid
            or jwt_data.is_support()
            or jwt_data.is_admin()
        ):
            status = form.status
            resolution = form.resolution

            if status and resolution:
                return json(
                    {
                        "error": "Bad Request",
                        "message": "You cannot provide both a status and a resolution to update the ticket",
                    },
                    status=400,
                )

            elif status:
                if (
                    status == TicketStatusEnum.CLOSED
                    and ticket.ticket_status == TicketStatusEnum.OPEN
                ):
                    await ticket_executor.close_ticket(ticket_id)
                    await message_executor.create_text_message(
                        ticket_id,
                        user_id=jwt_data.uuid,
                        message=f"Ticket closed by {jwt_data.name}",
                        message_type=MessageType.SYSTEM,
                    )
                elif (
                    status == TicketStatusEnum.OPEN
                    and ticket.ticket_status == TicketStatusEnum.CLOSED
                ):
                    await ticket_executor.reopen_ticket(ticket_id)
                    await message_executor.create_text_message(
                        ticket_id,
                        user_id=jwt_data.uuid,
                        message=f"Ticket reopened by {jwt_data.name}",
                        message_type=MessageType.SYSTEM,
                    )
                else:
                    return json(
                        {
                            "error": "Bad Request",
                            "message": "Nothing to update. The ticket is already in the requested status",
                        },
                        status=400,
                    )
            elif resolution:
                if (
                    resolution == TicketResolution.RESOLVED
                    and ticket.resolution_status == TicketResolution.UNRESOLVED
                ):
                    await ticket_executor.update_ticket_resolution(
                        ticket_id=ticket_id, resolution=TicketResolution.RESOLVED
                    )
                    await message_executor.create_text_message(
                        ticket_id,
                        user_id=jwt_data.uuid,
                        message=f"Ticket marked as resolved by {jwt_data.name}",
                        message_type=MessageType.SYSTEM,
                    )
                elif (
                    resolution == TicketResolution.UNRESOLVED
                    and ticket.resolution_status == TicketResolution.RESOLVED
                ):
                    await ticket_executor.update_ticket_resolution(
                        ticket_id=ticket_id, resolution=TicketResolution.UNRESOLVED
                    )
                    await message_executor.create_text_message(
                        ticket_id,
                        user_id=jwt_data.uuid,
                        message=f"Ticket marked as unresolved by {jwt_data.name}",
                        message_type=MessageType.SYSTEM,
                    )
                else:
                    return json(
                        {
                            "error": "Bad Request",
                            "message": "Nothing to update. The ticket is already in the requested status",
                        },
                        status=400,
                    )
            else:
                return json(
                    {
                        "error": "Bad Request",
                        "message": "You must provide either a status or resolution to update the ticket",
                    },
                    status=400,
                )

            return json({"status": "success"})

        return json(
            {
                "error": "Forbidden",
                "message": "You do not have permission to update this ticket",
            },
            status=403,
        )
