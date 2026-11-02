"""Real local-model, HTTP, pgvector and disposable-Redis retrieval boundaries."""

import asyncio
import copy
import hashlib
import json
from uuid import UUID, uuid4

import pytest
from conftest import migrate
from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy import create_engine as admin_engine
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from test_evidence import profile
from test_intake import FIRST, SECOND, authenticated
from test_materials import material

from tutor_copilot.db import create_engine
from tutor_copilot.embeddings import CONFIG_REVISION, DIMENSIONS, LocalEmbeddings
from tutor_copilot.evidence import tenant_transaction
from tutor_copilot.retrieval import Objective, build_search


@pytest.fixture
def bank(database):
    migrate(database)
    with authenticated(database) as client:
        yield client


def add_material(client, data=None):
    identity = str(uuid4())
    response = client.post(
        "/teaching-assets", json={"id": identity, "material": data or material()}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"id": identity, "revision": 1}
    return identity


def objective(target=None, **changes):
    return {
        **(target or material()["target"]),
        "objective_ref": str(uuid4()),
        "use_cache": False,
        **changes,
    }


def search(client, data):
    response = client.post("/teaching-search", json=data)
    assert response.status_code == 200, response.text
    return response.json()


def clone_version(settings, source, data, *, owner=FIRST):
    """Operator fixture keeps the genuine indexed vector and changes eligibility only."""
    identity = str(uuid4())
    engine = admin_engine(settings.database_url)
    try:
        with engine.begin() as connection:
            connection.execute(
                text("""INSERT INTO teaching_asset_owners(id,tutor_id,sharing_permission_ref)
                    VALUES (:id,:owner,:permission)"""),
                {
                    "id": UUID(identity),
                    "owner": owner,
                    "permission": "synthetic-separate-sharing-permission"
                    if owner is None
                    else None,
                },
            )
            connection.execute(
                text("""INSERT INTO teaching_assets
                    (id,revision,data,reviewed_by,embedding,embedding_revision)
                    SELECT :id,1,data || CAST(:data AS jsonb),reviewed_by,embedding,
                        embedding_revision FROM teaching_assets WHERE id=:source AND revision=1"""),
                {
                    "id": UUID(identity),
                    "source": UUID(source),
                    "data": json.dumps(data),
                },
            )
    finally:
        engine.dispose()
    return identity


def test_exact_confusion_hard_filters_and_preferred_domain(bank, database):
    suitable = material()
    suitable["target"]["domain"] = "general"
    eligible = add_material(bank, suitable)
    wrong_confusion = material()
    wrong_confusion["target"] |= {
        "confusion": "definite_vs_indefinite_article",
        "skills": ["articles"],
    }
    add_material(bank, wrong_confusion)
    for field, value in (
        ("level", "B2"),
        ("task", "recognition"),
        ("modality", "speech"),
        ("response_type", "free_response"),
        ("skills", ["articles"]),
    ):
        distractor = material()
        distractor["target"][field] = value
        clone_version(database, eligible, distractor)
    request = objective(domain="project_updates", limit=10)
    result = search(bank, request)
    assert [str(row["id"]) for row in result["candidates"]] == [eligible]
    candidate = result["candidates"][0]
    assert candidate["revision"] == 1 and candidate["reviewed_by"] == str(FIRST)
    assert candidate["data"]["source_ref"] == suitable["source_ref"]
    assert candidate["data"]["source_version"] == "1"
    assert candidate["distance"] is not None
    assert search(bank, request | {"domain_required": True})["status"] == "gap"
    preferred = add_material(bank)
    assert search(bank, request)["candidates"][0]["id"] == preferred
    assert [
        row["id"] for row in search(bank, request | {"domain_required": True})["candidates"]
    ] == [preferred]
    assert search(bank, request | {"kinds": ["explanation"]})["status"] == "gap"
    explanation = add_material(bank, material(kind="explanation"))
    assert [
        row["id"] for row in search(bank, request | {"kinds": ["explanation"]})["candidates"]
    ] == [explanation]


