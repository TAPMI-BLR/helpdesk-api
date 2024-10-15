from sanic.views import HTTPMethodView
from sanic import Request, json


class Ping(HTTPMethodView):
    # TODO
    async def get(self, request: Request):
        return json({"error": "Not implemented"}, status=501)
