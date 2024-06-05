from datetime import datetime, timedelta, UTC

from fastapi import APIRouter, Response, Depends

from api.auth.dependencies import authorize_dependency, authenticatе_dependency, update_tokens_dependency, AccessToken, RefreshToken


auth_router = APIRouter()


@auth_router.post("/authorizatе")
async def authorizatе(
    tokens: tuple[RefreshToken, AccessToken] = Depends(authorize_dependency)
    ) -> Response: 

    response = Response()

    now = datetime.now(UTC)

    response.set_cookie("refresh_token", tokens[0], httponly=True, secure=True, path="/auth", expires=now  + timedelta(days=1))
    response.set_cookie("access_token", tokens[1], httponly=True, secure=True, path="/api/v1", expires=now  + timedelta(minutes=60))

    return response


@auth_router.post("/authenticatе")
async def authenticatе(access_token: AccessToken = Depends(authenticatе_dependency)) -> Response:
    
    response = Response()

    exp = datetime.now(UTC) + timedelta(minutes=60)

    response.set_cookie("access_token", access_token, secure=True, httponly=True, path="/api/v1", expires=exp)

    return response


@auth_router.post("/update-tokens")
async def update_tokens(tokens: tuple[RefreshToken, AccessToken] = Depends(update_tokens_dependency)) -> Response:
    
    response = Response()

    now = datetime.now(UTC)
    refresh_exp = now + timedelta(days=1)
    access_exp = now + timedelta(minutes=60)

    response.set_cookie("refresh_token", tokens[0], secure=True, httponly=True, path="/auth", expires=refresh_exp)
    response.set_cookie("access_token", tokens[1], secure=True, httponly=True, path="/api/v1", expires=access_exp)

    return response
