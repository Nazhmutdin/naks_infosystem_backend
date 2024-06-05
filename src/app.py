from fastapi import FastAPI

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.routes import v1_router
from api.auth.routes import auth_router
from middlewares import CheckAccessTokenMiddleware
from database import get_session


app = FastAPI()

app.include_router(v1_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/auth")

app.add_middleware(CheckAccessTokenMiddleware)
