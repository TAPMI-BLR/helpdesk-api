from mayim import PostgresExecutor

from api.models.db.category import Category
from api.models.db.subcategory import SubCategory


class CategoryExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/categories/"

    async def get_categories(self) -> list[Category]:
        """Get all categories"""

    async def get_subcategories(self, parent_id: int) -> list[SubCategory]:
        """Get all subcategories for a category"""

    async def create_category(self, name: str):
        """Create a category"""

    async def create_subcategory(self, name: str, parent_id: int):
        """Create a subcategory"""
