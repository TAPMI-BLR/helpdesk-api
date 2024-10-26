from dataclasses import dataclass


@dataclass
class MessageQueryParams:
    limit: int = 10
    page: int = 0
