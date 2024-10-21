from dataclasses import dataclass


@dataclass(frozen=True)
class Severity:
    id: int
    name: str
    level: int
    note: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "note": self.note,
        }
