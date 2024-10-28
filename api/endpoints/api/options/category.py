from sanic import json
from sanic.views import HTTPMethodView


class CategoryOptions(HTTPMethodView):
    # TODO
    async def get(self, request):
        return json({"error": "Not implemented"}, status=501)
