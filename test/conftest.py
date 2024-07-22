from asyncio import run

import pytest

from shemas import *
from database import engine
from settings import Settings
from models import Base

from funcs import get_personals, get_personal_certifications, get_ndts


@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    assert Settings.DB_NAME() == "rhi_test_db"

    async def start_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    run(start_db())


@pytest.fixture
def personals() -> list[PersonalShema]:
    return get_personals()


@pytest.fixture
def personal_certifications() -> list[PersonalCertificationShema]:
    return get_personal_certifications()


@pytest.fixture
def ndts() -> list[NDTShema]:
    return get_ndts()
