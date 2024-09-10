from datetime import date
from uuid import UUID
import typing as t

from naks_library.validators import before_optional_date_validator
from pydantic import BaseModel, Field


from src.models import *


__all__ = [
    "PersonalCertificationSelectShema",
    "PersonalSelectShema",
    "NDTSelectShema",
]


class PersonalCertificationSelectShema(BaseModel):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None)
    certification_numbers: list[str] | None = Field(default=None)
    inserts: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)


class PersonalSelectShema(BaseModel):

    idents: list[UUID] | None = Field(default=None)
    certification_idents: list[UUID] | None = Field(default=None)
    names: list[str] | None = Field(default=None)
    kleymos: list[str] | None = Field(default=None)
    certification_numbers: list[str] | None = Field(default=None)
    inserts: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)


class NDTSelectShema(BaseModel):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None)
    ndt_types: list[str] | None = Field(default=None)
    welding_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    welding_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    total_welded_from: float | None = Field(default=None)
    total_welded_before: float | None = Field(default=None)
    total_ndt_from: float | None = Field(default=None)
    total_ndt_before: float | None = Field(default=None)
    total_accepted_from: float | None = Field(default=None)
    total_accepted_before: float | None = Field(default=None)
    total_rejected_from: float | None = Field(default=None)
    total_rejected_before: float | None = Field(default=None)
