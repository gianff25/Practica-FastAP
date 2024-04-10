import os
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Setting the base directory for the project
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Project Configuration
    PROJECT_NAME: str
    PROJECT_CODENAME: str
    PROJECT_VERSION: str = "0.1.0"

    # Deploy Specific Configuration
    DEBUG: bool
    TESTING: str
    URL_PREFIX: str
    ALLOWED_CORS: str
    SECRET_KEY: str

    # PostgreSQL Database Configuration
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_APPNAME: str
    ECHO_SQL: bool = False
    SQLALCHEMY_DATABASE_URL: Optional[str] = None

    # Generated URI from the configuration values
    @model_validator(mode="after")
    def validate_sqlalchemy_database_url(self):
        self.SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Authentication settings
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl="auth/token", scheme_name="JWT"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_EXPIRE_DAYS: int


settings = Settings()
