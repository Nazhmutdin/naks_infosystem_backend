from uuid import UUID
from datetime import date
import typing  as t

from pydantic import Field
from naks_library.common import BaseSelectShema
from naks_library.utils.validators import before_optional_date_validator


class PersonalNaksCertificationSelectShema(BaseSelectShema):
    idents: list[UUID] | None = Field(default=None)
    personal_idents: list[UUID] | None = Field(default=None)
    certification_numbers: list[str] | None = Field(default=None)
    inserts: list[str] | None = Field(default=None)
    methods: list[str] | None = Field(default=None)
    certification_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    certification_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_from: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
    expiration_date_fact_before: t.Annotated[date | None, before_optional_date_validator] = Field(default=None)
