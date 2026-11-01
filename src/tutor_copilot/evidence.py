"""Short, tenant-scoped PostgreSQL transactions for tutor evidence intake."""

import hashlib
import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC
from typing import Any, Literal
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from tutor_copilot.schemas import Activity, Observation, ProfileWrite, Source


@asynccontextmanager
async def tenant_transaction(database: AsyncEngine, tutor: UUID) -> AsyncIterator[AsyncConnection]:
    async with database.begin() as connection:
        await connection.execute(
            text("SELECT set_config('app.tutor_id', :tutor, true)"), {"tutor": str(tutor)}
        )
        yield connection


async def lock_learner(
    connection: AsyncConnection, learner: UUID, tutor: UUID, *, allow_inactive: bool = False
) -> int:
    revision = await connection.scalar(
        text("""SELECT profile_revision FROM learners WHERE id=:id AND tutor_id=:tutor
             AND (last_active > now() - interval '12 months' OR :allow_inactive) FOR UPDATE"""),
        {"id": learner, "tutor": tutor, "allow_inactive": allow_inactive},
    )
    if revision is None:
        raise HTTPException(404, "Learner unavailable")
    return int(revision)


async def touch_learner(connection: AsyncConnection, learner: UUID) -> None:
    await connection.execute(
        text("UPDATE learners SET last_active=now() WHERE id=:id"), {"id": learner}
    )


async def save_profile(
    connection: AsyncConnection, tutor: UUID, data: ProfileWrite, learner: UUID | None = None
) -> dict[str, Any]:
    current = await lock_learner(connection, learner, tutor) if learner else 0
    if current != data.expected_revision:
        raise HTTPException(409, "Profile revision changed")
    learner = learner or uuid4()
    if current == 0:
        await connection.execute(
            text("INSERT INTO learners(id,tutor_id,profile_revision) VALUES (:id,:tutor,1)"),
            {"id": learner, "tutor": tutor},
        )
    else:
        await connection.execute(
            text("UPDATE learners SET profile_revision=:revision WHERE id=:id"),
            {"id": learner, "revision": current + 1},
        )
    await connection.execute(
        text("""INSERT INTO profiles(learner_id,tutor_id,revision,data)
             VALUES (:id,:tutor,:revision,CAST(:data AS jsonb))"""),
        {
            "id": learner,
            "tutor": tutor,
            "revision": current + 1,
            "data": data.profile.model_dump_json(),
        },
    )
    await touch_learner(connection, learner)
    return {
        "id": str(learner),
        "revision": current + 1,
        "profile": data.profile.model_dump(mode="json"),
    }


async def read_profile(connection: AsyncConnection, learner: UUID, tutor: UUID) -> dict[str, Any]:
    revision = await lock_learner(connection, learner, tutor)
    profile = await connection.scalar(
        text("SELECT data FROM profiles WHERE learner_id=:id AND revision=:revision"),
        {"id": learner, "revision": revision},
    )
    return {"id": str(learner), "revision": revision, "profile": profile}


async def save_source(
    connection: AsyncConnection, learner: UUID, tutor: UUID, source: Source
) -> dict[str, Any]:
    await lock_learner(connection, learner, tutor)
    content = source.model_dump(mode="json", exclude={"id", "expected_revision"})
    content["occurred_at"] = (
        source.occurred_at.astimezone(UTC).isoformat() if source.occurred_at else None
    )
    fingerprint = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    previous = (
        (
            await connection.execute(
                text("SELECT learner_id,revision,fingerprint FROM sources WHERE id=:id"),
                {"id": source.id},
            )
        )
        .mappings()
        .first()
    )
    if previous:
        if previous["learner_id"] != learner:
            raise HTTPException(409, "Source identity already used")
        if (
            previous["fingerprint"] == fingerprint
            and source.expected_revision == previous["revision"] - 1
        ):
            return {"id": str(source.id), "revision": previous["revision"]}
        if source.expected_revision != previous["revision"]:
            raise HTTPException(409, "Source revision changed")
        await connection.execute(
            text("""INSERT INTO source_history
            (source_id,learner_id,tutor_id,revision,kind,occurred_at,qualification,raw_text,
             expires_at,fingerprint)
            SELECT id,learner_id,tutor_id,revision,kind,occurred_at,qualification,raw_text,
             expires_at,fingerprint FROM sources WHERE id=:id"""),
            {"id": source.id},
        )
        await connection.execute(
            text("""UPDATE sources SET revision=revision+1,kind=:kind,
            occurred_at=:occurred,qualification=:qualification,raw_text=:raw,
            expires_at=CASE WHEN raw_text IS NOT DISTINCT FROM :raw THEN expires_at
                ELSE now()+interval '30 days' END,fingerprint=:fingerprint WHERE id=:id"""),
            {
                "id": source.id,
                "kind": source.kind,
                "occurred": source.occurred_at,
                "qualification": source.qualification,
                "raw": source.raw_text,
                "fingerprint": fingerprint,
            },
        )
    else:
        if source.expected_revision != 0:
            raise HTTPException(409, "Source revision changed")
        await connection.execute(
            text("""INSERT INTO sources(id,learner_id,tutor_id,kind,occurred_at,qualification,
                 raw_text,fingerprint) VALUES (:id,:learner,:tutor,:kind,:occurred,:qualification,
                 :raw,:fingerprint)"""),
            {
                "id": source.id,
                "learner": learner,
                "tutor": tutor,
                "kind": source.kind,
                "occurred": source.occurred_at,
                "qualification": source.qualification,
                "raw": source.raw_text,
                "fingerprint": fingerprint,
            },
        )
    await touch_learner(connection, learner)
    return {"id": str(source.id), "revision": previous["revision"] + 1 if previous else 1}


