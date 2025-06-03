from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "app_db"
    database_url: str = "postgresql://postgres:postgres@db:5432/app_db"
    environment: str = "development"
    debug: bool = True
    secret_key: str = "26Xtncqvz3RiAr-to0LitviJQB1w3R40rV3laKSmRhI"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_reload: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
