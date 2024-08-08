from sqlalchemy.ext.asyncio import AsyncSession
from naks_library.testing.base_test_model import BaseTestModel
import pytest

from src.utils.uows import UOW
from src.utils.DTOs import *
from src.database import engine
from src.models import *
from funcs import test_data


"""
===================================================================================================================
Personal repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestPersonalModel(BaseTestModel[PersonalData]):
    __dto__ = PersonalData
    __model__ = PersonalModel

    uow = UOW(AsyncSession(engine))

    @pytest.mark.usefixtures('personals')
    async def test_create(self, personals: list[PersonalData]) -> None:
        await super().test_create(personals)
    

    @pytest.mark.usefixtures('personals')
    @pytest.mark.parametrize(
        "index",
        [1, 2, 4, 5, 7]
    )
    async def test_create_existing(self, personals: list[PersonalData], index: int) -> None:
        await super().test_create_existing(personals[index])
    

    @pytest.mark.usefixtures('personals')
    @pytest.mark.parametrize(
        "attr, index",
        [
            ("kleymo", 1), 
            ("ident", 7), 
            ("kleymo", 3), 
            ("ident", 4)
        ]
    )
    async def test_get(self, attr: str, index: int, personals: list[PersonalData]) -> None:
        ident = getattr(personals[index], attr)

        await super().test_get(ident, personals[index])
    

    async def test_get_many(self) -> None: ...
    

    @pytest.mark.parametrize(
        "ident, data",
        [(personal.ident, new_personal_data) for personal, new_personal_data in zip(test_data.fake_personals[:5], test_data.fake_personal_generator.generate(5))]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)
    

    @pytest.mark.usefixtures('personals')
    @pytest.mark.parametrize(
            "index",
            [0, 5, 7]
    )
    async def test_delete(self, personals: list[PersonalData], index: int) -> None:
        ident = getattr(personals[index], "ident")

        await super().test_delete(ident, personals[index])

    
"""
===================================================================================================================
personals certification repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestPersonalCertificationModel(BaseTestModel[PersonalCertificationData]):
    __dto__ = PersonalCertificationData
    __model__ = PersonalCertificationModel

    uow = UOW(AsyncSession(engine))

    @pytest.mark.usefixtures('personal_certifications')
    async def test_create(self, personal_certifications: list[PersonalCertificationData]) -> None:
        await super().test_create(personal_certifications)


    @pytest.mark.usefixtures('personal_certifications')
    @pytest.mark.parametrize(
        "index",
        [1, 2, 3, 4, 5, 6]
    )
    async def test_get(self, index: int, personal_certifications: list[PersonalCertificationData]) -> None:
        ident = getattr(personal_certifications[index], "ident")

        await super().test_get(ident, personal_certifications[index])

        
    async def test_get_many(self) -> None: ...


    @pytest.mark.usefixtures('personal_certifications')
    @pytest.mark.parametrize(
        "index",
        [0, 15, 18, 1, 4, 7]
    )
    async def test_create_existing(self, personal_certifications: list[PersonalCertificationData], index: int) -> None:
        await super().test_create_existing(personal_certifications[index])


    @pytest.mark.parametrize(
        "ident, data",
        [(personal_certification.ident, new_personal_certification_data) for personal_certification, new_personal_certification_data in zip(test_data.fake_personal_certifications[:5], test_data.fake_personal_certification_generator.generate(5))]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('personal_certifications')
    @pytest.mark.parametrize(
        "index",
        [0, 15, 18, 1, 4, 7]
    )
    async def test_delete(self, personal_certifications: list[PersonalCertificationData], index: int) -> None:
        ident = getattr(personal_certifications[index], "ident")

        await super().test_delete(ident, personal_certifications[index])


"""
===================================================================================================================
NDT repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestNDTModel(BaseTestModel[NDTData]):
    __dto__ = NDTData
    __model__ = NDTModel

    uow = UOW(AsyncSession(engine))

    @pytest.mark.usefixtures('ndts')
    async def test_create(self, ndts: list[NDTData]) -> None:
        await super().test_create(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
        "index", [1, 7, 18, 11]
    )
    async def test_get(self, index: int, ndts: list[NDTData]) -> None:
        ident = getattr(ndts[index], "ident")

        await super().test_get(ident, ndts[index])

        
    async def test_get_many(self) -> None: ...


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
        "index",
        [1, 2, 4, 5, 11]
    )
    async def test_create_existing(self, ndts: list[NDTData], index: int) -> None:
        await super().test_create_existing(ndts[index])

    
    @pytest.mark.parametrize(
        "ident, data",
        [(ndt.ident, new_ndt_data) for ndt, new_ndt_data in zip(test_data.fake_ndts[:5], test_data.fake_ndt_generator.generate(5))]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 4, 3, 1, 17, 11]
    )
    async def test_delete(self, ndts: list[NDTData], index: int) -> None:
        ident = getattr(ndts[index], "ident")

        await super().test_delete(ident, ndts[index])
