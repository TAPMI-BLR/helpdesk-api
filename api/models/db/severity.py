from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Severity:
    id: UUID
    name: str
    level: int
    note: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "level": self.level,
            "note": self.note,
        }
