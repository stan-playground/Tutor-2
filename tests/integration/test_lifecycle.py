import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from uuid import UUID

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from test_intake import activity, add_source, intake, observation

from tutor_copilot.lifecycle import cleanup
from tutor_copilot.telemetry import configure_logging

# Import the real intake fixture; these checks use the same HTTP/PostgreSQL boundary.
__all__ = ["intake"]


def test_raw_expiry_unavailable_provenance_and_physical_cleanup(intake, database):
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner, days=120, kind="actual_use")
    assert client.post(base + "/activities", json=activity(source)).status_code == 200
    frozen = client.post(base + "/contexts", json={}).json()
    corrected = source | {"expected_revision": 1, "occurred_at": None}
    assert client.post(base + "/sources", json=corrected).json()["revision"] == 2
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(text("UPDATE sources SET expires_at=now()-interval '1 second'"))
            connection.execute(
                text("UPDATE source_history SET expires_at=now()-interval '1 second'")
            )
        expired_response = client.get(base + f"/sources/{source['id']}")
        assert expired_response.headers["Cache-Control"] == "no-store"
        expired = expired_response.json()
        assert expired["raw_text"] is None and expired["available"] is False
        reread_response = client.get(base + f"/contexts/{frozen['id']}")
        assert reread_response.headers["Cache-Control"] == "no-store"
        reread = reread_response.json()
        assert reread["context"]["sources"][0]["available"] is False
        assert reread["context"]["history"] == frozen["context"]["history"]
        assert "PRIVATE_SYNTHETIC_SOURCE" not in str(reread)
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT raw_text FROM sources")) == source["raw_text"]

        async def purge():
            engine = create_async_engine(database.database_url, hide_parameters=True)
            try:
                async with engine.begin() as connection:
                    return await cleanup(connection)
            finally:
                await engine.dispose()

        assert asyncio.run(purge()) == {"expired_sources": 2, "inactive_learners": 0}
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT raw_text FROM sources")) is None
            assert connection.scalar(text("SELECT raw_text FROM source_history")) is None
            assert connection.scalar(text("SELECT count(*) FROM activities")) == 1
            assert connection.scalar(text("SELECT count(*) FROM contexts")) == 1
        assert asyncio.run(purge()) == {"expired_sources": 0, "inactive_learners": 0}
    finally:
        admin.dispose()


@pytest.mark.parametrize("inactive", [False, True])
def test_deletion_and_inactivity_remove_all_implemented_stores(intake, database, inactive):
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner)
    assert client.post(base + "/observations", json=observation(source)).status_code == 200
    assert client.post(base + "/activities", json=activity(source)).status_code == 200
    assert client.post(base + "/contexts", json={}).status_code == 201
    admin = create_engine(database.database_url)
    try:
        if inactive:
            with admin.begin() as connection:
                connection.execute(
                    text("UPDATE learners SET last_active=now()-interval '12 months'")
                )
            assert client.get(base).status_code == 404
            assert client.post(base + "/activities", json=activity(source)).status_code == 404

            async def purge():
                engine = create_async_engine(database.database_url, hide_parameters=True)
                try:
                    async with engine.begin() as connection:
                        return await cleanup(connection)
                finally:
                    await engine.dispose()

            assert asyncio.run(purge())["inactive_learners"] == 1
        else:
            assert client.delete(base).status_code == 200
        assert client.get(base).status_code == 404
        assert client.post(base + "/sources", json=source).status_code == 404
        with admin.connect() as connection:
            for table in (
                "learners",
                "profiles",
                "sources",
                "source_history",
                "observations",
                "activities",
                "contexts",
            ):
                assert connection.scalar(text(f"SELECT count(*) FROM {table}")) == 0
    finally:
        admin.dispose()


def test_reads_do_not_extend_inactivity_and_delete_fences_waiting_write(intake, database):
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner)
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            before = connection.scalar(text("SELECT last_active FROM learners"))
        assert client.get(base).status_code == 200
        assert client.get(base + "/context").status_code == 200
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT last_active FROM learners")) == before
        started = Event()

        def waiting_write():
            started.set()
            return client.post(base + "/activities", json=activity(source))

        with admin.begin() as deletion:
            deletion.execute(
                text("SELECT id FROM learners WHERE id=:id FOR UPDATE"), {"id": UUID(learner)}
            )
            with ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(waiting_write)
                assert started.wait(2)
                # Confirm the actual PostgreSQL write is waiting on the learner lock.
                for _ in range(100):
                    with admin.connect() as observer:
                        waiting = observer.scalar(
                            text("""SELECT count(*) FROM pg_stat_activity
                            WHERE datname=current_database() AND usename='tutor_app'
                            AND wait_event_type='Lock'""")
                        )
                    if waiting:
                        break
                    Event().wait(0.01)
                assert waiting, "The concurrent operation did not reach the database lock"
                deletion.execute(text("DELETE FROM learners WHERE id=:id"), {"id": UUID(learner)})
                deletion.commit()
                assert future.result(timeout=5).status_code == 404
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM activities")) == 0
    finally:
        admin.dispose()


def test_private_inputs_validation_and_database_failures_never_enter_logs(intake, database, capsys):
    configure_logging()
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner)
    bad = observation(source, accuracy={"correct": 8, "opportunities": 5})
    bad["subskill"] = "PRIVATE_VALIDATION_SENTINEL"
    rejected = client.post(base + "/observations", json=bad)
    assert rejected.status_code == 422
    assert "PRIVATE" not in rejected.text
    # A globally reused UUID hidden by RLS reaches the database uniqueness boundary.
    from test_intake import SECOND, authenticated

    with authenticated(database, SECOND) as other:
        from test_evidence import profile

        other_learner = other.post("/learners", json=profile()).json()["id"]
        conflict = other.post(f"/learners/{other_learner}/sources", json=source)
        assert conflict.status_code == 409
        assert "PRIVATE" not in conflict.text
    logging.getLogger("sqlalchemy.engine").error("PRIVATE_SQL_EXCEPTION")
    captured = capsys.readouterr()
    assert "PRIVATE" not in captured.out + captured.err


def test_owner_can_delete_inactive_learner_without_restoring_access(intake, database):
    client, learner = intake
    source = add_source(client, learner)
    assert client.post(f"/learners/{learner}/activities", json=activity(source)).status_code == 200
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(text("UPDATE learners SET last_active=now()-interval '12 months'"))
        assert client.get(f"/learners/{learner}").status_code == 404
        response = client.delete(f"/learners/{learner}")
        assert response.status_code == 200 and response.headers["Cache-Control"] == "no-store"
        with admin.connect() as connection:
            for table in ("learners", "profiles", "sources", "activities"):
                assert connection.scalar(text(f"SELECT count(*) FROM {table}")) == 0
    finally:
        admin.dispose()
