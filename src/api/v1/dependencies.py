from uuid import UUID
from re import fullmatch

from fastapi import HTTPException, Depends

from services.db_services import BaseDBService
from shemas import BaseShema
from errors import DeleteDBException, UpdateDBException


def validate_ident(ident: str) -> str:
    if not fullmatch(r"[A-Z0-9]{4}", ident):
        try:
            UUID(ident)
        
        except:
            raise HTTPException(
                400,
                "Invalid ident"
            )
    
    return ident


class UpdateDataDependency[Data: BaseShema]:
    def __init__(self, service: BaseDBService) -> None:
        self.service = service

    async def __call__(self, data: Data, ident: str = Depends(validate_ident)) -> str:

        try:
            await self.service.update(ident, data)
        except UpdateDBException as e:
            raise HTTPException(400, e.args)
        
        return ident


class DeleteDataDependency:
    def __init__(self, service: BaseDBService) -> None:
        self.service = service

    async def __call__(self, ident: str = Depends(validate_ident)) -> str:

        try:
            await self.service.delete(ident)
        except DeleteDBException as e:
            raise HTTPException(400, e.args)
        
        return ident
