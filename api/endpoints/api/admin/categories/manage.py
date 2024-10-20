from sanic import json
from sanic.views import HTTPMethodView
from sanic.request import Request

from api.decorators.require_role import require_role
from api.decorators.require_login import require_login
from api.models.internal.jwt_data import JWT_Data


class CategoriesManage(HTTPMethodView):
    # TODO
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, id: str):
        return json({"error": "Not implemented"}, status=501)
