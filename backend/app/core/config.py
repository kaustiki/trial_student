from functools import cached_property
from pathlib import Path

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",
        env_file_encoding="utf-8",
    )

    DB_URL: AnyUrl
    APP_NAME: str = "Student Care Referral System API"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    # Allow browser requests from the Vite frontend.
    BACKEND_CORS_ORIGINS: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173"
    )
    SECRET_KEY: str = "change-me-before-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
    # Legacy env values are kept so older local .env files still load.
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    CSRF_COOKIE_NAME: str = "csrf_token"
    CSRF_HEADER_NAME: str = "X-CSRF-Token"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    '''
    @property and @cached_property let you call a method like it is a normal variable.
    @property         = calculate every time you read it
    @cached_property = calculate once, remember forever
    '''
    @property
    def DATABASE_URL(self) -> str:
        return str(self.DB_URL)

    @cached_property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.BACKEND_CORS_ORIGINS.split(",")
            if origin.strip()
        ]


settings = Settings()
