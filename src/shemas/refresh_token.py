from uuid import UUID, uuid4
from datetime import datetime

from pydantic import Field, field_validator

from shemas.base import BaseShema
from shemas.validators import to_datetime_validator, validate_jwt_token


class BaseRefreshTokeShema(BaseShema):
    user_ident: UUID | None = Field(default=None)
    token: str | None = Field(default=None)
    revoked: bool | None = Field(default=None)
    exp_dt: datetime | None = Field(default=None)
    gen_dt: datetime | None = Field(default=None)
        

    @field_validator("exp_dt", "gen_dt", mode="before")
    @classmethod
    def validate_datetimes(cls, v: str | datetime | None):
        return to_datetime_validator(v)
        

    @field_validator("token")
    @classmethod
    def validate_datetimes(cls, v: str | None):
        if v == None:
            return None
        
        if validate_jwt_token(v):
            return v
        
        raise ValueError("invalid token")


class RefreshTokeShema(BaseRefreshTokeShema):
    ident: UUID
    user_ident: UUID
    token: str
    revoked: bool
    exp_dt: datetime
    gen_dt: datetime


    @field_validator("token")
    def validate_token(cls, v: str | None) -> str:
        if v == None:
            raise ValueError("token cannot be None")
        
        if validate_jwt_token(v):
            return v
        
        raise ValueError("invalid token")


    @field_validator("exp_dt", "gen_dt", mode="before")
    @classmethod
    def validate_datetimes(cls, v: str | datetime | None):
        result = to_datetime_validator(v)

        if not result:
            raise ValueError(f"invalid date data: {v}")
        
        return result
            

class CreateRefreshTokeShema(RefreshTokeShema):
    ident: UUID = Field(default_factory=uuid4)


class UpdateRefreshTokeShema(BaseRefreshTokeShema): ...
