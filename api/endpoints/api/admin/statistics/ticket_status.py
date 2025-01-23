from mayim import Mayim
from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.models.internal.jwt_data import JWT_Data
from api.mayim.statistics_executor import StatisticsExecutor


class TicketStatusCount(HTTPMethodView):
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        statistics_executor = Mayim.get(StatisticsExecutor)

        # Fetch all ticket status data count
        ticket_status_count = await statistics_executor.get_ticket_status_count()

        # return resolution status count
        ticket_status_count = [
            ticketStat_count.to_dict() for ticketStat_count in ticket_status_count
        ]

        return json({"ticket_status_count": ticket_status_count})
