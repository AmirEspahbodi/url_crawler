from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_DEBUG: bool
    HOST: str
    PORT: int
    BASE_URL: str
    DEFAULT_LOCALE: str
    ENVIRONMENT: str
    WORKER: int
    ORIGINS: list[str]
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


AppConfig = AppSettings()
