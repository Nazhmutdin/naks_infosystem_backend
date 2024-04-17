from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Response

from services.db_services import UserDBService
from services.auth_service import AuthService
from api.auth.dependencies import AuthData


auth_router = APIRouter()


@auth_router.post("/create-user")
async def create_user(): ...


@auth_router.post("/authenticate")
async def authenticate(data: AuthData): 
    service = AuthService()
    user = await UserDBService().get(data.login)

    if not user:
        raise HTTPException(
            400,
            f"user ({data.login}) not found",
        )
    
    if not service.validate_password(data.password, user.hashed_password):
        raise HTTPException(
            400,
            f"Invalid password",
        )
    
    res = Response()

    exp = datetime.now() + timedelta(minutes=60)

    res.set_cookie("access_token", service.create_token(exp_dt=exp, user_id=user.ident), secure=True, httponly=True, path="/api/v1")

    return res


@auth_router.post("/update-tokens")
async def update_tokens(): ...