from datetime import date
import typing as t

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from naks_library import BaseShema, to_date
import pytest

from src.utils.uows import UOW
from src.database import engine
from src.shemas import *
from src.models import *


"""
===================================================================================================================
repository base test
===================================================================================================================
"""


@pytest.mark.usefixtures("prepare_db")
class BaseTestModel[Shema: BaseShema]:
    __shema__: type[BaseShema]
    __model__: type[Base]

    uow = UOW(AsyncSession(engine))

    async def test_create(self, data: list[Shema]) -> None:
        async with self.uow as uow:

            insert_data = [
                el.model_dump() for el in data
            ]
            
            await self.__model__.create(
                insert_data,
                conn=uow.conn
            )

            for el in data:
                el = self.__shema__.model_validate(el, from_attributes=True)
                result = self.__shema__.model_validate((await self.__model__.get(uow.conn, el.ident)), from_attributes=True)
                assert result == el

            assert await self.__model__.count(uow.conn) == len(data)

            await uow.commit()


    async def test_create_existing(self, data: Shema) -> None:

        async with self.uow as uow:

            with pytest.raises(IntegrityError):
                await self.__model__.create(
                    data.model_dump(),
                    conn=uow.conn
                )

            await uow.commit()


    async def test_get(self, attr: str, el: Shema) -> None:

        async with self.uow as uow:
            res = await self.__model__.get(uow.conn, getattr(el, attr))

            assert self.__shema__.model_validate(res, from_attributes=True) == el

    
    async def test_get_many(self, k: int, request_shema: BaseRequestShema) -> None:

        async with self.uow as uow:

            res = await self.__model__.get_many(
                uow.conn,
                request_shema.dump_expression(),
                limit=request_shema.limit,
                offset=request_shema.offset
            )

            assert len(res[0]) == k


    async def test_update(self, ident: str, data: dict[str, t.Any]) -> None:
        async with self.uow as uow:

            await self.__model__.update(uow.conn, ident, data)

            res = await self.__model__.get(uow.conn, ident)

            el = self.__shema__.model_validate(res, from_attributes=True)

            for key, value in data.items():
                if isinstance(getattr(el, key), date):
                    assert getattr(el, key) == to_date(value, False)
                    continue

                assert getattr(el, key) == value

            await uow.commit()


    async def test_delete(self, item: Shema) -> None:
        async with self.uow as uow:

            await self.__model__.delete(uow.conn, item.ident)

            assert not await self.__model__.get(uow.conn, item.ident)

            await self.__model__.create(item.model_dump(), conn=uow.conn)

            await uow.commit()


"""
===================================================================================================================
Welder repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestWelderModel(BaseTestModel[WelderShema]):
    __shema__ = WelderShema
    __model__ = WelderModel

    @pytest.mark.usefixtures('welders')
    async def test_create(self, welders: list[WelderShema]) -> None:
        await super().test_create(welders)
    

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
        "index",
        [1, 2, 63, 4, 5, 11]
    )
    async def test_create_existing(self, welders: list[WelderShema], index: int) -> None:
        await super().test_create_existing(welders[index])
    

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
    

    async def test_get_many(self) -> None: ...
    

    @pytest.mark.parametrize(
        "ident, data",
        [
            ("d6f81d0030a44b21afc6d6cc8d99e13b", {"name": "dsdsds", "birthday": date(1995, 2, 2)}),
            ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
            ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
        ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)
    

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    async def test_delete(self, welders: list[WelderShema], index: int) -> None:
        await super().test_delete(welders[index])

    
"""
===================================================================================================================
Welder certification repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestWelderCertificationModel(BaseTestModel[WelderCertificationShema]):
    __shema__ = WelderCertificationShema
    __model__ = WelderCertificationModel


    @pytest.mark.usefixtures('welder_certifications')
    async def test_create(self, welder_certifications: list[WelderCertificationShema]) -> None:
        await super().test_create(welder_certifications)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
        "index",
        [1, 2, 3, 4, 5, 6]
    )
    async def test_get(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        await super().test_get("ident", welder_certifications[index])

        
    async def test_get_many(self) -> None: ...


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 13, 63, 31, 75, 89]
    )
    async def test_create_existing(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        await super().test_create_existing(welder_certifications[index])


    @pytest.mark.parametrize(
        "ident, data",
        [
            ("cccba2a0ea9047c8837691a740513f6d", {"welding_materials_groups": ["dsdsds"], "certification_date": date(1984, 1, 7)}),
            ("422786ffabd54d74867a8f34950ee0b5", {"job_title": "ппмфва", "kleymo": "11F9", "expiration_date": date(1990, 3, 17)}),
            ("71c20a79706d4fb28f7b84e94881565c", {"insert": "В1", "company": "asasas", "expiration_date_fact": date(2000, 1, 1)}),
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
NDT repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestNDTModel(BaseTestModel[NDTShema]):
    __shema__ = NDTShema
    __model__ = NDTModel


    @pytest.mark.usefixtures('ndts')
    async def test_create(self, ndts: list[NDTShema]) -> None:
        await super().test_create(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
        "index", [1, 7, 31, 80]
    )
    async def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        await super().test_get("ident", ndts[index])

        
    async def test_get_many(self) -> None: ...


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
        "index",
        [1, 2, 63, 4, 5, 11]
    )
    async def test_create_existing(self, ndts: list[NDTShema], index: int) -> None:
        await super().test_create_existing(ndts[index])

    
    @pytest.mark.parametrize(
        "ident, data",
        [
            ("7253f55ada5748e2b9d8e486a1d9692d", {"kleymo": "11F9", "company": "adsdsad"}),
            ("95b61f9d1b1c4dc2b79cce036d85f527", {"subcompany": "ппмffфва", "welding_date": date(2023, 7, 11)}),
            ("b02dd9d6740b403b8853b2d50917a20f", {"total_welded": 0.5, "accepted": 5.36}),
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
