from mayim import PostgresExecutor

from api.models.db.user import User
from json import dumps


class UserExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/users/"

    async def get_user_by_id(self, user_id: int) -> User:
        """Get a user by their ID"""

    async def get_user_by_email(self, email: str) -> User:
        """Get a user by their email"""

    async def create_user(self, name: str, email: str, data: dict):
        """Create a user"""
        query = self.get_query("create_user")
        return await self.run_sql(
            query.text,
            params={"name": name, "email": email, "data": dumps(data)},
            no_result=True,
        )
