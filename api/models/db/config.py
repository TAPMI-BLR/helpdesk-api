from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Config:
    id: UUID
    created_at: datetime
    default_sla: UUID
    default_severity: UUID
    default_assignee: UUID

    def to_dict(self):
        return {
            "id": str(self.id),
            "created_at": str(self.created_at),
            "default_sla": str(self.default_sla),
            "default_severity": str(self.default_severity),
            "default_assignee": str(self.default_assignee),
        }
