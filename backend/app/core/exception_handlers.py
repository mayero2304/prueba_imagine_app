import logging
from typing import Any
from datetime import UTC, datetime
from http import HTTPStatus

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.services.exceptions import ConflictError, DomainError, NotFoundError

logger = logging.getLogger(__name__)


def resolve_domain_status(error: DomainError) -> int:
    if isinstance(error, NotFoundError):
        return status.HTTP_404_NOT_FOUND

    if isinstance(error, ConflictError):
        return status.HTTP_409_CONFLICT

    return status.HTTP_400_BAD_REQUEST


def resolve_error_phrase(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Request Error"


def build_error_response(
    *,
    request: Request,
    status_code: int,
    message: Any,
    error: str | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({
            "statusCode": status_code,
            "error": error or resolve_error_phrase(status_code),
            "message": message,
            "path": request.url.path,
            "timestamp": datetime.now(UTC).isoformat(),
        }),
    )


async def domain_error_handler(request: Request, error: DomainError) -> JSONResponse:
    status_code = resolve_domain_status(error)

    return build_error_response(
        request=request,
        status_code=status_code,
        message=str(error),
    )


async def validation_error_handler(
    request: Request,
    error: RequestValidationError,
) -> JSONResponse:
    return build_error_response(
        request=request,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=error.errors(),
    )


async def http_exception_handler(
    request: Request,
    error: StarletteHTTPException,
) -> JSONResponse:
    return build_error_response(
        request=request,
        status_code=error.status_code,
        message=error.detail,
    )


async def unhandled_error_handler(
    request: Request,
    error: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled error while processing %s %s",
        request.method,
        request.url.path,
    )

    return build_error_response(
        request=request,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Internal Server Error",
    )
