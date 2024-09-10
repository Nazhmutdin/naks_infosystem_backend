from uuid import UUID, uuid4
from datetime import date
import typing as t

from pydantic import Field
from naks_library import BaseShema
from naks_library.validators import *


class BaseNDTShema(BaseShema):
    personal_ident: t.Annotated[UUID | None, plain_optional_uuid_serializer] = Field(default=None)
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None)
    ndt_type: str | None = Field(default=None)
    total_welded: float | None = Field(default=None)
    total_ndt: float | None = Field(default=None)
    total_accepted: float | None = Field(default=None)
    total_rejected: float | None = Field(default=None)


class NDTShema(BaseNDTShema):
    ident: t.Annotated[UUID, plain_uuid_serializer]
    personal_ident: t.Annotated[UUID, plain_uuid_serializer]
    welding_date: t.Annotated[date, before_date_validator, plain_date_serializer]


class CreateNDTShema(NDTShema):
    ident: t.Annotated[UUID, plain_uuid_serializer] = Field(default_factory=uuid4)


class UpdateNDTShema(BaseNDTShema): ...
