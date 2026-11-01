import asyncio
from uuid import UUID, uuid4

import pytest
from conftest import migrate
from fastapi import HTTPException
from sqlalchemy import create_engine, text

from tutor_copilot.db import create_engine as async_engine
from tutor_copilot.evidence import read_profile, save_profile, tenant_transaction
from tutor_copilot.schemas import ProfileWrite


def profile():
    return {
        "profile": {
            "alias": "Synthetic learner",
            "adult_confirmed": True,
            "learner_opt_in": True,
            "upload_permission": True,
            "assessment": {
                "summary": "Provisional estimate",
                "assessed_on": "2026-10-01",
                "source": "tutor_estimate",
                "level": "B1",
                "uncertainty": "provisional",
            },
            "goals": ["Work discussions"],
            "preferred_domains": ["Engineering"],
        }
    }


def test_profile_persistence_and_restricted_role(database):
    migrate(database)
    tutor, other = uuid4(), uuid4()

    async def exercise():
        engine = async_engine(database)
        try:
            async with tenant_transaction(engine, tutor) as connection:
                assert await connection.scalar(text("SELECT current_user")) == "tutor_app"
                result = await save_profile(
                    connection, tutor, ProfileWrite.model_validate(profile())
                )
                learner = UUID(result["id"])
            async with tenant_transaction(engine, other) as connection:
                assert await connection.scalar(text("SELECT count(*) FROM learners")) == 0
                with pytest.raises(HTTPException) as denied:
                    await read_profile(connection, learner, other)
                assert denied.value.status_code == 404
            async with engine.begin() as connection:
                assert await connection.scalar(text("SELECT count(*) FROM learners")) == 0
            async with tenant_transaction(engine, tutor) as connection:
                assert (await read_profile(connection, learner, tutor))["profile"][
                    "alias"
                ] == "Synthetic learner"
                updated = profile() | {"expected_revision": 1}
                updated["profile"]["alias"] = "Updated alias"
                assert (
                    await save_profile(
                        connection, tutor, ProfileWrite.model_validate(updated), learner
                    )
                )["revision"] == 2
            async with tenant_transaction(engine, tutor) as connection:
                with pytest.raises(HTTPException) as stale:
                    await save_profile(
                        connection, tutor, ProfileWrite.model_validate(profile()), learner
                    )
                assert stale.value.status_code == 409
        finally:
            await engine.dispose()

    asyncio.run(exercise())
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM profiles")) == 2
    finally:
        admin.dispose()
