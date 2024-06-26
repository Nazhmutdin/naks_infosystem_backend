from asyncio import run

import pytest

from shemas import *
from database import engine
from settings import Settings
from models import Base

from funcs import get_welders, get_welder_certifications, get_ndts


@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    assert Settings.DB_NAME() == "rhi_test"

    async def start_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    run(start_db())


@pytest.fixture
def welders() -> list[WelderShema]:
    return get_welders()


@pytest.fixture
def welder_certifications() -> list[WelderCertificationShema]:
    return get_welder_certifications()


@pytest.fixture
def ndts() -> list[NDTShema]:
    return get_ndts()
