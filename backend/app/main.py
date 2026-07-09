from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.health_controller import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

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

    app.include_router(health_router)

    return app


app = create_app()
