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
    raw_supplied = "raw_text" in source.model_fields_set
    legacy_fingerprint = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    fingerprint = (
        "v2:"
        + hashlib.sha256(
            json.dumps(
                {"content": content, "raw_text_supplied": raw_supplied}, sort_keys=True
            ).encode()
        ).hexdigest()
    )
    previous = (
        (
            await connection.execute(
                text("""SELECT s.revision,v.fingerprint FROM sources s JOIN source_versions v
                  ON v.learner_id=s.learner_id AND v.source_id=s.id AND v.revision=s.revision
                  WHERE s.learner_id=:learner AND s.id=:id"""),
                {"id": source.id, "learner": learner},
            )
        )
        .mappings()
        .first()
    )
    if previous:
        if (
            previous["fingerprint"] == fingerprint
            or (source.raw_text is not None and previous["fingerprint"] == legacy_fingerprint)
        ) and source.expected_revision == previous["revision"] - 1:
            return {"id": str(source.id), "revision": previous["revision"]}
        if source.expected_revision != previous["revision"]:
            raise HTTPException(409, "Source revision changed")
        await connection.execute(
            text("""INSERT INTO source_versions
            (learner_id,source_id,revision,tutor_id,kind,occurred_at,qualification,raw_text,
             expires_at,fingerprint)
            SELECT learner_id,source_id,revision+1,tutor_id,:kind,:occurred,:qualification,
              CASE WHEN :raw_supplied THEN :raw ELSE raw_text END,
              CASE WHEN NOT :raw_supplied OR raw_text IS NOT DISTINCT FROM :raw THEN expires_at
                ELSE now()+interval '30 days' END,:fingerprint
            FROM source_versions WHERE learner_id=:learner AND source_id=:id AND revision=:revision"""),
            {
                "id": source.id,
                "learner": learner,
                "revision": previous["revision"],
                "kind": source.kind,
                "occurred": source.occurred_at,
                "qualification": source.qualification,
                "raw": source.raw_text,
                "raw_supplied": raw_supplied,
                "fingerprint": fingerprint,
            },
        )
        await connection.execute(
            text("UPDATE sources SET revision=revision+1 WHERE learner_id=:learner AND id=:id"),
            {"id": source.id, "learner": learner},
        )
    else:
        if source.expected_revision != 0:
            raise HTTPException(409, "Source revision changed")
        await connection.execute(
            text("INSERT INTO sources(id,learner_id,tutor_id) VALUES (:id,:learner,:tutor)"),
            {"id": source.id, "learner": learner, "tutor": tutor},
        )
        await connection.execute(
            text("""INSERT INTO source_versions
              (source_id,learner_id,tutor_id,revision,kind,occurred_at,qualification,
               raw_text,expires_at,fingerprint)
              VALUES (:id,:learner,:tutor,1,:kind,:occurred,:qualification,
                :raw,now()+interval '30 days',:fingerprint)"""),
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
                text("""SELECT v.source_id AS id,v.revision,v.kind,v.occurred_at,v.qualification,
             CASE WHEN v.expires_at > now() THEN v.raw_text ELSE NULL END AS raw_text,
             (v.expires_at > now() AND v.raw_text IS NOT NULL) AS available
             FROM source_versions v JOIN sources s
               ON s.learner_id=v.learner_id AND s.id=v.source_id
             WHERE v.source_id=:id AND v.learner_id=:learner
             AND v.revision=COALESCE(CAST(:revision AS integer),s.revision)"""),
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
    source = await read_source(connection, learner, data.source_id)
    table = "observations" if isinstance(data, Observation) else "activities"
    identity_fields = (
        ("response_ref", "subskill") if table == "observations" else ("activity_ref", "kind")
    )
    payload = data.model_dump(mode="json", exclude={"expected_revision", "id"})
    previous = (
        (
            await connection.execute(
                text(
                    f"SELECT revision,data FROM {table} WHERE learner_id=:learner AND id=:id "
                    "ORDER BY revision DESC LIMIT 1"
                ),
                {"id": data.id, "learner": learner},
            )
        )
        .mappings()
        .first()
    )
    current = previous["revision"] if previous else 0
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
        if source["kind"] == "actual_use":
            raise HTTPException(422, "Performance needs a lesson or homework source")
    elif data.observation_id is not None:
        linked = await connection.scalar(
            text("""SELECT id FROM observations WHERE id=:id AND revision=:revision
                 AND learner_id=:learner AND confirmed"""),
            {"id": data.observation_id, "revision": data.observation_revision, "learner": learner},
        )
        if linked is None or data.kind != "checked_outcome":
            raise HTTPException(422, "Checked outcome needs an existing confirmed observation")
    parameters = {
            "id": data.id,
            "revision": current + 1,
            "learner": learner,
            "tutor": tutor,
            "source": data.source_id,
            "source_revision": source["revision"],
            "confirmed": data.confirmed,
            "data": json.dumps(payload),
        }
    if isinstance(data, Activity):
        parameters["observation_id"] = data.observation_id
        parameters["observation_revision"] = data.observation_revision
    extra_columns = ",observation_id,observation_revision" if isinstance(data, Activity) else ""
    extra_values = ",:observation_id,:observation_revision" if isinstance(data, Activity) else ""
    await connection.execute(
        text(f"""INSERT INTO {table}
             (id,revision,learner_id,tutor_id,source_id,source_revision,confirmed,data{extra_columns})
             VALUES (:id,:revision,:learner,:tutor,:source,:source_revision,:confirmed,
                     CAST(:data AS jsonb){extra_values})"""),
        parameters,
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
                text(f"""SELECT {selection} r.id,r.revision,r.data,v.source_id,
             v.revision AS source_revision,v.kind AS evidence_type,
             v.occurred_at AS source_date,v.qualification,
             (v.expires_at > now() AND v.raw_text IS NOT NULL) AS source_available
             FROM {table} r JOIN source_versions v ON v.learner_id=r.learner_id
               AND v.source_id=r.source_id AND v.revision=r.source_revision
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
