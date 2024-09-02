import asyncio

from src.controller.admin.delivery.executer.main import AdminExecuterController
from src.pkg.arch import CMD

from ._base import Init


class AdminExec(CMD, Init):

    name = "AdminExec"

    async def __run(self) -> None:
        if self.settings.HEALTHCHECK is True:
            healthcheck = self._create_healthcheck()
            script = asyncio.create_task(
                AdminExecuterController(
                    msg="123",
                ).run()
            )
            await asyncio.gather(healthcheck, script)

        else:
            await AdminExecuterController(
                msg="123",
            ).run()

    def run(self) -> None:
        asyncio.run(self.__run())
