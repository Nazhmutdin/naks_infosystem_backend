from uuid import UUID, uuid4
from datetime import date

from pydantic import Field, field_validator
from naks_library import BaseShema, to_date


class BasePersonalCertificationShema(BaseShema):
    personal_ident: UUID | None = Field(default=None)
    job_title: str | None = Field(default=None)
    certification_number: str | None = Field(default=None)
    certification_date: date | None = Field(default=None)
    expiration_date: date | None = Field(default=None)
    expiration_date_fact: date | None = Field(default=None)
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
    
    
    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date(cls, v: str | date | None):
        if v == None:
            return None
        
        return to_date(v)


class PersonalCertificationShema(BasePersonalCertificationShema):
    ident: UUID
    personal_ident: UUID
    job_title: str
    certification_number: str
    certification_date: date
    expiration_date: date
    expiration_date_fact: date
    company: str
    gtd: list[str]
    
    
    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date(cls, v: str | date | None):
        return to_date(v)


class CreatePersonalCertificationShema(PersonalCertificationShema):
    ident: UUID = Field(default_factory=uuid4)


class UpdatePersonalCertificationShema(BasePersonalCertificationShema): ...
   