"""Real HTTP/PostgreSQL intake; session seeding is separate from real OIDC tests."""

import asyncio
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from conftest import migrate
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError
from test_evidence import profile

from tutor_copilot.auth import COOKIE, ORIGIN, create_session
from tutor_copilot.db import create_engine as async_engine
from tutor_copilot.evidence import tenant_transaction
from tutor_copilot.web import create_app

FIRST = UUID("11111111-1111-4111-8111-111111111111")
SECOND = UUID("22222222-2222-4222-8222-222222222222")


@contextmanager
def authenticated(settings, tutor=FIRST):
    async def session():
        engine = async_engine(settings)
        try:
            return await create_session(engine, tutor_id=tutor)
        finally:
            await engine.dispose()

    token = asyncio.run(session())
    with TestClient(create_app(settings), base_url=ORIGIN) as client:
        client.cookies.set(COOKIE, token)
        me = client.get("/auth/me")
        assert me.status_code == 200
        client.headers["X-CSRF-Token"] = me.json()["csrf_token"]
        yield client


@pytest.fixture
def intake(database):
    migrate(database)
    with authenticated(database) as client:
        response = client.post("/learners", json=profile())
        assert response.status_code == 201
        yield client, response.json()["id"]


def source_payload(*, days=0, kind="lesson"):
    return {
        "id": str(uuid4()),
        "kind": kind,
        "occurred_at": (datetime.now(UTC) - timedelta(days=days)).isoformat(),
        "qualification": "tutor_notes",
        "raw_text": "PRIVATE_SYNTHETIC_SOURCE",
    }


def add_source(client, learner, **kwargs):
    source = source_payload(**kwargs)
    assert client.post(f"/learners/{learner}/sources", json=source).status_code == 200
    return source


def observation(source, **changes):
    return {
        "id": str(uuid4()),
        "source_id": source["id"],
        "response_ref": str(uuid4()),
        "subskill": "past-tense",
        "task": "controlled",
        "task_ref": "comparable-past-drill",
        "assistance": "independent",
        "confirmed": True,
        "accuracy": {"correct": 4, "opportunities": 5},
        **changes,
    }


def activity(source, **changes):
    return {
        "id": str(uuid4()),
        "source_id": source["id"],
        "activity_ref": str(uuid4()),
        "kind": "encounter",
        "occurred_at": None,
        "amount": None,
        "purpose": "Reading exposure",
        "task": "input",
        "task_ref": "reviewed-reading-v1",
        "assistance": "unknown",
        "confirmed": True,
        **changes,
    }


def test_sources_observations_replay_confirmation_and_correction(intake, database):
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner)
    assert client.post(base + "/sources", json=source).status_code == 200
    assert client.post(base + "/sources", json=source | {"raw_text": "changed"}).status_code == 409
    raw = client.get(base + f"/sources/{source['id']}").json()
    assert raw["raw_text"] == source["raw_text"] and raw["available"]
    item = observation(source, confirmed=False)
    saved = client.post(base + "/observations", json=item)
    assert saved.status_code == 200 and saved.json()["revision"] == 1
    assert client.get(base + "/context").json()["recent"]["groups"] == []
    assert client.get(base + "/evidence").json()["observations"][0]["data"]["confirmed"] is False
    confirmed = item | {"expected_revision": 1, "confirmed": True}
    assert client.post(base + "/observations", json=confirmed).json()["revision"] == 2
    assert client.post(base + "/observations", json=confirmed).json()["revision"] == 2
    duplicate = confirmed | {"id": str(uuid4()), "expected_revision": 0}
    assert client.post(base + "/observations", json=duplicate).status_code == 409
    assert client.post(base + "/observations", json=item).status_code == 409
    pending = confirmed | {
        "expected_revision": 2,
        "confirmed": False,
        "accuracy": {"correct": 1, "opportunities": 5},
    }
    assert client.post(base + "/observations", json=pending).json()["revision"] == 3
    groups = client.get(base + "/context").json()["recent"]["groups"]
    assert groups[0]["measures"]["accuracy"]["correct"] == 4
    corrected = pending | {"expected_revision": 3, "confirmed": True}
    assert client.post(base + "/observations", json=corrected).json()["revision"] == 4
    groups = client.get(base + "/context").json()["recent"]["groups"]
    assert groups[0]["measures"]["accuracy"]["correct"] == 1
    assert len(client.get(base + "/evidence?history=true").json()["observations"]) == 4
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM sources")) == 1
            assert connection.scalar(text("SELECT count(*) FROM observations")) == 4
    finally:
        admin.dispose()


