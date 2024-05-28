from datetime import datetime, timedelta
from uuid import UUID
import typing as t

from fastapi import APIRouter, Response, Depends

from api.auth.dependencies import create_access_token, create_refresh_token


auth_router = APIRouter()


@auth_router.post("/create-user")
async def create_user(): ...



@auth_router.post("/authorizatе")
async def authorizatе(access_token: str = Depends(create_access_token), refresh_token = Depends(create_refresh_token)) -> Response: 

    response = Response()

    exp = datetime.now() + timedelta(minutes=60)

    response.set_cookie("access_token", access_token, httponly=True, secure=True, path="/api/v1", expires=exp)

    exp = datetime.now() + timedelta(days=1)

    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=True, path="/auth/authenticatе", expires=exp)

    return response


@auth_router.post("/authenticate")
async def authenticatе(access_token = Depends(create_access_token)) -> Response:
    
    response = Response()

    response.set_cookie("access_token", access_token, secure=True, httponly=True, path="/api/v1")

    return response


@auth_router.post("/update-tokens")
async def update_tokens(): ...
