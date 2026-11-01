# Tutor Copilot — Repository Structure Plan

Plan only · 1 November 2026

Use one Python package for the web application and LangGraph worker. Finish homework first, then post-lesson feedback, then lesson planning and urgent replanning. Homework and feedback share learner evidence, subskill calculations, persistence and exact tutor approval; they do not need separate agent frameworks or services.

PD-39/40 extend those responsibilities with source-qualified cumulative activity facts and teaching routes beyond visible errors. Add them to the existing modules as working slices, without a scheduler, separate memory store, student app or automatic audio-assessment package.

[Product Decisions](<Product Decisions.md>) owns scope, [Architecture](Architecture.md) owns system design, [Implementation Plan](<Implementation Plan.md>) owns delivery order, and the [native specifications](specs/README.md) own requirements. This document proposes file ownership and developer commands. It creates no application, configuration, runnable recipe or tested dependency set.

## 1. Grow a small package

The following is a target map, **not a scaffold to create now**. Add a module only with the first working slice that needs it. Keep small related operations together; split a file when its real responsibilities require it.

```text
Legend2/
├── README.md                         # verified setup and command entry point
├── Product Decisions.md
├── Architecture.md
├── Implementation Plan.md
├── Repository Structure.md
├── AGENTS.md
├── specs/                            # native requirements and dataset contracts
├── pyproject.toml                    # dependencies and shared tool settings
├── uv.lock                           # reviewed, reproducible dependency resolution
├── Justfile                          # developer command entry point
├── .pre-commit-config.yaml
├── compose.yaml                      # local PostgreSQL/pgvector and Redis
├── alembic.ini
├── migrations/                       # reviewed application schema revisions
├── src/tutor_copilot/
│   ├── __init__.py
│   ├── web.py                        # FastAPI routes, session/access boundary
│   ├── worker.py                     # claim queued work; run/resume graph
│   ├── settings.py                   # validated process configuration
│   ├── db.py                         # engines/pools and transaction setup
│   ├── models.py                     # application relational metadata
│   ├── schemas.py                    # typed history facts, purpose/routes and artifacts
│   ├── evidence.py                   # intake, activity facts, cumulative views, snapshots
│   ├── metrics.py                    # deterministic rates and qualified trends
│   ├── retrieval.py                  # authorized material search and cache bypass
│   ├── homework.py                   # current/revisit purposes, routes and composition
│   ├── feedback.py                   # post-lesson feedback composition; add second
│   ├── validation.py                 # route/source criteria and applicable solution checks
│   ├── review.py                     # exact decisions, revisions and approved output
│   ├── graph.py                      # explicit job routes, durable waits and revisions
│   └── templates/                    # server-rendered tutor interface
├── tests/
│   ├── unit/                         # real calculations and local validation rules
│   └── integration/                  # API, PostgreSQL, checkpoint and Redis boundaries
└── evaluation/
    ├── homework/                     # planned homework fixtures/rubrics/manifests
    ├── feedback/                     # separate reviewed feedback cases when introduced
    └── calibration/                  # human judge labels with job/source-aware splits
```

Keep the existing HighGrade files and launchers. Do not replace native JSON with a second handwritten backlog. `evaluation/` will hold synthetic inputs, rights-cleared teaching fixtures, rubrics and versioned manifests; `specs/datasets.md` remains their construction contract, not a folder of approved gold.

The `src/` layout separates installed application imports from repository tooling. A flat package avoids premature `domain/ports/adapters` layers and generic repositories. Directly import the needed operation; add no base agent, plugin registry or universal model-provider wrapper.

## 2. Two jobs, shared records and review

`web.py` authenticates the tutor, resolves learner ownership and saves the selected job. `worker.py` loads that request and invokes `graph.py`. The graph uses shared evidence/metric functions, dispatches to `homework.py` or `feedback.py`, validates the resulting artifact and pauses for tutor decisions through `review.py`.

`evidence.py` owns tutor intake/confirmation of independent assignment, encounter, attempt and checked-outcome facts, linked to sources/observations with corrections and deduplication. Drafts/approval/copying are not actual-use evidence. It loads recent observations and retained relevant activity facts directly, derives separate qualified cumulative context and freezes selected revisions. `metrics.py` keeps PD-08/09's recent selection/count/rate/trend meaning; a cumulative view never widens its denominators or becomes editable model memory.

