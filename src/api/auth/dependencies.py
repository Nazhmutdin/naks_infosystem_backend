from datetime import datetime, timedelta

from pydantic import BaseModel
from fastapi import HTTPException, Depends

from shemas import UserShema
from services.auth_service import AuthService
from services.db_services import UserDBService


class AuthData(BaseModel):
    password: str
    login: str


async def get_user(auth_data: AuthData) -> UserShema:
    
    service = AuthService()
    user = await UserDBService().get(auth_data.login)

    if not user:
        raise HTTPException(
            400,
            f"user ({auth_data.login}) not found",
        )
    
    if not service.validate_password(auth_data.password, user.hashed_password):
        raise HTTPException(
            400,
            f"Invalid password",
        )

    return user


async def create_access_token(user: UserShema = Depends(get_user)) -> str:
    
    auth_service = AuthService()

    token = auth_service.create_access_token(
        user_id=user.ident.hex,
        gen_dt=datetime.now()
    )

    return token


async def create_refresh_token(user: UserShema = Depends(get_user)) -> str:
    
    auth_service = AuthService()

    exp = datetime.now() + timedelta(days=1)

    token = auth_service.gen_refresh_token(
        user_id=user.ident.hex,
        gen_dt=datetime.now(),
        exp_dt=exp
    )

    return token

