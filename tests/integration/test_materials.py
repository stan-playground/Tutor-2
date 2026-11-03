"""Private teaching imports exercise real HTTP, ownership and PostgreSQL versions."""

import asyncio
from uuid import UUID, uuid4

import pytest
from conftest import migrate
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from test_intake import FIRST, SECOND, authenticated

from tutor_copilot.bank import SharedPublication, publish
from tutor_copilot.db import create_engine
from tutor_copilot.evidence import tenant_transaction


def material(**changes):
    return {
        "kind": "activity",
        "target": {
            "route": "remediation",
            "outcome": "choose_meaning",
            "skills": ["tense_choice"],
            "confusion": "present_perfect_vs_past_simple",
            "level": "B1",
            "task": "controlled",
            "modality": "text",
            "response_type": "choice",
            "domain": "project_updates",
        },
        "source_ref": "synthetic-bank:tense-choice",
        "source_version": "1",
        "rights": {
            "basis": "owned",
            "reference": "synthetic-test-author",
            "attribution": "Synthetic fixture",
            "storage": True,
            "adaptation": True,
            "delivery": True,
            "restrictions": "Synthetic testing only",
        },
        "duration_minutes": 5,
        "content": "Choose: We finished the release yesterday.",
        "instructions": "Choose the appropriate tense for a finished past time.",
        "answer_key": "past simple",
        "criteria": "Meaning fits a finished past time.",
        "reviewed": True,
        "teaching_material_confirmed": True,
        **changes,
    }


@pytest.fixture
def bank(database):
    migrate(database)
    with authenticated(database) as client:
        yield client


def test_private_import_versions_rights_and_ownership(bank, database):
    identity = str(uuid4())
    payload = {"id": identity, "material": material()}
    assert bank.post("/teaching-assets", json=payload).json() == {"id": identity, "revision": 1}
    assert bank.post("/teaching-assets", json=payload).json()["revision"] == 1
    changed = payload | {"expected_revision": 1, "material": material(available=False)}
    assert bank.post("/teaching-assets", json=changed).json()["revision"] == 2
    assert bank.post("/teaching-assets", json=payload).status_code == 409
    assert bank.get(f"/teaching-assets/{identity}").json()["data"]["available"] is False
    with authenticated(database, SECOND) as other:
        assert other.get(f"/teaching-assets/{identity}").status_code == 404
        assert other.delete(f"/teaching-assets/{identity}").status_code == 404
        assert other.post("/teaching-assets", json=payload).status_code == 409
    for update in ({"tutor_id": str(SECOND)}, {"scope": "shared"}):
        assert bank.post("/teaching-assets", json=payload | update).status_code == 422
    for field in ("storage", "adaptation", "delivery"):
        invalid = material()
        invalid["rights"][field] = False
        assert (
            bank.post(
                "/teaching-assets", json={"id": str(uuid4()), "material": invalid}
            ).status_code
            == 422
        )
    invalid = material()
    invalid["rights"]["basis"] = "unknown"
    assert (
        bank.post("/teaching-assets", json={"id": str(uuid4()), "material": invalid}).status_code
        == 422
    )
    assert (
        bank.post(
            "/teaching-assets", json={"id": str(uuid4()), "material": material(kind="transcript")}
        ).status_code
        == 422
    )

    async def inspect():
        engine = create_engine(database)
        try:
            async with engine.connect() as connection:
                assert await connection.scalar(text("SELECT count(*) FROM teaching_assets")) == 0
            async with tenant_transaction(engine, FIRST) as connection:
                assert await connection.scalar(text("SELECT count(*) FROM teaching_assets")) == 2
            for statement in (
                "UPDATE teaching_assets SET reviewed_by='forged' WHERE id=:id",
                "DELETE FROM teaching_assets WHERE id=:id",
            ):
                with pytest.raises(DBAPIError) as denied:
                    async with tenant_transaction(engine, FIRST) as connection:
                        await connection.execute(text(statement), {"id": UUID(identity)})
                assert getattr(denied.value.orig, "sqlstate", None) == "42501"
        finally:
            await engine.dispose()

    asyncio.run(inspect())
    stored = bank.get(f"/teaching-assets/{identity}")
    assert stored.status_code == 200
    assert stored.json()["reviewed_by"] == str(FIRST)
    assert bank.delete(f"/teaching-assets/{identity}").status_code == 200
    assert bank.get(f"/teaching-assets/{identity}").status_code == 404


def test_material_csrf_and_listening_reference_validation(bank):
    payload = {"id": str(uuid4()), "material": material()}
    del bank.headers["X-CSRF-Token"]
    assert bank.post("/teaching-assets", json=payload).status_code == 403
    assert bank.delete(f"/teaching-assets/{payload['id']}").status_code == 403


def test_operator_publication_keeps_separate_permission_and_review(bank, database):
    identity = str(uuid4())
    data = SharedPublication.model_validate(
        {
            "id": identity,
            "material": material(),
            "reviewer_ref": "synthetic-qualified-reviewer-assertion",
            "reviewer_qualification": "qualified_english_tutor",
            "sharing_permission_ref": "synthetic-separate-sharing-authorization",
        }
    )
    assert asyncio.run(publish(data, database)) == {"id": identity, "revision": 1}
    assert bank.get(f"/teaching-assets/{identity}").json()["reviewed_by"] == data.reviewer_ref
    with authenticated(database, SECOND) as other:
        assert other.get(f"/teaching-assets/{identity}").status_code == 200
        assert (
            other.post(
                "/teaching-assets",
                json={
                    "id": identity,
                    "expected_revision": 1,
                    "material": material(available=False),
                },
            ).status_code
            == 404
        )
        assert other.delete(f"/teaching-assets/{identity}").status_code == 404
    withdrawn = data.model_copy(
        update={
            "expected_revision": 1,
            "material": data.material.model_copy(update={"available": False}),
        }
    )
    assert asyncio.run(publish(withdrawn, database))["revision"] == 2
    assert bank.get(f"/teaching-assets/{identity}").json()["data"]["available"] is False
