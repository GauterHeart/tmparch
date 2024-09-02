import asyncio

import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.config import get_config
from src.pkg.driver import PostgresqlDriver, RedisDriver
from src.repository import InitStandartRepository


class Init:
    def __init__(self) -> None:
        self.settings = get_config()

        postgres_driver = PostgresqlDriver(
            host=self.settings.POSTGRES_HOST,
            port=self.settings.POSTGRES_PORT,
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            db=self.settings.POSTGRES_DB,
        )
        redis_driver = RedisDriver(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            user=self.settings.REDIS_USER,
            password=self.settings.REDIS_PASSWORD,
            db=self.settings.REDIS_DB,
        )

        InitStandartRepository(
            postgres_cursor=postgres_driver,
            redis_cursor=redis_driver,
        )

    def _create_healthcheck(self):
        app = FastAPI()
        Instrumentator().instrument(app).expose(app)
        return asyncio.create_task(
            asyncio.to_thread(
                uvicorn.run,
                app,
                host=self.settings.HOST,
                port=self.settings.PORT,
            )
        )
