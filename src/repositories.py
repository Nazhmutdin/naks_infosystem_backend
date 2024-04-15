import typing as t
from uuid import UUID
from re import fullmatch
from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    BinaryExpression, 
    Column,
    Select,
    Update,
    Delete, 
    Insert,
    select, 
    and_, 
    or_, 
    any_,
    inspect, 
    delete, 
    insert, 
    update, 
    desc, 
    func
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import InstrumentedAttribute

from errors import GetDBException, GetManyDBException, UpdateDBException, DeleteDBException, CreateDBException
from shemas import *
from models import WelderModel, WelderCertificationModel, NDTModel
from db_engine import Base
from shemas import UpdateWelderCertificationShema


__all__ = [
    "BaseRepository",
    "WelderRepository",
    "WelderCertificationRepository",
    "NDTRepository"
]


"""
====================================================================================================
Base repository
====================================================================================================
"""


class BaseRepository[Shema: BaseShema, CreateShema: BaseShema, UpdateShema: BaseShema](ABC):
    __model__: type[Base]
    __shema__: type[Shema]


    def __init__(self, session: AsyncSession) -> None:
        self._session = session


    async def get(self, ident: UUID | str) -> t.Awaitable[Shema | None]:
        try:
            stmt = await self._dump_get_stmt(ident)
            response = await self._session.execute(stmt)
            result = response.scalar_one_or_none()

            if not result:
                return None

            return self.__shema__.model_validate(result, from_attributes=True)

        except IntegrityError as e:
            raise GetDBException(e.args[0])


    async def add(self, data: CreateShema) -> t.Awaitable[None]:
        try:
            stmt = await self._dump_add_stmt(data)
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise CreateDBException(e.args[0])


    async def update(self, ident: UUID | str, data: UpdateShema) -> t.Awaitable[None]:
        try:
            stmt = await self._dump_update_stmt(ident, data)
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise UpdateDBException(e.args[0])


    async def delete(self, ident: UUID | str) -> t.Awaitable[None]:
        try:
            stmt = await self._dump_delete_stmt(ident)
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise DeleteDBException(e.args[0])


    async def count(self, stmt: Select | None = None) -> int:
        if stmt:
            stmt.select(func.count()).select_from(self.__model__)

            return (await self._session.execute(stmt)).scalar_one()

        else:
            return (await self._session.execute(select(func.count()).select_from(self.__model__))).scalar_one()

    
    @property
    async def pk_column(self) -> Column:
        return inspect(self.__model__).primary_key[0]
    

    async def _dump_add_stmt(self, data: CreateShema) -> Insert:
        return insert(self.__model__).values(
            **data.model_dump(exclude_unset=True)
        )
    

    async def _dump_get_stmt(self, ident: str | UUID) -> Select:
        return select(self.__model__).where(
            await self.pk_column == ident
        )
    

    async def _dump_update_stmt(self, ident: str | UUID, data: UpdateShema) -> Update:
        return update(self.__model__).where(
            await self.pk_column == ident
        ).values(
            **data.model_dump(exclude_unset=True)
        )


    async def _dump_delete_stmt(self, ident: str | UUID) -> Delete:
        return delete(self.__model__).where(
            await self.pk_column == ident
        )


"""
====================================================================================================
Welder repository
====================================================================================================
"""


class WelderRepository(BaseRepository[WelderShema, CreateWelderShema, UpdateWelderShema]):
    __shema__ = WelderShema
    __model__ = WelderModel


    async def _dump_get_stmt(self, ident: str | UUID) -> Select:
        return select(self.__model__).where(
            await self._get_column(ident) == ident
        )
    

    async def _dump_update_stmt(self, ident: str | UUID, data: UpdateWelderShema) -> Update:
        return update(self.__model__).where(
            await self._get_column(ident) == ident
        ).values(
            **data.model_dump(exclude_unset=True)
        )
    

    async def _dump_delete_stmt(self, ident: str | UUID) -> Delete:
        return delete(self.__model__).where(
            await self._get_column(ident) == ident
        )
    

    async def _get_column(self, ident: str | UUID) -> InstrumentedAttribute:
        if isinstance(ident, str) and not fullmatch("[A-Z0-9]{4}", ident):
            ident = UUID(ident)

        return WelderModel.ident if isinstance(ident, UUID) else WelderModel.kleymo



class WelderCertificationRepository(BaseRepository[WelderCertificationShema, CreateWelderCertificationShema, UpdateWelderCertificationShema]):
    __shema__ = WelderCertificationShema
    __model__ = WelderCertificationModel


class NDTRepository(BaseRepository[NDTShema, CreateNDTShema, UpdateNDTShema]):
    __shema__ = NDTShema
    __model__ = NDTModel