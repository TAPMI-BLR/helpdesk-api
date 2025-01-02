from uuid import UUID
from pydantic import BaseModel


class TicketAssigneeForm(BaseModel):
    assignee_id: UUID
