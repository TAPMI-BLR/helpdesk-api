from typing import Optional

from pydantic import BaseModel
from sanic.request import File


class MessageForm(BaseModel):
    content: str
    file: Optional[File] = None
