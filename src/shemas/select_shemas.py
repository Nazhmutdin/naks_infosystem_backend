from datetime import date
from uuid import UUID
import typing as t

from naks_library.validators import before_optional_date_validator
from naks_library.base_shema import BaseSelectShema
from pydantic import Field


from src.models import *


__all__ = [
    "PersonalCertificationSelectShema",
    "PersonalSelectShema",
    "NDTSelectShema"
]


class PersonalCertificationSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None, validation_alias="personalIdents")
    certification_numbers: list[str] | None = Field(default=None, validation_alias="certificationNumbers")
    inserts: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="certificationDateFrom")
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="certificationDateBefore")
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFrom")
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateBefore")
    expiration_date_fact_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFactFrom")
    expiration_date_fact_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFactBefore")


class PersonalSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    certification_idents: list[UUID] | None = Field(default=None, validation_alias="certificationIdents")
    names: list[str] | None = Field(default=None)
    kleymos: list[str] | None = Field(default=None)
    certification_numbers: list[str] | None = Field(default=None, validation_alias="certificationNumbers")
    inserts: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="certificationDateFrom")
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="certificationDateBefore")
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFrom")
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateBefore")
    expiration_date_fact_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFactFrom")
    expiration_date_fact_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="expirationDateFactBefore")


class NDTSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None, validation_alias="personalIdents")
    ndt_types: list[str] | None = Field(default=None, validation_alias="ndtTypes")
    welding_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="weldingDateFrom")
    welding_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="weldingDateBefore")
    total_welded_from: float | None = Field(default=None, validation_alias="totalWeldedFrom")
    total_welded_before: float | None = Field(default=None, validation_alias="totalWeldedBefore")
    total_ndt_from: float | None = Field(default=None, validation_alias="totalNdtFrom")
    total_ndt_before: float | None = Field(default=None, validation_alias="totalNdtBefore")
    total_accepted_from: float | None = Field(default=None, validation_alias="totalAcceptedFrom")
    total_accepted_before: float | None = Field(default=None, validation_alias="totalAcceptedBefore")
    total_rejected_from: float | None = Field(default=None, validation_alias="totalRejectedFrom")
    total_rejected_before: float | None = Field(default=None, validation_alias="totalRejectedBefore")
