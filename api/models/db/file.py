from uuid import UUID

from pydantic import BaseModel


class File(BaseModel):
    id: UUID
    type: str
    data: bytes
