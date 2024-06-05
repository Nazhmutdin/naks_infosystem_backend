from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from models import *
from shemas import *
from utils.funcs import to_uuid


__all__: list[str] = [
    "BaseDBService",
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService",
    "UserDBService",
    "RefreshTokenDBService"
]


class BaseDBService[Shema: BaseShema, Model: Base]:
    __shema__: type[Shema]
    __model__: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get(self, ident: str | UUID) -> Shema | None:
        async with self.session.begin():

            res = await self.__model__.get(self.session, ident)

            if res:
                return self.__shema__.model_validate(res[0], from_attributes=True)
            
            return None


    async def get_many(self, request_shema: BaseRequestShema) -> list[Shema] | None:
        async with self.session.begin():

            res = await self.__model__.get_many(self.session, request_shema.dump_expression())

            if res:
                return [self.__shema__.model_validate(el[0], from_attributes=True) for el in res]
            
            return None


    async def add[CreateShema: BaseShema](self, *data: CreateShema) -> None:
        async with self.session.begin():
            data = [el.model_dump() for el in data]
            await self.__model__.create(*data, session=self.session)

            await self.session.commit()


    async def update[UpdateShema: BaseShema](self, ident: str | UUID, data: UpdateShema) -> None:
        async with self.session.begin():
            await self.__model__.update(self.session, ident, data.model_dump(exclude_unset=True))
            await self.session.commit()


    async def delete(self, *idents: str | UUID) -> None:
        async with self.session.begin():
            for ident in idents:
                await self.__model__.delete(self.session, ident)
            
            await self.session.commit()

    
    async def count(self) -> int:
        async with self.session.begin():
            return await self.__model__.count(self.session)


class WelderDBService(BaseDBService[WelderShema, WelderModel]):
    __shema__ = WelderShema
    __model__ = WelderModel


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, WelderCertificationModel]):
    __shema__ = WelderCertificationShema
    __model__ = WelderCertificationModel


class NDTDBService(BaseDBService[NDTShema, NDTModel]):
    __shema__ = NDTShema
    __model__ = NDTModel


class UserDBService(BaseDBService[UserShema, UserModel]):
    __shema__ = UserShema
    __model__ = UserModel


class RefreshTokenDBService(BaseDBService[RefreshTokenShema, RefreshTokenModel]):
    __shema__ = RefreshTokenShema
    __model__ = RefreshTokenModel

    async def revoke_all_user_tokens(self, user_ident: str | UUID) -> None:
        user_ident = to_uuid(user_ident)

        async with self.session.begin():
            stmt = update(self.__model__).where(
                self.__model__.user_ident == user_ident
            ).values(
                revoked=True
            )

            await self.session.execute(stmt)