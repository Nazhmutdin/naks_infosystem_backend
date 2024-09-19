from uuid import UUID

from fastapi import APIRouter, HTTPException
from naks_library.exc import *

from src.services.db_services import *
from src.api.v1.dependencies import *
from src._types import SelectResponse
from src.shemas import *


v1_router = APIRouter()


"""
=========================================================================================
personal routes
=========================================================================================
"""


@v1_router.post("/personal")
async def insert_personal(
    data: CreatePersonalShema, 
    session: SessionDep
    ) -> dict[str, str]:
    service = PersonalDBService()
    
    await insert(service, data, session)

    return {
        "detail": "personal inserted"
    }


@v1_router.get("/personal/{ident}")
async def get_personal(
    ident: UUID, 
    session: SessionDep
    ) -> PersonalShema:
    service = PersonalDBService()

    result = await get(service, ident, session)

    if not result:
        raise HTTPException(
            detail=f"personal ({ident}) not found",
            status_code=400
        )

    return result


@v1_router.post("/personal/select")
async def select_personal(
    filters: PersonalSelectShema,
    session: SessionDep
    ) -> SelectResponse[PersonalShema]:
    service = PersonalDBService()

    result, count = await get_many(service, filters, session)

    return {
        "result": result,
        "count": count
    }


@v1_router.patch("/personal/{ident}")
async def update_personal(
    ident: UUID, 
    data: UpdatePersonalShema, 
    session: SessionDep
    ) -> dict[str, str]:
    service = PersonalDBService()

    await update(service, ident, data, session)

    return {
        "detail": f"personal ({ident}) updated"
    }


@v1_router.delete("/personal/{ident}")
async def delete_personal(
    ident: UUID, 
    session: SessionDep
    ):
    service = PersonalDBService()

    await delete(service, ident, session)

    return {
        "detail": f"personal ({ident}) removed"
    }


"""
=========================================================================================
personal certification routes
=========================================================================================
"""


@v1_router.post("/personal-certification")
async def insert_personal_certification(
    data: CreatePersonalCertificationShema, 
    session: SessionDep
    ) -> dict[str, str]:

    service = PersonalCertificationDBService()
    
    await insert(service, data, session)
    
    return {
        "detail": "personal certification inserted"
    }


@v1_router.get("/personal-certification/{ident}")
async def get_personal_certification(
    ident: UUID, 
    session: SessionDep
    ) -> PersonalCertificationShema:
    service = PersonalCertificationDBService()

    result = await get(service, ident, session)

    if not result:
        raise HTTPException(
            detail=f"personal certification ({ident}) not found",
            status_code=400
        )

    return result


@v1_router.post("/personal-certification/select")
async def select_personal_certifications(
    filters: PersonalCertificationSelectShema,
    session: SessionDep
    ) -> dict[str, list[PersonalCertificationShema] | int]:
    service = PersonalCertificationDBService()

    result, count = await get_many(service, filters, session)

    return {
        "result": result,
        "count": count
    }


@v1_router.patch("/personal-certification/{ident}")
async def update_personal_certification( 
    ident: UUID, 
    data: UpdatePersonalCertificationShema,
    session: SessionDep
    ):
    service = PersonalCertificationDBService()

    await update(service, ident, data, session)
    
    return {
        "detail": f"personal certification ({ident}) updated"
    }


@v1_router.delete("/personal-certification/{ident}")
async def delete_personal_certification(
    ident: UUID, 
    session: SessionDep
    ):
    
    service = PersonalCertificationDBService()

    await delete(service, ident, session)
    
    return {
        "detail": f"personal certification ({ident}) removed"
    }


"""
=========================================================================================
ndt routes
=========================================================================================
"""


@v1_router.post("/ndt")
async def insert_ndt(
    data: CreateNDTShema, 
    session: SessionDep
    ) -> dict[str, str]:
    service = NDTDBService()
    
    await insert(service, data, session)

    return {
        "detail": f"ndt inserted"
    }


@v1_router.get("/ndt/{ident}")
async def get_ndt(
    ident: UUID, 
    session: SessionDep
    ) -> NDTShema:
    service = NDTDBService()

    result = await get(service, ident, session)
    
    if not result:
        raise HTTPException(
            detail="ndt not found",
            status_code=400
        )

    return result


@v1_router.post("/ndt/select")
async def select_ndts(
    filters: NDTSelectShema,
    session: SessionDep
    ) -> dict[str, list[NDTShema] | int]:
    service = NDTDBService()

    result, count = await get_many(service, filters, session)

    return {
        "result": result,
        "count": count
    }


@v1_router.patch("/ndt/{ident}")
async def update_ndt(
    ident: UUID, 
    data: UpdateNDTShema, 
    session: SessionDep
    ):    
    service = NDTDBService()

    await update(service, ident, data, session)

    return {
        "detail": f"ndt ({ident}) updated"
    }


@v1_router.delete("/ndt/{ident}")
async def delete_ndt(
    ident: UUID, 
    session: SessionDep
    ):    
    service = NDTDBService()

    await delete(service, ident, session)

    return {
        "detail": f"ndt ({ident}) removed"
    }
