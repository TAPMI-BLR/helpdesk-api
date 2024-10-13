from mayim import PostgresExecutor

from api.models.db.ticket import Ticket


class TicketExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/tickets/"

    async def get_my_tickets(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> list[Ticket]:
        """Get all tickets for a user"""

    async def get_ticket_by_id(self, ticket_id) -> Ticket:
        """Get a ticket by its ID"""

    async def get_open_tickets(self, limit: int = 10, offset: int = 0) -> list[Ticket]:
        """Get all open tickets"""

    async def create_ticket(self, user_id, title, description) -> Ticket:
        """Create a new ticket"""

    async def update_ticket_resolution(self, ticket_id: int, resolution: str) -> Ticket:
        """Update a ticket's resolution"""
