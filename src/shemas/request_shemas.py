from datetime import datetime, date
from uuid import UUID
import typing as t

from naks_library.base_request_shema import *
from naks_library import to_date, is_uuid, is_float
from pydantic import ValidationInfo, Field, field_validator

from src.utils.funcs import (
    validate_certification_number,
)
from src.models import *


__all__ = [
    "RefreshTokenRequestShema",
]


class PersonalCertificationRequestShema(BaseRequestShema):
    __and_model_columns__ = ["insert", "method", "certification_date", "expiration_date", "expiration_date_fact"]
    __or_model_columns__ = ["ident", "personal_ident", "certification_number"]
    __models__ = [PersonalCertificationModel]

    idents: InFilter | None = Field(default=None, serialization_alias="ident")
    personal_idents: InFilter | None = Field(default=None, serialization_alias="personal_ident", validation_alias="personalIdents")
    certification_numbers: InFilter | None = Field(default=None, serialization_alias="certification_number", validation_alias="certificationNumbers")
    inserts: InFilter | None = Field(default=None, serialization_alias="insert")
    methods: InFilter | None = Field(default=None, serialization_alias="method")
    certification_date_from: FromFilter | None = Field(default=None, serialization_alias="certification_date", validation_alias="certificationDateFrom")
    certification_date_before: BeforeFilter | None = Field(default=None, serialization_alias="certification_date", validation_alias="certificationDateBefore")
    expiration_date_from: FromFilter | None = Field(default=None, serialization_alias="expiration_date", validation_alias="expirationDateFrom")
    expiration_date_before: BeforeFilter | None = Field(default=None, serialization_alias="expiration_date", validation_alias="expirationDateBefore")
    expiration_date_fact_from: FromFilter | None = Field(default=None, serialization_alias="expiration_date_fact", validation_alias="expirationDateFactFrom")
    expiration_date_fact_before: BeforeFilter | None = Field(default=None, serialization_alias="expiration_date_fact", validation_alias="expirationDateFactBefore")


    @field_validator(
        "certification_date_from", 
        "certification_date_before", 
        "expiration_date_from", 
        "expiration_date_before", 
        "expiration_date_fact_from", 
        "expiration_date_fact_before", 
        mode="before"
    )
    @classmethod
    def validate_datetime_filters(cls, v: datetime | date | str | None):
        if v == None:
            return None
        
        if isinstance(v, (datetime, date)):
            return v
        
        return to_date(v)
    

    @field_validator("idents", "personal_idents", mode="before")
    @classmethod
    def validate_idents_filter(cls, v: list[UUID | str] | None | t.Any):
        if v == None:
            return None
        
        if not isinstance(v, list):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not is_uuid(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v


    @field_validator("certification_numbers", mode="before")
    @classmethod
    def validate_certification_numbers_filter(cls, v: list[str] | None | t.Any):
        if v == None:
            return None
        
        if not isinstance(v, list):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not validate_certification_number(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v


class PersonalRequestShema(PersonalCertificationRequestShema):
    __and_model_columns__ = PersonalCertificationRequestShema.__and_model_columns__
    __or_model_columns__ = ["ident", "certification_number", "kleymo", "name"]
    __models__ = [PersonalModel, PersonalCertificationModel]

    names: ILikeAnyFilter | None = Field(default=None, serialization_alias="name")
    kleymos: InFilter | None = Field(default=None, serialization_alias="kleymo")


class NDTRequestShema(BaseRequestShema):
    __and_model_columns__ = ["welding_date", "total_welded", "total_ndt", "total_accepted", "total_rejected"]
    __or_model_columns__ = ["ident", "personal_ident"]
    __models__ = [NDTModel]

    idents: InFilter | None = Field(default=None, serialization_alias="ident")
    personal_idents: InFilter | None = Field(default=None, serialization_alias="personal_ident", validation_alias="personalIdents")
    welding_date_from: FromFilter | None = Field(default=None, serialization_alias="welding_date", validation_alias="weldingDateFrom")
    welding_date_before: BeforeFilter | None = Field(default=None, serialization_alias="welding_date", validation_alias="weldingDateBefore")
    total_welded_from: FromFilter | None = Field(default=None, serialization_alias="total_welded", validation_alias="totalWeldedFrom")
    total_welded_before: BeforeFilter | None = Field(default=None, serialization_alias="total_welded", validation_alias="totalWeldedBefore")
    total_ndt_from: FromFilter | None = Field(default=None, serialization_alias="total_ndt", validation_alias="totalNDTFrom")
    total_ndt_before: BeforeFilter | None = Field(default=None, serialization_alias="total_ndt", validation_alias="totalNDTBefore")
    total_accepted_from: FromFilter | None = Field(default=None, serialization_alias="total_accepted", validation_alias="totalAcceptedFrom")
    total_accepted_before: BeforeFilter | None = Field(default=None, serialization_alias="total_accepted", validation_alias="totalAcceptedBefore")
    total_rejected_from: FromFilter | None = Field(default=None, serialization_alias="total_rejected", validation_alias="totalRejectedFrom")
    total_rejected_before: BeforeFilter | None = Field(default=None, serialization_alias="total_rejected", validation_alias="totalRejectedBefore")


    @field_validator("idents", mode="before")
    @classmethod
    def validate_idents_filter(cls, v: list[UUID | str] | None | t.Any):
        if v == None:
            return None
        
        if not isinstance(v, list):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not is_uuid(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v
    

    @field_validator(
        "welding_date_from", 
        "welding_date_before",
        mode="before"
    )
    @classmethod
    def validate_datetime_filters(cls, v: datetime | date | str | None):
        if v == None:
            return None
        
        return to_date(v)
    

    @field_validator(
        "total_welded_from",
        "total_welded_before",
        "total_ndt_from",
        "total_ndt_before",
        "total_accepted_from",
        "total_accepted_before",
        "total_rejected_from",
        "total_rejected_before",
        mode="before"
    )
    @classmethod
    def validate_float_filters(cls, v: str | float | None, info: ValidationInfo):
        if v == None:
            return None
        
        if not is_float(v):
            raise ValueError(f"Invalid {info.field_name} {v}")
        
        return v
