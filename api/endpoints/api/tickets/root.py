from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView

from api.decorators.require_role import require_role
from api.decorators.require_login import require_login
from api.mayim.ticket_executor import TicketExecutor
from api.models.internal.jwt_data import JWT_Data


class TicketRoot(HTTPMethodView):
    # TODO: If Team or Admin, return all tickets
    # TODO: Add Pagination
    # TODO: Flag to show closed tickets
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        # Get Page
        page = request.args.get("page", 0)
        # Get Ticket Executor
        executor = Mayim.get(TicketExecutor)
        # Get Tickets
        tickets = await executor.get_my_tickets(
            user_id=jwt_data.uuid, limit=10, offset=page * 10
        )
        # Generate Response
        return json({"tickets": [ticket.to_dict() for ticket in tickets]})
