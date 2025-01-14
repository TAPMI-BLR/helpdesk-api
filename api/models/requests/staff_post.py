from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class StaffPost(BaseModel):
    email: Optional[str] = None
    user_id: Optional[UUID] = None
    is_sys_admin: bool = False
