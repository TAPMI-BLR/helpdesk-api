from typing import Optional

from pydantic import BaseModel


class MessageForm(BaseModel):
    content: Optional[str] = None
