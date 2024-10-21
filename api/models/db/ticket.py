from dataclasses import dataclass
from datetime import datetime

from api.models.enums import TicketResolution, TicketStatus


@dataclass(frozen=True)
class Ticket:
    id: int
    title: str
    user_id: int
    subcategory_id: int
    assignee_id: int
    severity: str
    sla: str
    created_at: datetime
    closed_at: datetime | None
    is_resolved: TicketResolution
    is_closed: TicketStatus

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "subcategory_id": self.subcategory_id,
            "assignee_id": self.assignee_id,
            "severity": self.severity,
            "sla": self.sla,
            "created_at": str(self.created_at),
            "closed_at": str(self.closed_at) if self.closed_at else None,
            "is_resolved": self.is_resolved,
            "is_closed": self.is_closed,
        }
