from dataclasses import dataclass
from datetime import datetime

from api.models.enums import MessageType


@dataclass(frozen=True)
class Message:
    id: int
    type: MessageType
    ticket_id: int
    author_id: int
    created_at: datetime
    content: str | None
    file_id: int | None

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "ticket_id": self.ticket_id,
            "author_id": self.author_id,
            "created_at": str(self.created_at),
            "content": self.content,
            "file_id": self.file_id,
        }
