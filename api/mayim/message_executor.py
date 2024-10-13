from typing import List
from mayim import PostgresExecutor

from api.models.db.message import Message
from api.models.enums import MessageType


class MessageExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/messages/"

    async def get_messages(
        self, ticket_id: int, limit: int = 10, offset: int = 0
    ) -> List[Message]:
        """Get all messages for a ticket"""

    async def create_text_message(
        self, ticket_id: int, user_id: int, message: str, message_type: MessageType
    ) -> Message:
        """Create a new chat message"""

    async def create_message_with_file_id(
        self, ticket_id: int, user_id: int, file_id: int
    ) -> Message:
        """Create a message with a file attachment"""