from mayim import PostgresExecutor

from api.models.db.config import Config
from api.models.db.ticket import Ticket
from api.models.enums import TicketResolution, TicketStatus


class TicketExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/tickets/"

    async def get_my_tickets(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> list[Ticket]:
        """Get all tickets for a user"""

    async def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        """Get a ticket by its ID"""

    async def get_open_tickets(self, limit: int = 10, offset: int = 0) -> list[Ticket]:
        """Get all open tickets"""

    async def create_ticket(
        self, user_id: int, subcategory_id: int, title: str, config: Config
    ) -> Ticket:
        """Create a new ticket"""
        query = self.get_query("create_ticket")
        r = await self.run_sql(
            query.text,
            params={
                "user_id": user_id,
                "subcategory_id": subcategory_id,
                "title": title,
                "assignee_id": config.default_assignee,
                "severity": config.default_severity,
                "sla": config.default_sla,
            },
        )
        return self.hydrator.hydrate(r, Ticket)

    async def update_ticket_resolution(
        self, ticket_id: int, resolution: TicketResolution, name_of_updater: str
    ) -> Ticket:
        """Update a ticket's resolution"""

    async def update_ticket_status(
        self, ticket_id: int, status: TicketStatus, name_of_updater: str
    ) -> Ticket:
        """Update a ticket's status"""
