from abc import abstractmethod
from typing import Any, Generic, TypeVar

from .postgresql import PostgresqlDriver
from .redis import RedisDriver

__all__ = []


PT = TypeVar("PT", PostgresqlDriver, RedisDriver)


BASE_TYPE = [str, bytes, None]


class Repository(Generic[PT]):
    cursor: PT = NotImplemented

    @classmethod
    def setup(cls, cursor: PT) -> None:
        cls.cursor = cursor

    @classmethod
    def remove_pool(cls) -> None:
        cls.cursor.pool = None

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def fetch(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()


class RepositorySync:
    cursor = NotImplemented

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def fetch(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()
