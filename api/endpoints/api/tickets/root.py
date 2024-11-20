from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
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
            return json(
                {
                    "error": "Invalid Parameters",
                    "message": "Limit must be between 1 and 50",
                },
                status=400,
            )
        offset = page * limit
        # Get Ticket Executor
        executor = Mayim.get(TicketExecutor)

        if query.as_user:
            # Get Tickets as User
            tickets = await executor.get_tickets_as_user(
                user_id=jwt_data.uuid,
                offset=offset,
                show_closed=query.show_closed,
            )
        else:
            # Check if user has role of team or sys_admin in jwt_data.roles list
            if "team" in jwt_data.roles or "sys_admin" in jwt_data.roles:
                # Get Tickets as Team
                tickets = await executor.get_tickets_as_team(
                    offset=offset,
                    limit=limit,
                    show_closed=query.show_closed,
                )
            else:
                return json(
                    {
                        "error": "Forbidden",
                        "message": "You do not have the required role to access these tickets",
                    },
                    status=403,
                )

        return json(
            {"status": "success", "tickets": [ticket.to_dict() for ticket in tickets]}
        )
