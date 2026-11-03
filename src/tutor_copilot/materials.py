"""Reviewed teaching metadata and private, immutable bank versions."""

import json
from typing import Annotated, Any, Literal, Self
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import Field, model_validator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from tutor_copilot.auth import require_tutor
from tutor_copilot.embeddings import CONFIG_REVISION
from tutor_copilot.evidence import tenant_transaction
from tutor_copilot.intake import Transaction
from tutor_copilot.schemas import Intake, Task, Text

Route = Literal[
    "remediation",
    "reading",
    "listening",
    "vocabulary",
    "fluency",
    "discourse",
    "strategy",
    "project",
]
Skill = Literal[
    "tense_choice",
    "articles",
    "reading",
    "listening",
    "vocabulary",
    "fluency",
    "discourse",
    "strategy",
    "task_completion",
]
Support = Literal["glossary", "transcript", "model", "planning_time", "large_print"]
Domain = Literal["general", "work", "project_updates", "travel", "incident_reports"]
Outcome = Literal[
    "choose_meaning",
    "main_points",
    "vocabulary_use",
    "sustained_speech",
    "organized_report",
    "communication_repair",
    "completed_project",
]
Confusion = Literal["present_perfect_vs_past_simple", "definite_vs_indefinite_article"]
MaterialKind = Literal["input", "activity", "explanation", "framework"]


class TeachingTarget(Intake):
    route: Route
    outcome: Outcome
    skills: Annotated[list[Skill], Field(min_length=1, max_length=9)]
    level: Literal["A2", "B1", "B2"]
    task: Task
    modality: Literal["text", "audio", "speech", "mixed"]
    response_type: Literal["choice", "free_response", "summary", "performance", "project"]
    domain: Domain = "general"
    confusion: Confusion | None = None

    @model_validator(mode="after")
    def valid_route(self) -> Self:
        outcomes = {
            "remediation": "choose_meaning",
            "reading": "main_points",
            "listening": "main_points",
            "vocabulary": "vocabulary_use",
            "fluency": "sustained_speech",
            "discourse": "organized_report",
            "strategy": "communication_repair",
            "project": "completed_project",
        }
        if self.outcome != outcomes[self.route]:
            raise ValueError("Outcome must match the selected teaching route")
        if self.route == "remediation":
            expected = (
                "tense_choice" if self.confusion == "present_perfect_vs_past_simple" else "articles"
            )
            if self.confusion is None or expected not in self.skills:
                raise ValueError("Remediation needs an exact confusion and its skill")
        else:
            skill = "task_completion" if self.route == "project" else self.route
            if self.confusion is not None or skill not in self.skills:
                raise ValueError("Goal-led routes need their skill and no invented confusion")
        if self.route == "listening" and self.modality != "audio":
            raise ValueError("Listening requires audio")
        if self.route == "reading" and self.modality != "text":
            raise ValueError("Reading requires text")
        return self


class Rights(Intake):
    basis: Literal["owned", "public_domain", "licensed"]
    reference: Text
    attribution: Text
    storage: Literal[True]
    adaptation: Literal[True]
    delivery: Literal[True]
    restrictions: Text


class Recording(Intake):
    reference: Text
    version: Text
    available: bool
    permitted: bool
    criteria_recording_version: Text


class Material(Intake):
    kind: MaterialKind
    target: TeachingTarget
    source_ref: Text
    source_version: Text
    rights: Rights
    prerequisites: Annotated[list[Skill], Field(max_length=9)] = []
    support: Annotated[list[Support], Field(max_length=5)] = []
    duration_minutes: Annotated[int, Field(ge=1, le=120)]
    content: Annotated[str, Field(min_length=1, max_length=20000)]
    instructions: Text
    answer_key: Annotated[str, Field(max_length=10000)] | None = None
    criteria: Text
    reviewed: bool
    available: bool = True
    recording: Recording | None = None
    teaching_material_confirmed: Literal[True]

    @model_validator(mode="after")
    def complete_material(self) -> Self:
        if self.target.response_type == "choice" and not self.answer_key:
            raise ValueError("Closed-answer material needs its matching answer key")
        if self.target.modality == "audio" and self.recording is None:
            raise ValueError("A transcript alone is not audio material")
        return self


class MaterialWrite(Intake):
    id: UUID
    expected_revision: Annotated[int, Field(ge=0)] = 0
    material: Material


