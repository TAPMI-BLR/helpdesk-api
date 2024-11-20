from typing import Literal

from sanic.response import json
from sanic.views import HTTPMethodView

from api.models.internal.jwt_data import JWT_Data


def require_role(
    required_role: Literal["signup", "user", "team", "sys_admin"],
    allow_higher: bool = False,
):
    def decorator(f):
        async def decorated_function(*args, **kwargs):
            # Check if the first argument is a view or a request
            if isinstance(args[0], HTTPMethodView):
                jwt_idx = 2
            else:
                jwt_idx = 1

            authenticated = False

            # Check if the JWT Data is already present
            if jwt_idx < len(args):
                if not isinstance(args[jwt_idx], JWT_Data):
                    return json(
                        {
                            "error": "Unauthorized access",
                            "message": "JWT data is missing or invalid",
                        },
                        status=401,
                    )
                else:
                    jwt_data: JWT_Data = args[jwt_idx]
                    roles = jwt_data.roles
            else:
                return json(
                    {
                        "error": "Unauthorized access",
                        "message": "JWT data is required but missing or invalid",
                    },
                    status=401,
                )

            # Check if the user has the required role
            if required_role in roles:
                # The user has the required role
                authenticated = True
            elif allow_higher:
                # Check if the user has a higher role
                if required_role == "signup":
                    # If the user signup endpoint is different from the user endpoint
                    authenticated = False
                elif required_role == "user":
                    if any(r in roles for r in ["team", "sys_admin"]):
                        authenticated = True
                elif required_role == "team":
                    if "sys_admin" in roles:
                        authenticated = True
                elif required_role == "sys_admin":
                    # No higher role exists
                    authenticated = False

            # Call the function if the request is authorized
            if authenticated:
                # Call the function if the request is authorized
                return await f(*args, **kwargs)
            else:
                return json(
                    {
                        "error": "Unauthorized access",
                        "message": f"Access denied: User does not have the required role ({required_role})",
                    },
                    status=401,
                )

        return decorated_function

    return decorator
