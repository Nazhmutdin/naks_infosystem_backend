from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from naks_library.exc import *

from src.services.db_services import *
from src.api.v1.dependencies import *
from src.database import get_session
from src.shemas import *


v1_router = APIRouter()


"""
=========================================================================================
personal routes
=========================================================================================
"""


@v1_router.post("/personal")
async def add_personal(
    data: CreatePersonalShema = Depends(InputValidationDependency(CreatePersonalShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:
    service = PersonalDBService(session)

    try:
        await service.add(data)
    except CreateDBException as e:
        raise HTTPException(400, e.message)

    return {
        "detail": "personal added"
    }


@v1_router.get("/personal/{ident}")
async def get_personal(ident: str = Depends(validate_personal_ident_dependency), session: AsyncSession = Depends(get_session)) -> PersonalShema:
    service = PersonalDBService(session)

    try:
        result = await service.get(ident)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    if not result:
        raise HTTPException(
            detail=f"personal ({ident}) not found",
            status_code=400
        )

    return result


@v1_router.post("/personal/select")
async def select_personal(
    filters: PersonalRequestShema = Depends(InputValidationDependency(PersonalRequestShema).execute),
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, list[PersonalShema] | int]:
    service = PersonalDBService(session)

    try:
        result = await service.get_many(filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result[0],
        "count": result[1]
    }


@v1_router.patch("/personal/{ident}")
async def update_personal(
    ident: str = Depends(validate_personal_ident_dependency), 
    data: UpdatePersonalShema = Depends(InputValidationDependency(UpdatePersonalShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:
    service = PersonalDBService(session)

    try:
        await service.update(ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"personal ({ident}) updated"
    }


@v1_router.delete("/personal/{ident}")
async def delete_personal(ident: str = Depends(validate_personal_ident_dependency), session: AsyncSession = Depends(get_session)):
    service = PersonalDBService(session)

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"personal ({ident}) removed"
    }


"""
=========================================================================================
personal certification routes
=========================================================================================
"""


@v1_router.post("/personal-certification")
async def add_personal_certification(
    data: CreatePersonalCertificationShema = Depends(InputValidationDependency(CreatePersonalCertificationShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:

    service = PersonalCertificationDBService(session)

    try:
        await service.add(data)
    except CreateDBException as e:
        raise HTTPException(400, e.message)
    
    return {
        "detail": "personal certification added"
    }


@v1_router.get("/personal-certification/{ident}")
async def get_personal_certification(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)) -> PersonalCertificationShema:
    service = PersonalCertificationDBService(session)

    try:
        result = await service.get(ident)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    if not result:
        raise HTTPException(
            detail=f"personal certification ({ident}) not found",
            status_code=400
        )

    return result


@v1_router.post("/personal-certification/select")
async def select_personal_certifications(
    filters: PersonalCertificationRequestShema = Depends(InputValidationDependency(PersonalCertificationRequestShema).execute),
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, list[PersonalCertificationShema] | int]:
    service = PersonalCertificationDBService(session)

    try:
        result = await service.get_many(filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result[0],
        "count": result[1]
    }


@v1_router.patch("/personal-certification/{ident}")
async def update_personal_certification( 
    ident: str = Depends(validate_ident_dependency), 
    data: UpdatePersonalCertificationShema = Depends(InputValidationDependency(UpdatePersonalCertificationShema).execute),
    session: AsyncSession = Depends(get_session)
    ):
    service = PersonalCertificationDBService(session)

    try:
        await service.update(ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)
    
    return {
        "detail": f"personal certification ({ident}) updated"
    }


@v1_router.delete("/personal-certification/{ident}")
async def delete_personal_certification(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)):
    
    service = PersonalCertificationDBService(session)

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)
    
    return {
        "detail": f"personal certification ({ident}) removed"
    }


"""
=========================================================================================
ndt routes
=========================================================================================
"""


@v1_router.post("/ndt")
async def add_ndt(
    data: CreateNDTShema = Depends(InputValidationDependency(CreateNDTShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:
    service = NDTDBService(session)

    try:
        await service.add(data)
    except CreateDBException as e:
        raise HTTPException(400, e.message)

    return {
        "detail": f"ndt added"
    }


@v1_router.get("/ndt/{ident}")
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


@v1_router.post("/ndt/select")
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


@v1_router.patch("/ndt/{ident}")
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


@v1_router.delete("/ndt/{ident}")
async def delete_ndt(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)):    
    service = NDTDBService(session)

    try:
        await service.delete(ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt ({ident}) removed"
    }
