from uuid import UUID, uuid4
from datetime import date

from pydantic import Field, field_validator
from naks_library import BaseShema, to_date


class BaseNDTShema(BaseShema):
    personal_ident: UUID | None = Field(default=None)
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: date | None = Field(default=None)
    ndt_type: str | None = Field(default=None)
    total_welded: float | None = Field(default=None)
    total_ndt: float | None = Field(default=None)
    total_accepted: float | None = Field(default=None)
    total_rejected: float | None = Field(default=None)


    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | tuple[int, int, int] | None):
        if v == None:
            return None
        
        return to_date(v)


class NDTShema(BaseNDTShema):
    ident: UUID
    personal_ident: UUID
    welding_date: date


class CreateNDTShema(NDTShema):
    ident: UUID = Field(default_factory=uuid4)


    @field_validator("welding_date", mode="before")
    def validate_welding_date(cls, v: str | date | None):
        return to_date(v)


class UpdateNDTShema(BaseNDTShema): ...
