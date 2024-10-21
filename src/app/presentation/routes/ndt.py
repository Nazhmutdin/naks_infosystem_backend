from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from app.presentation.shemas import CreateNdtShema, UpdateNdtShema, NDTSelectShema, SelectResponse
from app.application.interactors import CreateNdtInteractor, UpdateNdtInteractor, DeleteNdtInteractor, GetNdtInteractor, SelectNdtInteractor
from app.application.dto import NdtDTO
from app.application.common.exc import NdtNotFoundException

ndt_router = APIRouter(
    route_class=DishkaRoute
)


@ndt_router.post("/ndt")
async def create_ndt(
    create: FromDishka[CreateNdtInteractor],
    data: CreateNdtShema
) -> ORJSONResponse:

    await create(data.to_dto())

    return ORJSONResponse(
        content={
            "detail": "ndt created"
        }
    ) 


@ndt_router.get("/ndt/{ident}")
async def get_ndt(
    get: FromDishka[GetNdtInteractor],
    ident: UUID
) -> NdtDTO:

    res = await get(ident)

    if res:
        return res
    
    raise NdtNotFoundException(ident)


@ndt_router.post("/ndt/select")
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
async def update_ndt(
    update: FromDishka[UpdateNdtInteractor],
    ident: UUID, 
    data: UpdateNdtShema, 
) -> ORJSONResponse: 

    await update(ident, data.to_dto())

    return ORJSONResponse(
        content={
            "detail": f"ndt ({ident}) updated"
        }
    )


@ndt_router.delete("/ndt/{ident}")
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
