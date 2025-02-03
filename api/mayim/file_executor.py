from uuid import UUID
from mayim import PostgresExecutor

from api.models.db.file import File
from api.models.enums import FileStorageType


class FileExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/files/"

    async def get_file_by_id(self, ticket_id: UUID, file_id: UUID) -> File:
        """Get a File by its ID"""

    async def add_file(
        self, file_name: str, file_type: str, storage_type: FileStorageType
    ) -> str:
        """Insert a new File"""

    async def delete_file(self, file_id: UUID):
        """Delete a File by its ID"""

    async def update_file_storage(
        self, file_id: UUID, new_storage_type: FileStorageType
    ):
        """Update the Storage Location of the file"""
