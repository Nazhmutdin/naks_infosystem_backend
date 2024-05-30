from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models import *
from shemas import *


__all__: list[str] = [
    "BaseDBService",
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService",
    "UserDBService",
    "RefreshTokenDBService"
]


class BaseDBService[Shema: BaseShema, CreateShema: BaseShema, UpdateShema: BaseShema]:
    __shema__: type[BaseShema]
    __model__: type[Base]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def get(self, ident: str | UUID) -> Shema | None:
        async with self.session.begin():

            res = await self.__model__.get(self.session, ident)

            if res:
                return self.__shema__.model_validate(res[0], from_attributes=True)
            
            return None


    async def add(self, *data: CreateShema) -> None:
        async with self.session.begin():
            data = [el.model_dump() for el in data]
            await self.__model__.create(*data, session=self.session)

            await self.session.commit()


    async def update(self, ident: str | UUID, data: UpdateShema) -> None:
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


class WelderDBService(BaseDBService[WelderShema, CreateWelderShema, UpdateWelderShema]):
    __shema__ = WelderShema
    __model__ = WelderModel


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, CreateWelderCertificationShema, UpdateWelderCertificationShema]):
    __shema__ = WelderCertificationShema
    __model__ = WelderCertificationModel


class NDTDBService(BaseDBService[NDTShema, CreateNDTShema, UpdateNDTShema]):
    __shema__ = NDTShema
    __model__ = NDTModel


class UserDBService(BaseDBService[UserShema, CreateUserShema, UpdateUserShema]):
    __shema__ = UserShema
    __model__ = UserModel


class RefreshTokenDBService(BaseDBService[RefreshTokenShema, CreateRefreshTokenShema, UpdateRefreshTokenShema]):
    __shema__ = RefreshTokenShema
    __model__ = RefreshTokenModel
