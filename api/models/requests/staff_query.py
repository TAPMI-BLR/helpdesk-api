from pydantic import BaseModel


class StaffQuery(BaseModel):
    show_all: bool = False
