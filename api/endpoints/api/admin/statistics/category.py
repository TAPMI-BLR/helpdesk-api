from mayim import Mayim
from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.models.internal.jwt_data import JWT_Data
from api.mayim.statistics_executor import StatisticsExecutor


class CategoriesCount(HTTPMethodView):
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data):
        statistics_executor = Mayim.get(StatisticsExecutor)

        # Fetch all categories data count
        categories_count = await statistics_executor.get_categories_count()

        print(categories_count)

        # return category count
        categories_count = [cat_count.to_dict() for cat_count in categories_count]

        return json({"categories_count": categories_count})
