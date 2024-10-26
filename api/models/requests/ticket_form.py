from dataclasses import dataclass


@dataclass
class TicketForm:
    subcategory_id: int
    inital_message: str
    title: str
