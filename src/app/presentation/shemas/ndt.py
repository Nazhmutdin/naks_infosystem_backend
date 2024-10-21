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
    personal_ident: t.Annotated[UUID, plain_uuid_serializer] = Field(serialization_alias="personalIdent")
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: t.Annotated[date, before_date_validator, plain_date_serializer] = Field(serialization_alias="weldingDate")
    ndt_type: str = Field(serialization_alias="ndtType")
    total_welded: float = Field(serialization_alias="totalWelded")
    total_ndt: float = Field(serialization_alias="totalNdt")
    total_accepted: float = Field(serialization_alias="totalAccepted")
    total_rejected: float = Field(serialization_alias="totalRejected")

    def to_dto(self) -> CreateNdtDTO:
        return CreateNdtDTO(
            **self.__dict__
        )


class UpdateNdtShema(BaseShema):
    personal_ident: t.Annotated[UUID | None, plain_optional_uuid_serializer] = Field(default=None, serialization_alias="personalIdent")
    company: str | None = Field(default=None)
    subcompany: str | None = Field(default=None)
    project: str | None = Field(default=None)
    welding_date: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer] = Field(default=None, serialization_alias="weldingDate")
    ndt_type: str | None = Field(default=None, serialization_alias="ndtType")
    total_welded: float | None = Field(default=None, serialization_alias="totalWelded")
    total_ndt: float | None = Field(default=None, serialization_alias="totalNdt")
    total_accepted: float | None = Field(default=None, serialization_alias="totalAccepted")
    total_rejected: float | None = Field(default=None, serialization_alias="totalRejected")

    def to_dto(self) -> UpdateNdtDTO:
        return UpdateNdtDTO(
            **self.__dict__
        )


class NDTSelectShema(BaseSelectShema):

    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None, validation_alias="personalIdents")
    ndt_types: list[str] | None = Field(default=None, validation_alias="ndtTypes")
    welding_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="weldingDateFrom")
    welding_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None, validation_alias="weldingDateBefore")
    total_welded_from: float | None = Field(default=None, validation_alias="totalWeldedFrom")
    total_welded_before: float | None = Field(default=None, validation_alias="totalWeldedBefore")
    total_ndt_from: float | None = Field(default=None, validation_alias="totalNdtFrom")
    total_ndt_before: float | None = Field(default=None, validation_alias="totalNdtBefore")
    total_accepted_from: float | None = Field(default=None, validation_alias="totalAcceptedFrom")
    total_accepted_before: float | None = Field(default=None, validation_alias="totalAcceptedBefore")
    total_rejected_from: float | None = Field(default=None, validation_alias="totalRejectedFrom")
    total_rejected_before: float | None = Field(default=None, validation_alias="totalRejectedBefore")
