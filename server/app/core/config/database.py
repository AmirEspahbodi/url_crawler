from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_DEBUG_MODE: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


PostgresConfig = PostgresSettings()
RedisConfig = RedisSettings()
