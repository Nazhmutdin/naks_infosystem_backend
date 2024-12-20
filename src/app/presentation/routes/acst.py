from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse
from pydantic import RootModel
from dishka.integrations.fastapi import inject
from dishka import FromDishka

from app.application.interactors import (
    CreateAcstInteractor,
    GetAcstInteractor,
    SelectAcstInteractor,
    UpdateAcstInteractor,
    DeleteAcstInteractor,
    GetAcstHtmlInteractor
)
from app.application.dto import (
    CreateAcstDTO,
    UpdateAcstDTO,
    AcstDTO
)
from app.application.common.exc import AcstNotFoundException
from app.presentation.shemas import SelectResponse, AcstSelectShema


acst_router = APIRouter()


@acst_router.post("/acst")
@inject
async def create_acst(
    create: FromDishka[CreateAcstInteractor],
    data: CreateAcstDTO
) -> ORJSONResponse:

    await create(data)

    return ORJSONResponse(
        content={
            "detail": "acst created"
        }
    ) 


@acst_router.get("/acst/select")
@inject
async def select_acst(
    select: FromDishka[SelectAcstInteractor],
    filters: Annotated[AcstSelectShema, Query()]
) -> SelectResponse[AcstDTO]:

    res = await select(
        filters=filters.model_dump(exclude_unset=True, exclude_none=True),
        limit=filters.limit,
        offset=filters.offset
    )

    return {
        "result": res[0],
        "count": res[1]
    }


@acst_router.get("/acst/html")
@inject
async def get_acst_html(
    get: FromDishka[GetAcstHtmlInteractor],
    ident: Annotated[UUID, Query()],
) -> str:

    res = await get(ident)

    if res:
        return res
    
    raise AcstNotFoundException(ident)


@acst_router.get("/acst")
@inject
async def get_acst(
    get: FromDishka[GetAcstInteractor],
    ident: Annotated[UUID, Query()],
) -> AcstDTO:

    res = await get(ident)

    if res:
        return res
    
    raise AcstNotFoundException(ident)


@acst_router.patch("/acst")
@inject
async def update_acst(
    update: FromDishka[UpdateAcstInteractor],
    ident: Annotated[UUID, Query()], 
    data: RootModel[UpdateAcstDTO], 
) -> ORJSONResponse: 

    await update(ident, data.model_dump(exclude_unset=True))

    return ORJSONResponse(
        content={
            "detail": f"acst ({ident}) updated"
        }
    )


@acst_router.delete("/acst")
@inject
async def delete_acst(
    delete: FromDishka[DeleteAcstInteractor],
    ident: Annotated[UUID, Query()],
) -> ORJSONResponse: 

    await delete(ident)

    return ORJSONResponse(
        content={
            "detail": "acst ({ident}) removed"
        }
    ) 
