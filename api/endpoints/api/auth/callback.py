import jwt
from mayim import Mayim
from mayim.exception import RecordNotFound
from sanic import Request, redirect
from sanic.log import logger
from sanic.views import HTTPMethodView

from api.app import HelpDesk
from api.mayim.user_executor import UserExecutor


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
            return redirect("/?error=invalid_token")
        except jwt.exceptions.InvalidIssuedAtError:
            logger.warning("JWT issued in future")
            # Invalid token
            return redirect("/?error=invalid_token")
        except jwt.exceptions.ImmatureSignatureError:
            logger.warning("JWT issued in future")
            # Invalid token
            return redirect("/?error=invalid_token")
        except jwt.exceptions.ExpiredSignatureError:
            logger.warning("JWT has expired")
            # Invalid token
            return redirect("/?error=invalid_token")
        except jwt.exceptions.DecodeError:
            logger.warning("JWT decode error")
            # Invalid token
            return redirect("/?error=invalid_token")

        # Get email from decoded token
        email = decoded["email"]
        name = decoded["name"]

        # Get domain from email
        domain: str = email.split("@")[1]

        # Hard domain check for email domain being "manipal.edu" or a subdomain
        if not domain.endswith("manipal.edu"):
            # Invalid domain
            return redirect(f"/?error=invalid_domain&domain={domain}")
        # Get user from database
        try:
            user = await executor.get_user_by_email(email)
        except RecordNotFound:
            user = None

        duration = 30 * 24 * 60
        if user:
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
            issued_token = await app.generate_jwt(payload, validity=duration)
        else:
            payload = {"email": email, "name": name, "roles": ["signup"]}
            duration = 12 * 60
            issued_token = await app.generate_jwt(payload, validity=duration)

        # Redirect to home with JWT set in cookie
        rsp = redirect("/")
        # Cookie will expire 1 minute before the token expires
        max_age = duration * 60
        max_age -= 60
        # Add Cookie
        rsp.add_cookie("JWT_TOKEN", issued_token, max_age=max_age)

        # Redirect to home
        return rsp
