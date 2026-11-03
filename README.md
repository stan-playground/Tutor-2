# Tutor Copilot

This repository prepares a tutor-facing assistant, with delivery priority homework → post-lesson feedback → lesson planning → urgent replanning. [Product Decisions.md](<Product Decisions.md>) owns product scope and distinguishes owner-confirmed priorities, delegated defaults, historical decisions and estimates. These describe intent, not implementation or measured results.

## Current structure

Stages 0–2 implement a local synthetic development foundation, tutor-owned learner evidence and reviewed teaching retrieval: FastAPI, a separate worker startup shell, PostgreSQL/pgvector, disposable Redis, local Keycloak login, learner/profile/source intake, confirmed observation/activity revisions, recent performance, frozen cumulative context and data cleanup. [Stage 0](docs/stage-0.md) and [Stage 1](docs/stage-1.md) record scope and evidence. [Stage 2](docs/stage-2.md) adds private reviewed material versions, operator shared-bank publication, controlled local-model/pgvector retrieval and disposable query-vector caching. Generation, queue processing and graph execution remain future work. Architecture.md records the broader design; production deployment and real-learner activation remain unverified.

- [Product Decisions.md](<Product Decisions.md>): product priorities, delegated pilot defaults and deferred scope; preserve their provenance and evidence limits.
- [Architecture.md](Architecture.md): proposed framework, storage, human-review and caching choices with trade-offs.
- [Implementation Plan.md](<Implementation Plan.md>): high-level delivery order, dependencies and completion barriers.
- [Repository Structure.md](<Repository Structure.md>): target package responsibilities and developer tools; add modules only with their first working operation.
- `src/tutor_copilot/`, `migrations/`, `tests/`: implemented local startup, authentication, evidence/history, lifecycle and verification boundaries.
- `dev/keycloak/`: non-secret synthetic realm template and disposable credential preparation; generated credentials stay ignored and are never printed by commands/tests.
- [evaluation/README.md](evaluation/README.md): two draft synthetic fixtures and reviewer assignments; no approved gold or model-quality result.
- [Initial specifications](specs/README.md): draft homework-pilot contracts, including the [dataset specification](specs/datasets.md).
- [AGENTS.md](AGENTS.md): engineering rules, task routing and authority.
- [HighGrade project instruction](.highgrade/project/INSTRUCTIONS.md): local adaptation and delivery boundaries.
- [Document registry](.highgrade/project/documents.json): document roles and explicitly unagreed size budgets.
- [Initialization survey](.highgrade/project/survey.json): observed setup state and history; not a product backlog.
- [Native specification catalog](specs/catalog.json): scoped changes tracked through HighGrade; the product descriptions remain in Product Decisions.md.
- `HighGrade UI.sh` / `HighGrade UI.cmd`: generated launchers for the globally installed HighGrade UI.
- `.highgrade/local/`: ignored temporary inputs, reports and continuation. Keep permanent project records outside it.

This README owns purpose/navigation, current structure and reproducible commands. AGENTS owns agent/engineering rules; Architecture.md owns design recommendations; the implementation plan coordinates delivery order; native specifications own their requirements and evidence.

## Local commands

Run from the repository root. Application development requires Python 3.12, uv, Just and Docker Compose with a running Docker engine. The locked dependencies and service image digests define the tested set. Initial setup downloads public packages/images; runtime uses loopback ports 8000, 55432, 56379 and 58080. PostgreSQL uses local trust access and synthetic data only. No `.env` loading is configured. Keycloak preparation generates disposable synthetic login credentials under ignored `.highgrade/local/keycloak/`, with restrictive file permissions; commands and tests never display them or access existing account secrets.

```bash
just                 # List recipes; starts nothing.
just setup           # uv sync --locked; does not install Git hooks.
just up              # Start PostgreSQL and Redis, waiting for health checks.
just auth-up         # Prepare synthetic identities and start Keycloak; wait for readiness.
just embeddings-prepare # Download the pinned public embedding model anonymously; no API key.
just migrate         # Migrate the fixed local development database.
just check           # Ruff formatting/lint, strict mypy, deterministic unit checks.
just integration     # Actual API/PostgreSQL/Redis/worker/Keycloak checks; no paid providers.
just cleanup         # Physically purge expired source bodies/sessions and inactive learners.
```

Start the two roles in separate terminals:

```bash
just web
just worker
```

Both stop with Ctrl+C. The worker checks startup dependencies and waits for shutdown; it does not yet process preparation jobs. For a startup check that exits, and HTTP checks while the web role runs:

```bash
UV_CACHE_DIR=.uv-cache uv run --locked tutor-worker --check
curl -i http://127.0.0.1:8000/health/live
curl -i http://127.0.0.1:8000/health/ready
```

The live endpoint returns `{"status":"alive"}`. Readiness returns HTTP 200 with `ready` when PostgreSQL, migration `0005`, pgvector and Redis are available. Redis failure yields HTTP 200 `degraded`; database/schema failure yields HTTP 503 `unavailable`. Keycloak failure is reported by login as HTTP 503; startup readiness checks database/cache only. Each HTTP request has a fresh `X-Correlation-ID` matching its console observation. Logs contain only fixed metadata fields, never paths, query strings, headers, bodies or exception text. No Langfuse exporter or generation-model client is installed yet; Stage 2 uses a local embedding model.

