from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Config:
    id: int
    created_at: datetime
    default_sla: int
    default_severity: int
    default_assignee: int

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": str(self.created_at),
            "default_sla": self.default_sla,
            "default_severity": self.default_severity,
            "default_assignee": self.default_assignee,
        }
