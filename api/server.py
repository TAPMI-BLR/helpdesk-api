from dotenv import dotenv_values
from sanic.log import logger

from api.app import HelpDesk, appserver
from . import endpoints  # noqa: F401

logger.debug("Loading ENV")
config = dotenv_values(".env")

# Read the public and private keys and add them to the config.
with open("public-key.pem") as public_key_file:
    config["PUB_KEY"] = public_key_file.read()

with open("private-key.pem") as private_key_file:
    config["PRIV_KEY"] = private_key_file.read()

# Try to get state from the ENV, defaults to being dev.
is_prod: str = config.get("IS_PROD", "false")

# Convert the string to a bool and update the config with the bool.
config.update({"IS_PROD": is_prod.lower() == "true"})

# Load default values for the database connection
config.update(
    {
        "DB_HOST": config.get("DB_HOST", "localhost"),
        "DB_PORT": int(config.get("DB_PORT", 5432)),
        "DB_USERNAME": config.get("DB_USERNAME", "root"),
        "DB_PASSWORD": config.get("DB_PASSWORD", "password"),
        "DB_NAME": config.get("DB_NAME", "helpdesk"),
    },
)

# Check if AZURE_AD env variables are set
if (
    config.get("AZURE_AD_TENANT_ID") is None
    or config.get("AZURE_AD_CLIENT_ID") is None
    or config.get("AZURE_AD_REDIRECT_URI") is None
):
    logger.error("MISSING AZURE AD ENV VARIABLES")
    quit(1)

app: HelpDesk = appserver
app.config.update(config)
app.config.PROXIES_COUNT = int(config.get("PROXIES_COUNT", 0))


@app.listener("before_server_start")
async def setup_app(app: HelpDesk):
    await app.load_entra_jwks()
    logger.info("Setup complete.")


if __name__ == "__main__":
    # Run the API Server
    app.run()
