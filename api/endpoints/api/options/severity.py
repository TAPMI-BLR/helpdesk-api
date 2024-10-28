from sanic import json
from sanic.views import HTTPMethodView


class SeverityOptions(HTTPMethodView):
    # TODO
    async def get(self, request):
        return json({"error": "Not implemented"}, status=501)
