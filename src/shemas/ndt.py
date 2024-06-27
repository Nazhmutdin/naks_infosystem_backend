from uuid import UUID, uuid4
from datetime import date

from pydantic import Field, field_validator
from naks_library import BaseShema, to_date, is_kleymo


class BaseNDTShema(BaseShema):
    __fields_ignore__ = ["ident"]
    
    kleymo: str | None = Field(default=None)
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: date | None = Field(default=None)
    ndt_type: str | None = Field(default=None)
    total_welded: float = Field(default=0)
    total_ndt: float = Field(default=0)
    accepted: float = Field(default=0)
    rejected: float = Field(default=0)


    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | tuple[int, int, int] | None):
        if v == None:
            return None
        
        return to_date(v)
        

    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | None):
        if v == None:
            return None
        
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


class NDTShema(BaseNDTShema):
    ident: UUID
    kleymo: str
    welding_date: date


    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | date | None):
        return to_date(v)


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | None):
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


class CreateNDTShema(NDTShema):
    ident: UUID = Field(default_factory=uuid4)


class UpdateNDTShema(BaseNDTShema): ...