"""Deterministic recent performance; cumulative history never enters these counts."""

from collections import defaultdict
from datetime import datetime, timedelta
from fractions import Fraction
from itertools import pairwise
from typing import Any

MEASURES = ("accuracy", "required_use", "avoidance")


def _counts(rows: list[dict[str, Any]], measure: str) -> dict[str, Any]:
    """Sum a supplied measure without treating missing or zero opportunities as success."""
    values = [row["data"].get(measure) for row in rows]
    known = [value for value in values if value is not None]
    correct = sum(value["correct"] for value in known)
    opportunities = sum(value["opportunities"] for value in known)
    return {
        "correct": correct,
        "opportunities": opportunities,
        "rate": float(Fraction(correct, opportunities)) if opportunities else None,
        "unknown_observations": sum(
            value is None or value["opportunities"] == 0 for value in values
        ),
    }


def _measure(sessions: list[tuple[str, list[dict[str, Any]]]], measure: str) -> dict[str, Any]:
    """Compare distinct comparable sessions, retaining the exact threshold arithmetic."""
    result = _counts([row for _, rows in sessions for row in rows], measure)
    points = []
    for source_id, rows in sessions:
        counts = _counts(rows, measure)
        if counts["opportunities"] >= 5:
            points.append((source_id, Fraction(counts["correct"], counts["opportunities"])))
    trend = "insufficient"
    if len(points) >= 3:
        change = points[-1][1] - points[0][1]
        trend = (
            "improving"
            if change >= Fraction(15, 100)
            else "regressing"
            if change <= Fraction(-15, 100)
            else "stable"
        )
    result.update(
        trend=trend,
        trend_source_ids=[source_id for source_id, _ in points],
        possible_regression=any(
            later[1] - earlier[1] <= Fraction(-15, 100) for earlier, later in pairwise(points)
        ),
        maintenance_support=len(points) >= 3
        and all(rate >= Fraction(85, 100) for _, rate in points),
    )
    return result


def summarize_recent(
    observations: list[dict[str, Any]],
    as_of: datetime,
    *,
    sources: list[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize confirmed current revisions from the latest four sessions of each kind.

    The evidence loader supplies authorized source metadata and validated observation
    revisions. This pure function owns no process resources or persisted state. Dates
    must be timezone-aware; unknown/future dates cannot supply recent performance.
    """
    if as_of.utcoffset() is None:
        raise ValueError("Recent performance needs a timezone-aware as_of")
    cutoff = as_of - timedelta(days=90)
    selected: dict[str, list[dict[str, Any]]] = {}
    for kind in ("lesson", "homework"):
        eligible = [
            source
            for source in sources
            if source["kind"] == kind
            and source["occurred_at"] is not None
            and cutoff <= source["occurred_at"] <= as_of
        ]
        selected[kind] = sorted(
            eligible, key=lambda source: (source["occurred_at"], str(source["id"])), reverse=True
        )[:4]
    source_by_id = {str(source["id"]): source for stream in selected.values() for source in stream}
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in observations:
        source = source_by_id.get(str(row["source_id"]))
        if source is None:
            continue
        data = row["data"]
        grouped[
            (
                data["subskill"],
                source["kind"],
                data["task"],
                data["task_ref"],
                data["assistance"],
            )
        ].append(row)
    groups = []
    for key, rows in sorted(grouped.items()):
        by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            by_source[str(row["source_id"])].append(row)
        sessions = sorted(
            by_source.items(), key=lambda item: (source_by_id[item[0]]["occurred_at"], item[0])
        )
        measures = {measure: _measure(sessions, measure) for measure in MEASURES}
        trends = {
            measure["trend"] for measure in measures.values() if measure["trend"] != "insufficient"
        }
        group_trend = "mixed" if len(trends) > 1 else next(iter(trends), "insufficient")
        groups.append(
            {
                "subskill": key[0],
                "evidence_type": key[1],
                "task": key[2],
                "task_ref": key[3],
                "assistance": key[4],
                "observation_refs": [
                    {
                        "id": str(row["id"]),
                        "revision": row["revision"],
                        "source_id": str(row["source_id"]),
                    }
                    for row in sorted(rows, key=lambda row: str(row["id"]))
                ],
                "measures": measures,
                "trend": group_trend,
                "completion": _counts(rows, "completion"),
                # Missing applicable measures cannot silently support maintenance.
                "maintenance_candidate": all(
                    measure["maintenance_support"] for measure in measures.values()
                ),
                "maintenance_confirmed": False,
            }
        )
    return {
        "as_of": as_of.isoformat(),
        "window_days": 90,
        "source_ids": {
            kind: [str(source["id"]) for source in stream] for kind, stream in selected.items()
        },
        "groups": groups,
    }
