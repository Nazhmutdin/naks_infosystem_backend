import pytest
import typing as t
from datetime import date, datetime
from uuid import UUID
from time import time_ns

from sqlalchemy.ext.asyncio import AsyncSession

from errors import CreateDBException
from utils.funcs import to_date
from shemas import *
from models import *
from database import engine


"""
===================================================================================================================
repository base test
===================================================================================================================
"""


@pytest.mark.usefixtures("prepare_db")
class BaseTestModel[Shema: BaseShema]:
    __shema__: type[BaseShema]
    __model__: type[Base]

    session = AsyncSession(engine)


    async def test_create(self, data: list[Shema]) -> None:
        start = time_ns()

        async with self.session.begin():

            insert_data = [
                el.model_dump() for el in data
            ]
            
            await self.__model__.create(
                *insert_data,
                session=self.session
            )

            for el in data:
                el = self.__shema__.model_validate(el, from_attributes=True)
                result = self.__shema__.model_validate((await self.__model__.get(self.session, el.ident))[0], from_attributes=True)
                assert result == el

            assert await self.__model__.count(self.session) == len(data)

            await self.session.commit()
            await self.session.close()

        print(f"\nExecution time: {(time_ns() - start) / 1_000_000_000} s")


    async def test_create_existing(self, data: Shema) -> None:
        start = time_ns()

        async with self.session.begin():

            with pytest.raises(CreateDBException):
                await self.__model__.create(
                    data.model_dump(),
                    session=self.session
                )

            await self.session.commit()
            await self.session.close()

        print(f"\nExecution time: {(time_ns() - start) / 1_000_000_000} s")

    
    async def test_get(self, attr: str, el: Shema) -> None:
        start = time_ns()

        async with self.session.begin():

            res = await self.__model__.get(self.session, getattr(el, attr))

            assert self.__shema__.model_validate(res[0], from_attributes=True) == el

            await self.session.close()

        print(f"\nExecution time: {(time_ns() - start) / 1_000_000_000} s")


    async def test_update(self, ident: str, data: dict[str, t.Any]) -> None:
        start = time_ns()

        async with self.session.begin():

            await self.__model__.update(self.session, ident, data)

            res = await self.__model__.get(self.session, ident)

            el = self.__shema__.model_validate(res[0], from_attributes=True)

            for key, value in data.items():
                if isinstance(getattr(el, key), date):
                    assert getattr(el, key) == to_date(value, False)
                    continue

                assert getattr(el, key) == value

            await self.session.commit()
            await self.session.close()

        print(f"\nExecution time: {(time_ns() - start) / 1_000_000_000} s")

    
    async def test_delete(self, item: Shema) -> None:
        start = time_ns()

        async with self.session.begin():

            await self.__model__.delete(self.session, item.ident)

            assert not await self.__model__.get(self.session, item.ident)

            await self.__model__.create(item.model_dump(), session=self.session)

            await self.session.commit()
            await self.session.close()

        print(f"\nExecution time: {(time_ns() - start) / 1_000_000_000} s")


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
        return await super().test_create(welders)
    

    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
        "index",
        [1, 2, 63, 4, 5, 11]
    )
    async def test_create_existing(self, welders: list[WelderShema], index: int) -> None:
        return await super().test_create_existing(welders[index])
    

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
            ("d6f81d0030a44b21afc6d6cc8d99e13b", {"name": "dsdsds", "birthday": date(1995, 2, 2)}),
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
            ("97c1a8b30a764bae84be20dab742644a", {"kleymo": "11F9", "company": "adsdsad"}),
            ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"subcompany": "ппмffфва", "welding_date": date(1968, 7, 11)}),
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


"""
===================================================================================================================
User repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestUserModel(BaseTestModel[UserShema]):
    __shema__ = UserShema
    __model__ = UserModel


    @pytest.mark.usefixtures('users')
    async def test_create(self, users: list[UserShema]) -> None:
        await super().test_create(users)


    @pytest.mark.usefixtures('users')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 7]
    )
    async def test_create_existing(self, users: list[UserShema], index: int) -> None:
        await super().test_create_existing(users[index])


    @pytest.mark.usefixtures('users')
    @pytest.mark.parametrize(
        "index, attr",
        [
            (1, "login"),
            (3, "ident"),
            (7, "login"),
            (5, "ident")
        ]
    )
    async def test_get(self, users: list[UserShema], index: int, attr: str) -> None:
        await super().test_get(attr, users[index])


    @pytest.mark.parametrize(
        "ident, data",
        [
            ("TestUser", {"name": "UpdatedName", "email": "hello@mail.ru"}),
            ("eee02230b2f34440bb349480a809bb10", {"sign_date": datetime(2024, 1, 11, 8, 38, 12, 906854), "is_superuser": False}),
            ("TestUser6", {"login_date": datetime(2024, 1, 1, 8, 38, 12, 906854)}),
        ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('users')
    @pytest.mark.parametrize(
            "index",
            [0, 5, 9]
    )
    async def test_delete(self, users: list[UserShema], index: int) -> None:
        await super().test_delete(users[index])


"""
===================================================================================================================
refresh token repository test
===================================================================================================================
"""


@pytest.mark.asyncio
class TestRefreshTokenModel(BaseTestModel[RefreshTokenShema]): 
    __shema__ = RefreshTokenShema
    __model__ = RefreshTokenModel


    @pytest.mark.usefixtures("refresh_tokens")
    async def test_create(self, refresh_tokens: list[RefreshTokenShema]) -> None:
        refresh_tokens = [CreateRefreshTokenShema.model_validate(el, from_attributes=True) for el in refresh_tokens]
        await super().test_create(refresh_tokens)


    @pytest.mark.usefixtures('refresh_tokens')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 4]
    )
    async def test_create_existing(self, refresh_tokens: list[RefreshTokenShema], index: int) -> None: 
        refresh_tokens = [CreateRefreshTokenShema.model_validate(el, from_attributes=True) for el in refresh_tokens]
        await super().test_create_existing(refresh_tokens[index])


    @pytest.mark.usefixtures('refresh_tokens')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 4]
    )
    async def test_get(self, refresh_tokens: list[RefreshTokenShema], index: int) -> None:
        await super().test_get("ident", refresh_tokens[index])


    @pytest.mark.parametrize(
        "ident, data",
        [
            ("60b5e81a6c2840648a0be60d294fbf63", {"revoked": True}),
            ("cdf7987d87a649259a7cf937282216a4", {"user_ident": UUID("72e38f60a025499db25c74aac04ca19b")}),
            ("a7088f670ef94b4f9ef75e3e7fdbfb8e", {"exp_dt": datetime(2024, 6, 1, 8, 38, 12, 906854)}),
        ]
    )
    async def test_update(self, ident: str, data: dict) -> None:
        await super().test_update(ident, data)


    @pytest.mark.usefixtures('refresh_tokens')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 4]
    )
    async def test_delete(self, refresh_tokens: list[RefreshTokenShema], index: int) -> None:
        refresh_tokens = [CreateRefreshTokenShema.model_validate(el, from_attributes=True) for el in refresh_tokens]
        await super().test_delete(refresh_tokens[index])
