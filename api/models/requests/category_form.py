from pydantic import BaseModel


class CategoryForm(BaseModel):
    name: str
