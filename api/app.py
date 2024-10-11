import json
from datetime import datetime, timedelta, timezone

import aiohttp
import jwt
from sanic import Sanic
from sanic.log import logger


from api.models.internal.jwt_data import JWT_Data
from api.models.internal.jwt_status import JWT_Status


class HelpDesk(Sanic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx.entra_public_keys = dict()

    def get_entra_jwt_keys(self) -> dict:
        return self.ctx.entra_public_keys

    async def load_entra_jwks(self):
        # Fetch OpenID Configuration of Entra
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://login.microsoftonline.com/common/.well-known/openid-configuration"
            ) as resp:
                config = await resp.json()
                jwks_uri = config["jwks_uri"]

        logger.info(
            "Fetching JSON Web Key Set (JWKS) from the OpenID Configuration of Entra"
        )

        # Fetch the JSON Web Key Set (JWKS) from the OpenID Configuration of Entra
        async with aiohttp.ClientSession() as session:
            async with session.get(jwks_uri) as resp:
                jwks = await resp.json()

        logger.info("Saving public keys from the JWKS")

        # Create a dictionary of public keys from the JWKS
        public_keys = {}
        for jwk in jwks["keys"]:
            kid = jwk["kid"]
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        self.ctx.entra_public_keys = public_keys

    def decode_jwt(self, jwt_token: str) -> JWT_Data:
        assert isinstance(jwt_token, str)
        data = JWT_Data(
            **jwt.decode(jwt_token, key=self.config["PUB_KEY"], algorithms="RS256")
        )
        return data

    def check_server_jwt(self, jwt_token: str) -> JWT_Status:
        if not jwt_token or jwt_token == "":
            return JWT_Status(authenticated=False, message="JWT Token not provided")
        try:
            jwt_data = self.decode_jwt(jwt_token)
        except jwt.exceptions.ImmatureSignatureError:
            # Raised when a token’s nbf claim represents a time in the future
            d = JWT_Status(
                authenticated=False, message="JWT Token not allowed to be used at time"
            )
        except jwt.exceptions.InvalidIssuedAtError:
            # Raised when a token’s iat claim is in the future
            d = JWT_Status(
                authenticated=False, message="JWT Token issued in the future"
            )
        except jwt.exceptions.ExpiredSignatureError:
            # Raised when a token’s exp claim indicates that it has expired
            d = JWT_Status(authenticated=False, message="JWT Token has expired")
        except jwt.exceptions.InvalidTokenError:
            # Generic invalid token
            d = JWT_Status(authenticated=False, message="JWT Token is invalid")
        else:
            # Valid Token
            d = JWT_Status(authenticated=True, JWT_Data=jwt_data)

        return d

    async def generate_jwt(
        self,
        data: dict,
        validity: int,
    ) -> str:
        """Generates JWT with given data"""
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=validity)

        try:
            # Attempt to get Host from config
            host = self.config["HOST"]
        except KeyError:
            logger.error("Host not found in configw")
            # Unable to get Host from config, Quit app due to required field
            self.stop()

        iss = f"NSS_API_{host}"
        data.update({"exp": expire, "iat": now, "nbf": now, "iss": iss})
        return jwt.encode(data, self.config["PRIV_KEY"], algorithm="RS256")


appserver = HelpDesk("helpdesk")