@pytest.mark.parametrize(
    ("route", "outcome", "task", "modality", "response", "skill"),
    [
        ("reading", "main_points", "input", "text", "summary", "reading"),
        ("listening", "main_points", "input", "audio", "summary", "listening"),
        ("vocabulary", "vocabulary_use", "controlled", "text", "free_response", "vocabulary"),
        ("fluency", "sustained_speech", "fluency", "speech", "performance", "fluency"),
        ("discourse", "organized_report", "discourse", "text", "free_response", "discourse"),
        ("strategy", "communication_repair", "strategy", "speech", "performance", "strategy"),
        ("project", "completed_project", "project", "mixed", "project", "task_completion"),
    ],
)
def test_goal_led_routes_need_no_error(
    bank, database, route, outcome, task, modality, response, skill
):
    data = material(kind="framework" if route == "project" else "input", answer_key=None)
    data["target"] |= {
        "route": route,
        "outcome": outcome,
        "task": task,
        "modality": modality,
        "response_type": response,
        "skills": [skill],
        "confusion": None,
    }
    data["support"] = ["glossary"]
    data["prerequisites"] = ["vocabulary"]
    if route == "listening":
        data["recording"] = {
            "reference": "synthetic-recording:local-listening",
            "version": "audio-1",
            "available": True,
            "permitted": True,
            "criteria_recording_version": "audio-1",
        }
    identity = add_material(bank, data)
    clone_version(database, identity, material())
    request = objective(
        data["target"], required_support=["glossary"], known_prerequisites=["vocabulary"]
    )
    result = search(bank, request)
    assert result["status"] == "candidates"
    assert [row["id"] for row in result["candidates"]] == [identity]
    assert result["candidates"][0]["data"]["target"]["confusion"] is None
    assert search(bank, request | {"known_prerequisites": []})["status"] == "gap"
    assert search(bank, request | {"required_support": ["large_print"]})["status"] == "gap"
    assert search(bank, request | {"max_minutes": 1})["status"] == "gap"


def test_eligibility_and_latest_revision_never_retain_withdrawn_material(bank, database):
    identity = add_material(bank)
    invalid = [
        {"reviewed": False},
        {"available": False},
        {"teaching_material_confirmed": False},
        {"duration_minutes": 40},
        {"prerequisites": ["articles"]},
    ]
    for changes in invalid:
        clone_version(database, identity, material(**changes))
    for field, value in (
        ("basis", "unlicensed"),
        ("storage", False),
        ("adaptation", False),
        ("delivery", False),
    ):
        data = material()
        data["rights"][field] = value
        clone_version(database, identity, data)
    clone_version(database, identity, material(), owner=SECOND)
    request = objective(limit=10)
    assert [row["id"] for row in search(bank, request)["candidates"]] == [identity]
    changed = bank.post(
        "/teaching-assets",
        json={"id": identity, "expected_revision": 1, "material": material(available=False)},
    )
    assert changed.status_code == 200 and changed.json()["revision"] == 2
    result = search(bank, request)
    assert result["status"] == "gap" and result["candidates"] == []
    assert result["reason"]


def test_listening_requires_available_permitted_matching_recording(bank, database):
    data = material(kind="input", answer_key=None)
    data["target"] |= {
        "route": "listening",
        "outcome": "main_points",
        "skills": ["listening"],
        "confusion": None,
        "task": "input",
        "modality": "audio",
        "response_type": "summary",
    }
    data["recording"] = {
        "reference": "synthetic-recording:listening",
        "version": "audio-2",
        "available": True,
        "permitted": True,
        "criteria_recording_version": "audio-2",
    }
    identity = add_material(bank, data)
    for changes in (
        {"available": False},
        {"permitted": False},
        {"criteria_recording_version": "audio-1"},
        {"reference": ""},
    ):
        invalid = copy.deepcopy(data)
        invalid["recording"].update(changes)
        clone_version(database, identity, invalid)
    transcript_only = copy.deepcopy(data)
    transcript_only["recording"] = None
    clone_version(database, identity, transcript_only)
    request = objective(data["target"], limit=10)
    assert [row["id"] for row in search(bank, request)["candidates"]] == [identity]
    assert bank.delete(f"/teaching-assets/{identity}").status_code == 200
    assert search(bank, request)["status"] == "gap"


