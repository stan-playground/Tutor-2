"""Remove expired data from the fixed, synthetic local database."""

import asyncio
import json

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from tutor_copilot.settings import Settings


async def cleanup(connection: AsyncConnection) -> dict[str, int]:
    # The maintenance account intentionally sees all tenants; request code never uses it.
    expired = await connection.execute(
        text("""UPDATE sources SET raw_text=NULL
        WHERE expires_at <= now() AND raw_text IS NOT NULL RETURNING id""")
    )
    expired_history = await connection.execute(
        text("""UPDATE source_history SET raw_text=NULL
        WHERE expires_at <= now() AND raw_text IS NOT NULL RETURNING source_id""")
    )
    inactive = await connection.execute(
        text("""DELETE FROM learners
        WHERE last_active <= now() - interval '12 months' RETURNING id""")
    )
    await connection.execute(text("DELETE FROM auth_sessions WHERE expires_at <= now()"))
    return {
        "expired_sources": len(expired.all()) + len(expired_history.all()),
        "inactive_learners": len(inactive.all()),
    }


async def run_cleanup() -> None:
    engine = create_async_engine(Settings().database_url, hide_parameters=True)
    try:
        async with engine.begin() as connection:
            counts = await cleanup(connection)
        print(json.dumps(counts))
    finally:
        await engine.dispose()


def main() -> None:
    asyncio.run(run_cleanup())
