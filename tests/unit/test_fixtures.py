import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

from tutor_copilot.metrics import summarize_recent

EVALUATION = Path(__file__).resolve().parents[2] / "evaluation"
ITEM_PATHS = sorted((EVALUATION / "homework").glob("*.json")) + sorted(
    (EVALUATION / "feedback").glob("*.json")
)
NUMERIC_PATHS = sorted((EVALUATION / "homework").glob("HW-NUM-*.json"))
WINDOW_PATHS = sorted((EVALUATION / "homework").glob("HW-WINDOW-*.json"))


def validate_items(items: list[dict[str, Any]]) -> None:
    schema = json.loads((EVALUATION / "item.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    seen = set()
    for item in items:
        validator.validate(item)
        identity = (item["metadata"]["case_id"], item["metadata"]["revision"])
        if identity in seen:
            raise ValueError(f"Duplicate fixture ID/revision: {identity}")
        seen.add(identity)


def test_fixtures_are_structurally_valid() -> None:
    items = [json.loads(path.read_text()) for path in ITEM_PATHS]
    assert items
    validate_items(items)
    for item in items:
        if item["metadata"]["review"]["state"] == "draft":
            assert item["metadata"]["review"]["reviewed"] is False


def test_recent_fixture_against_real_metrics_boundary() -> None:
    item = json.loads((EVALUATION / "homework" / "HW-RECENT-01.json").read_text())
    case_input = item["input"]
    sources = [
        source | {"occurred_at": datetime.fromisoformat(source["occurred_at"])}
        for source in case_input["sources"]
    ]
    result = summarize_recent(
        case_input["fixture_state"]["observations"],
        datetime.fromisoformat(case_input["fixture_time"]),
        sources=sources,
    )
    expected = item["expectedOutput"]
    assert result["source_ids"] == expected["source_ids"]
    assert len(result["groups"]) == 1
    group = result["groups"][0]
    assert group["observation_refs"] == expected["observation_refs"]
    assert set(expected["rates"]) == {"accuracy", "required_use", "avoidance"}
    for measure, counts in expected["rates"].items():
        assert set(counts) == {"correct", "opportunities", "rate"}
        assert {key: group["measures"][measure][key] for key in counts} == counts
    assert group["trend"] == expected["trend"]
    assert group["maintenance_candidate"] == expected["maintenance_candidate"]
    assert group["maintenance_confirmed"] == expected["maintenance_confirmed"]


@pytest.mark.parametrize("path", NUMERIC_PATHS, ids=lambda path: path.stem)
def test_numeric_boundary_fixture_against_real_metrics(path: Path) -> None:
    item = json.loads(path.read_text())
    case_input = item["input"]
    sources = [
        source | {"occurred_at": datetime.fromisoformat(source["occurred_at"])}
        for source in case_input["sources"]
    ]
    result = summarize_recent(
        case_input["fixture_state"]["observations"],
        datetime.fromisoformat(case_input["fixture_time"]),
        sources=sources,
    )
    expected = item["expectedOutput"]
    assert result["source_ids"] == expected["source_ids"]
    assert len(result["groups"]) == 1
    group = result["groups"][0]
    assert group["observation_refs"] == expected["observation_refs"]
    assert "accuracy" in expected["measure_checks"]
    for name, measure in expected["measure_checks"].items():
        assert set(measure) == {
            "correct",
            "opportunities",
            "rate",
            "unknown_observations",
            "trend",
            "trend_source_ids",
            "possible_regression",
            "maintenance_support",
        }
        assert {key: group["measures"][name][key] for key in measure} == measure
    assert group["trend"] == expected["trend"]
    assert group["maintenance_candidate"] == expected["maintenance_candidate"]
    assert group["maintenance_confirmed"] == expected["maintenance_confirmed"]


@pytest.mark.parametrize("path", WINDOW_PATHS, ids=lambda path: path.stem)
def test_recent_window_fixture_against_real_metrics(path: Path) -> None:
    item = json.loads(path.read_text())
    case_input = item["input"]
    sources = [
        source | {"occurred_at": datetime.fromisoformat(source["occurred_at"])}
        for source in case_input["sources"]
    ]
    result = summarize_recent(
        case_input["fixture_state"]["observations"],
        datetime.fromisoformat(case_input["fixture_time"]),
        sources=sources,
    )
    expected = item["expectedOutput"]
    assert result["source_ids"] == expected["source_ids"]
    groups = {group["evidence_type"]: group for group in result["groups"]}
    assert len(groups) == len(result["groups"])
    assert set(groups) == set(expected["group_checks"])
    for kind, check in expected["group_checks"].items():
        group = groups[kind]
        assert group["observation_refs"] == check["observation_refs"]
        assert {key: group["measures"]["accuracy"][key] for key in check["accuracy"]} == check[
            "accuracy"
        ]
        assert group["maintenance_candidate"] == check["maintenance_candidate"]
        assert group["maintenance_confirmed"] == check["maintenance_confirmed"]


def test_feedback_trend_boundaries_against_shared_metrics() -> None:
    path = EVALUATION / "feedback" / "FB-03-trend-boundaries-01.json"
    item = json.loads(path.read_text())
    case_input = item["input"]
    sources = [
        source | {"occurred_at": datetime.fromisoformat(source["occurred_at"])}
        for source in case_input["sources"]
    ]
    result = summarize_recent(
        case_input["fixture_state"]["observations"],
        datetime.fromisoformat(case_input["fixture_time"]),
        sources=sources,
    )
    expected = item["expectedOutput"]
    assert result["source_ids"] == expected["source_ids"]
    assert len(result["groups"]) == 1
    group = result["groups"][0]
    check = expected["group"]
    for field in (
        "subskill",
        "evidence_type",
        "task",
        "task_ref",
        "assistance",
        "observation_refs",
        "trend",
        "maintenance_candidate",
        "maintenance_confirmed",
    ):
        assert group[field] == check[field]
    assert set(check["measures"]) == {"accuracy", "required_use", "avoidance"}
    for name, expected_measure in check["measures"].items():
        assert group["measures"][name] == expected_measure


def test_feedback_history_fixture_against_shared_metrics() -> None:
    path = EVALUATION / "feedback" / "FB-03-incomparable-history-01.json"
    item = json.loads(path.read_text())
    case_input = item["input"]
    sources = [
        source | {"occurred_at": datetime.fromisoformat(source["occurred_at"])}
        for source in case_input["sources"]
    ]
    result = summarize_recent(
        case_input["fixture_state"]["observations"],
        datetime.fromisoformat(case_input["fixture_time"]),
        sources=sources,
    )
    expected = item["expectedOutput"]
    assert result["source_ids"] == expected["source_ids"]
    groups = {(group["task_ref"], group["assistance"]): group for group in result["groups"]}
    assert len(groups) == len(result["groups"]) == len(expected["groups"])
    for check in expected["groups"]:
        group = groups[check["task_ref"], check["assistance"]]
        for field in ("subskill", "evidence_type", "task", "observation_refs", "trend"):
            assert group[field] == check[field]
        assert {key: group["measures"]["accuracy"][key] for key in check["accuracy"]} == check[
            "accuracy"
        ]
        assert all(
            group["measures"][name]["rate"] is None for name in ("required_use", "avoidance")
        )
        assert group["maintenance_candidate"] == check["maintenance_candidate"]
        assert group["maintenance_confirmed"] == check["maintenance_confirmed"]


@pytest.mark.parametrize("condition", ["missing", "expired"])
def test_feedback_source_stop_drafts_have_consistent_inputs(condition: str) -> None:
    path = EVALUATION / "feedback" / f"FB-04-{condition}-current-transcript-01.json"
    item = json.loads(path.read_text())
    case_input = item["input"]
    clock = datetime.fromisoformat(case_input["fixture_time"])
    state = case_input["fixture_state"]
    notes = next(source for source in case_input["sources"] if source["kind"] == "lesson_notes")
    assert notes["available"] and datetime.fromisoformat(notes["expires_at"]) > clock
    assert notes["owner_ref"] == state["owner_ref"]
    assert notes["learner_ref"] == state["learner_ref"]
    assert state["recent_observations"][0]["confirmed"]
    selected = case_input["task_request"]["selected_transcript_ref"]
    if condition == "missing":
        assert selected is None
        assert not any(source["kind"] == "lesson_transcript" for source in case_input["sources"])
    else:
        transcript = next(source for source in case_input["sources"] if source["ref"] == selected)
        assert transcript["kind"] == "lesson_transcript" and not transcript["available"]
        assert datetime.fromisoformat(transcript["expires_at"]) < clock
        assert "segments" not in transcript and "text" not in transcript
    expected = item["expectedOutput"]
    assert expected["source_context_outcome"] == f"{condition}_current_transcript"
    assert expected["terminal_state"] == "incomplete" and expected["provider_calls"] == 0
    assert expected["reached_stages"] == ["source_context"]
    assert item["metadata"]["severity"] == "critical"


def test_feedback_permission_stop_draft_has_consistent_inputs() -> None:
    path = EVALUATION / "feedback" / "FB-05-no-permission-01.json"
    item = json.loads(path.read_text())
    case_input = item["input"]
    state = case_input["fixture_state"]
    permission = state["permission_state"]
    clock = datetime.fromisoformat(case_input["fixture_time"])
    assert permission["prior_learner_opt_in"] is True and state["learner_opt_in"] is False
    assert (
        datetime.fromisoformat(permission["prior_recorded_at"])
        < datetime.fromisoformat(permission["recorded_at"])
        <= clock
    )
    assert state["processing_permission"] is False
    selected = case_input["task_request"]["selected_transcript_ref"]
    transcript = next(source for source in case_input["sources"] if source["ref"] == selected)
    assert transcript["owner_ref"] == state["owner_ref"]
    assert transcript["learner_ref"] == state["learner_ref"]
    assert (
        datetime.fromisoformat(permission["prior_recorded_at"])
        < datetime.fromisoformat(transcript["recorded_at"])
        < datetime.fromisoformat(permission["recorded_at"])
    )
    assert transcript["available"] and datetime.fromisoformat(transcript["expires_at"]) > clock
    assert transcript["content_access"] == "denied"
    assert "segments" not in transcript and "text" not in transcript
    expected = item["expectedOutput"]
    assert expected["source_context_outcome"] == "processing_permission_denied"
    assert expected["terminal_state"] == "blocked" and expected["provider_calls"] == 0
    assert expected["reached_stages"] == ["source_context"]
    assert item["metadata"]["severity"] == "critical"


@pytest.mark.parametrize(
    ("location", "field", "replacement"),
    [
        ("metadata", "stage", "unknown-stage"),
        ("input", "fixture_time", "2026-99-99T12:00:00Z"),
        ("input", "fixture_time", "2026-11-01T12:00:00+01:00"),
    ],
)
def test_invalid_fields_are_rejected(location: str, field: str, replacement: str) -> None:
    item = json.loads(ITEM_PATHS[0].read_text())
    item[location][field] = replacement
    with pytest.raises(ValidationError):
        validate_items([item])


def test_missing_required_field_is_rejected() -> None:
    item = json.loads(ITEM_PATHS[0].read_text())
    del item["metadata"]["revision"]
    with pytest.raises(ValidationError):
        validate_items([item])


def test_empty_expectations_are_rejected() -> None:
    item = json.loads(ITEM_PATHS[0].read_text())
    item["expectedOutput"] = {}
    with pytest.raises(ValidationError):
        validate_items([item])


def test_duplicate_item_revision_is_rejected() -> None:
    item = json.loads(ITEM_PATHS[0].read_text())
    with pytest.raises(ValueError, match="Duplicate fixture ID/revision"):
        validate_items([item, deepcopy(item)])
