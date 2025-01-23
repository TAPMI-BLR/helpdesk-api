from uuid import UUID
from mayim import Mayim
from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView

from api.decorators.require_login import require_login
from api.decorators.require_role import require_role
from api.models.internal.jwt_data import JWT_Data
from api.mayim.statistics_executor import StatisticsExecutor


class SubcategoriesCount(HTTPMethodView):
    @require_login()
    @require_role(required_role="sys_admin", allow_higher=True)
    async def get(self, request: Request, jwt_data: JWT_Data, category_id: UUID):
        statistics_executor = Mayim.get(StatisticsExecutor)

        # Fetch all subcategories data count
        subcategories_count = await statistics_executor.get_subcategories_count(
            parent_id=category_id
        )

        # return category count
        subcategories_count = [
            subcat_count.to_dict() for subcat_count in subcategories_count
        ]

        return json({"subcategories_count": subcategories_count})
