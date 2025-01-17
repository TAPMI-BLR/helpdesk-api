from pydantic import BaseModel


class SeverityPost(BaseModel):
    name: str
    level: int
    note: str
