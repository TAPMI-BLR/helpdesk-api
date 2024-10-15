from sanic import Request, json
from sanic.views import HTTPMethodView


class TeamRoot(HTTPMethodView):
    # TODO
    async def get(self, request: Request):
        return json({"error": "Not implemented"}, status=501)
