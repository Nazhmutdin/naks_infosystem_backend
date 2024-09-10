from datetime import date
from uuid import UUID, uuid4
import typing  as t

from pydantic import Field, field_validator
from naks_library import BaseShema, is_kleymo
from naks_library.validators import *


class BasePersonalShema(BaseShema):
    
    kleymo: str | None = Field(default=None)
    name: str | None = Field(default=None)
    birthday: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None)
    passport_number: str | None = Field(default=None)
    nation: str | None = Field(default=None)
    exp_age: int | None = Field(default=None)


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int | None):
        if v == None:
            return None
        
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


class PersonalShema(BasePersonalShema):
    ident: t.Annotated[UUID, plain_uuid_serializer]
    name: str


class CreatePersonalShema(PersonalShema):
    ident: t.Annotated[UUID, plain_uuid_serializer] = Field(default_factory=uuid4)


class UpdatePersonalShema(BasePersonalShema): ...
