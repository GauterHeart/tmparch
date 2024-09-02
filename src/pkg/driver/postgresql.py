from abc import abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

import asyncpg
from asyncpg.exceptions import RaiseError
from pydantic import SecretStr

from ._base import Driver

__all__ = ["PostgresqlDriver"]


class _Cursor:
    @abstractmethod
    async def fetchrow(self) -> Dict[Any, Any]: ...

    @abstractmethod
    async def fetch(self, value: int) -> List[Dict[Any, Any]]: ...

    @abstractmethod
    async def forward(self, value: int) -> None: ...


class _Connector:
    @abstractmethod  # type: ignore
    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator["_Connector", None]: ...

    @abstractmethod
    async def cursor(self, query: str, *args: Any) -> _Cursor: ...

    @abstractmethod
    async def execute(self, query: str, *args: Any) -> None: ...

    @abstractmethod
    async def executemany(self, query: str, *args: Any) -> None: ...

    @abstractmethod
    async def fetchrow(self, query: str, *args: Any) -> Dict[Any, Any]: ...

    @abstractmethod
    async def fetchval(self, query: str, *args: Any) -> Dict[Any, Any]: ...

    @abstractmethod
    async def fetch(self, query: str, *args: Any) -> List[Dict[Any, Any]]: ...


class PostgresqlDriver(Driver):
    """Async postgresql driver."""

    def __init__(
        self, host: str, port: int, user: str, password: SecretStr, db: str
    ) -> None:
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__db = db
        self.pool: Optional[asyncpg.Pool] = None

    @asynccontextmanager
    async def _create_connector(self) -> AsyncGenerator[_Connector, None]:
        if self.pool is None:
            self.pool = await asyncpg.create_pool(
                database=self.__db,
                user=self.__user,
                port=self.__port,
                password=self.__password.get_secret_value(),
                host=self.__host,
            )

        async with self.pool.acquire() as connection:
            yield connection

    @asynccontextmanager
    async def cursor(self, query: str, *args: Any) -> AsyncGenerator[_Cursor, None]:
        async with self._create_connector() as conn:
            async with conn.transaction():
                yield await conn.cursor(query, *args)

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[_Connector, None]:
        async with self._create_connector() as conn:
            async with conn.transaction():
                yield conn

    async def execute(self, query: str, *args: Any) -> Optional[Dict[Any, Any]]:
        async with self._create_connector() as conn:
            async with conn.transaction():
                return await conn.execute(query, *args)

    async def executemany(self, query: str, *args: Any) -> None:
        async with self._create_connector() as conn:
            async with conn.transaction():
                await conn.executemany(query, *args)

    async def fetchrow_status(
        self, query: str, *args: Any
    ) -> Union[Optional[Dict[Any, Any]], Exception]:
        async with self._create_connector() as conn:
            try:
                resp = await conn.fetchrow(query, *args)
            except RaiseError as exc:
                return exc

        return resp

    async def fetchrow(self, query: str, *args: Any) -> Optional[Dict[Any, Any]]:
        async with self._create_connector() as conn:
            resp = await conn.fetchrow(query, *args)

        return resp

    async def fetch(self, query: str, *args: Any) -> List[Dict[Any, Any]]:
        async with self._create_connector() as conn:
            resp = await conn.fetch(query, *args)
        return resp

    async def fetchval(self, query: str, *args: Any) -> Optional[Dict[Any, Any]]:
        async with self._create_connector() as conn:
            async with conn.transaction():
                resp = await conn.fetchval(query, *args)
        return resp
