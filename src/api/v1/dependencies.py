from uuid import UUID
from re import fullmatch
import typing as t

from pydantic import ValidationError, BaseModel
from fastapi import HTTPException, Request

from src.shemas import *


__all__ = [
    "validate_ident_dependency",
    "validate_personal_ident_dependency",
    "InputValidationDependency"
]


def validate_ident_dependency(ident: str) -> str:
    try:
        UUID(ident)
    
    except:
        raise HTTPException(
            400,
            "Invalid ident"
        )

    return ident


def validate_personal_ident_dependency(ident: str) -> str:
    if not fullmatch(r"[A-Z0-9]{4}", ident):
        try:
            UUID(ident)
        
        except:
            raise HTTPException(
                400,
                "Invalid ident"
            )
    
    return ident


def base_error_handler(err: ValidationError) -> t.NoReturn:
    
    raise HTTPException(
        400,
        err.args
    )


class InputValidationDependency[T: BaseModel]:
    def __init__(self, validation_shema: type[T]) -> None:
        self.shema = validation_shema
        

    async def execute(self, request: Request, err_handler: t.Callable[[ValidationError], t.NoReturn] = base_error_handler):
        try:
            return self.shema.model_validate(
                await request.json()
            )
        except ValidationError as e:
            err_handler(e)
