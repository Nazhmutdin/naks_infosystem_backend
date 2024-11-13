from pydantic import BaseModel

from app.presentation.shemas.personal import PersonalSelectShema
from app.presentation.shemas.personal_naks_certification import PersonalNaksCertificationSelectShema
from app.presentation.shemas.ndt import NDTSelectShema
from app.presentation.shemas.acst import AcstSelectShema


class SelectResponse[T](BaseModel):
    result: list[T]
    count: int


__all__: list[str] = [
    "PersonalNaksCertificationSelectShema",
    "PersonalSelectShema",
    "NDTSelectShema",
    "AcstSelectShema",
    "SelectResponse"
]
