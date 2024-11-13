from datetime import date
from uuid import UUID
import typing  as t

from pydantic import Field
from naks_library.common import BaseSelectShema
from naks_library.utils.validators import before_optional_date_validator


class AcstSelectShema(BaseSelectShema):
    idents: list[UUID] | None = Field(default=None)
    acst_numbers: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