The Stage 2 bank/search surface is also JSON: `POST /teaching-assets`, `GET`/`DELETE /teaching-assets/{id}` and `POST /teaching-search`. Tutor imports stay private; `UV_CACHE_DIR=.uv-cache uv run --locked tutor-bank-publish FILE` is an explicit local operator command requiring qualified review and separate sharing permission. Prepare the pinned public model before importing reviewed available material or searching; runtime never downloads weights. [Stage 2](docs/stage-2.md) describes fields, methods, outcomes and synthetic verification.

The Stage 1 surface is an authenticated JSON API; a learner-management browser form is not yet implemented. [Stage 1](docs/stage-1.md#http-operations) lists operations and revision/confirmation rules. Browser login starts at `http://127.0.0.1:8000/auth/login`; `/auth/me` returns the session's CSRF token. All writes require `X-CSRF-Token`. The app cookie uses an explicit HTTP-loopback development exception, with HttpOnly, SameSite=Lax, server sessions and CSRF; production HTTPS configuration is not implemented. Keycloak's two synthetic invited subjects are seeded by migration. Automated login tests consume generated credentials internally; public registration and an administrator are disabled. The provider container has no persistent realm volume. Keep this configuration local and synthetic.

Integration tests create random `tc_test_<uuid>` databases and temporary Redis keys and remove them afterward. They never downgrade the application database or flush Redis. Run `just up` and `just auth-up` first; unavailable services fail the checks. If a test process is forcibly killed, its temporary database may need operator cleanup. `just down` stops all three services and retains the PostgreSQL volume. Redis and Keycloak have no persistence and are disposable. `just cleanup` uses the fixed local maintenance account; request handling uses the restricted `tutor_app` role with row-level security. No cleanup daemon is installed: run cleanup at least daily while synthetic services are active. Expiry guards block reads before cleanup. `just format` deliberately formats Python files. The optional `.pre-commit-config.yaml` invokes the same locked Ruff tools; hooks are not installed automatically. Evaluation recipes wait for a prepared experiment target.

HighGrade checks require Git, Python 3 and the installed global HighGrade CLI. They do not require Cargo/OpenSpec or model providers.

Resolve the active CLI instead of pinning a release path:

```bash
hgExe="$(python3 -c 'import json,pathlib; p=pathlib.Path.home()/".highgrade/global"; print(p/"releases"/json.loads((p/"active.json").read_text())["release"]/"highgrade")')"
```

Then check installation, local compatibility, registered documents and the saved survey:

```bash
"$hgExe" global-status --profile "$HOME"
"$hgExe" doctor --root "$PWD"
"$hgExe" inspect --root "$PWD" --registry .highgrade/project/documents.json
"$hgExe" survey-check --root "$PWD"
git diff --check
sh -n "HighGrade UI.sh"
python3 -m json.tool .highgrade/project/documents.json > /dev/null
python3 -m json.tool .highgrade/project/survey.json > /dev/null
```

Read the report as well as the exit code: `1` is failed and `2` is unknown. Document/route budgets remain unagreed, so registry inspection reports `BudgetNotAgreed`; this is not a successful budget check. Doctor may report missing Cargo/OpenSpec from its legacy probe before connection. Neither is required for this repository's documentation work or native HighGrade route. Investigate other findings rather than treating every unknown as harmless.

The registry checks the process documents. The product analysis remains outside that lint scope: its two original absolute provenance links are unsupported by HighGrade's link checker. The initialization survey preserves its historical hash; current task evidence records later edits. Check the exact source paths separately before using the originals, and record unavailable targets as gaps. A passing process-link check does not establish source-document accessibility or re-audit their content.

`git diff --check` checks tracked changes; review new untracked files too before committing. Application checks above verify the implemented stage-0/1/2 boundaries; they do not establish later product scenarios or teaching quality.

To open the project UI on this Mac, run:

```bash
sh "HighGrade UI.sh"
```

The launcher starts a local server and opens the browser; Ctrl+C stops the server. The Windows `.cmd` launcher is generated for portability, but Windows execution is not verified here.

## Evidence and next work

Keep significant original check reports and any unrecoverable inputs with the relevant task. When a native change exists, use `specs/changes/<ID>/evidence/`; retain the originals while current results, review, decisions or delivery depend on them. Ordinary setup checks need no duplicate permanent report set: the survey records their outcomes. Temporary diagnostics belong in `.highgrade/local/` and are not delivered automatically. Before an authorized handoff, verify required reports and links are included; do not upload automatically or delete the only needed evidence.

Initialization did not create or migrate product specifications. HG-0001/0002 record earlier documentation changes; [HG-0009](specs/changes/HG-0009/spec.json) records the feedback product update. [HG-0010](specs/changes/HG-0010/spec.json) drafts post-lesson feedback after the homework foundation for adult A2–B2 English learners. None implements application behavior. For later work, use `$highgrade-task`, `$highgrade-spec` for agreed changed requirements, and `$highgrade-work` within the request's authority.

[HG-0011](specs/changes/HG-0011/spec.json) aligns the four major design documents and unimplemented application drafts with cumulative learning history/on-request review and teaching routes beyond visible errors (PD-39/40). Recent performance measures remain distinct from historical context; no scheduler, student app or automated audio assessment is introduced.
