from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

import pytest

from tutor_copilot.metrics import summarize_recent

NOW = datetime(2026, 11, 1, 12, tzinfo=UTC)


def source(number: int, days: int, kind: str = "lesson") -> dict[str, Any]:
    return {"id": UUID(int=number), "kind": kind, "occurred_at": NOW - timedelta(days=days)}


def observation(
    number: int,
    session: dict[str, Any],
    correct: int = 3,
    opportunities: int = 5,
    **changes: Any,
) -> dict[str, Any]:
    data = {
        "subskill": "past-tense",
        "task": "controlled",
        "task_ref": "comparable-task",
        "assistance": "independent",
        "accuracy": {"correct": correct, "opportunities": opportunities},
        **changes,
    }
    return {"id": UUID(int=number), "revision": 1, "source_id": session["id"], "data": data}


@pytest.mark.parametrize(
    ("ratios", "expected"),
    [([10, 11, 13], "improving"), ([13, 12, 10], "regressing"), ([10, 11, 12], "stable")],
)
def test_exact_trend_boundaries(ratios: list[int], expected: str) -> None:
    sessions = [source(i + 1, 3 - i) for i in range(3)]
    rows = [observation(i + 1, session, ratios[i], 20) for i, session in enumerate(sessions)]
    group = summarize_recent(rows, NOW, sources=sessions)["groups"][0]
    accuracy = group["measures"]["accuracy"]
    assert accuracy["trend"] == expected
    assert accuracy["correct"] == sum(ratios)
    assert accuracy["opportunities"] == 60
    assert accuracy["trend_source_ids"] == [str(session["id"]) for session in sessions]
    assert accuracy["possible_regression"] is False


def test_single_qualified_drop_is_an_alert_without_a_three_session_trend() -> None:
    sessions = [source(1, 2), source(2, 1)]
    rows = [observation(1, sessions[0], 16, 20), observation(2, sessions[1], 13, 20)]
    accuracy = summarize_recent(rows, NOW, sources=sessions)["groups"][0]["measures"]["accuracy"]
    assert accuracy["possible_regression"] is True
    assert accuracy["trend"] == "insufficient"


@pytest.mark.parametrize(("session_count", "opportunities"), [(2, 5), (3, 4)])
def test_insufficient_observations_or_opportunities(session_count: int, opportunities: int) -> None:
    sessions = [source(i + 1, i + 1) for i in range(session_count)]
    rows = [observation(i + 1, session, 1, opportunities) for i, session in enumerate(sessions)]
    accuracy = summarize_recent(rows, NOW, sources=sessions)["groups"][0]["measures"]["accuracy"]
    assert accuracy["trend"] == "insufficient"
    assert accuracy["maintenance_support"] is False


def test_one_session_with_many_answers_cannot_manufacture_a_trend() -> None:
    session = source(1, 1)
    rows = [observation(i + 1, session) for i in range(3)]
    accuracy = summarize_recent(rows, NOW, sources=[session])["groups"][0]["measures"]["accuracy"]
    assert accuracy["opportunities"] == 15
    assert accuracy["trend"] == "insufficient"
    assert accuracy["trend_source_ids"] == [str(session["id"])]


def test_unknown_rates_and_completion_remain_separate() -> None:
    session = source(1, 1)
    row = observation(1, session, 0, 0, completion={"correct": 1, "opportunities": 4})
    group = summarize_recent([row], NOW, sources=[session])["groups"][0]
    for name in ("accuracy", "required_use", "avoidance"):
        assert group["measures"][name]["rate"] is None
        assert group["measures"][name]["unknown_observations"] == 1
        assert group["measures"][name]["trend"] == "insufficient"
    assert group["completion"]["rate"] == 0.25
    assert "trend" not in group["completion"]
    assert group["maintenance_candidate"] is False


def test_latest_four_sessions_per_stream_include_sessions_without_target_observations() -> None:
    sessions = [source(i + 1, i + 1) for i in range(5)]
    homework = [source(i + 10, i + 1, "homework") for i in range(5)]
    rows = [observation(1, sessions[4]), observation(2, homework[0])]
    result = summarize_recent(rows, NOW, sources=sessions + homework)
    assert result["source_ids"]["lesson"] == [str(session["id"]) for session in sessions[:4]]
    assert result["source_ids"]["homework"] == [str(session["id"]) for session in homework[:4]]
    assert len(result["groups"]) == 1
    assert result["groups"][0]["evidence_type"] == "homework"
    assert result["groups"][0]["measures"]["accuracy"]["opportunities"] == 5


def test_old_unknown_and_future_sources_cannot_change_recent_counts() -> None:
    current = source(1, 90)
    excluded = [source(2, 91), source(3, -1), source(4, 1, "actual_use")]
    unknown = {"id": UUID(int=5), "kind": "lesson", "occurred_at": None}
    row = observation(1, current)
    before = summarize_recent([row], NOW, sources=[current])
    after = summarize_recent(
        [row] + [observation(i + 2, session) for i, session in enumerate(excluded + [unknown])],
        NOW,
        sources=[current] + excluded + [unknown],
    )
    assert after == before


def test_equal_dates_use_stable_source_identity_to_break_ties() -> None:
    sessions = [source(i + 1, 1) for i in range(5)]
    result = summarize_recent([], NOW, sources=sessions)
    assert result["source_ids"]["lesson"] == [
        str(session["id"]) for session in reversed(sessions[1:])
    ]
    assert summarize_recent([], NOW, sources=list(reversed(sessions))) == result


def test_tasks_task_demands_and_assistance_are_not_combined() -> None:
    session = source(1, 1)
    rows = [
        observation(1, session),
        observation(2, session, task="spontaneous"),
        observation(3, session, task_ref="different-demands"),
        observation(4, session, assistance="supported"),
        observation(5, session, assistance="unknown"),
    ]
    groups = summarize_recent(rows, NOW, sources=[session])["groups"]
    assert len(groups) == 5
    assert all(group["measures"]["accuracy"]["opportunities"] == 5 for group in groups)


def test_conflicting_measure_trends_are_mixed() -> None:
    sessions = [source(i + 1, 3 - i) for i in range(3)]
    rows = [
        observation(
            i + 1,
            session,
            10 + i * 2,
            20,
            avoidance={"correct": 14 - i * 2, "opportunities": 20},
        )
        for i, session in enumerate(sessions)
    ]
    group = summarize_recent(rows, NOW, sources=sessions)["groups"][0]
    assert group["trend"] == "mixed"
    assert group["measures"]["accuracy"]["trend"] == "improving"
    assert group["measures"]["avoidance"]["trend"] == "regressing"


@pytest.mark.parametrize("with_support", [True, False])
def test_maintenance_at_point_85_is_only_a_candidate_with_support(with_support: bool) -> None:
    sessions = [source(i + 1, i + 1) for i in range(3)]
    supporting = {"correct": 17, "opportunities": 20} if with_support else None
    rows = [
        observation(i + 1, session, 17, 20, required_use=supporting, avoidance=supporting)
        for i, session in enumerate(sessions)
    ]
    group = summarize_recent(rows, NOW, sources=sessions)["groups"][0]
    assert group["maintenance_candidate"] is with_support
    assert group["maintenance_confirmed"] is False


def test_naive_clock_is_rejected() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        summarize_recent([], datetime(2026, 11, 1), sources=[])
