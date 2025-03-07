from typing import List
from uuid import UUID
from mayim import PostgresExecutor

from api.models.db.sla import SLA


class SLAExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/SLAs/"

    async def get_all_slas(self, limit: int = 10, offset: int = 0) -> List[SLA]:
        """Get all SLAs"""

    async def get_sla_by_id(self, sla_id: int) -> SLA:
        """Get an SLA by its ID"""

    async def create_sla(self, name: str, time_limit: int, note: str):
        """Create an SLA"""

    async def delete_sla(self, original_id: UUID, replacement_id: UUID, user_id: UUID):
        """Delete an SLA"""
