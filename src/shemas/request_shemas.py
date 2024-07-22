from datetime import datetime, date
from uuid import UUID
import typing as t

from naks_library.base_request_shema import *
from naks_library import to_date, to_datetime, is_kleymo, is_uuid, is_float
from pydantic import ValidationInfo, Field, field_validator

from src.utils.funcs import (
    validate_insert, 
    validate_method,
    validate_certification_number,
    validate_name, 
)
from src.models import *

__all__ = [
    "RefreshTokenRequestShema",
]


class PersonalCertificationRequestShema(BaseRequestShema):
    __and_model_columns__ = ["insert", "method", "certification_date", "expiration_date", "expiration_date_fact"]
    __or_model_columns__ = ["ident", "kleymo", "certification_number"]
    __models__ = [PersonalCertificationModel]

    idents: InFilter | None = Field(default=None, serialization_alias="ident")
    kleymos: InFilter | None = Field(default=None, serialization_alias="kleymo")
    certification_numbers: InFilter | None = Field(default=None, serialization_alias="certification_number")
    inserts: InFilter | None = Field(default=None, serialization_alias="insert")
    methods: InFilter | None = Field(default=None, serialization_alias="method")
    certification_date_from: FromFilter | None = Field(default=None, serialization_alias="certification_date")
    certification_date_before: BeforeFilter | None = Field(default=None, serialization_alias="certification_date")
    expiration_date_from: FromFilter | None = Field(default=None, serialization_alias="expiration_date")
    expiration_date_before: BeforeFilter | None = Field(default=None, serialization_alias="expiration_date")
    expiration_date_fact_from: FromFilter | None = Field(default=None, serialization_alias="expiration_date_fact")
    expiration_date_fact_before: BeforeFilter | None = Field(default=None, serialization_alias="expiration_date_fact")


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
        
        return to_datetime(v)
    

    @field_validator("inserts", mode="before")
    @classmethod
    def validate_inserts_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not validate_insert(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v
    

    @field_validator("kleymos", mode="before")
    @classmethod
    def validate_kleymos_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not is_kleymo(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v
    

    @field_validator("methods", mode="before")
    @classmethod
    def validate_methods_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not validate_method(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v
    

    @field_validator("idents", mode="before")
    @classmethod
    def validate_idents_filter(cls, v: list[UUID | str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not is_uuid(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v


    @field_validator("certification_numbers", mode="before")
    @classmethod
    def validate_certification_numbers_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not validate_certification_number(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v


class PersonalRequestShema(PersonalCertificationRequestShema):
    __and_model_columns__ = PersonalCertificationRequestShema.__and_model_columns__ + ["name"]
    __or_model_columns__ = ["ident", "kleymo", "certification_number"]
    __models__ = [PersonalModel, PersonalCertificationModel]

    names: ILikeAnyFilter | None = Field(default=None, serialization_alias="expiration_date_fact")
    

    @field_validator("names", mode="before")
    @classmethod
    def validate_names_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not validate_name(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v


class NDTRequestShema(BaseRequestShema):
    __and_model_columns__ = ["welding_date", "total_welded", "total_ndt", "accepted", "rejected"]
    __or_model_columns__ = ["ident", "kleymo"]
    __models__ = [NDTModel]

    idents: InFilter | None = Field(default=None, serialization_alias="ident")
    kleymos: InFilter | None = Field(default=None, serialization_alias="kleymo")
    welding_date_from: FromFilter | None = Field(default=None, serialization_alias="welding_date")
    welding_date_before: BeforeFilter | None = Field(default=None, serialization_alias="welding_date")
    total_welded_from: FromFilter | None = Field(default=None, serialization_alias="total_welded")
    total_welded_before: BeforeFilter | None = Field(default=None, serialization_alias="total_welded")
    total_ndt_from: FromFilter | None = Field(default=None, serialization_alias="total_ndt")
    total_ndt_before: BeforeFilter | None = Field(default=None, serialization_alias="total_ndt")
    accepted_from: FromFilter | None = Field(default=None, serialization_alias="accepted")
    accepted_before: BeforeFilter | None = Field(default=None, serialization_alias="accepted")
    rejected_from: FromFilter | None = Field(default=None, serialization_alias="rejected")
    rejected_before: BeforeFilter | None = Field(default=None, serialization_alias="rejected")
    

    @field_validator("kleymos", mode="before")
    @classmethod
    def validate_kleymos_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not is_kleymo(el):
                v.remove(el)
        
        if not v:
            return None
        
        return v


    @field_validator("idents", mode="before")
    @classmethod
    def validate_idents_filter(cls, v: list[UUID | str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
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
        "accepted_from",
        "accepted_before",
        "rejected_from",
        "rejected_before",
        mode="before"
    )
    @classmethod
    def validate_float_filters(cls, v: str | None, info: ValidationInfo):
        if v == None:
            return None
        
        if not is_float(v):
            raise ValueError(f"Invalid {info.field_name} {v}")
        
        return v
