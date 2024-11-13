import asyncio

import pytest

from app.application.dto import PersonalDTO, PersonalNaksCertificationDTO, NdtDTO, AcstDTO
from app.configs import DBConfig
from app.infrastructure.database.models import Base

from funcs import test_data, engine


@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    assert DBConfig.DB_NAME() == "rhi_test_db"

    async def start_db():

        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

            await conn.commit()

    asyncio.run(start_db())


@pytest.fixture
def personals() -> list[PersonalDTO]:
    return test_data.fake_personals


@pytest.fixture
def personal_dicts() -> list[dict]:
    return test_data.fake_personals_dicts


@pytest.fixture
def personal_certifications() -> list[PersonalNaksCertificationDTO]:
    return test_data.fake_personal_certifications


@pytest.fixture
def personal_certification_dicts() -> list[dict]:
    return test_data.fake_personal_certifications_dicts


@pytest.fixture
def ndts() -> list[NdtDTO]:
    return test_data.fake_ndts


@pytest.fixture
def ndt_dicts() -> list[dict]:
    return test_data.fake_ndts_dicts


@pytest.fixture
def acsts() -> list[AcstDTO]:
    return test_data.fake_acsts


@pytest.fixture
def acst_dicts() -> list[dict]:
    return test_data.fake_acsts_dicts
