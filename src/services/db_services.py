from sqlalchemy import select
from naks_library.base_db_service import BaseDBService

from src.models import WelderModel, WelderCertificationModel, NDTModel
from shemas import *


__all__: list[str] = [
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService"
]


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
