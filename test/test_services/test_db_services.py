import pytest
from datetime import date

from pydantic import ValidationError

from services.db_services import *
from utils.funcs import str_to_datetime
from shemas import *


@pytest.mark.usefixtures("prepare_db")
class BaseTestDBService[Shema: BaseShema]:
    service: BaseDBService[Shema, Shema, Shema]
    __create_Shema__: type[BaseShema]
    __update_Shema__: type[BaseShema]

    async def test_add(self, item: Shema) -> None:
        await self.service.add((self.__create_Shema__.model_validate(item, from_attributes=True)))
        assert await self.service.get(item.ident) == item


    async def test_add_many(self, items: list[Shema]) -> None:
        data = [self.__create_Shema__.model_validate(item, from_attributes=True) for item in items]

        await self.service.add_many(data)


    async def test_get(self, attr: str, item: Shema) -> None:

        assert await self.service.get(getattr(item, attr)) == item


    async def test_update(self, ident: str, data: dict) -> None:

        assert await self.service.get(ident)

        await self.service.update(ident, self.__update_Shema__.model_validate(data, from_attributes=True))
        item = await self.service.get(ident)

        for key, value in data.items():
            if isinstance(getattr(item, key), date):
                assert getattr(item, key) == str_to_datetime(value, False).date()
                continue

            assert getattr(item, key) == value

    
    async def test_fail_update(self, ident: str, data: dict, exception) -> None:
        with pytest.raises(exception):
            await self.service.update(ident, self.__update_Shema__.model_validate(data, from_attributes=True))


    async def test_delete(self, item: Shema) -> None:

        await self.service.delete(item.ident)

        assert not bool(await self.service.get(item.ident))

        await self.service.add(self.__create_Shema__.model_validate(item, from_attributes=True))


@pytest.mark.asyncio
class TestWelderDBService(BaseTestDBService):
    service = WelderDBService()
    __create_Shema__ = CreateWelderShema
    __update_Shema__ = UpdateWelderShema


    @pytest.mark.usefixtures('welders')
    async def test_add(self, welders: list[WelderShema]) -> None:
        await super().test_add(welders[0])


    @pytest.mark.usefixtures('welders')
    async def test_add_many(self, welders: list[WelderShema]) -> None:
        await super().test_add_many(welders[1:])


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
        await super().test_get(attr, welders[index])

    
    @pytest.mark.parametrize(
            "ident, data",
            [
                ("095898d1419641b3adf45af287aad3e7", {"name": "dsdsds", "birthday": "15.12.1995"}),
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


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, welders: list[WelderShema], index: int) -> None:
        await super().test_delete(welders[index])


@pytest.mark.asyncio
class TestWelderCertificationDBService(BaseTestDBService):
    service = WelderCertificationDBService()
    __create_Shema__ = CreateWelderCertificationShema
    __update_Shema__ = UpdateWelderCertificationShema


    @pytest.mark.usefixtures('welder_certifications')
    async def test_add(self, welder_certifications: list[WelderCertificationShema]) -> None:
        await super().test_add(welder_certifications[0])


    @pytest.mark.usefixtures('welder_certifications')
    async def test_add_many(self, welder_certifications: list[WelderCertificationShema]) -> None:
        await super().test_add_many(welder_certifications[1:])


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 7, 31, 80]
    )
    async def test_get(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        await super().test_get("ident", welder_certifications[index])


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


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        await super().test_delete(welder_certifications[index])


@pytest.mark.asyncio
class TestNDTDBService(BaseTestDBService):
    service = NDTDBService()
    __create_Shema__ = CreateNDTShema
    __update_Shema__ = UpdateNDTShema


    @pytest.mark.usefixtures('ndts')
    async def test_add(self, ndts: list[NDTShema]) -> None:
        await super().test_add(ndts[0])


    @pytest.mark.usefixtures('ndts')
    async def test_add_many(self, ndts: list[NDTShema]) -> None:
        await super().test_add_many(ndts[1:])


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
                ("97c1a8b30a764bae84be20dab742644a", {"kleymo": "11F9", "company": "adsdsad"}),
                ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"subcompany": "ппмffфва", "welding_date": "1990-05-15"}),
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"total_weld_1": 0.5, "total_weld_2": 5.36}),
            ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)

    
    @pytest.mark.parametrize(
            "ident, data, exception",
            [
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"welding_date": "dsdsds"}, ValidationError),
                ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"kleymo": "asdd"}, ValidationError)
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
