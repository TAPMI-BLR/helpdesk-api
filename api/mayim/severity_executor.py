from typing import List
from mayim import PostgresExecutor

from api.models.db.severity import Severity


class SeverityExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/severity/"

    async def get_all_severity_levels(
        self, limit: int = 10, offset: int = 0
    ) -> List[Severity]:
        """Get all Severity Levels"""

    async def get_severity_by_id(self, sla_id: int) -> Severity:
        """Get an Severity Level by its ID"""

    async def create_severity(self, name: str, level: int, note: str) -> Severity:
        """Create an Severity Level"""
