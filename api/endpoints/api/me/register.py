from mayim import Mayim
from json import JSONDecodeError, loads
from sanic import Request, json
from sanic.views import HTTPMethodView
from sanic_ext import validate
from psycopg.errors import UniqueViolation
from mayim.exception import RecordNotFound

from api.app import HelpDesk
from api.decorators.require_role import require_role
from api.decorators.require_login import require_login
from api.mayim.user_executor import UserExecutor
from api.models.internal.jwt_data import JWT_Data
from api.models.requests.register_form import RegisterForm


class MeRegister(HTTPMethodView):
    @validate(form=RegisterForm, body_argument="form")
    @require_login()
    @require_role(required_role="signup")
    async def post(self, request: Request, jwt_data: JWT_Data, form: RegisterForm):
        # Get the data from the request
        name = form.name
        email = form.email
        data = form.data
        # Convert string to dict
        try:
            data = loads(data)
        except JSONDecodeError:
            return json(
                {
                    "error": "Invalid Data Format",
                    "message": "The provided data is not a valid JSON format",
                },
                400,
            )
        # Compare the provided email with the JWT data
        if jwt_data.email != email:
            return json(
                {
                    "error": "Email Mismatch",
                    "message": "The email provided does not match the email associated with the JWT",
                },
                400,
            )
        # TODO: Check Name simlarity
        # Ensure Data is not Empty
        if not data:
            return json(
                {
                    "error": "Invalid Data",
                    "message": "The additional data provided is missing or empty",
                },
                400,
            )
        # Create the User
        executor = Mayim.get(UserExecutor)
        try:
            await executor.create_user(name, email, data)
        except UniqueViolation:
            # User Already Exists
            return json(
                {
                    "error": "User Already Exists",
                    "message": "An account with this email already exists. Please try logging in instead.",
                },
                status=400,
            )
        # Get user and generate JWT
        try:
            user = await executor.get_user_by_email(email)
        except RecordNotFound:
            user = None

        # Get app and typehint
        app: HelpDesk = request.app

        if user:
            message = "Authenticated"
            payload = {
                "name": user.name,
                "email": user.email,
                "uuid": str(user.id),
                "roles": ["user"],
            }
            if user.is_team:
                payload["roles"].append("team")
            if user.is_sys_admin:
                payload["roles"].append("sys_admin")

            issued_token = await app.generate_jwt(payload, validity=30 * 24 * 60)

            return json(
                {
                    "authenticated": True,
                    "message": message,
                    "token": issued_token,
                },
                status=200,
            )

        else:
            return json(
                {
                    "error": "Token Generation Failed",
                    "message": (
                        "An error occurred while generating the authentication token. "
                        "Please try logging in again after a few minutes."
                    ),
                },
                status=400,
            )
