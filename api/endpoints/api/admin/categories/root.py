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


class CategoriesRoot(HTTPMethodView):
    @require_login()
    @require_role(required_role="user", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        category_executor = Mayim.get(CategoryExecutor)

        # Fetch all categories
        categories = await category_executor.get_categories()

        # Convert categories to dictionary format
        categories = [category.to_dict() for category in categories]

        return json({"categories": categories})

    @validate(form=CategoryForm)
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def post(
        self,
        request: Request,
        jwt_data: JWT_Data,
        form: CategoryForm,
    ):
        category_executor = Mayim.get(CategoryExecutor)
        category_name = request.json.get(CategoryForm)

        # Check if category_name is empty
        if not category_name:
            return json({"error": "Category name cannot be empty"}, status=400)

        # Check for duplicate category
        existing_categories = await category_executor.get_categories()
        if any(cat.name == category_name for cat in existing_categories):
            return json({"error": "Category already exists"}, status=409)

        category = await category_executor.create_category(name=category_name)
        return json(
            {
                "message": "Category added successfully",
                "Category": category.to_dict(),
            },
            status=201,
        )
