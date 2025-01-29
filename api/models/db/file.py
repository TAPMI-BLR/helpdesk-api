from uuid import UUID

from pydantic import BaseModel

from api.models.enums import FileStorageType


class File(BaseModel):
    id: UUID
    file_name: str
    storage_type: FileStorageType
    file_type: str
