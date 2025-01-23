from mayim import Mayim
from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.models.internal.jwt_data import JWT_Data
from api.mayim.statistics_executor import StatisticsExecutor


class ResolutionStatusCount(HTTPMethodView):
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        statistics_executor = Mayim.get(StatisticsExecutor)

        # Fetch all resolution status data count
        resolution_status_count = (
            await statistics_executor.get_resolution_status_count()
        )

        # return resolution status count
        resolution_status_count = [
            ResolStat_count.to_dict() for ResolStat_count in resolution_status_count
        ]

        return json({"resolution_status_count": resolution_status_count})
