from uuid import UUID, uuid4
from datetime import date
import typing  as t

from pydantic import Field
from naks_library import BaseShema
from naks_library.validators import *


class BasePersonalCertificationShema(BaseShema):
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


class PersonalCertificationShema(BasePersonalCertificationShema):
    ident: t.Annotated[UUID, plain_uuid_serializer]
    personal_ident: t.Annotated[UUID, plain_uuid_serializer]
    job_title: str
    certification_number: str
    certification_date: t.Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date: t.Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date_fact: t.Annotated[date, before_date_validator, plain_date_serializer]
    company: str
    gtd: list[str]


class CreatePersonalCertificationShema(PersonalCertificationShema):
    ident: t.Annotated[UUID, plain_uuid_serializer] = Field(default_factory=uuid4)


class UpdatePersonalCertificationShema(BasePersonalCertificationShema): ...
   