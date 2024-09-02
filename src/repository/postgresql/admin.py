from typing import List

from src.model.admin import AdminModel
from src.pkg.driver import PostgresqlDriver, Repository

__all__ = ["AdminPgRepo"]


class AdminPgRepo(Repository[PostgresqlDriver]):
    async def fetch(self) -> List[AdminModel]:
        query = """
            select * from admin;
        """
        result = await self.cursor.fetch(query)
        return [AdminModel(**r) for r in result]
