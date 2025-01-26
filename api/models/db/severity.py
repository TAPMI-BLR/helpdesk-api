from uuid import UUID

from pydantic import BaseModel
from pydantic_extra_types.color import Color


class Severity(BaseModel):
    id: UUID
    name: str
    level: int
    note: str
    colour: Color

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "level": self.level,
            "note": self.note,
            "colour": self.colour.as_hex(),
        }
