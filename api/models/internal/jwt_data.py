from datetime import datetime


class JWT_Data:
    def __init__(self, name, email, roles, exp, iat, nbf, iss) -> None:
        # Make sure none of the values are None
        if None in (name, email, roles, exp, iat, nbf, iss):
            raise ValueError("All values must be provided")
        self.name = name
        self.email = email
        self.roles = roles
        self.exp = datetime.fromtimestamp(exp)
        self.iat = datetime.fromtimestamp(iat)
        self.nbf = datetime.fromtimestamp(nbf)
        self.iss = iss

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "roles": self.roles,
        }

    def is_admin(self) -> bool:
        return "admin" in self.roles

    def is_support(self) -> bool:
        return "support" in self.roles

    def is_valid(self) -> bool:
        now = datetime.now()
        return self.nbf < now < self.exp
