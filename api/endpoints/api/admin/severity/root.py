from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from mayim.exception import RecordNotFound

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.mayim.severity_executor import SeverityExecutor
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.deletion_post import DeletionPost
from api.models.requests.severity_post import SeverityPost


class SeverityRoot(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        executor = Mayim.get(SeverityExecutor)
        severity_levels = await executor.get_all_severity_levels()
        levels = [level.to_dict() for level in severity_levels]

        return json({"severity": levels})

    @validate(form=SeverityPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def post(self, request: Request, jwt_data: JWT_Data, form: SeverityPost):
        executor = Mayim.get(SeverityExecutor)

        severity_levels = await executor.get_all_severity_levels()
        for level in severity_levels:
            if level.name == form.name:
                return json(
                    {"error": "Severity with this name already exists"}, status=400
                )
        try:
            await executor.create_severity(
                name=form.name,
                level=form.level,
                note=form.note,
                colour=form.colour.as_hex(),
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=400)

        return json(
            {
                "status": "success",
                "message": "Severity added successfully",
            },
            status=201,
        )

    @validate(json=DeletionPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def delete(self, request: Request, jwt_data: JWT_Data, form: DeletionPost):
        executor = Mayim.get(SeverityExecutor)

        # Check if both IDs are valid
        try:
            await executor.get_severity_by_id(form.delete)
        except RecordNotFound:
            return json({"error": "Severity to delete does not exist"}, status=400)

        try:
            await executor.get_severity_by_id(form.replacement)
        except RecordNotFound:
            return json({"error": "Replacement Severity does not exist"}, status=400)

        # Ensure that both IDs are not the same
        if form.delete == form.replacement:
            return json(
                {
                    "error": "Replacement Severity cannot be the same as the Severity to delete"
                },
                status=400,
            )

        try:
            await executor.delete_severity(
                original_id=form.delete,
                replacement_id=form.replacement,
                user_id=jwt_data.uuid,
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=400)

        return json(
            {
                "status": "success",
                "message": "Severity deleted successfully",
            },
            status=200,
        )