`homework.py` selects explained important-now/worth-revisiting purposes and PD-40 routes from goals/recent evidence/history, with no compulsory split or invented error. `schemas.py` permits purpose/outcome, route, demands/support, criteria, modality, relevant skills and optional confusion; remediation still needs its actual confusion. `retrieval.py` constructs controlled descriptions/filters and searches authorized reviewed input/activity/task-framework versions. The chat model informs teaching choices without SQL/search authority. `validation.py` checks accessibility, recording/criteria correspondence and route-specific outcomes; independent solving applies to closed answers. These are existing-module responsibilities, not a module/class per route. See [Architecture section 6](Architecture.md#6-the-data-model-and-retrieval-boundary).

Homework uses reviewed input, activities, explanations and task frameworks to compose useful sections. Listening references available permitted recordings with matching reviewed criteria; this is no learner-recording/audio-scoring pipeline. [HG-0010 feedback](specs/changes/HG-0010/spec.json) uses the selected authorized current transcript and frozen recent/cumulative references for supported findings, recent comparisons and qualified continuity context. Notes/history cannot replace a missing/expired current transcript. Generation/review/export cannot create activity facts, confirm observations or update counts/trends/preferences. Tutor actual-use intake stays separate. Approved student sections remain manually handed off; private notes stay separate. No prior homework, exercise, duration, automatic grading or delivery is required.

Keep job-specific output schemas and rubrics explicit inside the shared modules. Reuse the actual evidence, ownership and approval operations, rather than forcing feedback into an exercise/key schema. One graph may select different composition/validation branches; no separate supervisor or second persistence framework is needed. Graph checkpoints hold execution references; relational records remain authoritative for evidence, decisions and approved artifacts.

Add feedback fixtures and stage/end-to-end evaluation membership separately. Homework's twelve golden families do not establish feedback quality. Defer feedback activation until its own reviewed coverage and the common safety/privacy/review boundaries pass.

Place required cumulative-history and every enabled non-error-route variant/isolated case in the existing `evaluation/homework/` area; feedback includes cumulative-context/no-history-write cases in its own area. Preserve twelve homework base families while counting all required applicable items in gate denominators. These remain planned fixtures until authored and reviewed.

Pools, provider clients and the compiled graph live for each process; transactions and loaded recent/cumulative context live for an invocation. Persisted activity facts survive requests under the existing retention policy, and requests reference frozen revisions; there is no long-lived per-learner model session. Use bounded async I/O for independent external waits, keep dependent stages sequential and never share a database session across tasks. Threads are only for a necessary blocking parser; processes need measured CPU work.

## 3. Recommended tools

Just is explicitly requested. The remaining tools are recommendations; prior use of some tools is context, not a universal personal preference. Lock compatible versions when implementation begins.

| Tool | Purpose and trade-off |
| --- | --- |
| [uv](https://docs.astral.sh/uv/concepts/projects/) | One project environment and lockfile; put Ruff, mypy, pytest and pre-commit in a development dependency group. Plain venv/pip works but needs separate locking conventions. |
| [Ruff](https://docs.astral.sh/ruff/) | Linting and formatting in one tool; avoid adding Black/isort/Flake8 for the same duties. |
| [mypy](https://mypy.readthedocs.io/en/stable/) | Check typed application boundaries; do not silence genuine errors with a project-wide ignore. Pyright is an alternative, not an additional checker. |
| [pytest](https://docs.pytest.org/en/stable/) | Meaningful calculation, persistence and workflow tests. Add the async-test support needed by the actual selected tests, rather than a broad plugin bundle. |
| [pre-commit](https://pre-commit.com/) | Fast local formatting/lint checks using pinned tools; full integration/evaluation runs stay explicit. Hooks complement reproducible checks and do not grant commit authority. |
| [SQLAlchemy](https://docs.sqlalchemy.org/) + [psycopg](https://www.psycopg.org/psycopg3/docs/) + [Alembic](https://alembic.sqlalchemy.org/en/latest/) | Maintained relational access and migrations, without a custom database adapter. Plain psycopg is smaller for a few queries; SQLAlchemy metadata becomes useful for versioned records. Review autogenerated migrations. Checkpointer setup stays saver-owned; a shared database does not make checkpoint/domain commits atomic. |
| [Docker Compose](https://docs.docker.com/compose/) | Reproduce local PostgreSQL with pgvector and disposable Redis. Native services remain an alternative. Use isolated test databases; Redis keeps the architecture's cache-only/no-persistence policy. |

## 4. Future Justfile command contract

**None of these recipes exists or has passed now.** Implement and document each when its real target exists. Set the default recipe to list commands; running `just` must not start services, install hooks or call providers.

| Proposed recipe | Future effect |
| --- | --- |
| `just setup` | Synchronize the reviewed lockfile/dev environment with `uv sync --locked`; downloads may require network. Hook installation is a separate explicit step. |
| `just up` / `just down` | Start/stop local Compose dependencies; stopping does not delete database volumes. |
| `just migrate` | Apply reviewed migrations to an explicitly selected local database. Never infer a production target. |
| `just web` / `just worker` | Start the separate process roles from the same installed package. |
| `just format` | Run Ruff formatting; deliberately changes source files. |
| `just check` | Read-only Ruff format/lint checks, mypy and local deterministic unit tests. No live model/embedding calls, remote Langfuse writes, migrations or service startup. |
| `just integration` | Run real API/database/checkpoint/cache tests against explicit disposable local services and synthetic data; no paid providers. |
| `just eval homework` / `just eval feedback` | Explicitly select the reviewed `homework` or `post_lesson_feedback` suite. Provider/embedding calls and Langfuse writes are explicit here; refuse an unknown/unprepared suite rather than run another job's gold. |

Keep recipe bodies thin: invoke the tool or actual operation rather than implement logic in shell. Use the same locked Ruff/tool versions in hooks and check recipes. `check` must fail for missing required tools/tests, not print a placeholder. Add exact commands to README only after verifying them. Context7 documentation checked for uv dependency groups/locked execution, Just recipes and Alembic migration candidates; this is documentation research, not a dependency compatibility test.

## 5. Data and first slice

Commit only synthetic/rights-cleared fixtures and necessary reviewed manifests. Keep uploads, raw learner sources, private exports, credentials, local database data and evaluation captures outside tracked fixture paths; exclusion from Git alone is not the application's retention/access control. Use metadata-only logs and sanitized errors. Do not add a private-data sample or inspect existing credentials to populate examples.

Start with the smallest web/worker startup, database migration and authorized learner-save operation from the implementation plan. Introduce its actual tests and commands, then add the next necessary module. Do not create all directories, empty tests, deployment scaffolds or feedback code from this diagram alone.
