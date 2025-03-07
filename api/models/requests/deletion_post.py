from pydantic import BaseModel
from uuid import UUID


class DeletionPost(BaseModel):
    delete: UUID
    replacement: UUID
