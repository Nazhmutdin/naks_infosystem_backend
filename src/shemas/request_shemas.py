from datetime import datetime, date
from uuid import UUID
import typing as t

from pydantic_core import core_schema

from sqlalchemy import BinaryExpression, ColumnClause, any_, and_, or_, ColumnExpressionArgument
from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler, ValidationInfo, Field, field_validator

from shemas.validators import to_datetime_validator, to_uuid_validator, validate_jwt_refresh_token
from models import *


__all__ = [
    "RefreshTokenRequestShema"
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


class BaseFromFilter(BaseFilter):


    def dump_expression(self, column: ColumnClause) -> BinaryExpression:

        return column > self.arg


class BaseBeforeFilter(BaseFilter):
        

    def dump_expression(self, column: ColumnClause) -> BinaryExpression:

        return column < self.arg


class BaseRequestShema(BaseModel):
    __and_model_columns__: list[str] = []
    __or_model_columns__: list[str] = []
    __model__: type[Base]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )


    def dump_expression(self) -> ColumnExpressionArgument:
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
    gen_dt_from: BaseFromFilter | None = Field(default=None, serialization_alias="gen_dt", validation_alias="genDtFrom")
    gen_dt_before: BaseBeforeFilter | None = Field(default=None, serialization_alias="gen_dt", validation_alias="genDtBefore")
    exp_dt_from: BaseFromFilter | None = Field(default=None, serialization_alias="exp_dt", validation_alias="expDtFrom")
    exp_dt_before: BaseBeforeFilter | None = Field(default=None, serialization_alias="exp_dt", validation_alias="expDtBefore")


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
                raise ValueError(f"invalid uuid string: {el}")
            
        return v
    

    @field_validator("tokens", mode="before")
    @classmethod
    def validate_tokens_filter(cls, v: list[str] | None):
        if v == None:
            return None
        
        if not isinstance(v, t.Iterable):
            raise ValueError(f"value must be iterable")
        
        for el in v:
            if not validate_jwt_refresh_token(el):
                raise ValueError(f"invalid token: {el}")
            
        return v
    

    @field_validator("revoked", mode="before")
    @classmethod
    def validate_revoked_filter(cls, v: bool | None):
        if v == None:
            return None
        
        if not isinstance(v, bool):
            raise ValueError(f"revoked filter must be bool")
        
        return v
