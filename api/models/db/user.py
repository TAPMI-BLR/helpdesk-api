from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str
    data: dict
