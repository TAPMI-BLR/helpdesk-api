from os import getenv

from dotenv import load_dotenv
from mayim import Mayim
from mayim.extension import SanicMayimExtension
from sanic.log import logger
from sanic_ext import Extend

from api.app import HelpDesk, appserver
from api.mayim.category_executor import CategoryExecutor
from api.mayim.file_executor import FileExecutor
from api.mayim.message_executor import MessageExecutor
from api.mayim.severity_executor import SeverityExecutor
from api.mayim.sla_executor import SLAExecutor
from api.mayim.statistics_executor import StatisticsExecutor
from api.mayim.system_executor import SystemExecutor
from api.mayim.team_executor import TeamExecutor
from api.mayim.ticket_executor import TicketExecutor
from api.mayim.user_executor import UserExecutor

from . import endpoints  # noqa: F401

# Load the .env file (mainly for local development)
load_dotenv()

config = {}
logger.debug("Loading RSA Keys")
# Read the public and private keys and add them to the config.
with open("public-key.pem") as public_key_file:
    config["PUB_KEY"] = public_key_file.read()

with open("private-key.pem") as private_key_file:
    config["PRIV_KEY"] = private_key_file.read()

logger.debug("Loading Configuration")
# Pull enviroment variables (or use defaults) and add them to the config.
config.update(
    {
        "IS_PROD": getenv("IS_PROD", "false"),
        "HOST": getenv("HOST", "default"),
        "PROXIES_COUNT": int(getenv("PROXIES_COUNT", 0)),
        "DB_HOST": getenv("DB_HOST", "postgres"),
        "DB_PORT": int(getenv("DB_PORT", 5432)),
        "DB_NAME": getenv("DB_NAME", "helpdesk"),
        "DB_USERNAME": getenv("DB_USERNAME", "root"),
        "DB_PASSWORD": getenv("DB_PASSWORD", "password"),
        "AZURE_AD_CLIENT_ID": getenv("AZURE_AD_CLIENT_ID", None),
        "AZURE_AD_TENANT_ID": getenv("AZURE_AD_TENANT_ID", None),
        "AZURE_AD_REDIRECT_URI": getenv(
            "AZURE_AD_REDIRECT_URI", "http://localhost:8000/api/login/callback"
        ),
        "AZURE_AD_DOMAIN_HINT": getenv("AZURE_AD_DOMAIN_HINT", "ycn.club"),
        "AZURE_AD_PROMPT": getenv("AZURE_AD_PROMPT", "select_account"),
        "MINIO_ENDPOINT": getenv("MINIO_ENDPOINT", "minio"),
        "MINIO_USERNAME": getenv("MINIO_USERNAME", "minio"),
        "MINIO_PASSWORD": getenv("MINIO_PASSWORD", "minio"),
        "MINIO_PUBLIC_ENDPOINT": getenv("MINIO_PUBLIC_ENDPOINT", None),
        "MINIO_BUCKET": getenv("MINIO_BUCKET", "helpdesk"),
        "MAX_FILE_SIZE": int(getenv("MAX_FILE_SIZE", 10 * 1024 * 1024)),
    }
)

# Try to get state from the ENV, defaults to being dev.
is_prod: str = config.get("IS_PROD", "false")

# Convert the string to a bool and update the config with the bool.
config.update({"IS_PROD": is_prod.lower() == "true"})

# Check if AZURE_AD env variables are set
if any(
    config.get(var) is None
    for var in [
        "AZURE_AD_TENANT_ID",
        "AZURE_AD_CLIENT_ID",
        "AZURE_AD_REDIRECT_URI",
        "AZURE_AD_DOMAIN_HINT",
        "MINIO_PUBLIC_ENDPOINT",
    ]
):
    logger.error("MISSING ENV VARIABLES")
    quit(1)

app: HelpDesk = appserver
app.config.update(config)
app.config.PROXIES_COUNT = config["PROXIES_COUNT"]

Extend.register(
    SanicMayimExtension(
        executors=[
            UserExecutor,
            MessageExecutor,
            TicketExecutor,
            CategoryExecutor,
            SystemExecutor,
            SLAExecutor,
            TeamExecutor,
            SeverityExecutor,
            StatisticsExecutor,
            FileExecutor,
        ],
        dsn=f"postgres://{config['DB_USERNAME']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}",  # noqa: E501
    )
)


@app.listener("before_server_start")
async def setup_app(app: HelpDesk):
    await app.load_entra_jwks()
    logger.info("Loaded Entra Keys")
    await app.setup_minio()
    logger.info("Setup Minio")


@app.listener("after_server_start")
async def setup_db(app: HelpDesk):
    # Setup the database functions used in deletion
    executor = Mayim.get(SystemExecutor)
    await executor.func_setup_migrate_category()
    await executor.func_setup_migrate_subcategory()
    await executor.func_setup_migrate_sla()
    await executor.func_setup_migrate_severity()
    logger.info("Setup Database Functions")


if __name__ == "__main__":
    # Use a KWARGS dict to pass to app.run dynamically
    kwargs = {"access_log": True, "host": "0.0.0.0"}

    kwargs["debug"] = not app.config["IS_PROD"]
    kwargs["auto_reload"] = True
    # Run the API Server
    app.run(**kwargs)
