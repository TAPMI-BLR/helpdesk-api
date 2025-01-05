from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.sla_executor import SLAExecutor
from api.models.internal.jwt_data import JWT_Data


class SLAOptions(HTTPMethodView):
    @require_login()
    @require_role(required_role="team", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        sla_executor = Mayim.get(SLAExecutor)
        sla_options = await sla_executor.get_all_slas()
        sla_options = [sla.to_dict() for sla in sla_options]
        return json({"slas": sla_options})
