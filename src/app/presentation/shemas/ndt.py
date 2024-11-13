from uuid import UUID
from datetime import date
import typing as t

from pydantic import Field
from naks_library.common import BaseSelectShema
from naks_library.utils.validators import before_optional_date_validator


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
