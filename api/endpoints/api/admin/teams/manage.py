from sanic import Request, json
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.models.internal.jwt_data import JWT_Data


class TeamManage(HTTPMethodView):
    # TODO
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, team_id: int):
        return json({"error": "Not implemented"}, status=501)
