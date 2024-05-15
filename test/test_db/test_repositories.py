import pytest
import typing as t
from datetime import date

from shemas import WelderCertificationShema
from errors import CreateDBException
from utils.funcs import to_date
from db.repositories import *
from db.uow import UnitOfWork
from shemas import *


"""
===================================================================================================================
repository base test
===================================================================================================================
"""


@pytest.mark.usefixtures("prepare_db")
class BaseTestRepository[Shema: BaseShema]:
    __shema__: type[BaseShema]
    __create_shema__: type[BaseShema]
    __update_shema__: type[BaseShema]
    __repository__: type[BaseRepository]


    async def test_add(self, data: list[Shema]) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:
            for el in data:
                await uow.repository.add(self.__create_shema__.model_validate(el, from_attributes=True).model_dump())
                res = await uow.repository.get(el.ident)

                assert res

                assert self.__shema__.model_validate(res[0], from_attributes=True) == el

            assert await uow.repository.count() == len(data)

            await uow.commit()

    
    async def test_get(self, attr: str, el: Shema) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:

            res = await uow.repository.get(getattr(el, attr))

            assert self.__shema__.model_validate(res[0], from_attributes=True) == el


    async def test_add_existing(self, data: Shema) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:
            with pytest.raises(CreateDBException):
                await uow.repository.add(self.__create_shema__.model_validate(data, from_attributes=True).model_dump())


    async def test_update(self, ident: str, data: dict[str, t.Any]) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:

            await uow.repository.update(ident, data)
            res = await uow.repository.get(ident)

            el = self.__shema__.model_validate(res[0], from_attributes=True)

            for key, value in data.items():
                if isinstance(getattr(el, key), date):
                    assert getattr(el, key) == to_date(value, False)
                    continue

                assert getattr(el, key) == value

            await uow.commit()

    
    async def test_delete(self, item: Shema) -> None:
        async with UnitOfWork(repository_type=self.__repository__) as uow:

            await uow.repository.delete(item.ident)

            assert not await uow.repository.get(item.ident)

            await uow.repository.add(self.__create_shema__.model_validate(item, from_attributes=True).model_dump())
            await uow.commit()


"""
===================================================================================================================
Welder repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestWelderRepository(BaseTestRepository[WelderShema]):
    __shema__ = WelderShema
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
            "ident, data",
            [
                ("d6f81d0030a44b21afc6d6cc8d99e13b", {"name": "dsdsds", "birthday": "15.12.1995"}),
                ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
                ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
            ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        return await super().test_update(ident, self.__update_shema__.model_validate(data).model_dump(exclude_unset=True))
    

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, welders: list[WelderShema], index: int) -> None:
        return await super().test_delete(welders[index])

    
"""
===================================================================================================================
Welder certification repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestWelderCertificationRepository(BaseTestRepository[WelderCertificationShema]):
    __shema__ = WelderCertificationShema
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
        await super().test_update(ident, self.__update_shema__.model_validate(data).model_dump(exclude_unset=True))


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        await super().test_delete(welder_certifications[index])


"""
===================================================================================================================
NDT repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestNDTRepository(BaseTestRepository[NDTShema]):
    __shema__ = NDTShema
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
        await super().test_update(ident, self.__update_shema__.model_validate(data).model_dump(exclude_unset=True))


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, ndts: list[NDTShema], index: int) -> None:
        await super().test_delete(ndts[index])
