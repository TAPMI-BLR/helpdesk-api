from uuid import UUID

from pydantic import BaseModel


class MessageAuthor(BaseModel):
    id: UUID
    name: str

    def to_dict(self):
        return {"id": str(self.id), "name": self.name}
