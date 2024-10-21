from pydantic import BaseModel

from app.presentation.shemas.personal import CreatePersonalShema, UpdatePersonalShema, PersonalSelectShema
from app.presentation.shemas.personal_naks_certification import CreatePersonalNaksCertificationShema, UpdatePersonalNaksCertificationShema, PersonalNaksCertificationSelectShema
from app.presentation.shemas.ndt import CreateNdtShema, UpdateNdtShema, NDTSelectShema


class SelectResponse[T](BaseModel):
    result: list[T]
    count: int


__all__: list[str] = [
    "CreatePersonalShema",
    "UpdatePersonalShema",
    "CreatePersonalNaksCertificationShema",
    "UpdatePersonalNaksCertificationShema",
    "CreateNdtShema",
    "UpdateNdtShema",
    "PersonalNaksCertificationSelectShema",
    "PersonalSelectShema",
    "NDTSelectShema"
]
