from dataclasses import dataclass
from typing import Optional
from sanic.request import File


@dataclass
class MessageForm:
    content: str
    file: Optional[File] = None
