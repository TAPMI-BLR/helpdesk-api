from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from api.decorators.require_role import require_role
from api.decorators.require_login import require_login
from api.mayim.message_executor import MessageExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.models.internal.jwt_data import JWT_Data
from mayim.exception import RecordNotFound
from sanic_ext import validate

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
                    "error": "Limit and page must be positive integers, limit must be below 50"
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
            return json({"error": "Ticket not found"}, 404)

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
