import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

EVALUATION = Path(__file__).resolve().parents[2] / "evaluation"
ITEM_PATHS = [
    EVALUATION / "homework" / "HW-ARITH-01.json",
    EVALUATION / "feedback" / "FB-SOURCE-01.json",
]


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


def test_initial_draft_fixtures_are_structurally_valid() -> None:
    items = [json.loads(path.read_text()) for path in ITEM_PATHS]
    validate_items(items)
    for item in items:
        assert item["metadata"]["review"]["state"] == "draft"
        assert item["metadata"]["review"]["reviewed"] is False
        assert item["metadata"]["review"]["decisions"] == []


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
