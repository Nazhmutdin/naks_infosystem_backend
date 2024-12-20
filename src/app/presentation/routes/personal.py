from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse
from pydantic import RootModel
from dishka import FromDishka
from dishka.integrations.fastapi import inject

from app.application.interactors import CreatePersonalInteractor, UpdatePersonalInteractor, DeletePersonalInteractor, SelectPersonalInteractor, GetPersonalInteractor
from app.presentation.shemas import PersonalSelectShema, SelectResponse
from app.application.dto import PersonalDTO, CreatePersonalDTO, UpdatePersonalDTO
from app.application.common.exc import PersonalNotFoundException


personal_router = APIRouter()


@personal_router.post("/personal")
@inject
async def create_personal(
    create: FromDishka[CreatePersonalInteractor],
    data: CreatePersonalDTO
) -> ORJSONResponse:

    await create(data)

    return ORJSONResponse(
        content={
            "detail": "personal created"
        }
    ) 


@personal_router.get("/personal/select")
@inject
async def select_personal(
    select: FromDishka[SelectPersonalInteractor],
    filters: Annotated[PersonalSelectShema, Query()],
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


@personal_router.get("/personal")
@inject
async def get_personal(
    get: FromDishka[GetPersonalInteractor],
    ident: Annotated[UUID, Query()]
) -> PersonalDTO:

    res = await get(ident)

    if res:
        return res
    
    raise PersonalNotFoundException(ident)


@personal_router.patch("/personal")
@inject
async def update_personal(
    update: FromDishka[UpdatePersonalInteractor],
    ident: Annotated[UUID, Query()],
    data: RootModel[UpdatePersonalDTO]
) -> ORJSONResponse:

    await update(ident, data.model_dump(exclude_unset=True))

    return ORJSONResponse(
        content={
            "detail": f"personal ({ident}) updated"
        }
    )


@personal_router.delete("/personal")
@inject
async def delete_personal(
    delete: FromDishka[DeletePersonalInteractor],
    ident: Annotated[UUID, Query()],
) -> ORJSONResponse: 

    await delete(ident)

    return ORJSONResponse(
        content={
            "detail": f"personal ({ident}) removed"
        }
    )