def test_activity_independence_frozen_revisions_and_old_history(intake):
    client, learner = intake
    base = f"/learners/{learner}"
    recent = add_source(client, learner)
    observed = observation(recent)
    assert client.post(base + "/observations", json=observed).status_code == 200
    before = client.get(base + "/context").json()["recent"]
    old = add_source(client, learner, days=120, kind="actual_use")
    assigned = activity(
        old, kind="assignment", purpose="Past tense practice", subskill="past-tense"
    )
    encountered = activity(old, occurred_at=old["occurred_at"])
    pending = activity(old, confirmed=False)
    for item in (assigned, encountered, pending):
        assert client.post(base + "/activities", json=item).status_code == 200
    assert client.post(base + "/activities", json=encountered).json()["revision"] == 1
    assert (
        client.post(base + "/activities", json=encountered | {"id": str(uuid4())}).status_code
        == 409
    )
    context = client.get(base + "/context").json()
    assert context["recent"]["source_ids"] == before["source_ids"]
    assert context["recent"]["groups"] == before["groups"]
    assert sorted(row["data"]["kind"] for row in context["history"]) == ["assignment", "encounter"]
    assignment = next(row for row in context["history"] if row["data"]["kind"] == "assignment")
    assert assignment["data"]["occurred_at"] is None and assignment["data"]["amount"] is None
    assert len(client.get(base + "/evidence").json()["activities"]) == 3
    frozen = client.post(base + "/contexts", json={}).json()
    assert "PRIVATE_SYNTHETIC_SOURCE" not in str(frozen)
    corrected = encountered | {"expected_revision": 1, "amount": 2}
    assert client.post(base + "/activities", json=corrected).json()["revision"] == 2
    corrected_observation = observed | {
        "expected_revision": 1,
        "accuracy": {"correct": 2, "opportunities": 5},
    }
    assert client.post(base + "/observations", json=corrected_observation).status_code == 200
    prior = client.get(base + f"/contexts/{frozen['id']}").json()
    assert prior == frozen
    new = client.post(base + "/contexts", json={"subskills": ["past-tense"]}).json()["context"]
    assert len(new["history"]) == 1
    assert new["recent"]["groups"][0]["observation_refs"][0]["revision"] == 2
    checked = activity(
        recent, kind="checked_outcome", observation_id=observed["id"], observation_revision=2
    )
    assert client.post(base + "/activities", json=checked).status_code == 200
    assert len(client.get(base + "/evidence").json()["observations"]) == 1


def test_every_learner_operation_is_owned_and_csrf_protected(intake, database):
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner)
    frozen = client.post(base + "/contexts", json={}).json()
    with authenticated(database, SECOND) as other:
        operations = [
            ("GET", base, None),
            ("PUT", base, profile() | {"expected_revision": 1}),
            ("DELETE", base, None),
            ("POST", base + "/sources", source_payload()),
            ("GET", base + f"/sources/{source['id']}", None),
            ("POST", base + "/observations", observation(source)),
            ("POST", base + "/activities", activity(source)),
            ("GET", base + "/evidence", None),
            ("GET", base + "/context", None),
            ("POST", base + "/contexts", {}),
            ("GET", base + f"/contexts/{frozen['id']}", None),
        ]
        for method, path, body in operations:
            result = other.request(method, path, json=body)
            assert result.headers["Cache-Control"] == "no-store"
            assert result.status_code == 404, (method, path, result.status_code)
            assert "Synthetic learner" not in result.text
    del client.headers["X-CSRF-Token"]
    for path, body in [
        ("/learners", profile()),
        (base + "/sources", source_payload()),
        (base + "/observations", observation(source)),
        (base + "/activities", activity(source)),
        (base + "/contexts", {}),
    ]:
        assert client.post(path, json=body).status_code == 403
    assert client.put(base, json=profile()).status_code == 403
    assert client.delete(base).status_code == 403
    with TestClient(create_app(database), base_url=ORIGIN) as anonymous:
        assert anonymous.get(base).status_code == 401
        assert anonymous.post("/learners", json=profile()).status_code == 401


