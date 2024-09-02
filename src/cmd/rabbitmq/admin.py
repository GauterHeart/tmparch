import asyncio

from src.controller.admin.delivery.rabbitmq.main import AdminRabbitmqController
from src.controller.admin.delivery.rabbitmq.model import SampleAdminModel
from src.internal.rabbitmq import RabbitStatusHandler
from src.pkg.arch import CMD
from src.pkg.rabbitmq import RabbitConsumer

from ._base import Init


class AdminRabbit(CMD, Init):

    name = "AdminRabbitConsumer"

    async def _run(self) -> None:
        consumer = RabbitConsumer(
            host=self.settings.RABBITMQ_HOST,
            port=self.settings.RABBITMQ_PORT,
            username=self.settings.RABBITMQ_USER,
            password=self.settings.RABBITMQ_PASSWORD,
            queue_name=self.settings.RABBITMQ_QUEUE,
            status_handler=RabbitStatusHandler(),
        )
        handler = AdminRabbitmqController()
        if self.settings.HEALTHCHECK is True:
            healthcheck = self._create_healthcheck()
            consumer_task = asyncio.create_task(
                consumer.broker(
                    handler=handler.execute,
                    schema=SampleAdminModel,
                )
            )
            await asyncio.gather(healthcheck, consumer_task)

        else:
            await consumer.broker(
                handler=handler.execute,
                schema=SampleAdminModel,
            )

    def run(self) -> None:
        asyncio.run(self._run())
