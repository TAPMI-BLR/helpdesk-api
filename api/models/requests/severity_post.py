from pydantic import BaseModel
from pydantic_extra_types.color import Color


class SeverityPost(BaseModel):
    name: str
    level: int
    note: str
    colour: Color
