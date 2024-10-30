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
    personal_ident: t.Annotated[UUID, plain_uuid_serializer]
    job_title: str | None = Field(default=None)
    certification_number: str = Field()
    certification_date: t.Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date: t.Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date_fact: t.Annotated[date, before_date_validator, plain_date_serializer] 
    insert: str | None = Field(default=None)
    company: str
    gtd: list[str]
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    welding_materials_groups: list[str] | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None)
    connection_type: str | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None)
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)


    def to_dto(self) -> CreatePersonalNaksCertificationDTO:
        return CreatePersonalNaksCertificationDTO(
            **self.__dict__
        )


class UpdatePersonalNaksCertificationShema(BaseShema):
    personal_ident: t.Annotated[UUID | None, plain_optional_uuid_serializer] = Field(default=None)
    job_title: str | None = Field(default=None)
    certification_number: str | None = Field(default=None)
    certification_date: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None)
    expiration_date: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None)
    expiration_date_fact: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None)
    insert: str | None = Field(default=None)
    company: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    welding_materials_groups: list[str] | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None)
    connection_type: str | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None)
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)


    def to_dto(self) -> UpdatePersonalNaksCertificationDTO:
        return UpdatePersonalNaksCertificationDTO(
            **self.__dict__
        )


class PersonalNaksCertificationSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None)
    certification_numbers: list[str] | None = Field(default=None)
    inserts: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
