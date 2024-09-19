from asyncio import run

import pytest

from shemas import *
from database import engine
from settings import Settings
from models import Base

from funcs import test_data
from src._types import PersonalData, PersonalCertificationData, NDTData


@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    assert Settings.DB_NAME() == "rhi_test_db"

    async def start_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    run(start_db())


@pytest.fixture
def personals() -> list[PersonalData]:
    return test_data.fake_personals


@pytest.fixture
def personal_dicts() -> list[dict]:
    return test_data.fake_personals_dicts


@pytest.fixture
def personal_certifications() -> list[PersonalCertificationData]:
    return test_data.fake_personal_certifications


@pytest.fixture
def personal_certification_dicts() -> list[dict]:
    return test_data.fake_personal_certifications_dicts


@pytest.fixture
def ndts() -> list[NDTData]:
    return test_data.fake_ndts

@pytest.fixture
def ndt_dicts() -> list[dict]:
    return test_data.fake_ndts_dicts
