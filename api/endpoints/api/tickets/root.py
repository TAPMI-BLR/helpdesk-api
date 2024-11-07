from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_role import require_role
from api.decorators.require_login import require_login
from api.mayim.ticket_executor import TicketExecutor
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.tickets_query import TicketsQuery


class TicketRoot(HTTPMethodView):
    @validate(query=TicketsQuery)
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, query: TicketsQuery):
        # Get Page
        page = query.page
        limit = query.limit
        # Ensure limit is under 50
        try:
            assert limit <= 50
            assert limit > 0
        except AssertionError:
            return json({"error": "Limit must be between 1 and 50"}, status=400)
        offset = page * limit
        # Get Ticket Executor
        executor = Mayim.get(TicketExecutor)

        if query.as_user:
            # Get Tickets as User
            # TODO: Flag to show closed tickets
            tickets = await executor.get_my_tickets(
                user_id=jwt_data.uuid,
                offset=offset,
            )
        else:
            # Check if user has role of team or sys_admin in jwt_data.roles list
            if "team" in jwt_data.roles or "sys_admin" in jwt_data.roles:
                # Get Tickets as Team
                # TODO: Get ALL tickets (with show closed flag) query in executor
                tickets = await executor.get_open_tickets(
                    offset=offset,
                    limit=limit,
                )
            else:
                return json({"error": "Unauthorized"}, status=403)
        return json(
            {"ststus": "success", "tickets": [ticket.to_dict() for ticket in tickets]}
        )
