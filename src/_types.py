import typing as t
from uuid import UUID
from datetime import date

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from naks_library import Eq
from naks_library.validators import before_optional_date_validator, before_date_validator


class SelectResponse[T](BaseModel):
    result: list[T]
    count: int


@dataclass(eq=False)
class PersonalData(Eq):
    ident: UUID
    kleymo: str | None
    name: str 
    birthday: t.Annotated[date | None, before_optional_date_validator]
    passport_number: str | None
    exp_age: int | None
    nation: str | None


@dataclass(eq=False)
class PersonalCertificationData(Eq):
    ident: UUID
    personal_ident: UUID
    job_title: str
    certification_number: str
    certification_date: t.Annotated[date, before_date_validator]
    expiration_date: t.Annotated[date, before_date_validator]
    expiration_date_fact: t.Annotated[date, before_date_validator]
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


@dataclass(eq=False)
class NDTData(Eq):
    ident: UUID
    personal_ident: UUID
    company: str | None
    subcompany: str | None
    project: str | None
    welding_date: t.Annotated[date, before_date_validator]
    ndt_type: str | None
    total_welded: float | None
    total_ndt: float | None
    total_accepted: float | None
    total_rejected: float | None
