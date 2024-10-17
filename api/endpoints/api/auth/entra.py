import uuid

from sanic.request import Request
from sanic.response import redirect, json
from sanic.views import HTTPMethodView


class AuthEntra(HTTPMethodView):
    template = (
        "https://login.microsoftonline.com/%(tenant)s/oauth2/v2.0/authorize?client_id=%(client_id)s"
        "&response_type=id_token "
        "&response_mode=form_post"
        "&redirect_uri=%(redirect_uri)s"
        "&nonce=%(nonce)s"
        "&scope=%(scope)s"
        "&state=%(state)s"
    )

    async def get(self, request: Request):
        state = uuid.uuid1()
        nonce = uuid.uuid1()

        # ENV Variables
        tenant_id = request.app.config["AZURE_AD_TENANT_ID"]
        client_id = request.app.config["AZURE_AD_CLIENT_ID"]
        redirect_url = request.app.config["AZURE_AD_REDIRECT_URI"]

        if len(tenant_id) == 0 or len(client_id) == 0 or len(redirect_url) == 0:
            return json(
                {"status": "error", "message": "Server is improperly configured"}
            )

        # Generate the URL to redirect the user to.
        url = self.template % {
            "tenant": tenant_id,
            "client_id": client_id,
            "redirect_uri": redirect_url,
            "scope": "openid profile email offline_access",
            "state": state,
            "nonce": nonce,
        }

        # Return a redirect
        return redirect(url)
