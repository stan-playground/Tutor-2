"""Recent performance and separately selected cumulative history, frozen without raw text."""

import json
from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from tutor_copilot.evidence import current_records, lock_learner, touch_learner
from tutor_copilot.metrics import summarize_recent
from tutor_copilot.schemas import ContextRequest


async def source_metadata(connection: AsyncConnection, learner: UUID) -> list[dict[str, Any]]:
    rows = (
        (
            await connection.execute(
                text("""SELECT v.source_id AS id,v.revision,v.kind,v.occurred_at,v.qualification,
             (v.expires_at > now() AND v.raw_text IS NOT NULL) AS available
             FROM sources s JOIN source_versions v ON v.learner_id=s.learner_id
               AND v.source_id=s.id AND v.revision=s.revision
             WHERE s.learner_id=:id ORDER BY v.occurred_at DESC NULLS LAST,v.source_id"""),
                {"id": learner},
            )
        )
        .mappings()
        .all()
    )
    return [dict(row) for row in rows]


async def build_context(
    connection: AsyncConnection, learner: UUID, tutor: UUID, selection: ContextRequest
) -> dict[str, Any]:
    revision = await lock_learner(connection, learner, tutor)
    as_of = await connection.scalar(text("SELECT now()"))
    assert isinstance(as_of, datetime)
    sources = await source_metadata(connection, learner)
    observations = await current_records(connection, learner, "observations")
    activities = await current_records(connection, learner, "activities")
    relevant = [
        row
        for row in activities
        if (not selection.subskills and not selection.purposes)
        or row["data"]["subskill"] in selection.subskills
        or row["data"]["purpose"] in selection.purposes
    ]
    relevant.sort(
        key=lambda row: (
            datetime.fromisoformat(row["data"]["occurred_at"])
            if row["data"]["occurred_at"]
            else datetime.min.replace(tzinfo=UTC),
            str(row["id"]),
        ),
        reverse=True,
    )
    # Expose selection limits; omitted history remains available through intake.
    history = relevant[:200]
    for row in history:
        row.pop("source_available", None)
    recent = summarize_recent(observations, as_of, sources=sources)
    selected_sources = {identity for stream in recent["source_ids"].values() for identity in stream}
    selected_sources.update(str(row["source_id"]) for row in history)
    return cast(
        dict[str, Any],
        jsonable_encoder(
            {
                "learner_id": learner,
                "profile_revision": revision,
                "as_of": as_of,
                "selection": selection.model_dump(),
                "recent": recent,
                "history": history,
                "history_coverage": {
                    "matching": len(relevant),
                    "selected": len(history),
                    "omitted": len(relevant) - len(history),
                    "limit": 200,
                },
                "sources": [
                    {key: value for key, value in source.items() if key != "available"}
                    for source in sources
                    if str(source["id"]) in selected_sources
                ],
            }
        ),
    )


async def freeze_context(
    connection: AsyncConnection, learner: UUID, tutor: UUID, selection: ContextRequest
) -> dict[str, Any]:
    data = await build_context(connection, learner, tutor, selection)
    identity = uuid4()
    await connection.execute(
        text("""INSERT INTO contexts(id,learner_id,tutor_id,data)
             VALUES (:id,:learner,:tutor,CAST(:data AS jsonb))"""),
        {"id": identity, "learner": learner, "tutor": tutor, "data": json.dumps(data)},
    )
    await touch_learner(connection, learner)
    return {"id": str(identity), "context": await resolve_availability(connection, learner, data)}


async def resolve_availability(
    connection: AsyncConnection, learner: UUID, data: dict[str, Any]
) -> dict[str, Any]:
    versions = (
        (
            await connection.execute(
                text("""SELECT source_id AS id,revision,
        expires_at > now() AND raw_text IS NOT NULL AS available
        FROM source_versions WHERE learner_id=:id"""),
                {"id": learner},
            )
        )
        .mappings()
        .all()
    )
    availability = {(str(row["id"]), row["revision"]): row["available"] for row in versions}
    for source in data["sources"]:
        source["available"] = availability.get((source["id"], source["revision"]), False)
    return data


async def read_context(
    connection: AsyncConnection, learner: UUID, tutor: UUID, identity: UUID
) -> dict[str, Any]:
    await lock_learner(connection, learner, tutor)
    data = await connection.scalar(
        text("SELECT data FROM contexts WHERE id=:id AND learner_id=:learner"),
        {"id": identity, "learner": learner},
    )
    if data is None:
        raise HTTPException(404, "Context unavailable")
    return {"id": str(identity), "context": await resolve_availability(connection, learner, data)}
