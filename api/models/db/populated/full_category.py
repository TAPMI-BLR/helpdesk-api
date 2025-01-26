from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic_extra_types.color import Color
from api.models.db.subcategory import SubCategory


class FullCategory(BaseModel):
    id: UUID
    name: str
    colour: Color
    subcategories: Optional[list[SubCategory]]

    def to_dict(self):
        subcategories = []
        if self.subcategories:
            subcategories = [
                subcategory.to_dict() for subcategory in self.subcategories
            ]
        return {
            "id": str(self.id),
            "name": self.name,
            "colour": self.colour.as_hex(),
            "subcategories": subcategories,
        }
