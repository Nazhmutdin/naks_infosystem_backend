from datetime import date
from uuid import UUID, uuid4

from pydantic import Field, field_validator
from naks_library import BaseShema, to_date, is_kleymo


class BaseWelderShema(BaseShema):
    __fields_ignore__ = ["ident"]
    
    kleymo: str | None = Field(default=None)
    name: str | None = Field(default=None)
    birthday: date | None = Field(default=None)
    passport_number: str | None = Field(default=None)
    sicil: str | None = Field(default=None)
    nation: str | None = Field(default=None)
    status: int = Field(default=0)


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


    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: int | str | None):
            
        if not v:
            return 0
        
        if isinstance(v, str):
            try:
                return int(v)
            except:
                raise ValueError(f"{v} cannot be converted to int")
        
        return v


class WelderShema(BaseWelderShema):
    ident: UUID
    kleymo: str
    name: str


    @field_validator("kleymo")
    @classmethod
    def validate_kleymo(cls, v: str | int):
        
        if is_kleymo(v):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")


class CreateWelderShema(WelderShema):
    ident: UUID = Field(default_factory=uuid4)


class UpdateWelderShema(BaseWelderShema): ...
