from uuid import UUID

from pydantic import BaseModel


class Severity(BaseModel):
    id: UUID
    name: str
    level: int
    note: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "level": self.level,
            "note": self.note,
        }
