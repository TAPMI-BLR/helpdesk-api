from uuid import UUID
from mayim import PostgresExecutor

from api.models.db.user import User


class TeamExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/teams/"

    async def get_members_by_category_id(self, category_id: UUID) -> list[User]:
        """Get all members by category"""

    async def add_member_to_category_team(self, category_id: UUID, user_id: UUID):
        """Add a member to a team"""

    async def remove_member_from_category_team(self, category_id: UUID, user_id: UUID):
        """Remove a member from a team"""
