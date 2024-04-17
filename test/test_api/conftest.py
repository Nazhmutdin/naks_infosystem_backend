from asyncio import run

import pytest
from services.db_services import UserDBService

from shemas import CreateUserShema, UserShema


@pytest.fixture
def add_users(users: list[UserShema]):

    async def add_users_async(users: list[UserShema]):
        service = UserDBService()
        
        await service.add_many([CreateUserShema.model_validate(user, from_attributes=True) for user in users])
    
    run(add_users_async(users))