def test_persisted_recent_selection_rates_and_unknowns(intake):
    client, learner = intake
    base = f"/learners/{learner}"
    lesson_ids = []
    homework_ids = []
    for days in range(5):
        lesson = add_source(client, learner, days=days)
        homework = add_source(client, learner, days=days, kind="homework")
        lesson_ids.append(lesson["id"])
        homework_ids.append(homework["id"])
        for source, correct in ((lesson, 5 - days), (homework, days)):
            item = observation(source, accuracy={"correct": correct, "opportunities": 5})
            assert client.post(base + "/observations", json=item).status_code == 200
    old = add_source(client, learner, days=91)
    assert client.post(base + "/observations", json=observation(old)).status_code == 200
    zero = observation(
        {"id": lesson_ids[0]}, subskill="unknown-use", accuracy={"correct": 0, "opportunities": 0}
    )
    assert client.post(base + "/observations", json=zero).status_code == 200
    use = add_source(client, learner, kind="actual_use")
    assert client.post(base + "/observations", json=observation(use)).status_code == 422
    summary = client.get(base + "/context").json()["recent"]
    assert summary["source_ids"] == {"lesson": lesson_ids[:4], "homework": homework_ids[:4]}
    lessons = next(
        group
        for group in summary["groups"]
        if group["subskill"] == "past-tense" and group["evidence_type"] == "lesson"
    )
    homework = next(
        group
        for group in summary["groups"]
        if group["subskill"] == "past-tense" and group["evidence_type"] == "homework"
    )
    assert lessons["measures"]["accuracy"]["correct"] == 14
    assert lessons["measures"]["accuracy"]["opportunities"] == 20
    assert lessons["measures"]["accuracy"]["trend"] == "improving"
    assert homework["measures"]["accuracy"]["correct"] == 6
    assert homework["measures"]["accuracy"]["trend"] == "regressing"
    unknown = next(group for group in summary["groups"] if group["subskill"] == "unknown-use")
    assert unknown["measures"]["accuracy"]["rate"] is None
    assert unknown["measures"]["required_use"]["rate"] is None
    assert unknown["trend"] == "insufficient" and not unknown["maintenance_confirmed"]


@pytest.mark.parametrize("flag", ["adult_confirmed", "learner_opt_in", "upload_permission"])
def test_explicit_permission_required_before_learner_data_is_saved(intake, database, flag):
    client, _ = intake
    invalid = profile()
    invalid["profile"][flag] = False
    response = client.post("/learners", json=invalid)
    assert response.status_code == 422 and response.headers["Cache-Control"] == "no-store"
    invalid = profile()
    invalid["profile"]["birth_date"] = "1980-01-01"
    assert client.post("/learners", json=invalid).status_code == 422
    admin = create_engine(database.database_url)
    try:
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM learners")) == 1
    finally:
        admin.dispose()


def test_source_corrections_and_confirmed_withdrawals_preserve_frozen_context(intake, database):
    client, learner = intake
    base = f"/learners/{learner}"
    sources = [add_source(client, learner, days=days) for days in range(4)]
    item = observation(sources[0])
    fact = activity(sources[0])
    assert client.post(base + "/observations", json=item).status_code == 200
    assert client.post(base + "/activities", json=fact).status_code == 200
    frozen = client.post(base + "/contexts", json={}).json()
    source = sources[0]
    corrected = source | {"expected_revision": 1, "occurred_at": sources[2]["occurred_at"]}
    saved = client.post(base + "/sources", json=corrected)
    assert saved.status_code == 200 and saved.json()["revision"] == 2
    assert client.post(base + "/sources", json=corrected).json()["revision"] == 2
    current = client.get(base + "/context").json()
    assert len(current["recent"]["source_ids"]["lesson"]) == 4
    assert set(current["recent"]["source_ids"]["lesson"]) == {source["id"] for source in sources}
    assert client.get(base + f"/contexts/{frozen['id']}").json() == frozen
    old = client.get(base + f"/sources/{source['id']}?revision=1").json()
    assert datetime.fromisoformat(old["occurred_at"]) == datetime.fromisoformat(
        source["occurred_at"]
    )
    for suffix, record in (("observations", item), ("activities", fact)):
        withdrawn = record | {"expected_revision": 1, "withdrawn": True}
        assert client.post(base + f"/{suffix}", json=withdrawn).status_code == 200
    withdrawn = client.get(base + "/context").json()
    assert withdrawn["history"] == [] and withdrawn["recent"]["groups"] == []
    audit = client.get(base + "/evidence").json()
    assert audit["activities"][0]["data"]["withdrawn"] is True
    assert client.get(base + f"/contexts/{frozen['id']}").json() == frozen
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            assert connection.scalar(text("SELECT count(*) FROM sources")) == 4
            assert connection.scalar(text("SELECT count(*) FROM source_history")) == 1
            assert (
                connection.scalar(
                    text("""SELECT s.expires_at=h.expires_at FROM sources s
                JOIN source_history h ON h.source_id=s.id""")
                )
                is True
            )
            connection.execute(
                text("UPDATE source_history SET expires_at=now()-interval '1 second'")
            )
        expired_old = client.get(base + f"/contexts/{frozen['id']}").json()["context"]
        prior_source = next(row for row in expired_old["sources"] if row["id"] == source["id"])
        assert prior_source["revision"] == 1 and prior_source["available"] is False
        assert client.get(base + f"/sources/{source['id']}").json()["available"] is True
    finally:
        admin.dispose()


