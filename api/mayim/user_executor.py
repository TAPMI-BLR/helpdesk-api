from mayim import PostgresExecutor

from api.models.db.user import User


class UserExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/users/"

    async def get_user_by_id(self, user_id: int) -> User:
        """Get a user by their ID"""

    async def get_user_by_email(self, email: str) -> User:
        """Get a user by their email"""

    async def create_user(self, name: str, email: str, data: dict) -> User:
        """Create a user"""
