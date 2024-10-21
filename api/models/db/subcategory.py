from dataclasses import dataclass


@dataclass(frozen=True)
class SubCategory:
    id: int
    parent_id: int
    name: str

    def to_dict(self):
        return {"id": self.id, "parent_id": self.parent_id, "name": self.name}
