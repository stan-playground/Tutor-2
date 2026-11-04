"""Real intake checks for scoped identities and source-version provenance."""

from datetime import UTC, datetime, timedelta

from conftest import migrate
from test_evidence import profile
from test_intake import FIRST, SECOND, activity, authenticated, observation, source_payload


def test_client_ids_are_scoped_to_each_learner(database):
    migrate(database)
    source = source_payload()
    observed = observation(source)
    fact = activity(source)
    with authenticated(database, FIRST) as first:
        learners = [first.post("/learners", json=profile()).json()["id"] for _ in range(2)]
        for learner in learners:
            for path, payload in (
                ("sources", source),
                ("observations", observed),
                ("activities", fact),
            ):
                url = f"/learners/{learner}/{path}"
                saved = first.post(url, json=payload)
                assert saved.status_code == 200, (learner, path, saved.json())
                assert first.post(url, json=payload).json() == saved.json()
    with authenticated(database, SECOND) as second:
        learner = second.post("/learners", json=profile()).json()["id"]
        for path, payload in (
            ("sources", source),
            ("observations", observed),
            ("activities", fact),
        ):
            url = f"/learners/{learner}/{path}"
            saved = second.post(url, json=payload)
            assert saved.status_code == 200, (path, saved.json())
            assert second.post(url, json=payload).json() == saved.json()


def test_evidence_preserves_exact_source_version_after_correction(database):
    migrate(database)
    source = source_payload()
    earlier = datetime.now(UTC) - timedelta(days=30)
    source["occurred_at"] = earlier.isoformat()
    with authenticated(database, FIRST) as client:
        learner = client.post("/learners", json=profile()).json()["id"]
        base = f"/learners/{learner}"
        assert client.post(base + "/sources", json=source).status_code == 200
        assert client.post(base + "/observations", json=observation(source)).status_code == 200
        assert client.post(base + "/activities", json=activity(source)).status_code == 200
        correction = source | {
            "expected_revision": 1,
            "occurred_at": datetime.now(UTC).isoformat(),
        }
        assert client.post(base + "/sources", json=correction).status_code == 200
        evidence = client.get(base + "/evidence?history=true").json()
        for collection in ("observations", "activities"):
            row = evidence[collection][0]
            assert datetime.fromisoformat(row["source_date"]) == earlier
            assert row["source_revision"] == 1
