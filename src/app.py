from fastapi import FastAPI

from src.api.v1.routes import v1_router
from src.api.auth.routes import auth_router
from src.middlewares import CheckAccessTokenMiddleware


app = FastAPI()

app.include_router(v1_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/auth")

app.add_middleware(CheckAccessTokenMiddleware)
