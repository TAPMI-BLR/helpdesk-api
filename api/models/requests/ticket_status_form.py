from typing import Optional
from pydantic import BaseModel

from api.models.enums import TicketResolution, TicketStatus


class TicketStatusForm(BaseModel):
    status: Optional[TicketStatus] = None
    resolution: Optional[TicketResolution] = None
