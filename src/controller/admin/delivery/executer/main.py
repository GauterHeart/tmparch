from src.pkg.arch import ExecuterController


class AdminExecuterController(ExecuterController):
    def __init__(
        self,
        msg: str,
    ) -> None:
        self.msg = msg

    async def execute(self) -> None:
        await self._execute()

    async def _execute(self) -> None:
        print(self.msg)
