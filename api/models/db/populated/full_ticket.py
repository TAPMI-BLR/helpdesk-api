from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from api.models.db.populated.full_subcategory import FullSubCategory
from api.models.db.severity import Severity
from api.models.db.sla import SLA
from api.models.db.user import User
from api.models.enums import TicketResolution, TicketStatus


class FullTicket(BaseModel):
    sl_no: int
    id: UUID
    title: str
    user: User
    subcategory: FullSubCategory
    assignee: User
    severity: Severity
    sla: SLA
    created_at: datetime
    closed_at: datetime | None
    resolution_status: TicketResolution
    ticket_status: TicketStatus

    def to_dict(self):
        return {
            "sl_no": self.sl_no,
            "id": str(self.id),
            "title": self.title,
            "user": self.user.to_dict(hide_data=True),
            "subcategory": self.subcategory.to_dict(),
            "assignee": self.assignee.to_dict(hide_data=True),
            "severity": self.severity.to_dict(),
            "sla": self.sla.to_dict(),
            "created_at": str(self.created_at),
            "closed_at": str(self.closed_at) if self.closed_at else None,
            "resolution_status": self.resolution_status,
            "ticket_status": self.ticket_status,
        }
