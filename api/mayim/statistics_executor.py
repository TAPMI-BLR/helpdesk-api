from uuid import UUID
from mayim import PostgresExecutor

from api.models.db.statistics import Statistics


class StatisticsExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/statistics/"

    async def get_categories_count(self) -> list[Statistics]:
        """get data of categories"""
        # query = self.get_query("get_categories_count").text
        # x = await self.run_sql(query=query, as_list=True)
        # print(x)

    async def get_resolution_status_count(self) -> list[Statistics]:
        """get data of resolution status"""

    async def get_subcategories_count(self, parent_id: UUID) -> list[Statistics]:
        """get data of subcategories"""

    async def get_ticket_status_count(self) -> list[Statistics]:
        """get data of ticket status"""
