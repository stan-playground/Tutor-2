"""Check a feedback draft's recent arithmetic at the shared metrics boundary."""

import json
from datetime import datetime, timedelta
from pathlib import Path

from tutor_copilot.metrics import summarize_recent


def test_feedback_cumulative_fixture_keeps_old_counts_out_of_recent_rates() -> None:
    path = (
        Path(__file__).resolve().parents[2]
        / "evaluation/feedback/FB-03-cumulative-context-01.json"
    )
    item = json.loads(path.read_text())
    case_input = item["input"]
    as_of = datetime.fromisoformat(case_input["fixture_time"])
    sources = [
        source | {"occurred_at": datetime.fromisoformat(source["occurred_at"])}
        for source in case_input["sources"]
    ]
    observations = case_input["fixture_state"]["observations"]
    result = summarize_recent(observations, as_of, sources=sources)

    recent_sources = [source for source in sources if source["occurred_at"] >= as_of - timedelta(days=90)]
    recent_ids = {source["id"] for source in recent_sources}
    recent_observations = [row for row in observations if row["source_id"] in recent_ids]
    assert len(recent_observations) < len(observations)
    assert result == summarize_recent(recent_observations, as_of, sources=recent_sources)

    expected = item["expectedOutput"]
    assert result["source_ids"] == expected["source_ids"]
    assert len(result["groups"]) == 1
    group = result["groups"][0]
    assert group["observation_refs"] == expected["recent_observation_refs"]
    assert group["measures"]["accuracy"] == expected["accuracy"]
    assert group["trend"] == expected["group_trend"]
    assert group["maintenance_candidate"] == expected["maintenance_candidate"]
    assert group["maintenance_confirmed"] == expected["maintenance_confirmed"]
