from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    name: str
    email: str
    data: dict
    is_team: int
    is_sys_admin: int

    def to_dict(self, hide_data: bool = False):
        d = {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "data": self.data,
            "is_team": self.is_team == 1,
            "is_sys_admin": self.is_sys_admin == 1,
        }
        if hide_data:
            del d["data"]
        return d
