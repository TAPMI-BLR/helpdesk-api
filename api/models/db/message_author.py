from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class MessageAuthor:
    id: UUID
    name: str

    def to_dict(self):
        return {"id": str(self.id), "name": self.name}
