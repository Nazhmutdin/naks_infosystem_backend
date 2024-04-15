import pytest

from shemas import WelderCertificationShema
from base_test_classes import BaseTestRepository
from repositories import *
from shemas import *


"""
===================================================================================================================
Welder repository
===================================================================================================================
"""


@pytest.mark.asyncio
@pytest.mark.run(order=1)
class TestWelderRepository(BaseTestRepository):
    __repository__ = WelderRepository
    __create_shema__ = CreateWelderShema
    __update_shema__ = UpdateWelderShema

    @pytest.mark.usefixtures('welders')
    async def test_add(self, welders: list[WelderShema]) -> None:
        return await super().test_add(welders)
    

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    async def test_add_existing(self, welders: list[WelderShema], index: int) -> None:
        return await super().test_add_existing(welders[index])
    

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "attr, index",
            [
                ("kleymo", 1), 
                ("ident", 7), 
                ("kleymo", 31), 
                ("ident", 80)
            ]
    )
    async def test_get(self, attr: str, index: int, welders: list[WelderShema]) -> None:
        return await super().test_get(attr, welders[index])
    

    @pytest.mark.parametrize(
            "ident",
            ["1M65", "1E41", "1HC0"]
    )
    async def test_res_type(self, ident: int | str) -> None:
        return await super().test_res_type(ident, WelderShema)
    

    @pytest.mark.parametrize(
            "ident, data",
            [
                ("095898d1419641b3adf45af287aad3e7", {"name": "dsdsds", "birthday": "15.12.1995"}),
                ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
                ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
            ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        return await super().test_update(ident, data)
    

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, welders: list[WelderShema], index: int) -> None:
        return await super().test_delete(welders[index])

    
"""
===================================================================================================================
Welder certification repository
===================================================================================================================
"""


@pytest.mark.asyncio
@pytest.mark.run(order=2)
class TestWelderCertificationRepository(BaseTestRepository):
    __repository__ = WelderCertificationRepository
    __create_shema__ = CreateWelderCertificationShema
    __update_shema__ = UpdateWelderCertificationShema


    @pytest.mark.usefixtures('welder_certifications')
    async def test_add(self, welder_certifications: list[WelderCertificationShema]) -> None:
        await super().test_add(welder_certifications)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 3, 4, 5, 6]
    )
    async def test_get(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        await super().test_get("ident", welder_certifications[index])


    @pytest.mark.parametrize(
            "ident",
            ["46a9381ae8cb4143958152bf25c30fbe", "10c58804bc7c4bfdb24bceba51334f00", "11d0248261db4f6ca236f194087daeca"]
    )
    async def test_res_type(self, ident: int | str) -> None:
        await super().test_res_type(ident, WelderCertificationShema)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 13, 63, 31, 75, 89]
    )
    async def test_add_existing(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        await super().test_add_existing(welder_certifications[index])


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


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        await super().test_delete(welder_certifications[index])


"""
===================================================================================================================
NDT repository
===================================================================================================================
"""


@pytest.mark.asyncio
@pytest.mark.run(order=3)
class TestNDTRepository(BaseTestRepository):
    __repository__ = NDTRepository
    __create_shema__ = CreateNDTShema
    __update_shema__ = UpdateNDTShema


    @pytest.mark.usefixtures('ndts')
    async def test_add(self, ndts: list[NDTShema]) -> None:
        await super().test_add(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index", [1, 7, 31, 80]
    )
    async def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        await super().test_get("ident", ndts[index])


    @pytest.mark.parametrize(
        "ident", ["bb380cb216fb4505aa0d78a1b6b7abc4", "b5636169bc624eeb9a4b61c1bdb059b5", "f0f0ba353ebf4fd39924afbccad0a24b",]
    )
    async def test_res_type(self, ident: int | str) -> None:
        await super().test_res_type(ident, NDTShema)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    async def test_add_existing(self, ndts: list[NDTShema], index: int) -> None:
        await super().test_add_existing(ndts[index])

    
    @pytest.mark.parametrize(
            "ident, data",
            [
                ("97c1a8b30a764bae84be20dab742644a", {"kleymo": "11F9", "company": "adsdsad"}),
                ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"subcompany": "ппмffфва", "welding_date": "1990-05-15"}),
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"total_weld_1": 0.5, "total_weld_2": 5.36}),
            ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, ndts: list[NDTShema], index: int) -> None:
        await super().test_delete(ndts[index])
