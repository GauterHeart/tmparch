import asyncio
import inspect
from abc import ABC, abstractmethod
from typing import Callable, Optional, Type

import aio_pika
import ujson
from aio_pika.abc import AbstractMessage, AbstractRobustConnection
from loguru import logger
from pydantic import BaseModel, SecretStr, parse_obj_as
from pydantic._internal._model_construction import ModelMetaclass

from src.pkg.exception import BaseExceptionHandler

from .exception import (
    RabbitInvalidHandlerFunctionException,
    RabbitInvalidModelTypeException,
    RabbitModelValidatorException,
)


class RabbitStatusHandler(ABC):
    @abstractmethod
    async def func_200(self, msg: AbstractMessage) -> None: ...

    @abstractmethod
    async def func_400(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None: ...

    @abstractmethod
    async def func_500(
        self, msg: AbstractMessage, exception: BaseExceptionHandler
    ) -> None: ...


class RabbitConsumer:
    _connection: AbstractRobustConnection

    def __init__(
        self,
        queue_name: str,
        username: str,
        password: SecretStr,
        host: str,
        port: int,
        status_handler: RabbitStatusHandler,
    ) -> None:
        self.__queue_name = queue_name
        self.__username = username
        self.__password = password
        self.__host = host
        self.__port = port
        self.__status_handler = status_handler

    def __create_dsn(self) -> str:
        return (
            f"amqp://{self.__username}:{self.__password.get_secret_value()}@"
            + f"{self.__host}:{self.__port}/"
        )

    def __model_validator(
        self, msg: AbstractMessage, model: Type[BaseModel]
    ) -> BaseModel:
        try:
            effect = parse_obj_as(model, ujson.loads(msg.body.decode("utf-8")))
            logger.info(f"Message: {effect}")
            return effect
        except Exception:
            raise RabbitModelValidatorException()

    async def broker(self, handler: Callable, schema: Type[BaseModel]) -> None:
        if len(inspect.signature(handler).parameters) != 1:
            raise RabbitInvalidHandlerFunctionException()

        if not isinstance(schema, ModelMetaclass):
            raise RabbitInvalidModelTypeException()

        self._connection = await aio_pika.connect_robust(url=self.__create_dsn())

        async with self._connection:
            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(self.__queue_name, auto_delete=False)
            logger.success(f"START: {self.__queue_name}")
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process() as msg:
                        try:
                            await handler(self.__model_validator(msg=msg, model=schema))
                            await self.__status_handler.func_200(msg=msg)
                            logger.success("Successfully")
                        except BaseExceptionHandler as e:
                            if e.status_code >= 500:
                                logger.critical(
                                    f"Status-Code: {e.status_code}, Detail: {e.detail}"
                                )
                                await self.__status_handler.func_500(
                                    msg=msg, exception=e
                                )
                                raise Exception(e.detail)

                            elif e.status_code >= 400:
                                await self.__status_handler.func_400(
                                    msg=msg, exception=e
                                )
                                logger.warning(
                                    f"Status-Code: {e.status_code}, Detail: {e.detail}"
                                )
                        except Exception as e:
                            logger.warning(e)


class RabbitmqPublisher:
    def __init__(
        self,
        queue: str,
        username: str,
        password: SecretStr,
        host: str,
        port: int,
    ) -> None:
        self.__queue = queue
        self.__username = username
        self.__password = password
        self.__host = host
        self.__port = port

    def __create_dsn(self) -> str:
        return (
            f"amqp://{self.__username}:{self.__password.get_secret_value()}@"
            + f"{self.__host}:{self.__port}/"
        )

    async def publish(self, message: bytes, header_map: Optional[dict] = None) -> None:
        connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
            self.__create_dsn(), loop=asyncio.get_event_loop()
        )  # type: ignore

        channel: aio_pika.abc.AbstractChannel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message,
                headers=header_map,
            ),
            routing_key=self.__queue,
        )

        await connection.close()
