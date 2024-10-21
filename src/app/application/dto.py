from typing import Annotated
from uuid import UUID
from datetime import date

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from naks_library.utils.validators import plain_optional_date_serializer, plain_date_serializer
from naks_library.common.root import camel_case_serialization_alias_generator

"""
===========================================================================================================
personal 
===========================================================================================================
"""


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class BasePersonal:
    kleymo: str | None
    birthday: Annotated[date | None, plain_optional_date_serializer]
    passport_number: str | None
    exp_age: int | None
    nation: str | None


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class PersonalDTO(BasePersonal):
    ident: UUID
    name: str 


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class CreatePersonalDTO(BasePersonal):
    ident: UUID
    name: str


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class UpdatePersonalDTO(BasePersonal): 
    name: str | None


"""
===========================================================================================================
personal naks certification
===========================================================================================================
"""


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class BasePersonalNaksCertification:
    personal_ident: UUID
    job_title: str
    certification_number: str
    certification_date: Annotated[date, plain_date_serializer]
    expiration_date: Annotated[date, plain_date_serializer]
    expiration_date_fact: Annotated[date, plain_date_serializer]
    insert: str | None
    company: str
    gtd: list[str]
    method: str | None
    details_type: list[str] | None
    joint_type: list[str] | None
    welding_materials_groups: list[str] | None
    details_thikness_from: float | None
    details_thikness_before: float | None
    outer_diameter_from: float | None
    outer_diameter_before: float | None
    welding_position: str | None
    connection_type: str | None
    rod_diameter_from: float | None
    rod_diameter_before: float | None
    rod_axis_position: str | None
    details_diameter_from: float | None
    details_diameter_before: float | None


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class PersonalNaksCertificationDTO(BasePersonalNaksCertification):
    ident: UUID


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class CreatePersonalNaksCertificationDTO(BasePersonalNaksCertification):
    ident: UUID


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class UpdatePersonalNaksCertificationDTO(BasePersonalNaksCertification):
    personal_ident: UUID | None
    job_title: str | None
    certification_number: str | None
    certification_date: Annotated[date | None, plain_optional_date_serializer]
    expiration_date: Annotated[date | None, plain_optional_date_serializer]
    expiration_date_fact: Annotated[date | None, plain_optional_date_serializer]
    company: str | None
    gtd: list[str] | None


"""
===========================================================================================================
ndt
===========================================================================================================
"""


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class BaseNdt:
    personal_ident: UUID
    welding_date: Annotated[date, plain_date_serializer]
    company: str | None
    subcompany: str | None
    project: str | None
    ndt_type: str
    total_welded: float
    total_ndt: float
    total_accepted: float
    total_rejected: float


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class NdtDTO(BaseNdt):
    ident: UUID


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class CreateNdtDTO(BaseNdt):
    ident: UUID


@dataclass(config=ConfigDict(alias_generator=camel_case_serialization_alias_generator))
class UpdateNdtDTO(BaseNdt):
    personal_ident: UUID | None
    welding_date: Annotated[date | None, plain_optional_date_serializer]
    ndt_type: str | None
    total_welded: float | None
    total_ndt: float | None
    total_accepted: float | None
    total_rejected: float | None
