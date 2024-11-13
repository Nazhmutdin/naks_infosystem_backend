from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from app.presentation.routes.personal import personal_router
from app.presentation.routes.personal_naks_certification import personal_naks_certification_router
from app.presentation.routes.ndt import ndt_router
from app.presentation.routes.acst import acst_router
from app.presentation.routes.exc_handler import (
    personal_not_found_exception_handler,
    personal_naks_certification_not_found_exception_handler,
    ndt_not_found_exception_handler,
    acst_not_found_exception_handler
)
from app.application.common.exc import (
    PersonalNotFoundException,
    PersonalNaksCertificationNotFoundException,
    NdtNotFoundException,
    AcstNotFoundException
)
from app.main.dependencies.ioc_container import container


app = FastAPI()

setup_dishka(container=container, app=app)

app.include_router(ndt_router, prefix="/v1")
app.include_router(personal_router, prefix="/v1")
app.include_router(personal_naks_certification_router, prefix="/v1")
app.include_router(acst_router, prefix="/v1")

app.add_exception_handler(PersonalNotFoundException, personal_not_found_exception_handler)
app.add_exception_handler(PersonalNaksCertificationNotFoundException, personal_naks_certification_not_found_exception_handler)
app.add_exception_handler(NdtNotFoundException, ndt_not_found_exception_handler)
app.add_exception_handler(AcstNotFoundException, acst_not_found_exception_handler)
