from typing import Callable

from fastapi.routing import APIRouter

from src.controller.admin.delivery.http.response import FetchAdminResponseSchema
from src.pkg.arch import HttpController
from src.repository.postgresql.admin import AdminPgRepo

__all__ = ["AdminController"]


class AdminController(HttpController):
    router = APIRouter(prefix="/admin", tags=["ADMIN"])

    def __init__(self) -> None: ...

    def fetch_endpoint(self) -> Callable:
        @self.router.get(path="/", status_code=200)
        async def wrap() -> FetchAdminResponseSchema:
            result = await AdminPgRepo().fetch()
            return FetchAdminResponseSchema(
                payload=result,
            )

        return wrap
