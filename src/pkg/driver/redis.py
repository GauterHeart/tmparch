from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import redis.asyncio as aioredis
from pydantic import SecretStr

from ._base import Driver

__all__ = ["RedisDriver"]


class RedisDriver(Driver):

    _connector: Optional[aioredis.Redis] = None

    def __init__(
        self, host: str, port: int, user: str, password: SecretStr, db: str
    ) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.pool = aioredis.ConnectionPool.from_url(
            self.__create_dsn(), max_connections=10
        )

    def __create_dsn(self) -> str:
        return (
            f"redis://{self.__user}:{self.__password.get_secret_value()}"
            + f"@{self.__host}:{self.__port}/{self.__db}"
        )

    @asynccontextmanager
    async def _create_connector(self) -> AsyncGenerator[aioredis.Redis, None]:
        if self._connector is None:
            self._connector = aioredis.Redis(connection_pool=self.pool)

        try:
            yield self._connector
        finally:
            await self._connector.close()

    async def set(self, name: str, value: str, expire: Optional[int] = None) -> None:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.set(name=name, value=value, ex=expire)

    async def get(self, name: str) -> str:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                return await conn.get(name=name)

    async def delete(self, name: str) -> None:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.delete(name)
