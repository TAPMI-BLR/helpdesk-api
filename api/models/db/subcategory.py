from uuid import UUID

from pydantic import BaseModel


class SubCategory(BaseModel):
    id: UUID
    category_id: UUID
    name: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "category_id": str(self.category_id),
            "name": self.name,
        }
