from mayim import PostgresExecutor


class UserExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/users/"

    async def get_user_by_id(self, user_id: int):
        """Get a user by their ID"""

    async def get_user_by_email(self, email: str):
        """Get a user by their email"""

    async def get_user_tickets(self, user_id: int):
        """Get all tickets for a user"""

    async def check_user_is_team_member(self, user_id: int):
        """Check if a user is a team member"""
