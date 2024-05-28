from uuid import UUID, uuid4
from datetime import datetime

from pydantic import ValidationInfo, EmailStr, Field, field_validator

from shemas.base import BaseShema
from shemas.validators import to_datetime_validator


class BaseUserShema(BaseShema):
    name: str | None = Field(default=None) 
    login: str | None = Field(default=None)
    hashed_password: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    sign_date: datetime | None = Field(default=None)
    update_date: datetime | None = Field(default=None)
    login_date: datetime | None = Field(default=None)
    is_superuser: bool | None = Field(default=None)
        

    @field_validator("sign_date", "update_date", "login_date", mode="before")
    @classmethod
    def validate_datetimes(cls, v: str | datetime | None, info: ValidationInfo):
        if v == None:
            return None
        
        result = to_datetime_validator(v)

        if not result:
            raise ValueError(f"{info.field_name} got invalid date data ({v})")
        
        return result


class UserShema(BaseUserShema):
    ident: UUID
    login: str
    name: str
    hashed_password: str
    sign_date: datetime = Field(default_factory=datetime.now)
    update_date: datetime = Field(default_factory=datetime.now)
    login_date: datetime = Field(default_factory=datetime.now)
    is_superuser: bool


    @field_validator("sign_date", "update_date", "login_date", mode="before")
    @classmethod
    def validate_datetimes(cls, v: str | datetime | None):
        date_result = to_datetime_validator(v)

        if date_result:
            return date_result
        
        raise ValueError(f"invalid date: {v}")


class CreateUserShema(UserShema):
    ident: UUID = Field(default=uuid4)
    sign_date: datetime = Field(default_factory=datetime.now)
    update_date: datetime = Field(default_factory=datetime.now)
    login_date: datetime = Field(default_factory=datetime.now)
    is_superuser: bool = Field(default=False)


class UpdateUserShema(BaseUserShema): ...