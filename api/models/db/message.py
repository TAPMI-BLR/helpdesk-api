from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from api.models.db.message_author import MessageAuthor
from api.models.enums import MessageType


@dataclass(frozen=True)
class Message:
    id: UUID
    type: MessageType
    ticket_id: UUID
    author: MessageAuthor
    created_at: datetime
    content: str | None
    file_id: UUID | None

    def to_dict(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "ticket_id": str(self.ticket_id),
            "author": self.author.to_dict(),
            "created_at": str(self.created_at),
            "content": self.content,
            "file_id": str(self.file_id) if self.file_id else None,
        }
