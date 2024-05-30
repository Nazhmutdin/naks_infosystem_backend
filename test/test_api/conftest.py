from asyncio import run

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from services.db_services import UserDBService

from shemas import CreateUserShema, UserShema
from database import engine


@pytest.fixture
def add_users(users: list[UserShema]):

    async def add_users_async(users: list[UserShema]):
        service = UserDBService(AsyncSession(engine))
        
        await service.add(*[CreateUserShema.model_validate(user, from_attributes=True) for user in users])
    
    run(add_users_async(users))