from src.config import get_config
from src.controller.admin.delivery.http.handler import AdminController
from src.pkg.arch import HttpController
from src.pkg.driver.postgresql import PostgresqlDriver
from src.pkg.driver.redis import RedisDriver
from src.repository._base import InitStandartRepository


class ServerMixin:

    def _init_standart_repository(self) -> None:
        settings = get_config()

        postgres_driver = PostgresqlDriver(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            db=settings.POSTGRES_DB,
        )
        redis_driver = RedisDriver(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            user=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
        )

        InitStandartRepository(
            redis_cursor=redis_driver,
            postgres_cursor=postgres_driver,
        )

    def __init_depend(self, controller: HttpController) -> None: ...

    def _init_admin_controller(self) -> AdminController:
        controller = AdminController()
        self.__init_depend(controller=controller)
        controller()
        return controller
