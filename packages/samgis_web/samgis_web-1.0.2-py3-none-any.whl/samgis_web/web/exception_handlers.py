from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from samgis_core import app_logger


def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    app_logger.error(f"exception errors: {exc.errors()}.")
    app_logger.error(f"exception body: {exc.body}.")
    headers = request.headers.items()
    app_logger.error(f'request header: {dict(headers)}.')
    params = request.query_params.items()
    app_logger.error(f'request query params: {dict(params)}.')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"msg": "Error - Unprocessable Entity"}
    )


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    app_logger.error(f"exception: {str(exc)}.")
    headers = request.headers.items()
    app_logger.error(f'request header: {dict(headers)}.')
    params = request.query_params.items()
    app_logger.error(f'request query params: {dict(params)}.')
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"msg": "Error - Internal Server Error"}
    )
