from sqlalchemy import select
from naks_library.base_db_service import BaseDBService

from src.shemas import *
from src.models import PersonalModel, PersonalCertificationModel, NDTModel
from src.utils.DTOs import *


__all__: list[str] = [
    "PersonalDBService",
    "PersonalCertificationDBService",
    "NDTDBService"
]


class PersonalDBService(BaseDBService[PersonalData, PersonalModel, PersonalRequestShema, CreatePersonalShema, UpdatePersonalShema]):
    __dto__ = PersonalData
    __model__ = PersonalModel


class PersonalCertificationDBService(BaseDBService[PersonalCertificationData, PersonalCertificationModel, PersonalCertificationRequestShema, CreatePersonalCertificationShema, UpdatePersonalCertificationShema]):
    __dto__ = PersonalCertificationData
    __model__ = PersonalCertificationModel


    async def select_by_kleymo(self, personal_ident: str) -> list[PersonalCertificationData] | None:
        async with self.uow as uow:
            stmt = select(self.__model__).where(
                self.__model__.personal_ident == personal_ident
            )

            res = await uow.session.execute(stmt)

            result = res.scalars().all()

            if result:
                return [self.__dto__(**el.__dict__) for el in result]


class NDTDBService(BaseDBService[NDTData, NDTModel, NDTRequestShema, CreateNDTShema, UpdateNDTShema]):
    __dto__ = NDTData
    __model__ = NDTModel


    async def select_by_kleymo(self, personal_ident: str) -> list[NDTData] | None:
        async with self.uow as uow:

            stmt = select(self.__model__).where(
                self.__model__.personal_ident == personal_ident
            )

            res = await uow.session.execute(stmt)

            result = res.scalars().all()

            if result:
                return [self.__dto__(**el.__dict__) for el in result]
