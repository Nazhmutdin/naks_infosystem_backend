from uuid import UUID, uuid4
from datetime import date
import typing as t

from pydantic import Field
from naks_library.common import BaseShema, BaseSelectShema
from naks_library.utils.validators import (
    plain_optional_uuid_serializer, 
    before_optional_date_validator, 
    plain_optional_date_serializer,
    before_date_validator,
    plain_date_serializer,
    plain_uuid_serializer
)

from app.application.dto import CreateNdtDTO, UpdateNdtDTO


class CreateNdtShema(BaseShema):
    ident: t.Annotated[UUID, plain_uuid_serializer] = Field(default_factory=uuid4)
    personal_ident: t.Annotated[UUID, plain_uuid_serializer] = Field()
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: t.Annotated[date, before_date_validator, plain_date_serializer] = Field()
    ndt_type: str = Field()
    total_welded: float = Field()
    total_ndt: float = Field()
    total_accepted: float = Field()
    total_rejected: float = Field()

    def to_dto(self) -> CreateNdtDTO:
        return CreateNdtDTO(
            **self.__dict__
        )


class UpdateNdtShema(BaseShema):
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

    def to_dto(self) -> UpdateNdtDTO:
        return UpdateNdtDTO(
            **self.__dict__
        )


class NDTSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None)
    ndt_types: list[str] | None = Field(default=None)
    welding_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    welding_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    total_welded_from: float | None = Field(default=None)
    total_welded_before: float | None = Field(default=None)
    total_ndt_from: float | None = Field(default=None)
    total_ndt_before: float | None = Field(default=None)
    total_accepted_from: float | None = Field(default=None)
    total_accepted_before: float | None = Field(default=None)
    total_rejected_from: float | None = Field(default=None)
    total_rejected_before: float | None = Field(default=None)
