from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, _StreamingResponse

__all__ = ["LockLoggerMiddelware"]


class LockLoggerMiddelware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"Request: {request.scope}")

        response: _StreamingResponse = await call_next(request)  # type: ignore
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk  # type: ignore

        response.headers["content-length"] = str(len(response_body))
        response_line = f"HTTP/1.1 {response.status_code} \r\n".encode("utf-8")
        response_headers = b"".join(
            [
                f"{key}: {value}\r\n".encode("utf-8")
                for key, value in response.headers.items()
            ]
        )
        full_response = response_line + response_headers + b"\r\n" + response_body
        logger.info(f"Response: {full_response}")
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
