from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class TicketUpdateForm(BaseModel):
    assignee_id: Optional[UUID] = None
    sla_id: Optional[UUID] = None
    severity_id: Optional[UUID] = None
    subcategory_id: Optional[UUID] = None
