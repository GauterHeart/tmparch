from aio_pika.abc import AbstractMessage

from src.pkg.exception import BaseExceptionHandler
from src.pkg.rabbitmq import RabbitStatusHandler as _RabbitStatusHandlerABC


class RabbitStatusHandler(_RabbitStatusHandlerABC):
    async def func_200(self, msg: AbstractMessage) -> None: ...

    async def func_400(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None: ...

    async def func_500(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None: ...
