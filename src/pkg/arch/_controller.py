from fastapi import APIRouter
from loguru import logger

from src.pkg.exception import BaseExceptionHandler

__all__ = ["Controller", "HttpController", "RabbitmqController", "ExecuterController"]


class Controller:
    name: str = NotImplemented


class HttpController(Controller):
    router: APIRouter = NotImplemented

    def __call__(self) -> None:
        endpoint_array = list(filter(lambda x: "_endpoint" in x, dir(self)))
        for el in endpoint_array:
            getattr(self, el)()


class RabbitmqController(Controller):
    async def execute(self, *args, **kwargs) -> None:
        raise NotImplementedError()


class ExecuterController(Controller):
    async def run(self, *args, **kwargs) -> None:
        logger.info("==========START==========")
        try:
            await self.execute(*args, **kwargs)

        except BaseExceptionHandler as exc:
            if exc.status_code >= 500:
                logger.critical(f"Status-Code: {exc.status_code}, Detail: {exc.detail}")
                raise Exception(exc.detail)

            elif exc.status_code >= 400:
                logger.warning(f"Status-Code: {exc.status_code}, Detail: {exc.detail}")

        except Exception as exc:
            logger.info(exc)

        logger.info("==========FINISH==========")

    async def execute(self, *args, **kwargs) -> None:
        raise NotImplementedError()
