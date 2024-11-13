from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from app.presentation.shemas import NDTSelectShema, SelectResponse
from app.application.interactors import CreateNdtInteractor, UpdateNdtInteractor, DeleteNdtInteractor, GetNdtInteractor, SelectNdtInteractor, GetCertainPersonalNdtsInteractor
from app.application.dto import NdtDTO, UpdateNdtDTO, CreateNdtDTO
from app.application.common.exc import NdtNotFoundException

ndt_router = APIRouter()


@ndt_router.post("/ndt")
@inject
async def create_ndt(
    create: FromDishka[CreateNdtInteractor],
    data: CreateNdtDTO
) -> ORJSONResponse:

    await create(data)

    return ORJSONResponse(
        content={
            "detail": "ndt created"
        }
    ) 


@ndt_router.get("/ndt/personal/{personal_ident}")
@inject
async def get_certain_personal_ndts(
    get: FromDishka[GetCertainPersonalNdtsInteractor],
    personal_ident: UUID
) -> list[NdtDTO]: 

    certs = await get(personal_ident)

    return certs


@ndt_router.get("/ndt/{ident}")
@inject
async def get_ndt(
    get: FromDishka[GetNdtInteractor],
    ident: UUID
) -> NdtDTO:

    res = await get(ident)

    if res:
        return res
    
    raise NdtNotFoundException(ident)


@ndt_router.post("/ndt/select")
@inject
async def select_ndt(
    select: FromDishka[SelectNdtInteractor],
    filters: NDTSelectShema
) -> SelectResponse[NdtDTO]:

    res = await select(
        filters=filters.model_dump(exclude_unset=True, exclude_none=True),
        limit=filters.limit,
        offset=filters.offset
    )

    return {
        "result": res[0],
        "count": res[1]
    }


@ndt_router.patch("/ndt/{ident}")
@inject
async def update_ndt(
    update: FromDishka[UpdateNdtInteractor],
    ident: UUID, 
    data: UpdateNdtDTO, 
) -> ORJSONResponse: 

    await update(ident, data)

    return ORJSONResponse(
        content={
            "detail": f"ndt ({ident}) updated"
        }
    )


@ndt_router.delete("/ndt/{ident}")
@inject
async def delete_ndt(
    delete: FromDishka[DeleteNdtInteractor],
    ident: UUID
) -> ORJSONResponse: 

    await delete(ident)

    return ORJSONResponse(
        content={
            "detail": "ndt ({ident}) removed"
        }
    ) 
