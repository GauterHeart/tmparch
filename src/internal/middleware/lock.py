import asyncio

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LockMiddelware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.__lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next) -> Response:
        async with self.__lock:
            response = await call_next(request)
        return response
