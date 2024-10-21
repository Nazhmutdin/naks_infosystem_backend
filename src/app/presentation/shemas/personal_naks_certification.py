from uuid import UUID, uuid4
from datetime import date
import typing  as t

from pydantic import Field
from naks_library.common import BaseShema, BaseSelectShema
from naks_library.utils.validators import (
    plain_uuid_serializer, 
    before_date_validator, 
    plain_date_serializer, 
    plain_optional_uuid_serializer, 
    before_optional_date_validator, 
    plain_optional_date_serializer
)

from app.application.dto import CreatePersonalNaksCertificationDTO, UpdatePersonalNaksCertificationDTO


class CreatePersonalNaksCertificationShema(BaseShema):
    ident: t.Annotated[UUID, plain_uuid_serializer] = Field(default_factory=uuid4)
    personal_ident: t.Annotated[UUID, plain_uuid_serializer] = Field(serialization_alias="personalIdent", validation_alias="personalIdent")
    job_title: str | None = Field(default=None, serialization_alias="jobTitle", validation_alias="jobTitle")
    certification_number: str = Field(serialization_alias="certificationNumber", validation_alias="certificationNumber")
    certification_date: t.Annotated[date, before_date_validator, plain_date_serializer] = Field(serialization_alias="certificationDate", validation_alias="certificationDate")
    expiration_date: t.Annotated[date, before_date_validator, plain_date_serializer] = Field(serialization_alias="expirationDate", validation_alias="expirationDate")
    expiration_date_fact: t.Annotated[date, before_date_validator, plain_date_serializer] = Field(serialization_alias="expirationDateFact", validation_alias="expirationDateFact")
    insert: str | None = Field(default=None)
    company: str
    gtd: list[str]
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None, serialization_alias="detailsType", validation_alias="detailsType")
    joint_type: list[str] | None = Field(default=None, serialization_alias="jointType", validation_alias="jointType")
    welding_materials_groups: list[str] | None = Field(default=None, serialization_alias="weldingMaterialsGroups", validation_alias="weldingMaterialsGroups")
    details_thikness_from: float | None = Field(default=None, serialization_alias="detailsThiknessFrom", validation_alias="detailsThiknessFrom")
    details_thikness_before: float | None = Field(default=None, serialization_alias="detailsThiknessBefore", validation_alias="detailsThiknessBefore")
    outer_diameter_from: float | None = Field(default=None, serialization_alias="outerDiameterFrom", validation_alias="outerDiameterFrom")
    outer_diameter_before: float | None = Field(default=None, serialization_alias="outerDiameterBefore", validation_alias="outerDiameterBefore")
    welding_position: str | None = Field(default=None, serialization_alias="weldingPosition", validation_alias="weldingPosition")
    connection_type: str | None = Field(default=None, serialization_alias="connectionType", validation_alias="connectionType")
    rod_diameter_from: float | None = Field(default=None, serialization_alias="rodDiameterFrom", validation_alias="rodDiameterFrom")
    rod_diameter_before: float | None = Field(default=None, serialization_alias="rodDiameterBefore", validation_alias="rodDiameterBefore")
    rod_axis_position: str | None = Field(default=None, serialization_alias="rodAxisPosition", validation_alias="rodAxisPosition")
    details_diameter_from: float | None = Field(default=None, serialization_alias="detailsDiameterFrom", validation_alias="detailsDiameterFrom")
    details_diameter_before: float | None = Field(default=None, serialization_alias="detailsDiameterBefore", validation_alias="detailsDiameterBefore")


    def to_dto(self) -> CreatePersonalNaksCertificationDTO:
        return CreatePersonalNaksCertificationDTO(
            **self.__dict__
        )


class UpdatePersonalNaksCertificationShema(BaseShema):
    personal_ident: t.Annotated[UUID | None, plain_optional_uuid_serializer] = Field(default=None, serialization_alias="personalIdent", validation_alias="personalIdent")
    job_title: str | None = Field(default=None, serialization_alias="jobTitle", validation_alias="jobTitle")
    certification_number: str | None = Field(default=None, serialization_alias="certificationNumber", validation_alias="certificationNumber")
    certification_date: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None, serialization_alias="certificationDate", validation_alias="certificationDate")
    expiration_date: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None, serialization_alias="expirationDate", validation_alias="expirationDate")
    expiration_date_fact: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None, serialization_alias="expirationDateFact", validation_alias="expirationDateFact")
    insert: str | None = Field(default=None)
    company: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None, serialization_alias="detailsType", validation_alias="detailsType")
    joint_type: list[str] | None = Field(default=None, serialization_alias="jointType", validation_alias="jointType")
    welding_materials_groups: list[str] | None = Field(default=None, serialization_alias="weldingMaterialsGroups", validation_alias="weldingMaterialsGroups")
    details_thikness_from: float | None = Field(default=None, serialization_alias="detailsThiknessFrom", validation_alias="detailsThiknessFrom")
    details_thikness_before: float | None = Field(default=None, serialization_alias="detailsThiknessBefore", validation_alias="detailsThiknessBefore")
    outer_diameter_from: float | None = Field(default=None, serialization_alias="outerDiameterFrom", validation_alias="outerDiameterFrom")
    outer_diameter_before: float | None = Field(default=None, serialization_alias="outerDiameterBefore", validation_alias="outerDiameterBefore")
    welding_position: str | None = Field(default=None, serialization_alias="weldingPosition", validation_alias="weldingPosition")
    connection_type: str | None = Field(default=None, serialization_alias="connectionType", validation_alias="connectionType")
    rod_diameter_from: float | None = Field(default=None, serialization_alias="rodDiameterFrom", validation_alias="rodDiameterFrom")
    rod_diameter_before: float | None = Field(default=None, serialization_alias="rodDiameterBefore", validation_alias="rodDiameterBefore")
    rod_axis_position: str | None = Field(default=None, serialization_alias="rodAxisPosition", validation_alias="rodAxisPosition")
    details_diameter_from: float | None = Field(default=None, serialization_alias="detailsDiameterFrom", validation_alias="detailsDiameterFrom")
    details_diameter_before: float | None = Field(default=None, serialization_alias="detailsDiameterBefore", validation_alias="detailsDiameterBefore")


    def to_dto(self) -> UpdatePersonalNaksCertificationDTO:
        return UpdatePersonalNaksCertificationDTO(
            **self.__dict__
        )


class PersonalNaksCertificationSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None, validation_alias="personalIdents")
    certification_numbers: list[str] | None = Field(default=None, validation_alias="certificationNumbers")
    inserts: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="certificationDateFrom")
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="certificationDateBefore")
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFrom")
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateBefore")
    expiration_date_fact_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFactFrom")
    expiration_date_fact_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFactBefore")
