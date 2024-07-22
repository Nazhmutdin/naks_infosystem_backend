from naks_library.testing.base_test_db_service import BaseTestDBService
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
import pytest

from services.db_services import *
from database import engine
from shemas import *


@pytest.mark.asyncio
class TestPersonalDBService(BaseTestDBService):
    service = PersonalDBService(AsyncSession(engine))
    __create_shema__ = CreatePersonalShema
    __update_shema__ = UpdatePersonalShema


    @pytest.mark.usefixtures('personals')
    async def test_add(self, personals: list[PersonalShema]) -> None:
        await super().test_add(personals)


    @pytest.mark.usefixtures('personals')
    @pytest.mark.parametrize(
            "attr, index",
            [
                ("kleymo", 1), 
                ("ident", 7), 
                ("kleymo", 31), 
                ("ident", 80)
            ]
    )
    async def test_get(self, attr: str, index: int, personals: list[PersonalShema]) -> None:
        await super().test_get(attr, personals[index])

    
    @pytest.mark.parametrize(
        "ident, data",
        [
            ("b322c9931e85407d8aa4a7463cf78d79", {"name": "dsdsds", "birthday": "15.12.1995"}),
            ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
            ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
        ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)

    
    @pytest.mark.parametrize(
        "ident, data",
        [
            ("095898d1419641b3adf45af287aad3e7", {"kleymo": "aaa"}),
            ("9c66aab293244178bb63e579b43474d4", {"name": 111}),
        ]
    )
    async def test_fail_update(self, ident: str, data: dict) -> None:
        await super().test_fail_update(ident, data, ValidationError)


    @pytest.mark.usefixtures('personals')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, personals: list[PersonalShema], index: int) -> None:
        await super().test_delete(personals[index])


@pytest.mark.asyncio
class TestPersonalCertificationDBService(BaseTestDBService):
    service = PersonalCertificationDBService(AsyncSession(engine))
    __create_shema__ = CreatePersonalCertificationShema
    __update_shema__ = UpdatePersonalCertificationShema


    @pytest.mark.usefixtures('personal_certifications')
    async def test_add(self, personal_certifications: list[PersonalCertificationShema]) -> None:
        await super().test_add(personal_certifications)


    @pytest.mark.usefixtures('personal_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 7, 31, 80]
    )
    async def test_get(self, index: int, personal_certifications: list[PersonalCertificationShema]) -> None:
        await super().test_get("ident", personal_certifications[index])


    @pytest.mark.parametrize(
        "ident, data",
        [
            ("cccba2a0ea9047c8837691a740513f6d", {"welding_materials_groups": ["dsdsds"], "certification_date": "15.12.1995"}),
            ("422786ffabd54d74867a8f34950ee0b5", {"job_title": "ппмфва", "kleymo": "11F9", "expiration_date": "1990-05-15"}),
            ("71c20a79706d4fb28f7b84e94881565c", {"insert": "В1", "company": "asasas", "expiration_date_fact": "2025-10-20"}),
            ("435a9de3ade64c38b316dd08c3c7bc7c", {"connection_type": "gggg", "outer_diameter_from": 11.65, "details_type": ["2025-10-20", "ffff"]}),
        ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)
        
    
    @pytest.mark.parametrize(
        "ident, data, exception",
        [
            ("65ea5301573b4e8e8c114c4385a2a5a8", {"certification_date": "dsdsds"}, ValidationError),
            ("1840a50837784bf9bbf1b282c1fcfb49", {"expiration_date": "T15563212"}, ValidationError),
            ("06beeb64be754167a251e7f756a1d2be", {"expiration_date_fact": "RUS"}, ValidationError),
            ("435a9de3ade64c38b316dd08c3c7bc7c", {"kleymo": "RUS"}, ValidationError),
        ]
    )
    async def test_fail_update(self, ident: str, data: dict, exception) -> None:
        await super().test_fail_update(ident, data, exception)


    @pytest.mark.usefixtures('personal_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, personal_certifications: list[PersonalCertificationShema], index: int) -> None:
        await super().test_delete(personal_certifications[index])


@pytest.mark.asyncio
class TestNDTDBService(BaseTestDBService):
    service = NDTDBService(AsyncSession(engine))
    __create_shema__ = CreateNDTShema
    __update_shema__ = UpdateNDTShema


    @pytest.mark.usefixtures('ndts')
    async def test_add(self, ndts: list[NDTShema]) -> None:
        await super().test_add(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [1, 7, 31, 80]
    )
    async def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        await super().test_get("ident", ndts[index])


    @pytest.mark.parametrize(
        "ident, data",
        [
            ("b02dd9d6740b403b8853b2d50917a20f", {"kleymo": "11F9", "company": "adsdsad"}),
            ("0164e678f8ae4acaa3a9921f25edf797", {"subcompany": "ппмffфва", "welding_date": "1990-05-15"}),
            ("4a71c969b3e1464b8951ed987a55ed90", {"total_welded": 0.5, "accepted": 5.36}),
        ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)

    
    @pytest.mark.parametrize(
        "ident, data, exception",
        [
            ("4a71c969b3e1464b8951ed987a55ed90", {"welding_date": "dsdsds"}, ValidationError),
            ("14130c3550454d0faad45f15bd88993f", {"kleymo": "asdd"}, ValidationError)
        ]
    )
    async def test_fail_update(self, ident: str, data: dict, exception) -> None:
        await super().test_fail_update(ident, data, exception)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, ndts: list[NDTShema], index: int) -> None:
        await super().test_delete(ndts[index])
