from mayim import PostgresExecutor

from api.models.db.config import Config


class SystemExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/system/"

    async def set_default_ticket_assignee(self, user_id: int):
        """Set the default system administrator"""

    async def set_default_sla_id(self, sla_id: int):
        """Set the default SLA ID"""

    async def set_default_severity_id(self, severity_id: int):
        """Set the default severity ID"""

    async def get_default_ticket_config(self) -> Config:
        """Get default ticket configuration"""
