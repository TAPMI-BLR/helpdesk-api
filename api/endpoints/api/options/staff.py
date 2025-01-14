from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.user_executor import UserExecutor
from api.models.internal.jwt_data import JWT_Data


class StaffOptions(HTTPMethodView):
    @require_login()
    @require_role(required_role="team", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        # TODO: Allow getting based on Category/SubCategory ID via Teams
        user_executor = Mayim.get(UserExecutor)
        staff = await user_executor.get_active_staff()
        staff = [user.to_dict() for user in staff]
        return json({"staff": staff})
