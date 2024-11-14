from dataclasses import dataclass
from uuid import UUID


@dataclass
class TicketForm:
    subcategory_id: UUID
    inital_message: str
    title: str
