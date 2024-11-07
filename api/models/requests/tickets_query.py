from dataclasses import dataclass


@dataclass
class TicketsQuery:
    limit: int = 10
    page: int = 0
    show_closed: bool = False
    as_user: bool = True
