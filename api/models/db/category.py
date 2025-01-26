from uuid import UUID

from pydantic import BaseModel
from pydantic_extra_types.color import Color


class Category(BaseModel):
    id: UUID
    name: str
    colour: Color

    def to_dict(self):
        return {"id": str(self.id), "name": self.name, "colour": self.colour.as_hex()}
