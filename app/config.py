from pydantic_settings import BaseSettings


def get_project_metadata() -> dict[str, str]:
    return {
        "title": "Data Processing API",
        "description": "A FastAPI application for data processing tasks.",
        "version": "0.1.0",
    }


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str
    environment: str
    debug: bool
    secret_key: str
    app_host: str
    app_port: int
    app_reload: bool

    class Config:
        env_file = ".env"


settings = Settings()
project_metadata = get_project_metadata()
