from uuid import UUID
from mayim import PostgresExecutor

from api.models.db.config import Config
from api.models.db.populated.full_ticket import FullTicket
from api.models.db.ticket import Ticket
from api.models.enums import TicketResolution


class TicketExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/tickets/"
    limit_page_filter = " LIMIT $limit OFFSET $offset"

    async def get_full_ticket_by_id(self, ticket_id: UUID) -> FullTicket:
        """Get a full ticket by its ID"""

    async def get_tickets_as_user(
        self, user_id: int, limit: int = 10, offset: int = 0, show_closed: bool = False
    ) -> list[Ticket]:
        """Get all tickets for a user"""
        fragment = self.get_query("fragment_get_ticket").text
        user_filter = " WHERE user_id = $user_id"
        status_filter = ""
        if not show_closed:
            status_filter = " AND ticket_status = 'OPEN'"
        query = fragment + user_filter + status_filter + self.limit_page_filter

        return await self.execute(
            query,
            model=Ticket,
            params={
                "user_id": user_id,
                "limit": limit,
                "offset": offset,
            },
            as_list=True,
        )

    async def get_ticket_by_id(self, ticket_id: UUID) -> Ticket:
        """Get a ticket by its ID"""
        fragment = self.get_query("fragment_get_ticket").text
        id_filter = " WHERE id = $ticket_id"
        query = fragment + id_filter
        return await self.execute(query, model=Ticket, params={"ticket_id": ticket_id})

    async def get_tickets_as_team(
        self, limit: int = 10, offset: int = 0, show_closed: bool = False
    ) -> list[Ticket]:
        """Get tickets as a team member"""
        fragment = self.get_query("fragment_get_ticket").text
        status_filter = ""
        if not show_closed:
            status_filter = " AND ticket_status = 'OPEN'"
        query = fragment + status_filter + self.limit_page_filter

        return await self.execute(
            query,
            model=Ticket,
            params={"limit": limit, "offset": offset},
            as_list=True,
        )

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
        self, ticket_id: UUID, resolution: TicketResolution, name_of_updater: str
    ) -> Ticket:
        """Update a ticket's resolution"""

    async def close_ticket(self, ticket_id: UUID) -> None:
        """Mark a ticket as closed"""

    async def reopen_ticket(self, ticket_id: UUID) -> None:
        """Reopen a closed ticket"""

    async def update_ticket_assignee(self, ticket_id: UUID, assignee_id: int) -> Ticket:
        """Update a ticket's assignee"""
