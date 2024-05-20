from typing import Callable, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class CheckAccessTokenMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_path = request.url.path

        if request_path.startswith(
            ("api/v1")
        ):
            ...

        res = await call_next(request)

        return res