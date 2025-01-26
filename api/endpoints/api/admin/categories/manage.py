from uuid import UUID
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


class CategoriesManage(HTTPMethodView):
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, category_id: UUID):
        category_executor = Mayim.get(CategoryExecutor)

        sub_categories = await category_executor.get_subcategories(
            parent_id=category_id
        )

        sub_categories = [sub_cat.to_dict() for sub_cat in sub_categories]

        return json({"sub_categories": sub_categories})

    @validate(form=CategoryForm, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def post(
        self,
        request: Request,
        jwt_data: JWT_Data,
        category_id: UUID,
        form: CategoryForm,
    ):
        category_executor = Mayim.get(CategoryExecutor)
        sub_category_name = form.name

        # Check if sub_category_name is empty
        if not sub_category_name:
            return json({"error": "Subcategory name cannot be empty"}, status=400)

        # Check if parent category exists
        parent_category = await category_executor.get_category_by_id(
            category_id=category_id
        )
        if not parent_category:
            return json({"error": "Parent category does not exist"}, status=404)

        # Check for duplicate subcategory
        existing_sub_categories = await category_executor.get_subcategories(
            parent_id=category_id
        )
        if any(
            sub_cat.name.lower() == sub_category_name.lower()
            for sub_cat in existing_sub_categories
        ):
            return json({"error": "Subcategory already exists"}, status=409)

        try:
            await category_executor.create_subcategory(
                parent_id=category_id,
                name=sub_category_name,
                colour=form.colour.as_hex(),
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=500)
        return json(
            {
                "status": "success",
                "message": "Subcategory added successfully",
            },
            status=201,
        )

    @validate(json=DeletionPost, body_argument="form")
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def delete(self, request: Request, jwt_data: JWT_Data, form: DeletionPost):
        """Delete a subcategory"""
        executor = Mayim.get(CategoryExecutor)

        # Check if both IDs are valid
        try:
            await executor.get_subcategory_by_id(form.delete)
        except RecordNotFound:
            return json({"error": "Subcategory to delete does not exist"}, status=400)

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
            await executor.delete_subcategory(
                original_id=form.delete,
                replacement_category_id=form.replacement,
                user_id=jwt_data.uuid,
            )
        except Exception as e:
            return json({"status": "failure", "error": str(e)}, status=400)
        return json(
            {
                "status": "success",
                "message": "Subcategory deleted successfully",
            },
            status=200,
        )
