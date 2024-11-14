from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class User:
    id: UUID
    name: str
    email: str
    data: dict
    is_team: int
    is_sys_admin: int

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "data": self.data,
            "is_team": self.is_team,
            "is_sys_admin": self.is_sys_admin,
        }
