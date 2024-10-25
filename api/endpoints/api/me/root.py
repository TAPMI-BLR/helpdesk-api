from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from api.decorators.require_role import require_role
from api.decorators.require_login import require_login
from api.mayim.user_executor import UserExecutor
from api.models.internal.jwt_data import JWT_Data


class MeRoot(HTTPMethodView):
    # TODO
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        # Get User Executor
        executor = Mayim.get(UserExecutor)

        # Get the User
        user = await executor.get_user_by_id(jwt_data.uuid)

        # Return the User
        return json({"status": "success", "user": user.to_dict()})
