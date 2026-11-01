"""Validated tutor intake. Structured summaries must not contain verbatim source passages."""

from datetime import date
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

Text = Annotated[str, Field(min_length=1, max_length=500)]
Task = Literal[
    "recognition",
    "controlled",
    "spontaneous",
    "input",
    "fluency",
    "discourse",
    "strategy",
    "project",
]
Assistance = Literal["independent", "supported", "unknown"]


class Intake(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Assessment(Intake):
    summary: Text
    assessed_on: date
    source: Literal["tutor_estimate", "formal_assessment"]
    level: Literal["A2", "B1", "B2"]
    uncertainty: Literal["provisional", "confirmed"]


class Profile(Intake):
    alias: Annotated[str, Field(min_length=1, max_length=80)]
    adult_confirmed: Literal[True]
    learner_opt_in: Literal[True]
    upload_permission: Literal[True]
    assessment: Assessment
    goals: Annotated[list[Text], Field(min_length=1, max_length=10)]
    preferred_domains: Annotated[list[Text], Field(min_length=1, max_length=10)]


class ProfileWrite(Intake):
    expected_revision: Annotated[int, Field(ge=0)] = 0
    profile: Profile


class Source(Intake):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)
    id: UUID
    expected_revision: Annotated[int, Field(ge=0)] = 0
    kind: Literal["lesson", "homework", "actual_use"]
    occurred_at: AwareDatetime | None
    qualification: Literal["tutor_notes", "transcript", "homework_submission", "tutor_report"]
    raw_text: Annotated[str, Field(max_length=100_000)] | None = None


class Count(Intake):
    correct: Annotated[int, Field(ge=0, le=10000)]
    opportunities: Annotated[int, Field(ge=0, le=10000)]

    @model_validator(mode="after")
    def valid_counts(self) -> Self:
        if self.correct > self.opportunities:
            raise ValueError("Correct counts cannot exceed opportunities")
        return self


class Observation(Intake):
    id: UUID
    expected_revision: Annotated[int, Field(ge=0)] = 0
    source_id: UUID
    # A stable response identity, reused across imports, prevents counting one answer twice.
    response_ref: Text
    subskill: Text
    task: Task
    task_ref: Text
    assistance: Assistance
    confirmed: bool
    withdrawn: bool = False
    accuracy: Count | None = None
    required_use: Count | None = None
    avoidance: Count | None = None
    completion: Count | None = None


class Activity(Intake):
    id: UUID
    expected_revision: Annotated[int, Field(ge=0)] = 0
    source_id: UUID
    activity_ref: Text
    kind: Literal["assignment", "encounter", "attempt", "checked_outcome"]
    occurred_at: AwareDatetime | None
    amount: Annotated[float, Field(ge=0, le=100000, allow_inf_nan=False)] | None = None
    purpose: Text
    subskill: Text | None = None
    material_ref: Text | None = None
    task: Task
    task_ref: Text
    assistance: Assistance
    confirmed: bool
    withdrawn: bool = False
    observation_id: UUID | None = None
    observation_revision: Annotated[int, Field(ge=1)] | None = None
    outcome: Literal["met", "partially_met", "not_met", "unknown"] | None = None
    criterion_ref: Text | None = None

    @model_validator(mode="after")
    def complete_reference(self) -> Self:
        if (self.observation_id is None) != (self.observation_revision is None):
            raise ValueError("Observation references need both identity and revision")
        if self.kind == "checked_outcome":
            if self.observation_id is None and (self.outcome is None or self.criterion_ref is None):
                raise ValueError(
                    "A checked outcome needs observed counts or a qualitative criterion/result"
                )
        elif (
            self.observation_id is not None
            or self.outcome is not None
            or self.criterion_ref is not None
        ):
            raise ValueError("Only a checked outcome may reference a result")
        return self


class ContextRequest(Intake):
    subskills: Annotated[list[Text], Field(max_length=20)] = []
    purposes: Annotated[list[Text], Field(max_length=20)] = []
