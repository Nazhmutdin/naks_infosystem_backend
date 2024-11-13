from typing import Annotated
from uuid import UUID
from datetime import date

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from naks_library.utils.validators import plain_optional_date_serializer, plain_date_serializer, before_date_validator, before_optional_date_validator
from naks_library.common.root import camel_case_alias_generator

"""
===========================================================================================================
personal 
===========================================================================================================
"""


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class BasePersonal:
    kleymo: str | None
    birthday: Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer]
    passport_number: str | None
    exp_age: int | None
    nation: str | None


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class PersonalDTO(BasePersonal):
    ident: UUID
    name: str 


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class CreatePersonalDTO(BasePersonal):
    ident: UUID
    name: str


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class UpdatePersonalDTO(BasePersonal): 
    name: str | None


"""
===========================================================================================================
personal naks certification
===========================================================================================================
"""


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class BasePersonalNaksCertification:
    personal_ident: UUID
    certification_number: str
    certification_date: Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date: Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date_fact: Annotated[date, before_date_validator, plain_date_serializer]
    insert: str | None
    company: str
    gtd: list[str]
    method: str | None
    detail_types: list[str] | None
    joint_types: list[str] | None
    materials: list[str] | None
    detail_thikness_from: float | None
    detail_thikness_before: float | None
    outer_diameter_from: float | None
    outer_diameter_before: float | None
    rod_diameter_from: float | None
    rod_diameter_before: float | None
    detail_diameter_from: float | None
    detail_diameter_before: float | None
    html: str | None


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class PersonalNaksCertificationDTO(BasePersonalNaksCertification):
    ident: UUID
    html: str


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class CreatePersonalNaksCertificationDTO(BasePersonalNaksCertification):
    ident: UUID
    html: str


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class UpdatePersonalNaksCertificationDTO(BasePersonalNaksCertification):
    personal_ident: UUID | None
    certification_number: str | None
    certification_date: Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer]
    expiration_date: Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer]
    expiration_date_fact: Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer]
    company: str | None
    gtd: list[str] | None


"""
===========================================================================================================
ndt
===========================================================================================================
"""


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class BaseNdt:
    personal_ident: UUID
    welding_date: Annotated[date, before_date_validator, plain_date_serializer]
    company: str | None
    subcompany: str | None
    project: str | None
    ndt_type: str
    total_welded: float
    total_ndt: float
    total_accepted: float
    total_rejected: float


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class NdtDTO(BaseNdt):
    ident: UUID


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class CreateNdtDTO(BaseNdt):
    ident: UUID


@dataclass(config=ConfigDict(alias_generator=camel_case_alias_generator, populate_by_name=True))
class UpdateNdtDTO(BaseNdt):
    personal_ident: UUID | None
    welding_date: Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer]
    ndt_type: str | None
    total_welded: float | None
    total_ndt: float | None
    total_accepted: float | None
    total_rejected: float | None
