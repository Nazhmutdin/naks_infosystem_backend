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
    _uow: UnitOfWork[BaseRepository]
    __shema__: type[BaseShema]


    async def get(self, ident: str | UUID) -> Shema | None:
        async with self._uow as uow:

            res = await uow.repository.get(ident)

            if res:
                return self.__shema__.model_validate(res[0], from_attributes=True)
            
            return None


    async def add(self, *data: CreateShema) -> None:
        async with self._uow as uow:
            data = [el.model_dump() for el in data]
            await uow.repository.add(*data)

            await uow.commit()


    async def update(self, ident: str | UUID, data: UpdateShema) -> None:
        async with self._uow as uow:
            await uow.repository.update(ident, data.model_dump(exclude_unset=True))
            await uow.commit()


    async def delete(self, *idents: str | UUID) -> None:
        async with self._uow as uow:
            for ident in idents:
                await uow.repository.delete(ident)
            
            await uow.commit()

    
    async def count(self) -> int:
        async with self._uow as uow:
            return await uow.repository.count()


class WelderDBService(BaseDBService[WelderShema, CreateWelderShema, UpdateWelderShema]):
    _uow = UnitOfWork(WelderRepository)
    __shema__ = WelderShema


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, CreateWelderCertificationShema, UpdateWelderCertificationShema]):
    _uow = UnitOfWork(WelderCertificationRepository)
    __shema__ = WelderCertificationShema


class NDTDBService(BaseDBService[NDTShema, CreateNDTShema, UpdateNDTShema]):
    _uow = UnitOfWork(NDTRepository)
    __shema__ = NDTShema


class UserDBService(BaseDBService[UserShema, CreateUserShema, UpdateUserShema]):
    _uow = UnitOfWork(UserRepository)
    __shema__ = UserShema


class RefreshTokenDBService(BaseDBService[RefreshTokenShema, CreateRefreshTokenShema, UpdateRefreshTokenShema]):
    _uow = UnitOfWork(RefreshTokenRepository)
    __shema__ = RefreshTokenShema
