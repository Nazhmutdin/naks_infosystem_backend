from datetime import datetime, date
from uuid import UUID
import typing as t

from pydantic_core import core_schema
from sqlalchemy import BinaryExpression, ColumnClause, ColumnElement, any_, and_, or_
from pydantic import GetCoreSchemaHandler, ValidationInfo, Field, field_validator

from shemas.base import BaseShema

from shemas.validators import (
    to_datetime_validator, 
    to_uuid_validator, 
    validate_refresh_token, 
    validate_kleymo, 
    validate_insert, 
    validate_method,
    validate_certification_number,
    validate_name,
    is_float
)
from models import *


__all__ = [
    "RefreshTokenRequestShema",
    "WelderCertificationRequestShema",
    "WelderRequestShema",
    "NDTRequestShema"
]


class BaseFilter: 
    arg: t.Any

    def __init__(self, arg: t.Any) -> None:
        self.arg = arg

        
    def dump_expression(self, column: ColumnClause) -> BinaryExpression: ...


    @classmethod
    def validate(cls, value: t.Any, info: ValidationInfo):

        return cls(value)


    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: t.Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate, handler(t.Any), field_name=handler.field_name
        )


class BaseListFilter(BaseFilter): ...
            

class ILikeAnyFilter(BaseListFilter):

    def dump_expression(self, column: ColumnClause) -> BinaryExpression:

        return column.ilike(any_(self.arg))
    

class InFilter(BaseListFilter):


    def dump_expression(self, column: ColumnClause) -> BinaryExpression:

        return column.in_(self.arg)


class EqualFilter(BaseFilter):


    def dump_expression(self, column: ColumnClause) -> BinaryExpression:

        return column == self.arg


class FromFilter(BaseFilter):


    def dump_expression(self, column: ColumnClause) -> BinaryExpression:

        return column > self.arg


class BeforeFilter(BaseFilter):
        

    def dump_expression(self, column: ColumnClause) -> BinaryExpression:

        return column < self.arg


class BaseRequestShema(BaseShema):
    __and_model_columns__: list[str] = []
    __or_model_columns__: list[str] = []
    __model__: type[Base]


    def dump_expression(self) -> ColumnElement:
        and_expressions = []
        or_expressions = []

        for key, info in self.model_fields.items():
            if info.serialization_alias:
                model_field: ColumnClause | None = getattr(self.__model__, info.serialization_alias, None)

                if not model_field:
                    raise ValueError("serialization_alias must be one of model columns name")
                
                shema_value: BaseFilter = getattr(self, key)

                if shema_value == None:
                    continue

                if model_field.name in self.__and_model_columns__:
                    and_expressions.append(
                        shema_value.dump_expression(model_field)
                    )

                elif model_field.name in self.__or_model_columns__:
                    or_expressions.append(
                        shema_value.dump_expression(model_field)
                    )
                else:
                    continue
            
            else:
                raise ValueError("serialization_alias is required") 
            
        if and_expressions and or_expressions:
            return and_(
                or_(*or_expressions),
                *and_expressions
            )
        
        elif and_expressions:
            return and_(*and_expressions)
        
        elif or_expressions:
            return or_(*or_expressions)
        
        else:
            return True


class RefreshTokenRequestShema(BaseRequestShema):
    __and_model_columns__ = ["exp_dt", "gen_dt", "revoked"]
    __or_model_columns__ = ["token", "user_ident", "ident"]
    __model__ = RefreshTokenModel

    tokens: InFilter | None = Field(default=None, serialization_alias="token")
    idents: InFilter | None = Field(default=None, serialization_alias="ident")
    user_idents: InFilter | None = Field(default=None, serialization_alias="user_ident", validation_alias="userIdents")
    revoked: EqualFilter | None = Field(default=None, serialization_alias="revoked")
    gen_dt_from: FromFilter | None = Field(default=None, serialization_alias="gen_dt", validation_alias="genDtFrom")
    gen_dt_before: BeforeFilter | None = Field(default=None, serialization_alias="gen_dt", validation_alias="genDtBefore")
    exp_dt_from: FromFilter | None = Field(default=None, serialization_alias="exp_dt", validation_alias="expDtFrom")
    exp_dt_before: BeforeFilter | None = Field(default=None, serialization_alias="exp_dt", validation_alias="expDtBefore")


    @field_validator("exp_dt_from", "exp_dt_before", "gen_dt_from", "gen_dt_before", mode="before")
    @classmethod
    def validate_datetime_filters(cls, v: datetime | date | str | None):
        if v == None:
            return None
        
        if isinstance(v, (datetime, date)):
            return v
        
        date_result = to_datetime_validator(v)

        if not date_result:
            raise ValueError(f"invalid date string: {v}")
        
        return date_result
    

    @field_validator("idents", "user_idents", mode="before")
    @classmethod
    def validate_ident_filters(cls, v: list[UUID | str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            uuid_result = to_uuid_validator(el)

            if not uuid_result:
                v.remove(el)
        
        if not v:
            return None
        
        return v
    

    @field_validator("tokens", mode="before")
    @classmethod
    def validate_tokens_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not validate_refresh_token(el):
                print(el)
                v.remove(el)
        
        if not v:
            return None
        
        return v
    

    @field_validator("revoked", mode="before")
    @classmethod
    def validate_revoked_filter(cls, v: bool | None):
        if v == None:
            return None
        
        if not isinstance(v, bool):
            raise ValueError(f"revoked filter must be bool")
        
        return v


class WelderCertificationRequestShema(BaseRequestShema):
    __and_model_columns__ = ["insert", "method", "certification_date", "expiration_date", "expiration_date_fact"]
    __or_model_columns__ = ["ident", "kleymo", "certification_number"]
    __model__ = WelderCertificationModel

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
        
        date_result = to_datetime_validator(v)

        if not date_result:
            raise ValueError(f"invalid date string: {v}")
        
        return date_result
    

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
            if not validate_kleymo(el):
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
            uuid_result = to_uuid_validator(el)

            if not uuid_result:
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


class WelderRequestShema(WelderCertificationRequestShema):
    __and_model_columns__ = WelderCertificationRequestShema.__and_model_columns__ + ["name"]
    __or_model_columns__ = ["ident", "kleymo", "certification_number"]
    __model__ = WelderModel

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
    __model__ = NDTModel

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
            if not validate_kleymo(el):
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
            uuid_result = to_uuid_validator(el)

            if not uuid_result:
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
        
        if isinstance(v, (datetime, date)):
            return v
        
        date_result = to_datetime_validator(v)

        if not date_result:
            raise ValueError(f"invalid date string: {v}")
        
        return date_result
    

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
