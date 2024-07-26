from datetime import date
from uuid import UUID, uuid4

from pydantic import Field, field_validator
from naks_library import BaseShema, to_date, is_kleymo


class BasePersonalShema(BaseShema):
    
    kleymo: str | None = Field(default=None)
    name: str | None = Field(default=None)
    birthday: date | None = Field(default=None)
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
    

    @field_validator("birthday", mode="before")
    @classmethod
    def validate_birthday(cls, v: str | None):
        if v == None:
            return None
        
        return to_date(v)


class PersonalShema(BasePersonalShema):
    ident: UUID
    name: str


class CreatePersonalShema(PersonalShema):
    ident: UUID = Field(default_factory=uuid4)


class UpdatePersonalShema(BasePersonalShema): ...
