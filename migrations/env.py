from alembic import context
from sqlalchemy import Connection, create_engine
from sqlalchemy.pool import NullPool

from tutor_copilot.settings import Settings


def run_migrations(connection: Connection) -> None:
    context.configure(connection=connection)
    with context.begin_transaction():
        context.run_migrations()


provided_connection = context.config.attributes.get("connection")
if provided_connection is not None:
    run_migrations(provided_connection)
else:
    with create_engine(Settings().database_url, poolclass=NullPool).connect() as connection:
        run_migrations(connection)
