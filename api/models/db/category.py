from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    id: int
    name: str

    def to_dict(self):
        return {"id": self.id, "name": self.name}
