from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from app.application.interactors import CreatePersonalInteractor, UpdatePersonalInteractor, DeletePersonalInteractor, SelectPersonalInteractor, GetPersonalInteractor
from app.presentation.shemas import CreatePersonalShema, UpdatePersonalShema, PersonalSelectShema, SelectResponse
from app.application.dto import PersonalDTO
from app.application.common.exc import PersonalNotFoundException


personal_router = APIRouter(
    route_class=DishkaRoute
)


@personal_router.post("/personal")
async def create_personal(
    create: FromDishka[CreatePersonalInteractor],
    data: CreatePersonalShema
) -> ORJSONResponse:

    await create(data.to_dto())

    return ORJSONResponse(
        content={
            "detail": "personal created"
        }
    ) 


@personal_router.get("/personal/{ident}")
async def get_personal(
    get: FromDishka[GetPersonalInteractor],
    ident: UUID
) -> PersonalDTO:

    res = await get(ident)

    if res:
        return res
    
    raise PersonalNotFoundException(ident)


@personal_router.post("/personal/select")
async def select_personal(
    select: FromDishka[SelectPersonalInteractor],
    filters: PersonalSelectShema
) -> SelectResponse[PersonalDTO]:

    res = await select(
        filters=filters.model_dump(exclude_unset=True, exclude_none=True),
        limit=filters.limit,
        offset=filters.offset
    )

    return {
        "result": res[0],
        "count": res[1]
    }


@personal_router.patch("/personal/{ident}")
async def update_personal(
    update: FromDishka[UpdatePersonalInteractor],
    ident: UUID, 
    data: UpdatePersonalShema
) -> ORJSONResponse:

    await update(ident, data.to_dto())

    return ORJSONResponse(
        content={
            "detail": f"personal ({ident}) updated"
        }
    )


@personal_router.delete("/personal/{ident}")
async def delete_personal(
    delete: FromDishka[DeletePersonalInteractor],
    ident: UUID
) -> ORJSONResponse: 

    await delete(ident)

    return ORJSONResponse(
        content={
            "detail": f"personal ({ident}) removed"
        }
    )
