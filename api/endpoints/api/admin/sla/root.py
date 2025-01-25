from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from mayim.exception import RecordNotFound

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.sla_executor import SLAExecutor
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.deletion_post import DeletionPost
from api.models.requests.sla_post import SLAPost


class SLARoot(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        executor = Mayim.get(SLAExecutor)
        slas = await executor.get_all_slas()
        slas = [sla.to_dict() for sla in slas]

        return json({"slas": slas})

    @validate(form=SLAPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def post(self, request: Request, jwt_data: JWT_Data, form: SLAPost):
        executor = Mayim.get(SLAExecutor)

        slas = await executor.get_all_slas()
        for sla in slas:
            if sla.name == form.name:
                return json({"error": "SLA with this name already exists"}, status=400)
        try:
            await executor.create_sla(
                name=form.name, time_limit=form.time_limit, note=form.note
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=400)

        return json(
            {
                "status": "success",
                "message": "SLA added successfully",
            },
            status=201,
        )

    @validate(json=DeletionPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def delete(self, request: Request, jwt_data: JWT_Data, form: DeletionPost):
        executor = Mayim.get(SLAExecutor)

        # Check if both IDs are valid
        try:
            await executor.get_sla_by_id(form.delete)
        except RecordNotFound:
            return json({"error": "SLA to delete does not exist"}, status=400)

        try:
            await executor.get_sla_by_id(form.replacement)
        except RecordNotFound:
            return json({"error": "Replacement SLA does not exist"}, status=400)

        # Ensure that both IDs are not the same
        if form.delete == form.replacement:
            return json(
                {"error": "Replacement SLA cannot be the same as the SLA to delete"},
                status=400,
            )

        try:
            await executor.delete_sla(
                original_id=form.delete,
                replacement_id=form.replacement,
                user_id=jwt_data.uuid,
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=400)

        return json(
            {
                "status": "success",
                "message": "SLA deleted successfully",
            },
            status=200,
        )
