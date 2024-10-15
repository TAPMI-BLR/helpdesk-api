from sanic import json
from sanic.views import HTTPMethodView
from sanic.request import Request


class CategoriesManage(HTTPMethodView):
    # TODO
    async def get(self, request: Request):
        return json({"error": "Not implemented"}, status=501)
