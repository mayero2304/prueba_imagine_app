from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Imagine Support API"
    app_env: str = "local"
    api_prefix: str = "/api"
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/imagine_support"
    )
    backend_cors_origins: str = "http://localhost:5173"
    mongo_audit_enabled: bool = False
    mongo_url: str = "mongodb://localhost:27017"
    mongo_database: str = "imagine_support_audit"
    mongo_audit_collection: str = "ticket_events"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
