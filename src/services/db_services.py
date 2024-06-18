from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, and_

from src.models import *
from src.shemas import *
from src.utils.funcs import to_uuid
from src.utils.uows import UOW


__all__: list[str] = [
    "BaseDBService",
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService",
    "UserDBService",
    "RefreshTokenDBService"
]


class BaseDBService[Shema: BaseShema, Model: Base, RequestShema: BaseRequestShema]:
    __shema__: type[Shema]
    __model__: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.uow = UOW(self.session)


    async def get(self, ident: str | UUID) -> Shema | None:
        async with self.uow as uow:

            res = await self.__model__.get(uow.conn, ident)

            if res:
                return self.__shema__.model_validate(res, from_attributes=True)
            
            return None


    async def get_many(self, request_shema: RequestShema) -> tuple[list[Shema], int]:
        async with self.uow as uow:

            expression = request_shema.dump_expression()

            result, amount = await self.__model__.get_many(uow.conn, expression, request_shema.limit, request_shema.offset)

            if result:
                result = [self.__shema__.model_validate(el, from_attributes=True) for el in result]
            
            return (result, amount)


    async def add[CreateShema: BaseShema](self, *data: CreateShema) -> None:
        async with self.uow as uow:
            data = [el.model_dump() for el in data]
            await self.__model__.create(*data, conn=uow.conn)

            await uow.commit()


    async def update[UpdateShema: BaseShema](self, ident: str | UUID, data: UpdateShema) -> None:
        async with self.uow as uow:
            await self.__model__.update(uow.conn, ident, data.model_dump(exclude_unset=True))

            await uow.commit()


    async def delete(self, *idents: str | UUID) -> None:
        async with self.uow as uow:
            for ident in idents:
                await self.__model__.delete(uow.conn, ident)
            
            await uow.commit()

    
    async def count(self) -> int:
        async with self.uow as uow:
            return await self.__model__.count(uow.conn)


class WelderDBService(BaseDBService[WelderShema, WelderModel, WelderRequestShema]):
    __shema__ = WelderShema
    __model__ = WelderModel


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, WelderCertificationModel, WelderCertificationRequestShema]):
    __shema__ = WelderCertificationShema
    __model__ = WelderCertificationModel


    async def select_by_kleymo(self, kleymo: str) -> list[WelderCertificationShema] | None:
        async with self.uow as uow:
            stmt = select(self.__model__).where(
                self.__model__.kleymo == kleymo
            )

            res = await uow.conn.execute(stmt)

            result = res.scalars().all()

            if result:
                return [self.__shema__.model_validate(el, from_attributes=True) for el in result]

            return None


class NDTDBService(BaseDBService[NDTShema, NDTModel, NDTRequestShema]):
    __shema__ = NDTShema
    __model__ = NDTModel


    async def select_by_kleymo(self, kleymo: str) -> list[NDTShema] | None:
        async with self.uow as uow:

            stmt = select(self.__model__).where(
                self.__model__.kleymo == kleymo
            )

            res = await uow.conn.execute(stmt)

            result = res.scalars().all()

            if result:
                return [self.__shema__.model_validate(el, from_attributes=True) for el in result]

            return None


class UserDBService(BaseDBService[UserShema, UserModel, BaseRequestShema]):
    __shema__ = UserShema
    __model__ = UserModel


class RefreshTokenDBService(BaseDBService[RefreshTokenShema, RefreshTokenModel, RefreshTokenRequestShema]):
    __shema__ = RefreshTokenShema
    __model__ = RefreshTokenModel

    async def revoke_all_user_tokens(self, user_ident: str | UUID) -> None:
        user_ident = to_uuid(user_ident)
 
        async with self.uow as uow:
            stmt = update(self.__model__).where(
                and_(
                    self.__model__.user_ident == user_ident,
                    self.__model__.revoked == False
                )
            ).values(
                revoked=True
            )

            await uow.conn.execute(stmt)
            await uow.commit()
