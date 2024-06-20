from re import fullmatch
from datetime import date, datetime
from uuid import UUID

from src.utils.funcs import to_date, str_to_datetime
from src.services.auth_service import AuthService


def validate_kleymo(v: str) -> bool:
    if fullmatch(r"[A-Z0-9]{4}", v):
        return True
    
    return False


def validate_insert(v: str) -> bool:
    if fullmatch(r"В[0-9]", v):
        return True
    
    return False


def validate_method(v: str) -> bool:
    if fullmatch(r"[A-Яа-я]+", v):
        return True
    
    return False


def validate_certification_number(v: str) -> bool:
    if fullmatch(r"[A-Я]+-[0-9A-Я]+-[IV]+-[0-9]{5}", v):
        return True
    
    return False


def validate_name(v: str) -> bool:
    if fullmatch(r"[A-ЯA-Za-zа-я ]+", v):
        return True
    
    return False


def is_float(v: str) -> bool:
    try:
        float(v)
        return True
    except:
        return False


def validate_refresh_token(v: str) -> bool:
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
