from pydantic import BaseModel


class MessageQueryParams(BaseModel):
    limit: int = 10
    page: int = 0
