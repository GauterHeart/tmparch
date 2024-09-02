from src.pkg.driver import RedisDriver, Repository

__all__ = ["RequestRedisRepo"]


class RequestRedisRepo(Repository[RedisDriver]):
    async def get(self, name: str) -> str:
        return await self.cursor.get(name)

    async def create(self, name: str, value: str, expire: int) -> None:
        await self.cursor.set(name=name, value=value, expire=expire)
