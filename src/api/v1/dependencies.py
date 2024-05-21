from uuid import UUID
from re import fullmatch

from fastapi import HTTPException, Depends

from services.db_services import *
from shemas import *
from errors import DeleteDBException, UpdateDBException, GetDBException


__all__ = [
    "add_welder_dependency",
    "add_welder_certification_dependency",
    "add_ndt_dependency",
    "get_welder_dependency",
    "get_welder_certification_dependency",
    "get_ndt_dependency",
    "update_welder_dependency",
    "update_welder_certification_dependency",
    "update_ndt_dependency",
    "delete_welder_dependency",
    "delete_welder_certification_dependency",
    "delete_ndt_dependency",
]


def validate_ident_dependency(ident: str) -> str:
    if not fullmatch(r"[A-Z0-9]{4}", ident):
        try:
            UUID(ident)
        
        except:
            raise HTTPException(
                400,
                "Invalid ident"
            )
    
    return ident


async def add_dependency[Data: BaseShema](data: Data, service: BaseDBService) -> Data:

    try:
        await service.add(data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)
    
    res = await service.get(data.ident)
    
    if not res:
        raise HTTPException(
            400,
            "something gone wrong"
        )
    
    return res


async def add_welder_dependency(data: CreateWelderShema) -> WelderShema:
    return await add_dependency(
        data, 
        WelderDBService()
    )


async def add_welder_certification_dependency(data: CreateWelderCertificationShema) -> WelderCertificationShema:
    return await add_dependency(
        data, 
        WelderCertificationDBService()
    )


async def add_ndt_dependency(data: CreateNDTShema) -> NDTShema:
    return await add_dependency(
        data, 
        NDTDBService()
    )


async def get_dependency[Result: BaseShema](ident: str, service: BaseDBService) -> Result | None:

    try:
        return await service.get(ident)
    except GetDBException as e:
        raise HTTPException(400, e.args)


async def get_welder_dependency(ident: str = Depends(validate_ident_dependency)) -> WelderShema | None:
    return await get_dependency(
        ident, 
        WelderDBService()
    )


async def get_welder_certification_dependency(ident: str = Depends(validate_ident_dependency)) -> WelderCertificationShema | None:
    return await get_dependency(
        ident, 
        WelderCertificationDBService()
    )


async def get_ndt_dependency(ident: str = Depends(validate_ident_dependency)) -> NDTShema | None:
    return await get_dependency(
        ident, 
        NDTDBService()
    )


async def update_dependency[Data: BaseShema](data: Data, ident: str, service: BaseDBService) -> str:

    try:
        await service.update(ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)
    
    return ident


async def update_welder_dependency(data: UpdateWelderShema, ident: str = Depends(validate_ident_dependency)) -> str:
    return await update_dependency(
        data, 
        ident, 
        WelderDBService()
    )


async def update_welder_certification_dependency(data: UpdateWelderCertificationShema, ident: str = Depends(validate_ident_dependency)) -> str:
    return await update_dependency(
        data, 
        ident, 
        WelderCertificationDBService()
    )


async def update_ndt_dependency(data: UpdateNDTShema, ident: str = Depends(validate_ident_dependency)) -> str:
    return await update_dependency(
        data, 
        ident, 
        NDTDBService()
    )


async def delete_dependency(ident: str, service: BaseDBService) -> str:

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)
    
    return ident


async def delete_welder_dependency(ident: str = Depends(validate_ident_dependency)) -> str:
    return await delete_dependency(
        ident, 
        WelderDBService()
    )


async def delete_welder_certification_dependency(ident: str = Depends(validate_ident_dependency)) -> str:
    return await delete_dependency(
        ident, 
        WelderCertificationDBService()
    )


async def delete_ndt_dependency(ident: str = Depends(validate_ident_dependency)) -> str:
    return await delete_dependency(
        ident, 
        NDTDBService()
    )