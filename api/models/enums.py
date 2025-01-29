from enum import Enum


class MessageType(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
    SUPPORT = "SUPPORT"


class CategoryTeamRole(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class TicketResolution(str, Enum):
    RESOLVED = "RESOLVED"
    UNRESOLVED = "UNRESOLVED"


class FileStorageType(str, Enum):
    MINIO = "MINIO"
    ONEDRIVE = "ONEDRIVE"
