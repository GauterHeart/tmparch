from src.pkg.driver import PostgresqlDriver, RedisDriver

from .postgresql.admin import AdminPgRepo
from .redis.request import RequestRedisRepo


class InitStandartRepository:
    def __init__(self, redis_cursor: RedisDriver, postgres_cursor: PostgresqlDriver):
        self.__postgres_cursor = postgres_cursor
        self.__redis_cursor = redis_cursor
        self._init_postgres_crud()
        self._init_redis_crud()

    def _init_postgres_crud(self) -> None:
        AdminPgRepo.setup(self.__postgres_cursor)

    def _init_redis_crud(self) -> None:
        RequestRedisRepo.setup(self.__redis_cursor)
