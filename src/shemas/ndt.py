from uuid import UUID, uuid4
from datetime import date

from pydantic import Field, field_validator

from shemas.base import BaseShema
from shemas.validators import validate_kleymo, to_date_validator


class BaseNDTShema(BaseShema):
    kleymo: str | None = Field(default=None)
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: date | None = Field(default=None)
    total_weld_1: float | None = Field(default=None)
    total_ndt_1: float | None = Field(default=None)
    total_accepted_1: float | None = Field(default=None)
    total_repair_1: float | None = Field(default=None)
    repair_status_1: float | None = Field(default=None)
    total_weld_2: float | None = Field(default=None)
    total_ndt_2: float | None = Field(default=None)
    total_accepted_2: float | None = Field(default=None)
    total_repair_2: float | None = Field(default=None)
    repair_status_2: float | None = Field(default=None)
    total_weld_3: float | None = Field(default=None)
    total_ndt_3: float | None = Field(default=None)
    total_accepted_3: float | None = Field(default=None)
    total_repair_3: float | None = Field(default=None)
    repair_status_3: float | None = Field(default=None)


    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | tuple[int, int, int] | None):
        if v == None:
            return None
        
        return to_date_validator(v)
        

    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | None):
        if v == None:
            return None
        
        if validate_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


class NDTShema(BaseNDTShema):
    ident: UUID
    kleymo: str
    welding_date: date


    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | date | None):
        return to_date_validator(v)


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | None):
        if validate_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


class CreateNDTShema(NDTShema):
    ident: UUID = Field(default_factory=uuid4)


class UpdateNDTShema(BaseNDTShema): ...