from datetime import date
from uuid import UUID, uuid4
import typing  as t

from pydantic import Field, field_validator
from naks_library.common import BaseShema, BaseSelectShema
from naks_library.utils.validators import (
    before_optional_date_validator, 
    plain_optional_date_serializer, 
    plain_uuid_serializer
)
from naks_library.utils.funcs import is_kleymo

from app.application.dto import CreatePersonalDTO, UpdatePersonalDTO


class CreatePersonalShema(BaseShema):
    ident: t.Annotated[UUID, plain_uuid_serializer] = Field(default_factory=uuid4)
    kleymo: str | None = Field(default=None)
    name: str = Field(default=None)
    birthday: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None)
    passport_number: str | None = Field(default=None)
    nation: str | None = Field(default=None)
    exp_age: int | None = Field(default=None)


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if v is None:
            return None
        
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


    def to_dto(self) -> CreatePersonalDTO:
        return CreatePersonalDTO(
            **self.__dict__
        )


class UpdatePersonalShema(BaseShema): 
    
    kleymo: str | None = Field(default=None)
    name: str | None = Field(default=None)
    birthday: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None)
    passport_number: str | None = Field(default=None)
    nation: str | None = Field(default=None)
    exp_age: int | None = Field(default=None)


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if v is None:
            return None
        
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


    def to_dto(self) -> UpdatePersonalDTO:
        return UpdatePersonalDTO(
            **self.__dict__
        )


class PersonalSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    certification_idents: list[UUID] | None = Field(default=None,)
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
