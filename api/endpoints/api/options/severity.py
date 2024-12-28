from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.severity_executor import SeverityExecutor


class SeverityOptions(HTTPMethodView):
    @require_login()
    @require_role(required_role="team", allow_higher=True)
    async def get(self, request: Request):
        severity_executor = Mayim.get(SeverityExecutor)
        severities = await severity_executor.get_all_severity_levels()
        severities = [severity.to_dict() for severity in severities]
        return json({"levels": severities})
