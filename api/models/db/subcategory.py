from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class SubCategory:
    id: UUID
    category_id: UUID
    name: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "category_id": str(self.category_id),
            "name": self.name,
        }
