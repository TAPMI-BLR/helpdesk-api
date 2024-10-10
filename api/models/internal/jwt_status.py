from typing import Optional

from api.models.internal.jwt_data import JWT_Data


class JWT_Status:
    def __init__(
        self,
        authenticated: bool,
        message: Optional[str] = None,
        JWT_Data: Optional[JWT_Data] = None,
    ):
        # Ensure that there is either a message (if not authenticated) or JWT_Data
        if not authenticated and JWT_Data is not None:
            raise ValueError("JWT_Data should be None if authenticated is False")
        if authenticated and JWT_Data is None:
            raise ValueError("JWT_Data should not be None if authenticated is True")

        self.authenticated = authenticated
        self.message = message
        self.JWT_Data = JWT_Data

    @property
    def is_valid(self) -> bool:
        return self.authenticated

    @property
    def error_message(self) -> str:
        if self.authenticated:
            return "No error"
        if self.message is None:
            return "An error occurred while validating the JWT token"
        return self.message
