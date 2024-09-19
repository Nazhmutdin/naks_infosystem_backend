from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.routes import v1_router
from src.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router, prefix="/v1")
