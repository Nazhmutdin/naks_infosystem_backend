from uuid import UUID

from naks_library.crud_mapper import SqlAlchemyCrudMapper
from sqlalchemy import select, desc

from app.application.dto import (
    PersonalDTO, 
    CreatePersonalDTO, 
    UpdatePersonalDTO, 
    PersonalNaksCertificationDTO, 
    CreatePersonalNaksCertificationDTO, 
    UpdatePersonalNaksCertificationDTO, 
    NdtDTO,
    CreateNdtDTO,
    UpdateNdtDTO
)
from app.infrastructure.database.models import PersonalModel, PersonalNaksCertificationModel, NdtModel


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
        stmt = select(PersonalNaksCertificationModel).where(
            PersonalNaksCertificationModel.personal_ident == personal_ident
        ).order_by(desc(PersonalNaksCertificationModel.expiration_date_fact))

        res = (await self.session.execute(stmt)).scalars().all()

        return [self._convert(el) for el in res]


    def _convert(self, row: PersonalNaksCertificationModel) -> PersonalNaksCertificationDTO:
        return PersonalNaksCertificationDTO(
            ident=row.ident,
            personal_ident=row.personal_ident,
            job_title=row.job_title,
            certification_number=row.certification_number,
            certification_date=row.certification_date,
            expiration_date=row.expiration_date,
            expiration_date_fact=row.expiration_date_fact,
            insert=row.insert,
            company=row.company,
            gtd=row.gtd,
            method=row.method,
            details_type=row.details_type,
            joint_type=row.joint_type,
            welding_materials_groups=row.welding_materials_groups,
            details_thikness_from=row.details_thikness_from,
            details_thikness_before=row.details_thikness_before,
            outer_diameter_from=row.outer_diameter_from,
            outer_diameter_before=row.outer_diameter_before,
            welding_position=row.welding_position,
            connection_type=row.connection_type,
            rod_diameter_from=row.rod_diameter_from,
            rod_diameter_before=row.rod_diameter_before,
            rod_axis_position=row.rod_axis_position,
            details_diameter_from=row.details_diameter_from,
            details_diameter_before=row.details_diameter_before
        )


class NdtMapper(SqlAlchemyCrudMapper[NdtDTO, CreateNdtDTO, UpdateNdtDTO]):
    __model__ = NdtModel


    async def get_certain_personal_ndts(self, personal_ident: UUID) -> list[NdtDTO]:
        stmt = select(NdtModel).where(
            NdtModel.personal_ident == personal_ident
        ).order_by(desc(NdtModel.welding_date))

        res = (await self.session.execute(stmt)).scalars().all()

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
