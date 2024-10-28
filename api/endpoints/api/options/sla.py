from sanic import json
from sanic.views import HTTPMethodView


class SLAOptions(HTTPMethodView):
    # TODO
    async def get(self, request):
        return json({"error": "Not implemented"}, status=501)
