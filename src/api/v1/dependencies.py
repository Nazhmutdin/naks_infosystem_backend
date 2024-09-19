from uuid import UUID
import typing as t

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends
from naks_library.exc import *
from naks_library import BaseDBService
from naks_library.base_shema import BaseSelectShema, BaseShema

from src.database import get_session

__all__ = [
    "get",
    "get_many",
    "insert",
    "update",
    "delete",
    "SessionDep"
]


SessionDep = t.Annotated[AsyncSession, Depends(get_session)]


_DBService = t.TypeVar("_DBService", bound=BaseDBService)
_SelectShema = t.TypeVar("_SelectShema", bound=BaseSelectShema)
_CreateShema = t.TypeVar("_CreateShema", bound=BaseShema)
_UpdateShema = t.TypeVar("_UpdateShema", bound=BaseShema)
_DTO = t.TypeVar("_DTO")


async def get(
    service: _DBService, 
    ident: UUID, 
    session: AsyncSession
    ) -> _DTO | None:
    try:
        result = await service.get(session, ident)
    except SelectDBException as err:
        raise HTTPException(400, err.message)

    return result


async def get_many(
    service: _DBService,
    filters: _SelectShema,
    session: AsyncSession
    ) -> tuple[list[_DTO], int]:

    try:
        result = await service.get_many(session, filters, filters.limit, filters.offset)
        count = await service.count(session, filters)
    except SelectDBException as err:
        raise HTTPException(400, err.args)

    return result, count


async def insert(
    service: _DBService,
    data: _CreateShema, 
    session: AsyncSession
    ):

    try:
        await service.insert(session, data)
    except InsertDBException as err:
        raise HTTPException(session, 400, err.message)
    

async def update(
    service: _DBService,
    ident: UUID, 
    data: _UpdateShema, 
    session: AsyncSession
    ):

    try:
        await service.update(session, ident, data)
    except UpdateDBException as err:
        raise HTTPException(400, err.args)
    

async def delete(
    service: _DBService,
    ident: UUID, 
    session: AsyncSession
    ):

    try:
        await service.delete(session, ident)
    except DeleteDBException as err:
        raise HTTPException(400, err.args)