async def read_source(
    connection: AsyncConnection, learner: UUID, source: UUID, revision: int | None = None
) -> dict[str, Any]:
    row = (
        (
            await connection.execute(
                text("""WITH versions AS (
             SELECT id,revision,kind,occurred_at,qualification,raw_text,expires_at FROM sources
               WHERE id=:id AND learner_id=:learner
             UNION ALL SELECT source_id,revision,kind,occurred_at,qualification,raw_text,expires_at
               FROM source_history WHERE source_id=:id AND learner_id=:learner)
             SELECT id,revision,kind,occurred_at,qualification,
             CASE WHEN expires_at > now() THEN raw_text ELSE NULL END AS raw_text,
             (expires_at > now() AND raw_text IS NOT NULL) AS available
             FROM versions WHERE CAST(:revision AS integer) IS NULL OR revision=:revision
             ORDER BY revision DESC LIMIT 1"""),
                {"id": source, "learner": learner, "revision": revision},
            )
        )
        .mappings()
        .first()
    )
    if row is None:
        raise HTTPException(404, "Source unavailable")
    return dict(row)


async def save_revision(
    connection: AsyncConnection, learner: UUID, tutor: UUID, data: Observation | Activity
) -> dict[str, Any]:
    await lock_learner(connection, learner, tutor)
    await read_source(connection, learner, data.source_id)
    table = "observations" if isinstance(data, Observation) else "activities"
    identity_fields = (
        ("response_ref", "subskill") if table == "observations" else ("activity_ref", "kind")
    )
    payload = data.model_dump(mode="json", exclude={"expected_revision", "id"})
    previous = (
        (
            await connection.execute(
                text(
                    f"SELECT learner_id,revision,data FROM {table} WHERE id=:id "
                    "ORDER BY revision DESC LIMIT 1"
                ),
                {"id": data.id},
            )
        )
        .mappings()
        .first()
    )
    current = previous["revision"] if previous else 0
    if previous and previous["learner_id"] != learner:
        raise HTTPException(409, "Evidence identity already used")
    # A retried identical correction returns its existing revision without another write.
    if previous and previous["data"] == payload and data.expected_revision == current - 1:
        return {"id": str(data.id), "revision": current}
    if data.expected_revision != current:
        raise HTTPException(409, "Evidence revision changed")
    if previous and any(previous["data"][field] != payload[field] for field in identity_fields):
        raise HTTPException(409, "Stable evidence identity cannot change")
    duplicate = await connection.scalar(
        text(f"""SELECT id FROM {table} WHERE learner_id=:learner AND id<>:id
             AND data->>:field1=:value1 AND data->>:field2=:value2 LIMIT 1"""),
        {
            "learner": learner,
            "id": data.id,
            "field1": identity_fields[0],
            "field2": identity_fields[1],
            "value1": payload[identity_fields[0]],
            "value2": payload[identity_fields[1]],
        },
    )
    if duplicate:
        raise HTTPException(409, "Evidence already recorded under another identity")
    if isinstance(data, Observation):
        kind = await connection.scalar(
            text("SELECT kind FROM sources WHERE id=:id"), {"id": data.source_id}
        )
        if kind == "actual_use":
            raise HTTPException(422, "Performance needs a lesson or homework source")
    elif data.observation_id is not None:
        linked = await connection.scalar(
            text("""SELECT id FROM observations WHERE id=:id AND revision=:revision
                 AND learner_id=:learner AND confirmed"""),
            {"id": data.observation_id, "revision": data.observation_revision, "learner": learner},
        )
        if linked is None or data.kind != "checked_outcome":
            raise HTTPException(422, "Checked outcome needs an existing confirmed observation")
    await connection.execute(
        text(f"""INSERT INTO {table}(id,revision,learner_id,tutor_id,source_id,confirmed,data)
             VALUES (:id,:revision,:learner,:tutor,:source,:confirmed,CAST(:data AS jsonb))"""),
        {
            "id": data.id,
            "revision": current + 1,
            "learner": learner,
            "tutor": tutor,
            "source": data.source_id,
            "confirmed": data.confirmed,
            "data": json.dumps(payload),
        },
    )
    await touch_learner(connection, learner)
    return {"id": str(data.id), "revision": current + 1}


async def current_records(
    connection: AsyncConnection,
    learner: UUID,
    table: Literal["observations", "activities"],
    *,
    confirmed_only: bool = True,
    history: bool = False,
) -> list[dict[str, Any]]:
    selection = "" if history else "DISTINCT ON (r.id)"
    confirmation = " AND r.confirmed" if confirmed_only else ""
    rows = (
        (
            await connection.execute(
                text(f"""SELECT {selection} r.id,r.revision,r.data,s.id AS source_id,
             s.kind AS evidence_type,s.occurred_at AS source_date,s.qualification,
             (s.expires_at > now() AND s.raw_text IS NOT NULL) AS source_available
             FROM {table} r JOIN sources s ON s.id=r.source_id
             WHERE r.learner_id=:learner{confirmation}
             ORDER BY r.id,r.revision DESC"""),
                {"learner": learner},
            )
        )
        .mappings()
        .all()
    )
    return [
        dict(row) for row in rows if not (confirmed_only and row["data"].get("withdrawn", False))
    ]
