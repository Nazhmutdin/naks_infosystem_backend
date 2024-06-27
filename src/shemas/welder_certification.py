from uuid import UUID, uuid4
from datetime import date

from pydantic import Field, field_validator
from naks_library import BaseShema, to_date, is_kleymo


class BaseWelderCertificationShema(BaseShema):
    __fields_ignore__ = ["ident"]
    
    kleymo: str | None = Field(default=None)
    job_title: str | None = Field(default=None)
    certification_number: str | None = Field(default=None)
    certification_date: date | None = Field(default=None)
    expiration_date: date | None = Field(default=None)
    expiration_date_fact: date | None = Field(default=None)
    insert: str | None = Field(default=None)
    certification_type: str | None = Field(default=None)
    company: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    welding_materials_groups: list[str] | None = Field(default=None)
    welding_materials: str | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None)
    connection_type: str | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None)
    weld_type: str | None = Field(default=None)
    joint_layer: str | None = Field(default=None)
    sdr: str | None = Field(default=None)
    automation_level: str | None = Field(default=None)
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)
    welding_equipment: str | None = Field(default=None)


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | None):
        if v == None:
            return None
        
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")
    
    
    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date(cls, v: str | date | None):
        if v == None:
            return None
        
        return to_date(v)


class WelderCertificationShema(BaseWelderCertificationShema):
    ident: UUID
    kleymo: str
    certification_number: str
    certification_date: date
    expiration_date: date
    expiration_date_fact: date


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | None):
        
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")
    
    
    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date(cls, v: str | date | None):
        return to_date(v)


class CreateWelderCertificationShema(WelderCertificationShema):
    ident: UUID = Field(default_factory=uuid4)


class UpdateWelderCertificationShema(BaseWelderCertificationShema): ...
   