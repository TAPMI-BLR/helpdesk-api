from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from api.models.enums import TicketResolution, TicketStatus


@dataclass(frozen=True)
class Ticket:
    id: UUID
    title: str
    user_id: UUID
    subcategory_id: UUID
    assignee_id: UUID
    severity_id: UUID
    sla_id: UUID
    created_at: datetime
    closed_at: datetime | None
    resolution_status: TicketResolution
    ticket_status: TicketStatus

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "user_id": str(self.user_id),
            "subcategory_id": str(self.subcategory_id),
            "assignee_id": str(self.assignee_id),
            "severity": str(self.severity_id),
            "sla": str(self.sla_id),
            "created_at": str(self.created_at),
            "closed_at": str(self.closed_at) if self.closed_at else None,
            "resolution_status": self.resolution_status,
            "ticket_status": self.ticket_status,
        }
