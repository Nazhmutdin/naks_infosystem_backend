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
    service = PersonalDBService()

    try:
        await service.insert(session, data)
    except CreateDBException as e:
        raise HTTPException(session, 400, e.message)

    return {
        "detail": "personal added"
    }


@v1_router.get("/personal/{ident}")
async def get_personal(ident: str = Depends(validate_personal_ident_dependency), session: AsyncSession = Depends(get_session)) -> PersonalShema:
    service = PersonalDBService()

    try:
        result = await service.get(session, ident)
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
    filters: PersonalSelectShema = Depends(InputValidationDependency(PersonalSelectShema).execute),
    session: AsyncSession = Depends(get_session),
    limit: int = 100,
    offset: int = 0
    ) -> dict[str, list[PersonalShema] | int]:
    service = PersonalDBService()

    try:
        result = await service.get_many(session, filters, limit, offset)
        count = await service.count(session, filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result,
        "count": count
    }


@v1_router.patch("/personal/{ident}")
async def update_personal(
    ident: str = Depends(validate_personal_ident_dependency), 
    data: UpdatePersonalShema = Depends(InputValidationDependency(UpdatePersonalShema).execute), 
    session: AsyncSession = Depends(get_session)
    ) -> dict[str, str]:
    service = PersonalDBService()

    try:
        await service.update(session, ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"personal ({ident}) updated"
    }


@v1_router.delete("/personal/{ident}")
async def delete_personal(ident: str = Depends(validate_personal_ident_dependency), session: AsyncSession = Depends(get_session)):
    service = PersonalDBService()

    try:
        await service.delete(session, ident)
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

    service = PersonalCertificationDBService()

    try:
        await service.insert(session, data)
    except CreateDBException as e:
        raise HTTPException(400, e.message)
    
    return {
        "detail": "personal certification added"
    }


@v1_router.get("/personal-certification/{ident}")
async def get_personal_certification(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)) -> PersonalCertificationShema:
    service = PersonalCertificationDBService()

    try:
        result = await service.get(session, ident)
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
    filters: PersonalCertificationSelectShema = Depends(InputValidationDependency(PersonalCertificationSelectShema).execute),
    session: AsyncSession = Depends(get_session),
    limit: int = 100,
    offset: int = 0
    ) -> dict[str, list[PersonalCertificationShema] | int]:
    service = PersonalCertificationDBService()

    try:
        result = await service.get_many(session, filters, limit, offset)
        count = await service.count(session, filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result,
        "count": count
    }


@v1_router.patch("/personal-certification/{ident}")
async def update_personal_certification( 
    ident: str = Depends(validate_ident_dependency), 
    data: UpdatePersonalCertificationShema = Depends(InputValidationDependency(UpdatePersonalCertificationShema).execute),
    session: AsyncSession = Depends(get_session)
    ):
    service = PersonalCertificationDBService()

    try:
        await service.update(session, ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)
    
    return {
        "detail": f"personal certification ({ident}) updated"
    }


@v1_router.delete("/personal-certification/{ident}")
async def delete_personal_certification(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)):
    
    service = PersonalCertificationDBService()

    try:
        await service.delete(session, ident)
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
    service = NDTDBService()

    try:
        await service.insert(session, data)
    except CreateDBException as e:
        raise HTTPException(400, e.message)

    return {
        "detail": f"ndt added"
    }


@v1_router.get("/ndt/{ident}")
async def get_ndt(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)) -> NDTShema:
    service = NDTDBService()

    try:
        result = await service.get(session, ident)
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
    filters: NDTSelectShema = Depends(InputValidationDependency(NDTSelectShema).execute),
    session: AsyncSession = Depends(get_session),
    limit: int = 100,
    offset: int = 0
    ) -> dict[str, list[NDTShema] | int]:
    service = NDTDBService()

    try:
        result = await service.get_many(session, filters, limit, offset)
        count = await service.count(session, filters)
    except GetDBException as e:
        raise HTTPException(400, e.args)

    return {
        "result": result,
        "count": count
    }


@v1_router.patch("/ndt/{ident}")
async def update_ndt(
    ident: str = Depends(validate_ident_dependency), 
    data: UpdateNDTShema = Depends(InputValidationDependency(UpdateNDTShema).execute), 
    session: AsyncSession = Depends(get_session)
    ):    
    service = NDTDBService()

    try:
        await service.update(session, ident, data)
    except UpdateDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt ({ident}) updated"
    }


@v1_router.delete("/ndt/{ident}")
async def delete_ndt(ident: str = Depends(validate_ident_dependency), session: AsyncSession = Depends(get_session)):    
    service = NDTDBService()

    try:
        await service.delete(session, ident)
    except DeleteDBException as e:
        raise HTTPException(400, e.args)

    return {
        "detail": f"ndt ({ident}) removed"
    }
