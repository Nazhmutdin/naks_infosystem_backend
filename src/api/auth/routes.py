from datetime import datetime, timedelta

from fastapi import APIRouter, Response, Depends

from services.auth_service import AuthService
from api.auth.dependencies import get_user


auth_router = APIRouter()


@auth_router.post("/create-user")
async def create_user(): ...


@auth_router.post("/authenticate")
async def authenticate(user = Depends(get_user)):
    
    res = Response()
    
    auth_service = AuthService()

    exp = datetime.now() + timedelta(minutes=60)

    res.set_cookie("access_token", auth_service.create_token(exp_dt=exp, user_id=user.ident), secure=True, httponly=True, path="/api/v1")

    return res


@auth_router.post("/update-tokens")
async def update_tokens(): ...