from uuid import UUID
from re import fullmatch

from fastapi import HTTPException


__all__ = [
    "validate_ident_dependency",
    "validate_welder_ident_dependency"
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


def validate_welder_ident_dependency(ident: str) -> str:
    if not fullmatch(r"[A-Z0-9]{4}", ident):
        try:
            UUID(ident)
        
        except:
            raise HTTPException(
                400,
                "Invalid ident"
            )
    
    return ident
