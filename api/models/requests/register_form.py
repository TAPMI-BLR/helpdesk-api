from dataclasses import dataclass


@dataclass
class RegisterForm:
    name: str
    email: str
    data: str
