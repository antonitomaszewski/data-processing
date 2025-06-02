from typing import Literal

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


def get_project_metadata() -> dict[str, str]:
    return {
        "title": "Data Processing API",
        "description": "A FastAPI application for data processing tasks.",
        "version": "0.1.0",
    }


class Settings(BaseSettings):
    postgres_db: str = Field(default="app_db", env="POSTGRES_DB")
    postgres_user: str = Field(default="postgres", env="POSTGRES_USER")
    postgres_password: str = Field(default="postgres", env="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="db", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")

    database_url: PostgresDsn = Field(
        default=None,
        env="DATABASE_URL",
        example="postgresql://user:password@host:port/dbname",
    )

    environment: Literal["dev", "staging", "prod"] = Field(
        default="dev", env="ENVIRONMENT"
    )
    debug: bool = Field(default=False, env="DEBUG")
    secret_key: str = Field(
        default="26Xtncqvz3RiAr-to0LitviJQB1w3R40rV3laKSmRhI",
        env="SECRET_KEY",
        min_length=32,
    )

    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")
    app_reload: bool = Field(default=False, env="APP_RELOAD")

    @property
    def sync_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def async_database_url(self) -> str:
        return self.sync_database_url.replace(
            "postgresql://", "postgresql+asyncpg://"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
project_metadata = get_project_metadata()
