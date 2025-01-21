from pydantic import BaseModel
from pydantic_extra_types.color import Color


class CategoryForm(BaseModel):
    name: str
    colour: Color
