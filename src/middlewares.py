from typing import Callable, Awaitable

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.services.auth_service import AuthService


class CheckAccessTokenMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_path = request.url.path

        if request_path.startswith(
            ("/api/v1")
        ):
            service = AuthService()
            token = request.cookies.get("access_token")

            if not token:
                raise HTTPException(
                    400,
                    "access token required"
                )
            
            is_valid_token = service.validate_access_token(token)
            
            if not is_valid_token:
                raise HTTPException(
                    400,
                    "invalid access token"
                )

        res = await call_next(request)

        return res
