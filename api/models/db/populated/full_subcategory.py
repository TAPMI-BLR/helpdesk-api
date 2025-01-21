from uuid import UUID

from pydantic import BaseModel
from pydantic_extra_types.color import Color
from api.models.db.category import Category


class FullSubCategory(BaseModel):
    id: UUID
    category_id: UUID
    category: Category
    name: str
    colour: Color

    def to_dict(self):
        return {
            "id": str(self.id),
            "category": self.category.to_dict(),
            "name": self.name,
            "colour": self.colour.as_hex(),
        }
