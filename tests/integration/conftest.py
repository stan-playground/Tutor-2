from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

from tutor_copilot.settings import Settings


@pytest.fixture
def database():
    settings = Settings(database_name=f"tc_test_{uuid4().hex}")
    admin = create_engine(Settings().database_url, isolation_level="AUTOCOMMIT")
    with admin.connect() as connection:
        connection.execute(text(f'CREATE DATABASE "{settings.database_name}"'))
    try:
        yield settings
    finally:
        with admin.connect() as connection:
            connection.execute(text(f'DROP DATABASE "{settings.database_name}" WITH (FORCE)'))
        admin.dispose()


def migrate(settings: Settings, revision: str = "head") -> None:
    engine = create_engine(settings.database_url)
    try:
        with engine.begin() as connection:
            config = Config("alembic.ini")
            config.attributes["connection"] = connection
            if revision == "base":
                command.downgrade(config, revision)
            else:
                command.upgrade(config, revision)
    finally:
        engine.dispose()
