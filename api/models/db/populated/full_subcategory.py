from uuid import UUID

from pydantic import BaseModel

from api.models.db.category import Category


class FullSubCategory(BaseModel):
    id: UUID
    category_id: UUID
    category: Category
    name: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "category": self.category.to_dict(),
            "name": self.name,
        }
