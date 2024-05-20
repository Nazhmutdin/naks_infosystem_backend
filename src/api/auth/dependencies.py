from pydantic import BaseModel
from fastapi import HTTPException

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