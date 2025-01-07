from uuid import UUID
from mayim import Mayim
from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.models.internal.jwt_data import JWT_Data
from api.mayim.category_executor import CategoryExecutor
from api.models.requests.category_form import CategoryForm


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
        parent_category = await category_executor.get_categories(category_id)
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

        sub_category = await category_executor.create_subcategory(
            parent_id=category_id, name=sub_category_name
        )
        return json(
            {
                "message": "Subcategory added successfully",
                "sub_category": sub_category.to_dict(),
            },
            status=201,
        )
