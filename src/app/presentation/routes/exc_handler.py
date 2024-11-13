from fastapi import Request
from fastapi.responses import JSONResponse


async def personal_not_found_exception_handler(
    request: Request,
    exception: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "code": "personal_not_found",
            "detail": f"personal ({request.path_params["ident"]}) not found"
        }
    )


async def personal_naks_certification_not_found_exception_handler(
    request: Request,
    exception: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "code": "personal_naks_certification_not_found",
            "detail": f"personal naks certification ({request.path_params["ident"]}) not found"
        }
    )


async def ndt_not_found_exception_handler(
    request: Request,
    exception: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "code": "ndt_not_found",
            "detail": f"ndt ({request.path_params["ident"]}) not found"
        }
    )


async def acst_not_found_exception_handler(
    request: Request,
    exception: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "code": "acst_not_found",
            "detail": f"acst ({request.path_params["ident"]}) not found"
        }
    )
