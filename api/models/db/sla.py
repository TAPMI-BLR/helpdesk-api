from uuid import UUID

from pydantic import BaseModel


class SLA(BaseModel):
    id: UUID
    name: str
    note: str
    time_limit: int

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "note": self.note,
            "time_limit": self.time_limit,
        }
