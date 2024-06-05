from re import fullmatch
from datetime import date, datetime
from uuid import UUID

from utils.funcs import to_date, str_to_datetime
from services.auth_service import AuthService


def validate_kleymo(v: str) -> bool:
    if fullmatch(r"[A-Z0-9]{4}", v):
        return True
    
    return False


def validate_jwt_refresh_token(v: str) -> bool:
    return AuthService().validate_refresh_token(v)


def to_date_validator(v: str | date | datetime | None) -> date | None:
    if not v:
        return None

    if isinstance(v, datetime):
        return v.date()
    else:
        return to_date(v)


def to_datetime_validator(v: str | date | datetime | None) -> datetime | None:

    if isinstance(v, datetime):
        return v
    elif isinstance(v, date):
        return datetime.fromordinal(v.toordinal())
    else:
        v = str_to_datetime(v)

        if v:
            return v


def to_uuid_validator(v: str | UUID | None) -> UUID | None:
    if isinstance(v, UUID):
        return v
    
    try:
        v = UUID(v)
        return v
    except:
        return None
