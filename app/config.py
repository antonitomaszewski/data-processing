from pydantic_settings import BaseSettings


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