def test_shared_operator_material_is_readable_but_not_writable_by_tutors(bank, database):
    private = add_material(bank)
    shared = clone_version(database, private, material(), owner=None)
    with authenticated(database, SECOND) as other:
        assert [row["id"] for row in search(other, objective())["candidates"]] == [shared]
        assert other.get(f"/teaching-assets/{private}").status_code == 404
        assert other.get(f"/teaching-assets/{shared}").status_code == 200
        assert other.delete(f"/teaching-assets/{shared}").status_code == 404
        assert (
            other.post(
                "/teaching-assets",
                json={"id": shared, "expected_revision": 1, "material": material()},
            ).status_code
            == 404
        )

    async def inspect():
        engine = create_engine(database)
        try:
            async with engine.connect() as connection:
                for table in ("teaching_assets", "teaching_asset_owners"):
                    assert await connection.scalar(text(f"SELECT count(*) FROM {table}")) == 0
            async with tenant_transaction(engine, SECOND) as connection:
                assert await connection.scalar(text("SELECT count(*) FROM teaching_assets")) == 1
                changed = await connection.execute(
                    text("UPDATE teaching_assets SET reviewed_by='forged' WHERE id=:id"),
                    {"id": UUID(shared)},
                )
                assert changed.rowcount == 0
            with pytest.raises(DBAPIError) as denied:
                async with tenant_transaction(engine, SECOND) as connection:
                    await connection.execute(
                        text("""INSERT INTO teaching_assets(id,revision,data)
                            VALUES (:id,2,'{}')"""),
                        {"id": UUID(shared)},
                    )
            assert denied.value.orig.sqlstate == "42501"
            with pytest.raises(DBAPIError) as denied:
                async with tenant_transaction(engine, SECOND) as connection:
                    await connection.execute(
                        text("INSERT INTO teaching_asset_owners(id,tutor_id) VALUES (:id,NULL)"),
                        {"id": uuid4()},
                    )
            assert denied.value.orig.sqlstate == "42501"
        finally:
            await engine.dispose()

    asyncio.run(inspect())


def test_invalid_fields_and_private_context_never_reach_embeddings(bank, monkeypatch):
    calls = []
    original = LocalEmbeddings.embed

    async def capture(self, description, *, passage=False):
        calls.append((description, passage))
        return await original(self, description, passage=passage)

    monkeypatch.setattr(LocalEmbeddings, "embed", capture)
    learner = bank.post("/learners", json=profile()).json()["id"]
    reference = str(uuid4())
    response = bank.post(
        f"/learners/{learner}/sources",
        json={
            "id": reference,
            "kind": "lesson",
            "occurred_at": None,
            "qualification": "tutor_notes",
            "raw_text": "PRIVATE_SOURCE_CANARY",
        },
    )
    assert response.status_code == 200
    request = objective()
    for changes in (
        {"private_text": "PRIVATE_SOURCE_CANARY"},
        {"scope": "shared"},
        {"tutor_id": str(SECOND)},
        {"level": "C2"},
        {"confusion": None},
        {"route": "reading"},
        {"limit": 100},
        {"max_minutes": 0},
        {"evidence_refs": ["PRIVATE_SOURCE_CANARY"]},
    ):
        response = bank.post("/teaching-search", json=request | changes)
        assert response.status_code == 422
        assert "PRIVATE" not in response.text
    assert calls == []
    result = search(bank, request | {"evidence_refs": [reference]})
    assert result["status"] == "gap" and len(calls) == 1
    description, passage = calls[0]
    assert passage is False
    assert "present_perfect_vs_past_simple" in description
    assert reference not in description and request["objective_ref"] not in description
    assert "PRIVATE" not in description


