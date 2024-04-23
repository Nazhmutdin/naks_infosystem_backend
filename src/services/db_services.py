from uuid import UUID

from db.repositories import BaseRepository
from db.uow import UnitOfWork
from db.repositories import *
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
    _uow: UnitOfWork[BaseRepository[Shema]]


    async def get(self, ident: str | UUID) -> Shema | None:
        async with self._uow as uow:
            return await uow.repository.get(ident)


    async def add(self, data: CreateShema) -> None:
        async with self._uow as uow:
            await uow.repository.add(data.model_dump())
            await uow.commit()


    async def add_many(self, data: list[CreateShema]) -> None:
        async with self._uow as uow:
            for el in data:
                await uow.repository.add(el.model_dump())
                
            await uow.commit()


    async def update(self, ident: str | UUID, data: UpdateShema) -> None:
        async with self._uow as uow:
            await uow.repository.update(ident, data.model_dump(exclude_unset=True))
            await uow.commit()


    async def delete(self, ident: str | UUID) -> None:
        async with self._uow as uow:
            await uow.repository.delete(ident)
            await uow.commit()

    
    async def count(self) -> int:
        async with self._uow as uow:
            return await uow.repository.count()


class WelderDBService(BaseDBService[WelderShema, CreateWelderShema, UpdateWelderShema]):
    _uow = UnitOfWork(WelderRepository)


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, CreateWelderCertificationShema, UpdateWelderCertificationShema]):
    _uow = UnitOfWork(WelderCertificationRepository)


class NDTDBService(BaseDBService[NDTShema, CreateNDTShema, UpdateNDTShema]):
    _uow = UnitOfWork(NDTRepository)


class UserDBService(BaseDBService[UserShema, CreateUserShema, UpdateUserShema]):
    _uow = UnitOfWork(UserRepository)


class RefreshTokenDBService(BaseDBService[RefreshTokeShema, CreateRefreshTokeShema, UpdateRefreshTokeShema]):
    _uow = UnitOfWork(RefreshTokenRepository)
