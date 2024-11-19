from uuid import UUID

from pydantic import BaseModel

from api.models.db.category import Category


class SubCategory(BaseModel):
    id: UUID
    category: Category
    name: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "category_id": self.category.to_dict(),
            "name": self.name,
        }
