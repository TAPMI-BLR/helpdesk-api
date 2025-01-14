from mayim import Mayim
from mayim.exception import RecordNotFound
from psycopg.errors import UniqueViolation
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate


from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.user_executor import UserExecutor
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.staff_post import StaffPost
from api.models.requests.staff_query import StaffQuery


class StaffRoot(HTTPMethodView):
    @validate(query=StaffQuery)
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, query: StaffQuery):
        executor = Mayim.get(UserExecutor)
        if query.show_all:
            staff = await executor.get_all_staff()
        else:
            staff = await executor.get_active_staff()

        staff = [user.to_dict() for user in staff]

        return json({"staff": staff})

    @validate(form=StaffPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def post(self, request: Request, jwt_data: JWT_Data, form: StaffPost):
        executor = Mayim.get(UserExecutor)
        try:
            if form.user_id:
                user = await executor.get_user_by_id(form.user_id)
            elif form.email:
                user = await executor.get_user_by_email(form.email)
            else:
                return json({"error": "No email or user_id provided"}, status=400)
        except RecordNotFound:
            return json({"error": "User not found"}, status=404)

        try:
            await executor.create_staff(user.id, form.is_sys_admin)
        except UniqueViolation:
            return json({"error": "User is already staff"}, status=400)
        return json({"success": True})