def describe_target(target: TeachingTarget) -> str:
    return (
        f"Teaching purpose: {target.route}; outcome: {target.outcome}; "
        f"skills: {', '.join(sorted(set(target.skills)))}; "
        f"confusion: {target.confusion or 'none'}; level: {target.level}; "
        f"task: {target.task}; modality: {target.modality}; "
        f"response: {target.response_type}; domain: {target.domain}."
    )


async def save_material(
    connection: AsyncConnection,
    tutor: UUID | None,
    data: MaterialWrite,
    embedding: list[float] | None = None,
    *,
    reviewer_ref: str | None = None,
    sharing_permission_ref: str | None = None,
) -> dict[str, Any]:
    if tutor is None and (
        not reviewer_ref or not sharing_permission_ref or not data.material.reviewed
    ):
        raise ValueError(
            "Shared material requires qualified review and separate sharing permission"
        )
    # Serialize one identity, including its first insert, without a process-local lock.
    await connection.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:identity, 0))"),
        {"identity": str(data.id)},
    )
    current = (
        (
            await connection.execute(
                text(
                    "SELECT revision, data FROM teaching_assets WHERE id=:id "
                    "ORDER BY revision DESC LIMIT 1"
                ),
                {"id": data.id},
            )
        )
        .mappings()
        .first()
    )
    payload = data.material.model_dump(mode="json")
    revision = int(current["revision"]) if current else 0
    if current:
        owner = await connection.scalar(
            text("SELECT tutor_id FROM teaching_asset_owners WHERE id=:id"), {"id": data.id}
        )
        if owner != tutor:
            raise HTTPException(404, "Material unavailable")
    if current and current["data"] == payload and data.expected_revision == revision - 1:
        return {"id": str(data.id), "revision": revision}
    if revision != data.expected_revision:
        raise HTTPException(409, "Material revision changed")
    if not current:
        await connection.execute(
            text("""INSERT INTO teaching_asset_owners(id,tutor_id,sharing_permission_ref)
                 VALUES (:id,:tutor,:permission)"""),
            {"id": data.id, "tutor": tutor, "permission": sharing_permission_ref},
        )
    await connection.execute(
        text("""INSERT INTO teaching_assets
             (id,revision,data,reviewed_by,embedding,embedding_revision)
             VALUES (:id,:revision,CAST(:data AS jsonb),:reviewer,
                     CAST(:embedding AS vector),:config)"""),
        {
            "id": data.id,
            "revision": revision + 1,
            "tutor": tutor,
            "data": data.material.model_dump_json(),
            "reviewer": (reviewer_ref or str(tutor)) if data.material.reviewed else None,
            "embedding": json.dumps(embedding) if embedding is not None else None,
            "config": CONFIG_REVISION if embedding is not None else None,
        },
    )
    return {"id": str(data.id), "revision": revision + 1}


router = APIRouter()


@router.post("/teaching-assets")
async def import_material(
    data: MaterialWrite, request: Request, tutor: Annotated[UUID, Depends(require_tutor)]
) -> dict[str, Any]:
    resources = request.app.state.resources
    vector = None
    if data.material.reviewed and data.material.available:
        description = (
            describe_target(data.material.target)
            + "\n"
            + data.material.content
            + "\n"
            + data.material.instructions
        )
        try:
            vector = await resources.embeddings.embed(description, passage=True)
        except (ValueError, RuntimeError, OSError, TimeoutError):
            raise HTTPException(503, "Material embedding failed") from None
    async with tenant_transaction(resources.database, tutor) as connection:
        return await save_material(connection, tutor, data, vector)


@router.get("/teaching-assets/{identity}")
async def get_material(identity: UUID, tx: Transaction) -> dict[str, Any]:
    row = (
        (
            await tx[0].execute(
                text(
                    "SELECT id,revision,data,reviewed_by FROM teaching_assets WHERE id=:id "
                    "ORDER BY revision DESC LIMIT 1"
                ),
                {"id": identity},
            )
        )
        .mappings()
        .first()
    )
    if row is None:
        raise HTTPException(404, "Material unavailable")
    return dict(row)


@router.delete("/teaching-assets/{identity}")
async def delete_material(identity: UUID, tx: Transaction) -> dict[str, str]:
    result = await tx[0].execute(
        text("DELETE FROM teaching_asset_owners WHERE id=:id AND tutor_id=:tutor"),
        {"id": identity, "tutor": tx[1]},
    )
    if not result.rowcount:
        raise HTTPException(404, "Material unavailable")
    return {"status": "deleted"}
