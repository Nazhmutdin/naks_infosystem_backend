from sqlalchemy import select
from naks_library.base_db_service import BaseDBService

from src.models import PersonalModel, PersonalCertificationModel, NDTModel
from src.shemas import *


__all__: list[str] = [
    "PersonalDBService",
    "PersonalCertificationDBService",
    "NDTDBService"
]


class PersonalDBService(BaseDBService[PersonalShema, PersonalModel, PersonalRequestShema]):
    __shema__ = PersonalShema
    __model__ = PersonalModel


class PersonalCertificationDBService(BaseDBService[PersonalCertificationShema, PersonalCertificationModel, PersonalCertificationRequestShema]):
    __shema__ = PersonalCertificationShema
    __model__ = PersonalCertificationModel


    async def select_by_kleymo(self, kleymo: str) -> list[PersonalCertificationShema] | None:
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
