from uuid import UUID
from datetime import date
from typing import Self

from pydantic.dataclasses import dataclass


__all__ = [ 
    "PersonalData",
    "PersonalCertificationData",
    "NDTData"
]

@dataclass(eq=False)
class PersonalData:
    ident: UUID
    kleymo: str | None
    name: str 
    birthday: date | None
    passport_number: str | None
    exp_age: int | None
    nation: str | None


    def __eq__(self, other: Self) -> bool:
        self_dict = self.__dict__

        for key, value in other.__dict__.items():
            if self_dict[key] != value:
                return False
            
        return True


@dataclass(eq=False)
class PersonalCertificationData:
    ident: UUID
    personal_ident: UUID
    job_title: str
    certification_number: str
    certification_date: date
    expiration_date: date
    expiration_date_fact: date
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


    def __eq__(self, other: Self) -> bool:
        self_dict = self.__dict__

        for key, value in other.__dict__.items():
            if self_dict[key] != value:
                return False
            
        return True


@dataclass(eq=False)
class NDTData:
    ident: UUID
    personal_ident: UUID
    company: str | None
    subcompany: str | None
    project: str | None
    welding_date: date
    ndt_type: str | None
    total_welded: float | None
    total_ndt: float | None
    total_accepted: float | None
    total_rejected: float | None


    def __eq__(self, other: Self) -> bool:
        self_dict = self.__dict__

        for key, value in other.__dict__.items():
            if self_dict[key] != value:
                return False
            
        return True
