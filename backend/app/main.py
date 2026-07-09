from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.controllers.customer_controller import router as customer_router
from app.controllers.health_controller import router as health_router
from app.controllers.ticket_controller import router as ticket_router
from app.core.config import settings
from app.core.database import init_db
from app.core.exception_handlers import (
    domain_error_handler,
    http_exception_handler,
    unhandled_error_handler,
    validation_error_handler,
)
from app.services.exceptions import DomainError


def create_app(init_database: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        if init_database:
            init_db()

        yield

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    origins = [
        origin.strip()
        for origin in settings.backend_cors_origins.split(",")
        if origin.strip()
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)

    app.include_router(health_router)
    app.include_router(customer_router, prefix=settings.api_prefix)
    app.include_router(ticket_router, prefix=settings.api_prefix)

    return app


app = create_app()
