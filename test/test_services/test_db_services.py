from naks_library.testing.base_test_db_service import BaseTestDBService
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
import pytest

from services.db_services import *
from src.utils.DTOs import *
from database import engine
from shemas import *
from funcs import test_data


@pytest.mark.asyncio
class TestPersonalDBService(BaseTestDBService):
    service = PersonalDBService(AsyncSession(engine))
    __dto__ = PersonalData
    __create_shema__ = CreatePersonalShema
    __update_shema__ = UpdatePersonalShema


    @pytest.mark.usefixtures('personals')
    async def test_add(self, personals: list[PersonalData]) -> None:
        await super().test_add(personals)


    @pytest.mark.usefixtures('personals')
    @pytest.mark.parametrize(
            "attr, index",
            [
                ("kleymo", 1), 
                ("ident", 7), 
                ("kleymo", 5), 
                ("ident", 4)
            ]
    )
    async def test_get(self, attr: str, index: int, personals: list[PersonalData]) -> None:
        ident = getattr(personals[index], attr)

        await super().test_get(ident, personals[index])

    
    @pytest.mark.parametrize(
        "ident, data",
        [(personal.ident, new_personal_data) for personal, new_personal_data in zip(test_data.fake_personals[:5], test_data.fake_personal_generator.generate(5))]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('personal_dicts')
    @pytest.mark.parametrize(
            "index",
            [0, 8, 1]
    )
    async def test_delete(self, personal_dicts: list[dict], index: int) -> None:
        personal = personal_dicts[index]

        await super().test_delete(personal["ident"], personal)


@pytest.mark.asyncio
class TestPersonalCertificationDBService(BaseTestDBService):
    service = PersonalCertificationDBService(AsyncSession(engine))
    __dto__ = PersonalCertificationData
    __create_shema__ = CreatePersonalCertificationShema
    __update_shema__ = UpdatePersonalCertificationShema


    @pytest.mark.usefixtures('personal_certifications')
    async def test_add(self, personal_certifications: list[PersonalCertificationData]) -> None:
        await super().test_add(personal_certifications)


    @pytest.mark.usefixtures('personal_certifications')
    @pytest.mark.parametrize(
        "index",
        [1, 7, 21, 18]
    )
    async def test_get(self, index: int, personal_certifications: list[PersonalCertificationData]) -> None:
        personal_certification = personal_certifications[index]

        await super().test_get(personal_certification.ident, personal_certification)


    @pytest.mark.parametrize(
        "ident, data",
        [(personal_certification.ident, new_personal_certification_data) for personal_certification, new_personal_certification_data in zip(test_data.fake_personal_certifications[:5], test_data.fake_personal_certification_generator.generate(5))]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('personal_certification_dicts')
    @pytest.mark.parametrize(
        "index",
        [1, 7, 21, 18]
    )
    async def test_delete(self, personal_certification_dicts: list[dict], index: int) -> None:
        personal_certification = personal_certification_dicts[index]

        await super().test_delete(personal_certification["ident"], personal_certification)


@pytest.mark.asyncio
class TestNDTDBService(BaseTestDBService):
    service = NDTDBService(AsyncSession(engine))
    __dto__ = NDTData
    __create_shema__ = CreateNDTShema
    __update_shema__ = UpdateNDTShema


    @pytest.mark.usefixtures('ndts')
    async def test_add(self, ndts: list[NDTShema]) -> None:
        await super().test_add(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
        "index",
        [1, 7, 21, 18]
    )
    async def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        ndt = ndts[index]

        await super().test_get(ndt.ident, ndt)


    @pytest.mark.parametrize(
        "ident, data",
        [(ndt.ident, new_ndt_data) for ndt, new_ndt_data in zip(test_data.fake_ndts[:5], test_data.fake_ndt_generator.generate(5))]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('ndt_dicts')
    @pytest.mark.parametrize(
        "index",
        [1, 7, 21, 18]
    )
    async def test_delete(self, ndt_dicts: list[dict], index: int) -> None:
        ndt = ndt_dicts[index]

        await super().test_delete(ndt["ident"], ndt)
