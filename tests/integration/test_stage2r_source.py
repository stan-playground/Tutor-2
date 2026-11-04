"""Source-correction behavior against the real intake and PostgreSQL boundary."""

import asyncio
import hashlib
import json
from datetime import UTC

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from test_intake import add_source, observation
from test_intake import intake as intake

from tutor_copilot.lifecycle import cleanup
from tutor_copilot.schemas import Source


def test_source_body_omission_clear_replacement_and_replay(intake, database):
    client, learner = intake
    base = f"/learners/{learner}/sources"
    source = add_source(client, learner)
    assert (
        client.post(f"/learners/{learner}/observations", json=observation(source)).status_code
        == 200
    )
    frozen = client.post(f"/learners/{learner}/contexts", json={}).json()
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            original_expiry = connection.scalar(text("SELECT expires_at FROM sources"))

        omitted = {key: value for key, value in source.items() if key != "raw_text"}
        omitted |= {"expected_revision": 1, "qualification": "transcript"}
        saved = client.post(base, json=omitted)
        assert saved.status_code == 200 and saved.json()["revision"] == 2
        assert client.post(base, json=omitted).json()["revision"] == 2
        assert client.get(f"{base}/{source['id']}").json()["raw_text"] == source["raw_text"]
        assert client.get(f"/learners/{learner}/contexts/{frozen['id']}").json() == frozen
        with admin.connect() as connection:
            rows = connection.execute(
                text("""SELECT revision,raw_text,expires_at FROM sources
                        UNION ALL SELECT revision,raw_text,expires_at FROM source_history
                        ORDER BY revision""")
            ).all()
        assert [(r.revision, r.raw_text, r.expires_at) for r in rows] == [
            (1, source["raw_text"], original_expiry),
            (2, source["raw_text"], original_expiry),
        ]

        clear = omitted | {"expected_revision": 2, "raw_text": None}
        assert client.post(base, json=clear).json()["revision"] == 3
        assert client.post(base, json=clear).json()["revision"] == 3
        assert client.post(base, json=omitted | {"expected_revision": 2}).status_code == 409
        assert client.get(f"{base}/{source['id']}").json()["raw_text"] is None
        assert (
            client.get(f"{base}/{source['id']}?revision=2").json()["raw_text"] == source["raw_text"]
        )

        replacement = clear | {"expected_revision": 3, "raw_text": "REPLACEMENT_SYNTHETIC"}
        assert client.post(base, json=replacement).json()["revision"] == 4
        assert client.post(base, json=replacement).json()["revision"] == 4
        assert client.get(f"{base}/{source['id']}").json()["raw_text"] == "REPLACEMENT_SYNTHETIC"
        with admin.begin() as connection:
            rows = connection.execute(
                text("""SELECT revision,raw_text,expires_at FROM sources
                        UNION ALL SELECT revision,raw_text,expires_at FROM source_history
                        ORDER BY revision""")
            ).all()
            assert [(r.revision, r.raw_text, r.expires_at) for r in rows[:2]] == [
                (1, source["raw_text"], original_expiry),
                (2, source["raw_text"], original_expiry),
            ]
            assert rows[3].expires_at >= original_expiry
            connection.execute(text("UPDATE sources SET expires_at=now()-interval '1 second'"))
            connection.execute(
                text("UPDATE source_history SET expires_at=now()-interval '1 second'")
            )

        async def run_cleanup():
            engine = create_async_engine(database.database_url)
            try:
                async with engine.begin() as connection:
                    return await cleanup(connection)
            finally:
                await engine.dispose()

        assert asyncio.run(run_cleanup())["expired_sources"] == 3
        with admin.connect() as connection:
            assert (
                connection.scalar(text("SELECT count(*) FROM sources WHERE raw_text IS NOT NULL"))
                == 0
            )
            assert (
                connection.scalar(
                    text("SELECT count(*) FROM source_history WHERE raw_text IS NOT NULL")
                )
                == 0
            )
            assert connection.scalar(text("SELECT count(*) FROM observations")) == 1
        expired = client.get(f"/learners/{learner}/contexts/{frozen['id']}").json()
        assert expired["context"]["sources"][0]["available"] is False
    finally:
        admin.dispose()


def test_ambiguous_legacy_body_retry_does_not_mutate(intake, database):
    client, learner = intake
    base = f"/learners/{learner}/sources"
    source = add_source(client, learner)
    omitted = {key: value for key, value in source.items() if key != "raw_text"}
    omitted |= {"expected_revision": 1, "qualification": "transcript"}
    legacy = Source.model_validate(omitted)
    content = legacy.model_dump(mode="json", exclude={"id", "expected_revision"})
    content["occurred_at"] = legacy.occurred_at.astimezone(UTC).isoformat()
    fingerprint = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(
                text("""INSERT INTO source_history
                (source_id,learner_id,tutor_id,revision,kind,occurred_at,qualification,
                 raw_text,expires_at,fingerprint)
                SELECT id,learner_id,tutor_id,revision,kind,occurred_at,qualification,
                       raw_text,expires_at,fingerprint
                FROM sources""")
            )
            connection.execute(
                text(
                    "UPDATE sources SET revision=2,qualification='transcript',"
                    "raw_text=NULL,fingerprint=:fingerprint"
                ),
                {"fingerprint": fingerprint},
            )
        assert client.post(base, json=omitted).status_code == 409
        assert client.post(base, json=omitted | {"raw_text": None}).status_code == 409
        current = client.get(f"{base}/{source['id']}").json()
        assert current["revision"] == 2 and current["raw_text"] is None
        assert (
            client.get(f"{base}/{source['id']}?revision=1").json()["raw_text"] == source["raw_text"]
        )
        correction = omitted | {"expected_revision": 2}
        assert client.post(base, json=correction).json()["revision"] == 3
        assert client.get(f"{base}/{source['id']}").json()["raw_text"] is None
    finally:
        admin.dispose()


def test_unambiguous_legacy_body_retry_is_accepted(intake, database):
    client, learner = intake
    base = f"/learners/{learner}/sources"
    source = add_source(client, learner)
    legacy = Source.model_validate(source)
    content = legacy.model_dump(mode="json", exclude={"id", "expected_revision"})
    content["occurred_at"] = legacy.occurred_at.astimezone(UTC).isoformat()
    fingerprint = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(
                text("UPDATE sources SET fingerprint=:fingerprint"), {"fingerprint": fingerprint}
            )
        assert client.post(base, json=source).json()["revision"] == 1
    finally:
        admin.dispose()
