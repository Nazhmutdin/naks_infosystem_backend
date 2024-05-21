from fastapi import APIRouter, HTTPException, Depends

from api.v1.dependencies import *

from shemas import *
from services.db_services import *


v1_router = APIRouter()


"""
=========================================================================================
welder routes
=========================================================================================
"""


@v1_router.post("/welders")
async def add_welder(result: WelderShema = Depends(add_welder_dependency)) -> dict[str, str | WelderShema]:

    return {
        "detail": "welder added",
        "data": result
    }


@v1_router.get("/welders/{ident}")
async def get_welder(result: WelderShema | None = Depends(get_welder_dependency)) -> WelderShema:

    if not result:
        raise HTTPException(
            detail="welder certification not found",
            status_code=400
        )

    return result


@v1_router.patch("/welders/{ident}")
async def update_welder(ident: str = Depends(update_welder_dependency)) -> dict[str, str]:

    return {
        "detail": f"welder ({ident}) updated"
    }


@v1_router.delete("/welders/{ident}")
async def delete_welder(ident: str = Depends(delete_welder_dependency)):

    return {
        "detail": f"welder ({ident}) removed"
    }


"""
=========================================================================================
welder certification routes
=========================================================================================
"""


@v1_router.post("/welder-certifications")
async def add_welder_certification(result: WelderCertificationShema = Depends(add_welder_certification_dependency)) -> dict[str, str | WelderCertificationShema]:

    return {
        "detail": "welder certification added",
        "data": result
    }


@v1_router.get("/welder-certifications/{ident}")
async def get_welder_certification(result: WelderCertificationShema | None = Depends(get_welder_certification_dependency)) -> WelderCertificationShema:

    if not result:
        raise HTTPException(
            detail="welder certification not found",
            status_code=400
        )

    return result


@v1_router.patch("/welder-certifications/{ident}")
async def update_welder_certification(ident: str = Depends(update_welder_certification_dependency)):
    return {
        "detail": f"welder certification ({ident}) updated"
    }


@v1_router.delete("/welder-certifications/{ident}")
async def delete_welder_certification(ident: str = Depends(delete_welder_certification_dependency)):
    return {
        "detail": f"welder certification ({ident}) removed"
    }


"""
=========================================================================================
ndt routes
=========================================================================================
"""


@v1_router.post("/ndts")
async def add_ndt(result: NDTShema = Depends(add_ndt_dependency)) -> dict[str, str | NDTShema]:

    return {
        "detail": f"ndt added",
        "data": result
    }


@v1_router.get("/ndts/{ident}")
async def get_ndt(result: NDTShema | None = Depends(get_ndt_dependency)) -> NDTShema:

    if not result:
        raise HTTPException(
            detail="ndt not found",
            status_code=400
        )

    return result


@v1_router.patch("/ndts/{ident}")
async def update_ndt(ident: str = Depends(update_ndt_dependency)):

    return {
        "detail": f"ndt ({ident}) updated"
    }


@v1_router.delete("/ndts/{ident}")
async def delete_ndt(ident: str = Depends(delete_ndt_dependency)):

    return {
        "detail": f"ndt ({ident}) removed"
    }