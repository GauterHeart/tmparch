import uvicorn
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.config import get_config
from src.internal.middleware import ProcessTimeMiddelware
from src.pkg.arch import CMD
from src.pkg.exception import BaseExceptionHandler

from ._server import ServerMixin


class Http(CMD, ServerMixin):
    name = "Http"

    __app = FastAPI()

    def __init__(self) -> None:
        self.__redis_connection()
        self.__reg_controller()
        self.__reg_middleware()
        self._config = get_config()
        self._init_standart_repository()

    def __redis_connection(self) -> None: ...

    @staticmethod
    @__app.exception_handler(BaseExceptionHandler)
    async def validation_exception_handler(
        request: Request, exc: BaseExceptionHandler
    ) -> JSONResponse:
        _ = request
        return JSONResponse(exc.detail, status_code=exc.status_code)

    def __reg_controller(self) -> None:
        admin_controller = self._init_admin_controller()
        self.__app.include_router(router=admin_controller.router)

    def __reg_middleware(self) -> None:
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.__app.add_middleware(ProcessTimeMiddelware)
        Instrumentator().instrument(self.__app).expose(self.__app)

    def __call__(self) -> FastAPI:
        return self.__app

    def run(self) -> None:
        uvicorn.run(
            "main:app",
            host=self._config.HOST,
            port=self._config.PORT,
            workers=self._config.WORKER,
            factory=True,
            reload=self._config.RELOAD,
        )
