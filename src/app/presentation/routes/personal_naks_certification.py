from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from app.presentation.shemas import (
    PersonalNaksCertificationSelectShema,
    SelectResponse
)
from app.application.interactors import (
    CreatePersonalNaksCertificationInteractor,
    UpdatePersonalNaksCertificationInteractor,
    DeletePersonalNaksCertificationInteractor,
    GetPersonalNaksCertificationInteractor,
    GetCertainPersonalNaksCertificationsInteractor,
    SelectPersonalNaksCertificationInteractor
)
from app.application.dto import PersonalNaksCertificationDTO, UpdatePersonalNaksCertificationDTO, CreatePersonalNaksCertificationDTO
from app.application.common.exc import PersonalNaksCertificationNotFoundException


personal_naks_certification_router = APIRouter()


@personal_naks_certification_router.post("/personal-naks-certification")
@inject
async def create_personal_naks_certification(
    create: FromDishka[CreatePersonalNaksCertificationInteractor],
    data: CreatePersonalNaksCertificationDTO
) -> ORJSONResponse: 

    await create(data)

    return ORJSONResponse(
        content={
            "detail": "personal naks certification created"
        }
    )


@personal_naks_certification_router.get("/personal-naks-certification/personal/{personal_ident}")
@inject
async def get_certain_personal_naks_certifications(
    get: FromDishka[GetCertainPersonalNaksCertificationsInteractor],
    personal_ident: UUID
) -> list[PersonalNaksCertificationDTO]: 

    certs = await get(personal_ident)

    return certs


@personal_naks_certification_router.get("/personal-naks-certification/{ident}")
@inject
async def get_personal_naks_certification(
    get: FromDishka[GetPersonalNaksCertificationInteractor],
    ident: UUID
) -> PersonalNaksCertificationDTO: 

    res = await get(ident)

    if res:
        return res
    
    raise PersonalNaksCertificationNotFoundException(ident)


@personal_naks_certification_router.post("/personal-naks-certification/select")
@inject
async def select_personal_naks_certification(
    select: FromDishka[SelectPersonalNaksCertificationInteractor],
    filters: PersonalNaksCertificationSelectShema
) -> SelectResponse[PersonalNaksCertificationDTO]:

    res = await select(
        filters=filters.model_dump(exclude_unset=True, exclude_none=True),
        limit=filters.limit,
        offset=filters.offset
    )

    return {
        "result": res[0],
        "count": res[1]
    }


@personal_naks_certification_router.patch("/personal-naks-certification/{ident}")
@inject
async def update_personal_naks_certification( 
    update: FromDishka[UpdatePersonalNaksCertificationInteractor],
    ident: UUID, 
    data: UpdatePersonalNaksCertificationDTO
) -> ORJSONResponse: 

    await update(ident, data)

    return ORJSONResponse(
        content={
            "detail": f"personal naks certification ({ident}) updated"
        }
    ) 


@personal_naks_certification_router.delete("/personal-naks-certification/{ident}")
@inject
async def delete_personal_naks_certification(
    delete: FromDishka[DeletePersonalNaksCertificationInteractor],
    ident: UUID
) -> ORJSONResponse: 

    await delete(ident)
    
    return ORJSONResponse(
        content={
            "detail": f"personal naks certification ({ident}) removed"
        }
    ) 