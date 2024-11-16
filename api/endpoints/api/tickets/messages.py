from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, json
from sanic.log import logger
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.message_executor import MessageExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.models.enums import MessageType
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.message_form import MessageForm
from api.models.requests.message_query_params import MessageQueryParams


class TicketMessages(HTTPMethodView):
    @validate(query=MessageQueryParams)
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(
        self,
        request: Request,
        jwt_data: JWT_Data,
        ticket_id: int,
        query: MessageQueryParams,
    ):
        # Get query params
        limit = query.limit
        page = query.page

        # Ensure that both numbers are positive and in range
        try:
            assert limit > 0
            assert limit <= 50
            assert page >= 0
        except AssertionError:
            return json(
                {
                    "error": "Invalid parameters",
                    "message": (
                        "Limit must be a positive integer less than or equal to 50,"
                        " and page must be a non-negative integer."
                    ),
                },
                400,
            )

        # Get executors
        ticket_executor = Mayim.get(TicketExecutor)
        message_executor = Mayim.get(MessageExecutor)

        # Get Ticket by ID
        try:
            ticket = await ticket_executor.get_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {
                    "error": "Ticket not found",
                    "message": "The requested ticket does not exist.",
                },
                404,
            )

        # Get Messages by Ticket ID
        offset = limit * page
        messages = await message_executor.get_messages(
            ticket_id, limit=limit, offset=offset
        )

        message = [msg.to_dict() for msg in messages]

        # If user owns the ticket
        if ticket.user_id == jwt_data.uuid:
            return json({"status": "success", "messages": message}, 200)

        # If user is an admin
        elif jwt_data.is_admin():
            return json({"status": "success", "messages": message}, 200)

        # If user is assigned to the ticket
        elif ticket.assignee_id == jwt_data.uuid:
            return json({"status": "success", "messages": message}, 200)

        # If user is a team member
        elif jwt_data.is_support():
            return json({"status": "success", "messages": message}, 200)

        else:
            return json({"error": "Unauthorized"}, 403)

    @validate(form=MessageForm, body_argument="form")
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def post(
        self, request: Request, jwt_data: JWT_Data, ticket_id: int, form: MessageForm
    ):
        # Get executors
        ticket_executor = Mayim.get(TicketExecutor)
        message_executor = Mayim.get(MessageExecutor)

        # Get Ticket by ID
        try:
            ticket = await ticket_executor.get_ticket_by_id(ticket_id)
        except RecordNotFound:
            return json(
                {
                    "error": "Ticket not found",
                    "message": "The requested ticket does not exist.",
                },
                404,
            )

        # Check if user is allowed to post a message and set message type
        if ticket.user_id == jwt_data.uuid:
            message_type = MessageType.USER
        elif jwt_data.is_admin() or jwt_data.is_support():
            message_type = MessageType.SUPPORT
        else:
            return json(
                {
                    "error": "Unauthorized",
                    "message": "You do not have permission to post a message on this ticket.",
                },
                403,
            )

        # Get message data
        message = form.content
        file = form.file

        # Create message
        if file:
            return json(
                {
                    "error": "Not Implemented",
                    "message": "File uploads are not supported yet.",
                },
                501,
            )
        else:
            try:
                await message_executor.create_text_message(
                    ticket_id, jwt_data.uuid, message, message_type
                )
            except RecordNotFound:
                return json(
                    {
                        "error": "Ticket not found",
                        "message": "The requested ticket does not exist.",
                    },
                    404,
                )
            except Exception as e:
                logger.error(e)
                return json(
                    {
                        "error": "Internal Server Error",
                        "message": "An unexpected error occurred while creating the message.",
                    },
                    500,
                )
        return json({"status": "success"}, 200)
