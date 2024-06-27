from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from src.models import Base


__all__ = [
    "CreateDBException",
    "GetDBException",
    "GetManyDBException",
    "UpdateDBException",
    "DeleteDBException",
    "DBServiceException",
    "FieldValidationException"
]


class CreateDBException(Exception):
    def __init__[Model: Base](self, exc: IntegrityError, model: Model) -> None:
        self.exception = exc
        self.model = model
        self.detail = exc.detail
        super().__init__(exc.detail)

    
    @property
    def message(self) -> str:
        return f"{self._get_item_type()} already exists"

        
    
    def _get_item_type(self) -> str:
        if self.model.__name__ == "WelderModel":
            return "welder"
        elif self.model.__name__ == "WelderCertificationModel":
            return "welder certification"
        elif self.model.__name__ == "NDTModel":
            return "ndt"


class GetDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class GetManyDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class UpdateDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class DeleteDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class DBServiceException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class FieldValidationException(ValueError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
