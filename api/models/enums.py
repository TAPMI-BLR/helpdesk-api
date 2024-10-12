from enum import Enum


class MessageType(Enum):
    USER = 1
    SYSTEM = 2
    SUPPORT = 3


class CategoryTeamRole(Enum):
    ADMIN = 1
    MEMBER = 2


class TicketStatus(Enum):
    OPEN = 1
    CLOSED = 2


class TicketResolution(Enum):
    RESOLVED = 1
    UNRESOLVED = 2