def test_qualitative_checked_outcomes_need_criteria_and_never_create_rates(intake):
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner, kind="actual_use")
    checked = activity(source, kind="checked_outcome", task="fluency", purpose="Sustained speaking")
    assert client.post(base + "/activities", json=checked).status_code == 422
    checked |= {"criterion_ref": "reviewed-fluency-rubric-v1", "outcome": "partially_met"}
    assert client.post(base + "/activities", json=checked).status_code == 200
    unknown = activity(
        source,
        kind="checked_outcome",
        task="project",
        purpose="Presentation",
        criterion_ref="reviewed-project-rubric-v1",
        outcome="unknown",
    )
    assert client.post(base + "/activities", json=unknown).status_code == 200
    assert (
        client.post(base + "/activities", json=activity(source, outcome="met")).status_code == 422
    )
    context = client.post(
        base + "/contexts", json={"purposes": ["Sustained speaking", "Presentation"]}
    ).json()["context"]
    assert context["recent"]["groups"] == []
    assert len(context["history"]) == 2
    assert {row["data"]["outcome"] for row in context["history"]} == {"partially_met", "unknown"}
    assert all(row["data"]["subskill"] is None for row in context["history"])


def test_all_child_tables_enforce_database_rls(intake, database):
    client, learner = intake
    base = f"/learners/{learner}"
    source = add_source(client, learner)
    assert client.post(base + "/observations", json=observation(source)).status_code == 200
    assert client.post(base + "/activities", json=activity(source)).status_code == 200
    assert (
        client.post(
            base + "/sources", json=source | {"expected_revision": 1, "occurred_at": None}
        ).status_code
        == 200
    )
    assert client.post(base + "/contexts", json={}).status_code == 201
    tables = (
        "learners",
        "profiles",
        "sources",
        "source_history",
        "observations",
        "activities",
        "contexts",
    )

    async def exercise():
        engine = async_engine(database)
        try:
            async with tenant_transaction(engine, FIRST) as connection:
                for table in tables:
                    assert await connection.scalar(text(f"SELECT count(*) FROM {table}")) > 0
            async with tenant_transaction(engine, SECOND) as connection:
                for table in tables:
                    assert await connection.scalar(text(f"SELECT count(*) FROM {table}")) == 0
            async with engine.begin() as connection:
                for table in tables:
                    assert await connection.scalar(text(f"SELECT count(*) FROM {table}")) == 0
            with pytest.raises(DBAPIError) as denied:
                async with tenant_transaction(engine, SECOND) as connection:
                    await connection.execute(
                        text("""INSERT INTO profiles
                        (learner_id,tutor_id,revision,data) VALUES (:learner,:tutor,99,'{}')"""),
                        {"learner": UUID(learner), "tutor": SECOND},
                    )
            assert denied.value.orig.sqlstate == "42501"
        finally:
            await engine.dispose()

    asyncio.run(exercise())


def test_commit_failure_never_returns_http_success(intake, database, capsys):
    client, _ = intake
    admin = create_engine(database.database_url)
    try:
        with admin.begin() as connection:
            connection.execute(
                text("""CREATE FUNCTION reject_profile_commit() RETURNS trigger
                LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'PRIVATE_COMMIT_FAILURE'; END $$;
                CREATE CONSTRAINT TRIGGER reject_profile_commit AFTER INSERT ON profiles
                DEFERRABLE INITIALLY DEFERRED FOR EACH ROW
                EXECUTE FUNCTION reject_profile_commit();""")
            )
        response = client.post("/learners", json=profile())
        assert response.status_code == 500 and response.json() == {"status": "error"}
        assert response.headers["Cache-Control"] == "no-store"
        with admin.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM learners")) == 1
            assert connection.scalar(text("SELECT count(*) FROM profiles")) == 1
        captured = capsys.readouterr()
        assert "PRIVATE" not in captured.out + captured.err + response.text
    finally:
        admin.dispose()
