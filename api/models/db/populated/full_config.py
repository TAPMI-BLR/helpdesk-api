from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from api.models.db.severity import Severity
from api.models.db.sla import SLA
from api.models.db.user import User


class FullConfig(BaseModel):
    id: UUID
    created_at: datetime
    default_sla: SLA
    default_severity: Severity
    default_assignee: User

    def to_dict(self):
        return {
            "id": str(self.id),
            "created_at": str(self.created_at),
            "default_sla": str(self.default_sla),
            "default_severity": str(self.default_severity),
            "default_assignee": str(self.default_assignee),
        }
