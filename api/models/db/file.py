from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class File:
    id: UUID
    type: str
    data: bytes
