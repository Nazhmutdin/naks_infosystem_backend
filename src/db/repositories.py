import typing as t
from uuid import UUID
from re import fullmatch
from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    Row,
    Column,
    Select,
    Update,
    Delete,
    Insert,
    select,
    inspect,
    delete,
    insert,
    update,
    func
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import InstrumentedAttribute

from errors import GetDBException, UpdateDBException, DeleteDBException, CreateDBException
from db.models import WelderModel, WelderCertificationModel, NDTModel, UserModel, RefreshTokenModel
from db.db_engine import Base


__all__ = [
    "BaseRepository",
    "WelderRepository",
    "WelderCertificationRepository",
    "NDTRepository",
    "UserRepository",
    "RefreshTokenRepository"
]


"""
====================================================================================================
Base repository
====================================================================================================
"""


class BaseRepository(ABC):
    __model__: type[Base]


    def __init__(self, session: AsyncSession) -> None:
        self._session = session


    async def get(self, ident: UUID | str) -> Row | None:
        try:
            stmt = self._dump_get_stmt(ident)
            response = await self._session.execute(stmt)
            result = response.one_or_none()

            return result

        except IntegrityError as e:
            raise GetDBException(e.args[0])


    async def add(self, *data: dict[str, t.Any]) -> None:
        try:
            stmt = self._dump_add_stmt(data)
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise CreateDBException(e.args[0])


    async def update(self, ident: UUID | str, data: dict[str, t.Any]) -> None:
        try:
            stmt = self._dump_update_stmt(ident, data)
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise UpdateDBException(e.args[0])


    async def delete(self, ident: UUID | str) -> None:
        try:
            stmt = self._dump_delete_stmt(ident)
            await self._session.execute(stmt)
        except IntegrityError as e:
            raise DeleteDBException(e.args[0])


    async def count(self, stmt: Select | None = None) -> int:
        if stmt:
            stmt.select(func.count()).select_from(self.__model__)

            return (await self._session.execute(stmt)).scalar_one()

        else:
            return (await self._session.execute(select(func.count()).select_from(self.__model__))).scalar_one()


    def _get_column(self, ident: str | UUID) -> Column:
        return inspect(self.__model__).primary_key[0]


    def _dump_add_stmt(self, data: list[dict[str, t.Any]]) -> Insert:
        return insert(self.__model__).values(
            data
        )


    def _dump_get_stmt(self, ident: str | UUID) -> Select:
        return select(self.__model__).where(
            self._get_column(ident) == ident
        )
    

    def _dump_update_stmt(self, ident: str | UUID, data: dict[str, t.Any]) -> Update:
        return update(self.__model__).where(
            self._get_column(ident) == ident
        ).values(
            **data
        )


    def _dump_delete_stmt(self, ident: str | UUID) -> Delete:
        return delete(self.__model__).where(
            self._get_column(ident) == ident
        )


"""
====================================================================================================
Welder repository
====================================================================================================
"""


class WelderRepository(BaseRepository):
    __model__ = WelderModel

    def _get_column(self, ident: str | UUID) -> InstrumentedAttribute:
        if isinstance(ident, str) and not fullmatch("[A-Z0-9]{4}", ident):
            ident = UUID(ident)

        return WelderModel.ident if isinstance(ident, UUID) else WelderModel.kleymo


"""
====================================================================================================
Welder certification repository
====================================================================================================
"""


class WelderCertificationRepository(BaseRepository):
    __model__ = WelderCertificationModel


"""
====================================================================================================
ndt repository
====================================================================================================
"""


class NDTRepository(BaseRepository):
    __model__ = NDTModel


"""
====================================================================================================
user repository
====================================================================================================
"""


class UserRepository(BaseRepository):
    __model__ = UserModel
    

    def _get_column(self, ident: str | UUID) -> InstrumentedAttribute:
        if isinstance(ident, UUID):
            return UserModel.ident
        
        try:
            UUID(ident)
            return UserModel.ident
        except:
            return UserModel.login


"""
====================================================================================================
refresh token repository
====================================================================================================
"""


class RefreshTokenRepository(BaseRepository):
    __model__ = RefreshTokenModel
