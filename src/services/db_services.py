from uuid import UUID
import typing as t

from _types import (
    WelderData, 
    WelderCertificationData, 
    NDTData, 
    DataBaseRequest,
    WelderDataBaseRequest, 
    WelderCertificationDataBaseRequest, 
    NDTDataBaseRequest
)
from repositories import BaseRepository
from utils.uow import UnitOfWork
from repositories import *
from shemas import *


__all__: list[str] = [
    "BaseDBService",
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService",
]


class BaseDBService[Shema: BaseShema, Request: DataBaseRequest]:
    _uow: UnitOfWork[BaseRepository[Shema, Shema, Shema]]
    __create_shema__: type[BaseShema]
    __update_shema__: type[BaseShema]


    async def get(self, ident: str | UUID) -> Shema | None:
        async with self._uow as uow:
            return await uow.repository.get(ident)


    async def add(self, data: dict) -> None:
        async with self._uow as uow:
            data = self.__create_shema__.model_validate(data)
            await uow.repository.add(data)
            await uow.commit()


    async def add_many(self, data: list[dict]) -> None:
        async with self._uow as uow:
            for el in data:
                await uow.repository.add(self.__create_shema__.model_validate(el))
                
            await uow.commit()


    async def update(self, ident: str | UUID, data: dict) -> None:
        async with self._uow as uow:
            await uow.repository.update(ident, self.__update_shema__.model_validate(data))
            await uow.commit()


    async def delete(self, ident: str | UUID) -> None:
        async with self._uow as uow:
            await uow.repository.delete(ident)
            await uow.commit()

    
    async def count(self) -> int:
        async with self._uow as uow:
            return await uow.repository.count()


class WelderDBService(BaseDBService[WelderShema, WelderDataBaseRequest]):
    _uow = UnitOfWork(WelderRepository)
    __create_shema__ = CreateWelderShema
    __update_shema__ = UpdateWelderShema

    
    async def add(self, **data: t.Unpack[WelderData]) -> None:
        await super().add(data)
    

    async def update(self, ident: str | UUID, **data: t.Unpack[WelderData]) -> None:
        await super().update(ident, data)


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, WelderCertificationDataBaseRequest]):
    _uow = UnitOfWork(WelderCertificationRepository)
    __create_shema__ = CreateWelderCertificationShema
    __update_shema__ = UpdateWelderCertificationShema

    
    async def add(self, **data: t.Unpack[WelderCertificationData]) -> None:
        await super().add(data)


    async def update(self, ident: str | UUID, **data: t.Unpack[WelderCertificationData]) -> None:
        await super().update(ident, data)


class NDTDBService(BaseDBService[NDTShema, NDTDataBaseRequest]):
    _uow = UnitOfWork(NDTRepository)
    __create_shema__ = CreateNDTShema
    __update_shema__ = UpdateNDTShema

    
    async def add(self, **data: t.Unpack[NDTData]) -> None:
        await super().add(data)
    

    async def update(self, ident: str | UUID, **data: t.Unpack[NDTData]) -> None:
        await super().update(ident, data)
