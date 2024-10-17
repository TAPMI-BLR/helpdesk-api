from sanic.views import HTTPMethodView
from sanic import Request
from sanic.response import json
from sanic.log import logger
import jwt

from api.app import HelpDesk
from api.mayim.user_executor import UserExecutor
from mayim import Mayim
from mayim.exception import RecordNotFound


class AuthCallback(HTTPMethodView):
    async def post(self, request: Request):
        # Get the executor
        executor = Mayim.get(UserExecutor)

        app: HelpDesk = request.app
        # Get the token from the request.
        form = request.form
        token = form["id_token"][0]

        # Get the ID of the key used to sign the token.
        kid = jwt.get_unverified_header(token)["kid"]

        # Get the public key to verify the token.
        key = app.get_entra_jwt_keys().get(kid, "")

        try:
            # Decode the token.
            decoded = jwt.decode(
                token,
                key=key,
                algorithms=["RS256"],
                audience=request.app.config["AZURE_AD_CLIENT_ID"],
            )
        except jwt.exceptions.InvalidAudienceError:
            logger.warning("Invalid audience for JWT")
            # Invalid token
            return json(
                {
                    "authenticated": False,
                    "message": "Invalid token",
                },
                status=401,
            )
        except jwt.exceptions.InvalidIssuedAtError:
            logger.warning("JWT issued in future")
            # Invalid token
            return json(
                {
                    "authenticated": False,
                    "message": "Invalid token",
                },
                status=401,
            )
        except jwt.exceptions.ImmatureSignatureError:
            logger.warning("JWT issued in future")
            # Invalid token
            return json(
                {
                    "authenticated": False,
                    "message": "Invalid token",
                },
                status=401,
            )
        except jwt.exceptions.ExpiredSignatureError:
            logger.warning("JWT has expired")
            # Invalid token
            return json(
                {
                    "authenticated": False,
                    "message": "Invalid token",
                },
                status=401,
            )
        except jwt.exceptions.DecodeError:
            logger.warning("JWT decode error")
            # Invalid token
            return json(
                {
                    "authenticated": False,
                    "message": "Invalid token",
                },
                status=401,
            )

        # Get email from decoded token
        email = decoded["email"]
        name = decoded["name"]

        # Get domain from email
        domain: str = email.split("@")[1]

        # Hard domain check for email domain being "manipal.edu" or a subdomain
        if not domain.endswith("manipal.edu"):
            # Invalid domain
            return json(
                {
                    "authenticated": False,
                    "message": "Invalid domain",
                },
                status=401,
            )
        # Get user from database
        try:
            user = await executor.get_user_by_email(email)
        except RecordNotFound:
            user = None

        if user:
            message = "Authenticated"
            payload = {
                "name": user.name,
                "email": user.email,
                "uuid": user.email,
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
            message = "Signup Required"
            payload = {"email": email, "name": name, "roles": ["signup"]}
            issued_token = await app.generate_jwt(payload, validity=30 * 24 * 60)

        return json(
            {
                "authenticated": False,
                "message": message,
                "token": issued_token,
            },
            status=200,
        )
