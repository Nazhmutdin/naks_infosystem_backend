from fastapi import APIRouter, HTTPException, Depends

from api.v1.dependencies import DeleteDataDependency, UpdateDataDependency, validate_ident

from shemas import *
from errors import *
from services.db_services import *


v1_router = APIRouter()


"""
=========================================================================================
welder routes
=========================================================================================
"""


@v1_router.post("/welders")
async def add_welder(data: CreateWelderShema):
    service = WelderDBService()

    try:
        await service.add(data)
    except CreateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": "welder added"
    }


@v1_router.get("/welders/{ident}")
async def get_welder(ident = Depends(validate_ident)) -> WelderShema:
    service = WelderDBService()

    result = await service.get(ident)

    if not result:
        raise HTTPException(
            detail="welder certification not found",
            status_code=400
        )

    return result


@v1_router.patch("/welders")
async def update_welder(ident = Depends(
    UpdateDataDependency[UpdateWelderShema](
        WelderDBService()
    )
)):

    return {
        "detail": f"welder ({ident}) updated"
    }


@v1_router.delete("/welders/{ident}")
async def delete_welder(ident: str = Depends(
    DeleteDataDependency(WelderDBService())
)):

    return {
        "detail": f"welder ({ident}) removed"
    }


"""
=========================================================================================
welder certification routes
=========================================================================================
"""


@v1_router.post("/welder-certifications")
async def add_welder_certification(data: CreateWelderCertificationShema):
    service = WelderCertificationDBService()

    try:
        await service.add(data)
    except CreateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": "welder certification added"
    }


@v1_router.get("/welder-certifications/{ident}")
async def get_welder_certification(ident = Depends(validate_ident)) -> WelderCertificationShema:
    service = WelderCertificationDBService()

    result = await service.get(ident)

    if not result:
        raise HTTPException(
            detail="welder certification not found",
            status_code=400
        )

    return result


@v1_router.patch("/welder-certifications")
async def update_welder_certification(ident: str = Depends(
    UpdateDataDependency[UpdateWelderCertificationShema](
        WelderCertificationDBService()
    )
)):
    return {
        "detail": f"welder certification ({ident}) updated"
    }


@v1_router.delete("/welder-certifications/{ident}")
async def delete_welder_certification(ident: str = Depends(
    DeleteDataDependency(WelderCertificationDBService())
)):
    return {
        "detail": f"welder certification ({ident}) removed"
    }


"""
=========================================================================================
ndt routes
=========================================================================================
"""


@v1_router.post("/ndts")
async def add_ndt(data: CreateNDTShema):
    service = NDTDBService()

    try:
        await service.add(data)
    except CreateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt added"
    }


@v1_router.get("/ndts/{ident}")
async def get_ndt(ident = Depends(validate_ident)) -> NDTShema:
    service = NDTDBService()

    result = await service.get(ident)

    if not result:
        raise HTTPException(
            detail="welder certification not found",
            status_code=400
        )

    return result


@v1_router.patch("/ndts")
async def update_ndt(ident: str = Depends(
    UpdateDataDependency[UpdateNDTShema](
        NDTDBService()
    )
)):

    return {
        "detail": f"ndt ({ident}) updated"
    }


@v1_router.delete("/ndts/{ident}")
async def delete_ndt(ident: str = Depends(
    DeleteDataDependency(NDTDBService())
)):

    return {
        "detail": f"ndt ({ident}) removed"
    }