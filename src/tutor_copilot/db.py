from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from tutor_copilot.settings import Settings


def create_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        settings.database_url,
        pool_size=5,
        max_overflow=0,
        pool_timeout=3,
        pool_pre_ping=True,
        hide_parameters=True,
        connect_args={"connect_timeout": 3, "options": "-c statement_timeout=3000"},
    )
