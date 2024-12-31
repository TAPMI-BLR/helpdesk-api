from mayim import Mayim
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate

from api.decorators.require_login import require_login
from api.mayim.category_executor import CategoryExecutor
from api.models.requests.category_options_query import CategoryOptionsQuery


class CategoryOptions(HTTPMethodView):
    @validate(query=CategoryOptionsQuery)
    @require_login()
    async def get(self, request: Request, query: CategoryOptionsQuery):
        category_executor = Mayim.get(CategoryExecutor)
        options = []
        if query.category_id:
            options = await category_executor.get_subcategories(
                parent_id=query.category_id
            )
        else:
            options = await category_executor.get_categories()

        options = [option.to_dict() for option in options]
        return json({"options": options})
