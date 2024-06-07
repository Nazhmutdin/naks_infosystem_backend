from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import *
from shemas import *
from services.db_services import *
from database import get_session
from errors import *


v1_router = APIRouter()


"""
=========================================================================================
welder routes
=========================================================================================
"""


@v1_router.post("/welders")
async def add_welder(
    data: CreateWelderShema = Depends(InputValidationDependency(CreateWelderShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:
    service = WelderDBService(session)

    try:
        await service.add(data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": "welder added"
    }


@v1_router.get("/welders/{ident}")
async def get_welder(ident: str = Depends(validate_welder_ident_dependency), session: AsyncSession = Depends(get_session)) -> WelderShema:
    service = WelderDBService(session)

    try:
        result = await service.get(ident)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    if not result:
        raise HTTPException(
            detail=f"welder ({ident}) not found",
            status_code=400
        )

    return result


@v1_router.post("/welders/select")
async def select_welders(
    filters: WelderRequestShema = Depends(InputValidationDependency(WelderRequestShema).execute),
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, list[WelderShema] | int]:
    service = WelderDBService(session)

    try:
        result = await service.get_many(filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result[0],
        "count": result[1]
    }


@v1_router.patch("/welders/{ident}")
async def update_welder(
    ident: str = Depends(validate_welder_ident_dependency), 
    data: UpdateWelderShema = Depends(InputValidationDependency(UpdateWelderShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:
    service = WelderDBService(session)

    try:
        await service.update(ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"welder ({ident}) updated"
    }


@v1_router.delete("/welders/{ident}")
async def delete_welder(ident: str = Depends(validate_welder_ident_dependency), session: AsyncSession = Depends(get_session)):
    service = WelderDBService(session)

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"welder ({ident}) removed"
    }


"""
=========================================================================================
welder certification routes
=========================================================================================
"""


@v1_router.post("/welder-certifications")
async def add_welder_certification(
    data: CreateWelderCertificationShema = Depends(InputValidationDependency(CreateWelderCertificationShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:

    service = WelderCertificationDBService(session)

    try:
        await service.add(data)
    except CreateDBException as e:
        raise HTTPException(400, e.args)
    
    return {
        "detail": "welder certification added"
    }


@v1_router.get("/welder-certifications/{ident}")
async def get_welder_certification(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)) -> WelderCertificationShema:
    service = WelderCertificationDBService(session)

    try:
        result = await service.get(ident)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    if not result:
        raise HTTPException(
            detail=f"welder certification ({ident}) not found",
            status_code=400
        )

    return result


@v1_router.post("/welder-certifications/select")
async def select_welder_certifications(
    filters: WelderCertificationRequestShema = Depends(InputValidationDependency(WelderCertificationRequestShema).execute),
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, list[WelderCertificationShema] | int]:
    service = WelderCertificationDBService(session)

    try:
        result = await service.get_many(filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result[0],
        "count": result[1]
    }


@v1_router.patch("/welder-certifications/{ident}")
async def update_welder_certification( 
    ident: str = Depends(validate_ident_dependency), 
    data: UpdateWelderCertificationShema = Depends(InputValidationDependency(UpdateWelderCertificationShema).execute),
    session: AsyncSession = Depends(get_session)
    ):
    service = WelderCertificationDBService(session)

    try:
        await service.update(ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)
    
    return {
        "detail": f"welder certification ({ident}) updated"
    }


@v1_router.delete("/welder-certifications/{ident}")
async def delete_welder_certification(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)):
    
    service = WelderCertificationDBService(session)

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)
    
    return {
        "detail": f"welder certification ({ident}) removed"
    }


"""
=========================================================================================
ndt routes
=========================================================================================
"""


@v1_router.post("/ndts")
async def add_ndt(
    data: CreateNDTShema = Depends(InputValidationDependency(CreateNDTShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:
    service = NDTDBService(session)

    try:
        await service.add(data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt added"
    }


@v1_router.get("/ndts/{ident}")
async def get_ndt(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)) -> NDTShema:
    service = NDTDBService(session)

    try:
        result = await service.get(ident)
    except GetDBException as e:
        raise HTTPException(400, e.args)
    
    if not result:
        raise HTTPException(
            detail="ndt not found",
            status_code=400
        )

    return result


@v1_router.post("/ndts/select")
async def select_ndts(
    filters: NDTRequestShema = Depends(InputValidationDependency(NDTRequestShema).execute),
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, list[NDTShema] | int]:
    service = NDTDBService(session)

    try:
        result = await service.get_many(filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result[0],
        "count": result[1]
    }


@v1_router.patch("/ndts/{ident}")
async def update_ndt(
    ident: str = Depends(validate_ident_dependency), 
    data: UpdateNDTShema = Depends(InputValidationDependency(UpdateNDTShema).execute), 
    session: AsyncSession = Depends(get_session)
    ):    
    service = NDTDBService(session)

    try:
        await service.update(ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt ({ident}) updated"
    }


@v1_router.delete("/ndts/{ident}")
async def delete_ndt(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)):    
    service = NDTDBService(session)

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt ({ident}) removed"
    }
