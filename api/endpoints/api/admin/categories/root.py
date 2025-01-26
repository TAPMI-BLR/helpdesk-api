from mayim import Mayim
from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import validate
from mayim.exception import RecordNotFound

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.models.internal.jwt_data import JWT_Data
from api.mayim.category_executor import CategoryExecutor
from api.models.requests.category_form import CategoryForm
from api.models.requests.deletion_post import DeletionPost


class CategoriesRoot(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        category_executor = Mayim.get(CategoryExecutor)

        # Fetch all categories
        categories = await category_executor.get_categories_with_children()

        # Convert categories to dictionary format
        categories = [category.to_dict() for category in categories]

        return json({"categories": categories})

    @validate(form=CategoryForm, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def post(
        self,
        request: Request,
        jwt_data: JWT_Data,
        form: CategoryForm,
    ):
        category_executor = Mayim.get(CategoryExecutor)
        category_name = form.name

        # Check if category_name is empty
        if not category_name:
            return json({"error": "Category name cannot be empty"}, status=400)

        # Check for duplicate category
        existing_categories = await category_executor.get_categories()
        if any(
            cat.name.lower() == category_name.lower() for cat in existing_categories
        ):
            return json({"error": "Category already exists"}, status=409)

        try:
            await category_executor.create_category(
                name=category_name, colour=form.colour.as_hex()
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=500)

        return json(
            {
                "status": "success",
                "message": "Category added successfully",
            },
            status=201,
        )

    @validate(json=DeletionPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def delete(self, request: Request, jwt_data: JWT_Data, form: DeletionPost):
        executor = Mayim.get(CategoryExecutor)

        # Check if category exists
        try:
            await executor.get_category_by_id(form.delete)
        except RecordNotFound:
            return json({"error": "Category to delete does not exist"}, status=400)

        # Check if replacement category exists
        try:
            await executor.get_category_by_id(form.replacement)
        except RecordNotFound:
            return json({"error": "Replacement Category does not exist"}, status=400)

        # Ensure that both IDs are not the same
        if form.delete == form.replacement:
            return json(
                {
                    "error": "Replacement Category cannot be the same as the Category to delete"
                },
                status=400,
            )

        try:
            await executor.delete_category(
                category_id=form.delete,
                replacement_id=form.replacement,
                user_id=jwt_data.uuid,
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=400)

        return json(
            {
                "status": "success",
                "message": "Category deleted successfully",
            },
        )
