from src.pkg.arch import RabbitmqController

from .model import SampleAdminModel


class AdminRabbitmqController(RabbitmqController):
    async def execute(self, schema: SampleAdminModel) -> None:
        print("NAME = ", schema.name)
