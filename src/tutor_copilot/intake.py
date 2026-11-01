"""Authenticated HTTP operations; each request owns one tenant-scoped transaction."""

from collections.abc import AsyncIterator
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from tutor_copilot.auth import require_tutor
from tutor_copilot.context import build_context, freeze_context, read_context, resolve_availability
from tutor_copilot.evidence import (
    current_records,
    lock_learner,
    read_profile,
    read_source,
    save_profile,
    save_revision,
    save_source,
    tenant_transaction,
)
from tutor_copilot.schemas import Activity, ContextRequest, Observation, ProfileWrite, Source

router = APIRouter()


async def transaction(
    request: Request, tutor: Annotated[UUID, Depends(require_tutor)]
) -> AsyncIterator[tuple[AsyncConnection, UUID]]:
    async with tenant_transaction(request.app.state.resources.database, tutor) as connection:
        yield connection, tutor


Transaction = Annotated[tuple[AsyncConnection, UUID], Depends(transaction, scope="function")]


@router.post("/learners", status_code=201)
async def create_learner(data: ProfileWrite, tx: Transaction) -> dict[str, Any]:
    return await save_profile(tx[0], tx[1], data)


@router.get("/learners/{learner}")
async def get_learner(learner: UUID, tx: Transaction) -> dict[str, Any]:
    return await read_profile(tx[0], learner, tx[1])


@router.put("/learners/{learner}")
async def update_learner(learner: UUID, data: ProfileWrite, tx: Transaction) -> dict[str, Any]:
    return await save_profile(tx[0], tx[1], data, learner)


@router.delete("/learners/{learner}")
async def delete_learner(learner: UUID, tx: Transaction) -> dict[str, str]:
    await lock_learner(tx[0], learner, tx[1], allow_inactive=True)
    await tx[0].execute(text("DELETE FROM learners WHERE id=:id"), {"id": learner})
    return {"status": "deleted"}


@router.post("/learners/{learner}/sources")
async def add_source(learner: UUID, data: Source, tx: Transaction) -> dict[str, Any]:
    return await save_source(tx[0], learner, tx[1], data)


@router.get("/learners/{learner}/sources/{source}")
async def get_source(
    learner: UUID, source: UUID, tx: Transaction, revision: int | None = None
) -> dict[str, Any]:
    await lock_learner(tx[0], learner, tx[1])
    return await read_source(tx[0], learner, source, revision)


@router.post("/learners/{learner}/observations")
async def add_observation(learner: UUID, data: Observation, tx: Transaction) -> dict[str, Any]:
    return await save_revision(tx[0], learner, tx[1], data)


@router.post("/learners/{learner}/activities")
async def add_activity(learner: UUID, data: Activity, tx: Transaction) -> dict[str, Any]:
    return await save_revision(tx[0], learner, tx[1], data)


@router.get("/learners/{learner}/evidence")
async def get_evidence(learner: UUID, tx: Transaction, history: bool = False) -> dict[str, Any]:
    await lock_learner(tx[0], learner, tx[1])
    return {
        "observations": await current_records(
            tx[0], learner, "observations", confirmed_only=False, history=history
        ),
        "activities": await current_records(
            tx[0], learner, "activities", confirmed_only=False, history=history
        ),
    }


@router.get("/learners/{learner}/context")
async def get_current_context(learner: UUID, tx: Transaction) -> dict[str, Any]:
    data = await build_context(tx[0], learner, tx[1], ContextRequest())
    return await resolve_availability(tx[0], learner, data)


@router.post("/learners/{learner}/contexts", status_code=201)
async def create_context(learner: UUID, data: ContextRequest, tx: Transaction) -> dict[str, Any]:
    return await freeze_context(tx[0], learner, tx[1], data)


@router.get("/learners/{learner}/contexts/{identity}")
async def get_context(learner: UUID, identity: UUID, tx: Transaction) -> dict[str, Any]:
    return await read_context(tx[0], learner, tx[1], identity)