def test_query_cache_validates_vectors_and_always_refreshes_eligibility(
    bank, database, monkeypatch
):
    identity = add_material(bank)
    request = objective(use_cache=True, max_minutes=19)
    description = build_search(Objective.model_validate(request))
    key = f"qemb:{CONFIG_REVISION}:{hashlib.sha256(description.encode()).hexdigest()}"
    redis = Redis.from_url(database.redis_url, decode_responses=True)
    calls = []
    original = LocalEmbeddings.embed

    async def capture(self, description, *, passage=False):
        calls.append((description, passage))
        return await original(self, description, passage=passage)

    monkeypatch.setattr(LocalEmbeddings, "embed", capture)
    redis.delete(key)
    try:
        first = search(bank, request)
        assert first["cache"] == "miss" and first["status"] == "candidates"
        assert len(calls) == 1 and 0 < redis.ttl(key) <= 86400
        stored = json.loads(redis.get(key))
        assert len(stored) == DIMENSIONS and all(type(value) in (int, float) for value in stored)
        assert "PRIVATE" not in redis.get(key) and description not in key
        assert search(bank, request)["cache"] == "hit" and len(calls) == 1
        engine = admin_engine(database.database_url)
        try:
            with engine.begin() as connection:
                connection.execute(
                    text("UPDATE teaching_asset_owners SET tutor_id=:owner WHERE id=:id"),
                    {"owner": SECOND, "id": UUID(identity)},
                )
            revoked = search(bank, request)
            assert revoked["cache"] == "hit" and revoked["status"] == "gap"
            assert len(calls) == 1
            with engine.begin() as connection:
                connection.execute(
                    text("UPDATE teaching_asset_owners SET tutor_id=:owner WHERE id=:id"),
                    {"owner": FIRST, "id": UUID(identity)},
                )
        finally:
            engine.dispose()
        assert search(bank, request)["status"] == "candidates" and len(calls) == 1
        bank.post(
            "/teaching-assets",
            json={"id": identity, "expected_revision": 1, "material": material(available=False)},
        ).raise_for_status()
        changed = search(bank, request)
        assert changed["cache"] == "hit" and changed["status"] == "gap" and len(calls) == 1
        bypassed = search(bank, request | {"use_cache": False})
        assert bypassed["cache"] == "bypass" and bypassed["status"] == "gap" and len(calls) == 2
        for corrupt in (
            "not-json",
            "[]",
            json.dumps([float("nan")] * DIMENSIONS),
            json.dumps([0] * DIMENSIONS),
            json.dumps([10**400] * DIMENSIONS),
            json.dumps([1e308] * DIMENSIONS),
            json.dumps([1e-300] * DIMENSIONS),
            b"\xff",
            "[" * 10000 + "0" + "]" * 10000,
        ):
            redis.set(key, corrupt, ex=60)
            before = len(calls)
            repaired = search(bank, request)
            assert repaired["status"] == "gap" and repaired["cache"] == "miss"
            assert len(calls) == before + 1 and json.loads(redis.get(key)) == stored
        resources = bank.app.state.resources
        healthy = resources.cache
        unavailable = AsyncRedis(
            host="127.0.0.1", port=1, socket_connect_timeout=0.1, socket_timeout=0.1
        )
        resources.cache = unavailable
        try:
            result = search(bank, request)
            assert result["status"] == "gap" and result["cache"] == "error"
        finally:
            resources.cache = healthy
            bank.portal.call(unavailable.aclose)
    finally:
        redis.delete(key)
        redis.close()


def test_provider_and_database_failures_are_not_content_gaps(bank, database, monkeypatch, capsys):
    request = objective()
    assert search(bank, request)["status"] == "gap"

    async def unavailable(self, description, *, passage=False):
        raise RuntimeError("PRIVATE_PROVIDER_FAILURE")

    with monkeypatch.context() as patch:
        patch.setattr(LocalEmbeddings, "embed", unavailable)
        response = bank.post("/teaching-search", json=request)
        assert response.status_code == 503
        assert response.json()["status"] == "failed" and response.json()["candidates"] == []
        assert "PRIVATE" not in response.text
    for vector in ([], [float("inf")] * DIMENSIONS, [0] * DIMENSIONS):

        async def invalid(self, description, *, passage=False, vector=vector):
            return vector

        with monkeypatch.context() as patch:
            patch.setattr(LocalEmbeddings, "embed", invalid)
            response = bank.post("/teaching-search", json=request)
            assert response.status_code == 503 and response.json()["status"] == "failed"
    engine = admin_engine(database.database_url)
    try:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE teaching_assets RENAME TO temporarily_unavailable_assets")
            )
        try:
            response = bank.post("/teaching-search", json=request)
            assert response.status_code == 503 and response.json()["status"] == "failed"
            assert response.json()["candidates"] == []
        finally:
            with engine.begin() as connection:
                connection.execute(
                    text("ALTER TABLE temporarily_unavailable_assets RENAME TO teaching_assets")
                )
    finally:
        engine.dispose()
    captured = capsys.readouterr()
    assert "PRIVATE_PROVIDER_FAILURE" not in captured.out + captured.err
