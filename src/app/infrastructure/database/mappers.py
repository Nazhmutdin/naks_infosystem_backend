from uuid import UUID

from naks_library.crud_mapper import SqlAlchemyCrudMapper

from app.application.dto import (
    PersonalDTO, 
    CreatePersonalDTO, 
    UpdatePersonalDTO, 
    PersonalNaksCertificationDTO, 
    CreatePersonalNaksCertificationDTO, 
    UpdatePersonalNaksCertificationDTO, 
    NdtDTO,
    CreateNdtDTO,
    UpdateNdtDTO,
    AcstDTO,
    CreateAcstDTO, 
    UpdateAcstDTO
)
from app.infrastructure.database.models import PersonalModel, PersonalNaksCertificationModel, NdtModel, AcstModel


class PersonalMapper(SqlAlchemyCrudMapper[PersonalDTO, CreatePersonalDTO, UpdatePersonalDTO]):
    __model__ = PersonalModel

    def _convert(self, row: PersonalModel) -> PersonalDTO:
        return PersonalDTO(
            kleymo=row.kleymo,
            name=row.name,
            birthday=row.birthday,
            passport_number=row.passport_number,
            exp_age=row.exp_age,
            nation=row.nation,
            ident=row.ident
        )


class PersonalNaksCertificationMapper(SqlAlchemyCrudMapper[PersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO, UpdatePersonalNaksCertificationDTO]):
    __model__ = PersonalNaksCertificationModel


    async def get_certain_personal_naks_certifications(self, personal_ident: UUID) -> list[PersonalNaksCertificationDTO]:
        res = (await self.get_by(PersonalNaksCertificationModel.personal_ident == personal_ident)).scalars().all()

        return [self._convert(el) for el in res]


    def _convert(self, row: PersonalNaksCertificationModel) -> PersonalNaksCertificationDTO:
        return PersonalNaksCertificationDTO(
            ident=row.ident,
            personal_ident=row.personal_ident,
            certification_number=row.certification_number,
            certification_date=row.certification_date,
            expiration_date=row.expiration_date,
            expiration_date_fact=row.expiration_date_fact,
            insert=row.insert,
            company=row.company,
            gtd=row.gtd,
            method=row.method,
            detail_types=row.detail_types,
            joint_types=row.joint_types,
            materials=row.materials,
            detail_thikness_from=row.detail_thikness_from,
            detail_thikness_before=row.detail_thikness_before,
            outer_diameter_from=row.outer_diameter_from,
            outer_diameter_before=row.outer_diameter_before,
            rod_diameter_from=row.rod_diameter_from,
            rod_diameter_before=row.rod_diameter_before,
            detail_diameter_from=row.detail_diameter_from,
            detail_diameter_before=row.detail_diameter_before,
            html=row.html
        )


class NdtMapper(SqlAlchemyCrudMapper[NdtDTO, CreateNdtDTO, UpdateNdtDTO]):
    __model__ = NdtModel


    async def get_certain_personal_ndts(self, personal_ident: UUID) -> list[NdtDTO]:
        res = (await self.get_by(NdtModel.personal_ident == personal_ident)).scalars().all()

        return [self._convert(el) for el in res]


    def _convert(self, row: NdtModel) -> NdtDTO:
        return NdtDTO(
            ident=row.ident,
            personal_ident=row.personal_ident,
            welding_date=row.welding_date,
            company=row.company,
            subcompany=row.subcompany,
            project=row.project,
            ndt_type=row.ndt_type,
            total_welded=row.total_welded,
            total_ndt=row.total_ndt,
            total_accepted=row.total_accepted,
            total_rejected=row.total_rejected
        )


class AcstMapper(SqlAlchemyCrudMapper[AcstDTO, CreateAcstDTO, UpdateAcstDTO]):
    __model__ = AcstModel


    def _convert(self, row: AcstModel) -> AcstDTO:
        return AcstDTO(
            ident=row.ident,
            acst_number=row.acst_number,
            certification_date=row.certification_date,
            expiration_date=row.expiration_date,
            company=row.company,
            gtd=row.gtd,
            method=row.method,
            detail_types=row.detail_types,
            joint_types=row.joint_types,
            materials=row.materials,
            thikness_from=row.thikness_from,
            thikness_before=row.thikness_before,
            diameter_from=row.diameter_from,
            diameter_before=row.diameter_before,
            preheating=row.preheating,
            heat_treatment=row.heat_treatment,
            html=row.html
        )
