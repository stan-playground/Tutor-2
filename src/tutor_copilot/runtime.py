import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from redis.asyncio import Redis
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine

from tutor_copilot.db import create_engine
from tutor_copilot.settings import Settings

SCHEMA_REVISION = "0001"


@dataclass
class Resources:
    database: AsyncEngine
    cache: Redis


@asynccontextmanager
async def open_resources(settings: Settings) -> AsyncIterator[Resources]:
    database = create_engine(settings)
    cache = Redis.from_url(
        settings.redis_url,
        socket_connect_timeout=2,
        socket_timeout=2,
        max_connections=5,
        decode_responses=True,
    )
    try:
        yield Resources(database, cache)
    finally:
        try:
            await cache.aclose()
        finally:
            await database.dispose()


async def database_ready(database: AsyncEngine) -> bool:
    try:
        async with asyncio.timeout(4), database.connect() as connection:
            revision = await connection.scalar(text("SELECT version_num FROM alembic_version"))
            vector = await connection.scalar(
                text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')")
            )
            return revision == SCHEMA_REVISION and bool(vector)
    except (SQLAlchemyError, TimeoutError):
        return False


async def cache_ready(cache: Redis) -> bool:
    try:
        async with asyncio.timeout(3):
            return bool(await cache.ping())
    except (RedisError, TimeoutError):
        return False


async def readiness(resources: Resources) -> tuple[bool, bool]:
    database, cache = await asyncio.gather(
        database_ready(resources.database), cache_ready(resources.cache)
    )
    return database, cache
