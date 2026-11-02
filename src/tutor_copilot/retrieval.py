"""Controlled objective → local embedding → freshly authorized, exact pgvector search."""

import asyncio
import hashlib
import json
import logging
import time
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import Field
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from tutor_copilot.auth import require_tutor
from tutor_copilot.embeddings import CONFIG_REVISION, validate_vector
from tutor_copilot.evidence import tenant_transaction
from tutor_copilot.materials import MaterialKind, Skill, Support, TeachingTarget, describe_target
from tutor_copilot.runtime import Resources


class Objective(TeachingTarget):
    objective_ref: UUID
    evidence_refs: Annotated[list[UUID], Field(max_length=20)] = []
    kinds: Annotated[list[MaterialKind], Field(min_length=1, max_length=4)] = [
        "input",
        "activity",
        "explanation",
        "framework",
    ]
    known_prerequisites: Annotated[list[Skill], Field(max_length=9)] = []
    required_support: Annotated[list[Support], Field(max_length=5)] = []
    max_minutes: Annotated[int, Field(ge=1, le=120)] = 20
    domain_required: bool = False
    limit: Annotated[int, Field(ge=1, le=10)] = 5
    use_cache: bool = True


def build_search(objective: Objective) -> str:
    # Construct a base target explicitly: references and private context cannot enter the text.
    target = TeachingTarget.model_validate(
        {name: getattr(objective, name) for name in TeachingTarget.model_fields}
    )
    return describe_target(target) + (
        f" Material kinds: {', '.join(sorted(set(objective.kinds)))};"
        f" Known prerequisites: {', '.join(sorted(set(objective.known_prerequisites))) or 'none'};"
        f" required support: {', '.join(sorted(set(objective.required_support))) or 'none'};"
        f" maximum minutes: {objective.max_minutes}."
    )


async def query_vector(
    resources: Resources, description: str, use_cache: bool
) -> tuple[list[float], str]:
    key = f"qemb:{CONFIG_REVISION}:{hashlib.sha256(description.encode()).hexdigest()}"
    status = "bypass" if not use_cache else "miss"
    if use_cache:
        try:
            async with asyncio.timeout(0.25):
                cached = await resources.cache.get(key)
            if cached is not None:
                try:
                    return validate_vector(json.loads(cached)), "hit"
                except (ValueError, TypeError, RecursionError):
                    pass
        except UnicodeError:
            pass
        except (RedisError, TimeoutError):
            status = "error"
    vector = validate_vector(await resources.embeddings.embed(description))
    if use_cache:
        try:
            async with asyncio.timeout(0.25):
                await resources.cache.set(key, json.dumps(vector), ex=86400)
        except (RedisError, TimeoutError):
            status = "error"
    return vector, status


async def retrieve(resources: Resources, tutor: UUID, objective: Objective) -> dict[str, Any]:
    try:
        vector, cache_status = await query_vector(
            resources, build_search(objective), objective.use_cache
        )
        async with tenant_transaction(resources.database, tutor) as connection:
            result = await connection.execute(
                text("""
                WITH latest AS MATERIALIZED (
                  SELECT DISTINCT ON (id) id,revision,data,reviewed_by,embedding,embedding_revision
                  FROM teaching_assets ORDER BY id,revision DESC
                ), eligible AS MATERIALIZED (
                  SELECT * FROM latest
                  WHERE data->>'reviewed'='true' AND reviewed_by IS NOT NULL
                    AND data->>'available'='true' AND embedding_revision=:config
                    AND data->'rights'->>'basis' IN ('owned','public_domain','licensed')
                    AND data->'rights'->>'storage'='true'
                    AND data->'rights'->>'adaptation'='true'
                    AND data->'rights'->>'delivery'='true'
                    AND data->>'teaching_material_confirmed'='true'
                    AND data->>'kind'=ANY(CAST(:kinds AS text[]))
                    AND data->'target'->>'route'=:route
                    AND data->'target'->>'outcome'=:outcome
                    AND data->'target'->>'level'=:level
                    AND data->'target'->>'task'=:task
                    AND data->'target'->>'modality'=:modality
                    AND data->'target'->>'response_type'=:response
                    AND (data->'target'->>'confusion') IS NOT DISTINCT FROM :confusion
                    AND data->'target'->'skills' @> CAST(:skills AS jsonb)
                    AND data->'prerequisites' <@ CAST(:known AS jsonb)
                    AND data->'support' @> CAST(:support AS jsonb)
                    AND CAST(data->>'duration_minutes' AS integer) <= :minutes
                    AND (NOT :domain_required OR data->'target'->>'domain'=:domain)
                    AND (:route <> 'listening' OR (
                      data->'recording'->>'available'='true'
                      AND data->'recording'->>'permitted'='true'
                      AND length(data->'recording'->>'reference') > 0
                      AND data->'recording'->>'version'=
                          data->'recording'->>'criteria_recording_version'
                    ))
                )
                SELECT id,revision,data,reviewed_by,
                  embedding <=> CAST(:vector AS vector) AS distance,
                  data->'target'->>'domain'=:domain AS domain_match
                FROM eligible
                ORDER BY domain_match DESC, distance, id LIMIT :limit
            """),
                {
                    "config": CONFIG_REVISION,
                    "kinds": objective.kinds,
                    "route": objective.route,
                    "outcome": objective.outcome,
                    "level": objective.level,
                    "task": objective.task,
                    "modality": objective.modality,
                    "response": objective.response_type,
                    "confusion": objective.confusion,
                    "skills": json.dumps(objective.skills),
                    "known": json.dumps(objective.known_prerequisites),
                    "support": json.dumps(objective.required_support),
                    "minutes": objective.max_minutes,
                    "domain_required": objective.domain_required,
                    "domain": objective.domain,
                    "vector": json.dumps(vector),
                    "limit": objective.limit,
                },
            )
            candidates = [dict(row) for row in result.mappings()]
        return {
            "status": "candidates" if candidates else "gap",
            "objective_ref": str(objective.objective_ref),
            "embedding_revision": CONFIG_REVISION,
            "cache": cache_status,
            "candidates": candidates,
            "reason": None
            if candidates
            else "No eligible reviewed material for the selected constraints",
        }
    except (ValueError, RuntimeError, OSError, SQLAlchemyError, TimeoutError):
        return {
            "status": "failed",
            "objective_ref": str(objective.objective_ref),
            "candidates": [],
            "reason": "Material retrieval unavailable",
        }


router = APIRouter()


@router.post("/teaching-search")
async def search_materials(
    data: Objective, request: Request, tutor: Annotated[UUID, Depends(require_tutor)]
) -> JSONResponse:
    started = time.monotonic()
    result = await retrieve(request.app.state.resources, tutor, data)
    logging.getLogger("tutor_copilot").info(
        "",
        extra={
            "metadata_line": json.dumps(
                {
                    "stage": "retrieval",
                    "correlation_id": str(request.state.correlation_id),
                    "outcome": result["status"],
                    "candidate_count": len(result["candidates"]),
                    "cache": result.get("cache"),
                    "embedding_calls_avoided": int(result.get("cache") == "hit"),
                    "duration_ms": round((time.monotonic() - started) * 1000),
                }
            )
        },
    )
    return JSONResponse(
        jsonable_encoder(result), status_code=503 if result["status"] == "failed" else 200
    )
