from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.sla_executor import SLAExecutor
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.sla_post import SLAPost


class SLARoot(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        executor = Mayim.get(SLAExecutor)
        slas = await executor.get_all_slas()
        slas = [sla.to_dict() for sla in slas]

        return json({"slas": slas})

    @validate(form=SLAPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def post(self, request: Request, jwt_data: JWT_Data, form: SLAPost):
        executor = Mayim.get(SLAExecutor)

        slas = await executor.get_all_slas()
        for sla in slas:
            if sla.name == form.name:
                return json({"error": "SLA with this name already exists"}, status=400)
        try:
            await executor.create_sla(
                name=form.name, time_limit=form.time_limit, note=form.note
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=400)

        return json(
            {
                "status": "success",
                "message": "SLA added successfully",
            },
            status=201,
        )
