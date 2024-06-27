from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from naks_library import BaseShema

from src.errors import CreateDBException, UpdateDBException, GetDBException, GetManyDBException, DeleteDBException
from src.utils.uows import UOW
from src.models import *
from src.shemas import *


__all__: list[str] = [
    "BaseDBService",
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService"
]


class BaseDBService[Shema: BaseShema, Model: Base, RequestShema: BaseRequestShema]:
    __shema__: type[Shema]
    __model__: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.uow = UOW(self.session)


    async def get(self, ident: str | UUID) -> Shema | None:
        try:
            return await self._get(ident)
        except IntegrityError as e:
            raise GetDBException(e)


    async def get_many(self, request_shema: RequestShema) -> tuple[list[Shema], int]:
        try:
            return await self._get_many(request_shema)
        except IntegrityError as e:
            raise GetManyDBException(e)


    async def add[CreateShema: BaseShema](self, *data: CreateShema) -> None:
        try:
            await self._add(list(data))
        except IntegrityError as e:
            raise CreateDBException(e, self.__model__)


    async def update[UpdateShema: BaseShema](self, ident: str | UUID, data: UpdateShema) -> None:
        try:
            await self._update(ident, data)
        except IntegrityError as e:
            raise UpdateDBException(e)


    async def delete(self, *idents: str | UUID) -> None:
        try:
            await self._delete(idents)
        except IntegrityError as e:
            raise DeleteDBException(e)

    
    async def count(self) -> int:
        async with self.uow as uow:

                return await self.__model__.count(uow.conn)
            

    async def _get(self, ident: UUID | str) -> Shema | None:
        async with self.uow as uow:

            res = await self.__model__.get(uow.conn, ident)

            if res:
                return self.__shema__.model_validate(res, from_attributes=True)


    async def _get_many(self, request_shema: RequestShema) -> tuple[list[Shema], int]:
        async with self.uow as uow:
            expression = request_shema.dump_expression()

            result, amount = await self.__model__.get_many(uow.conn, expression, request_shema.limit, request_shema.offset)

            if result:
                result = [self.__shema__.model_validate(el, from_attributes=True) for el in result]
            
            return (result, amount)


    async def _add[CreateShema: BaseShema](self, data: list[CreateShema]) -> None:
        async with self.uow as uow:
            await self.__model__.create(
                [el.model_dump() for el in data], 
                uow.conn
            )

            await uow.commit()


    async def _update[UpdateShema: BaseShema](self, ident: str | UUID, data: UpdateShema) -> None:
        async with self.uow as uow:
            await self.__model__.update(uow.conn, ident, data.model_dump(exclude_unset=True))

            await uow.commit()


    async def _delete(self, idents: list[str | UUID]) -> None:
        async with self.uow as uow:
            for ident in idents:
                await self.__model__.delete(uow.conn, ident)
            
            await uow.commit()


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
