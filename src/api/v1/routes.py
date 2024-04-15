from fastapi import APIRouter, HTTPException

from shemas import *
from errors import *
from services.db_services import *


v1_router = APIRouter()


"""
=========================================================================================
welder routes
=========================================================================================
"""


@v1_router.get("/welders/{ident}")
async def get_welder(ident: str) -> WelderShema:
    service = WelderDBService()

    return await service.get(ident)


@v1_router.put("/welders")
async def add_welder(data: CreateWelderShema):
    service = WelderDBService()

    try:
        await service.add(**data.model_dump(exclude_unset=True))
    except CreateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": "welder data added"
    }


@v1_router.patch("/welders")
async def update_welder(ident: str, data: UpdateWelderShema):
    service = WelderDBService()

    try:
        await service.update(ident, **data.model_dump(exclude_unset=True))
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"welder data updated"
    }


@v1_router.delete("/welders")
async def delete_welder(ident: str):
    service = WelderDBService()

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"welder data removed"
    }


"""
=========================================================================================
welder certification routes
=========================================================================================
"""


@v1_router.put("/welder-certifications")
async def add_welder_certification(data: CreateWelderCertificationShema):
    service = WelderCertificationDBService()

    try:
        await service.add(**data.model_dump(exclude_unset=True))
    except CreateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": "welder certification data added"
    }


@v1_router.get("/welder-certifications/{ident}")
async def get_welder_certification(ident: str) -> WelderCertificationShema:
    service = WelderCertificationDBService()

    return await service.get(ident)


@v1_router.patch("/welder-certifications")
async def update_welder_certification(ident: str, data: UpdateWelderCertificationShema):
    service = WelderCertificationDBService()

    try:
        await service.update(ident, **data.model_dump(exclude_unset=True))
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"welder certification data updated"
    }


@v1_router.delete("/welder-certifications")
async def delete_welder_certification(ident: str):
    service = WelderCertificationDBService()

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"welder certification data removed"
    }


"""
=========================================================================================
ndt routes
=========================================================================================
"""


@v1_router.put("/ndts")
async def add_ndt(data: CreateNDTShema):
    service = NDTDBService()

    try:
        await service.add(**data.model_dump(exclude_unset=True))
    except CreateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": "ndt data added"
    }


@v1_router.get("/ndts/{ident}")
async def get_ndt(ident: str) -> NDTShema:
    service = NDTDBService()

    return await service.get(ident)


@v1_router.patch("/ndts")
async def update_ndt(ident: str, data: UpdateNDTShema):
    service = NDTDBService()

    try:
        await service.update(ident, **data.model_dump(exclude_unset=True))
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt data updated"
    }


@v1_router.delete("/ndts")
async def delete_ndt(ident: str):
    service = NDTDBService()

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt data removed"
    }