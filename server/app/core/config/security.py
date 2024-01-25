import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecuritySettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


APP_KEY = os.getenv("APP_KEY")
SecurityConfig = SecuritySettings()
