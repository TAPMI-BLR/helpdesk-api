from typing import Tuple
from sanic import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from api.app import HelpDesk
from api.models.internal.jwt_data import JWT_Data


def require_login():
    def decorator(f):
        async def decorated_function(*args, **kwargs):
            # Check if the first argument is a view or a request
            if isinstance(args[0], HTTPMethodView):
                request: Request = args[1]
                jwt_idx = 2
            else:
                request: Request = args[0]
                jwt_idx = 1

            def authorize_and_inject_jwt_data(
                request: Request, jwt_idx: int, args: list
            ) -> Tuple[bool, list]:
                # Get the app object
                app: HelpDesk = request.app
                # Check if the request is authorized
                jwt_status = app.check_server_jwt(request.token)
                # Check if the JWT is valid
                if jwt_status.authenticated:
                    # Inject the JWT Data into function via args
                    args.insert(jwt_idx, jwt_status.JWT_Data)
                return jwt_status.authenticated, args

            # Check if the JWT Data is already present
            if jwt_idx < len(args):
                if not isinstance(args[jwt_idx], JWT_Data):
                    authenticated, new_args = authorize_and_inject_jwt_data(
                        request, jwt_idx, list(args)
                    )
                else:
                    authenticated = new_args[jwt_idx].is_valid()
                    new_args = list(args)
            else:
                authenticated, new_args = authorize_and_inject_jwt_data(
                    request, jwt_idx, list(args)
                )

            # Call the function if the request is authorized
            if authenticated:
                # Call the function if the request is authorized
                return await f(*new_args, **kwargs)
            else:
                return json({"error": "Unauthorized access"}, status=401)

        return decorated_function

    return decorator
