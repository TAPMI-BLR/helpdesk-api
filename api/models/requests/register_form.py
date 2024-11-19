from pydantic import BaseModel


class RegisterForm(BaseModel):
    name: str
    email: str
    data: str
