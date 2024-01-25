from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncAttrs,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config.database import PostgresConfig

# Generate Database URL
DATABASE_URL = f"postgresql+asyncpg://{PostgresConfig.DATABASE_USERNAME}:{PostgresConfig.DATABASE_PASSWORD}@{PostgresConfig.DATABASE_HOSTNAME}:{PostgresConfig.DATABASE_PORT}/{PostgresConfig.DATABASE_NAME}"

# Create Database Engine
engine = create_async_engine(
    DATABASE_URL,
    echo=PostgresConfig.DATABASE_DEBUG_MODE,
    future=True,
    pool_size=PostgresConfig.POOL_SIZE,
    max_overflow=PostgresConfig.MAX_OVERFLOW,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def connection():
    async with async_session() as session:
        yield session

class Base(AsyncAttrs, DeclarativeBase):
    pass
