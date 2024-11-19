from uuid import UUID

from pydantic import BaseModel


class TicketForm(BaseModel):
    subcategory_id: UUID
    initial_message: str
    title: str
