from pydantic import BaseModel


class SLAPost(BaseModel):
    name: str
    time_limit: int
    note: str
