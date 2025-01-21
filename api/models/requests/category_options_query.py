from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CategoryOptionsQuery(BaseModel):
    category_id: Optional[UUID] = None
    show_children: Optional[bool] = False
