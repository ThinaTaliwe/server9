"""Application configuration using Pydantic settings.

All sensitive values should be provided via environment variables or a `.env` file.
"""

import secrets

# BaseSettings has been moved to the `pydantic-settings` package in recent
# versions of Pydantic.  Attempt to import from there first for compatibility.
try:
    from pydantic_settings import BaseSettings  # type: ignore
except ImportError:  # pragma: no cover
    from pydantic import BaseSettings  # type: ignore

from pydantic import Field, AnyHttpUrl


class Settings(BaseSettings):
    # Database connection URL, e.g., ``mysql+pymysql://user:pass@host/db``
    database_url: str = Field(..., env="DATABASE_URL")

    # Secret key for sessions and JWT token signing
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32), env="SECRET_KEY")

    # Token expiry in minutes
    access_token_expire_minutes: int = Field(60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # External API configuration
    shipsgo_base_url: AnyHttpUrl = Field("https://api.shipsgo.com/v2", env="SHIPSGO_BASE_URL")
    shipsgo_token: str = Field(..., env="SHIPSGO_TOKEN")
    searate_base_url: AnyHttpUrl = Field("https://tracking.searates.com", env="SEARATE_BASE_URL")
    searate_api_key: str = Field(..., env="SEARATE_API_KEY")

    # CORS configuration
    cors_allow_origins: list[str] = Field(["*"], env="CORS_ALLOW_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()