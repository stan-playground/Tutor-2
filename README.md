# Tutor Copilot

This repository prepares a tutor-facing assistant, with delivery priority homework → post-lesson feedback → lesson planning → urgent replanning. [Product Decisions.md](<Product Decisions.md>) owns product scope and distinguishes owner-confirmed priorities, delegated defaults, historical decisions and estimates. These describe intent, not implementation or measured results.

## Current structure

Stage 0 implements a local synthetic development foundation: an installed Python package, FastAPI health endpoints, a separate worker startup shell, PostgreSQL/pgvector migrations, disposable Redis, safe console observations and real checks. [Stage 0](docs/stage-0.md) records scope and evidence. Learner intake, authentication, generation, queue processing and graph execution remain future work. Architecture.md records the broader design; production deployment and provider integrations remain unverified.

- [Product Decisions.md](<Product Decisions.md>): product priorities, delegated pilot defaults and deferred scope; preserve their provenance and evidence limits.
- [Architecture.md](Architecture.md): proposed framework, storage, human-review and caching choices with trade-offs.
- [Implementation Plan.md](<Implementation Plan.md>): high-level delivery order, dependencies and completion barriers.
- [Repository Structure.md](<Repository Structure.md>): target package responsibilities and developer tools; add modules only with their first working operation.
- `src/tutor_copilot/`, `migrations/`, `tests/`: implemented local startup, migration and verification boundaries.
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

Run from the repository root. Application development requires Python 3.12, uv, Just and Docker Compose with a running Docker engine. The locked dependencies and service image digests define the tested set. Initial setup downloads public packages/images; runtime uses loopback ports 8000, 55432 and 56379. Services use local trust access and synthetic data only. No credentials or `.env` loading are configured.

```bash
just                 # List recipes; starts nothing.
just setup           # uv sync --locked; does not install Git hooks.
just up              # Start PostgreSQL and Redis, waiting for health checks.
just migrate         # Migrate the fixed local development database.
just check           # Ruff formatting/lint, strict mypy, deterministic unit checks.
just integration     # Actual API/PostgreSQL/Redis/worker checks; no paid providers.
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

The live endpoint returns `{"status":"alive"}`. Readiness returns HTTP 200 with `ready` when PostgreSQL, migration `0001`, pgvector and Redis are available. Redis failure yields HTTP 200 `degraded`; database/schema failure yields HTTP 503 `unavailable`. Each HTTP request has a fresh `X-Correlation-ID` matching its console observation. Logs contain only fixed metadata fields, never paths, query strings, headers, bodies or exception text. No Langfuse exporter/model client is installed yet.

Integration tests create random `tc_test_<uuid>` databases and temporary Redis keys and remove them afterward. They never downgrade the application database or flush Redis. Services must be running; unavailable services fail the checks. If a test process is forcibly killed, its temporary database may need operator cleanup. `just down` stops services and retains the PostgreSQL volume. Redis has no persistence and its contents are disposable. `just format` deliberately formats Python files. The optional `.pre-commit-config.yaml` invokes the same locked Ruff tools; hooks are not installed automatically. Evaluation recipes wait for a prepared experiment target.

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

`git diff --check` checks tracked changes; review new untracked files too before committing. Application checks above verify the implemented stage-0 boundaries; they do not establish later product scenarios or teaching quality.

To open the project UI on this Mac, run:

```bash
sh "HighGrade UI.sh"
```

The launcher starts a local server and opens the browser; Ctrl+C stops the server. The Windows `.cmd` launcher is generated for portability, but Windows execution is not verified here.

## Evidence and next work

Keep significant original check reports and any unrecoverable inputs with the relevant task. When a native change exists, use `specs/changes/<ID>/evidence/`; retain the originals while current results, review, decisions or delivery depend on them. Ordinary setup checks need no duplicate permanent report set: the survey records their outcomes. Temporary diagnostics belong in `.highgrade/local/` and are not delivered automatically. Before an authorized handoff, verify required reports and links are included; do not upload automatically or delete the only needed evidence.

Initialization did not create or migrate product specifications. HG-0001/0002 record earlier documentation changes; [HG-0009](specs/changes/HG-0009/spec.json) records the feedback product update. [HG-0010](specs/changes/HG-0010/spec.json) drafts post-lesson feedback after the homework foundation for adult A2–B2 English learners. None implements application behavior. For later work, use `$highgrade-task`, `$highgrade-spec` for agreed changed requirements, and `$highgrade-work` within the request's authority.

[HG-0011](specs/changes/HG-0011/spec.json) aligns the four major design documents and unimplemented application drafts with cumulative learning history/on-request review and teaching routes beyond visible errors (PD-39/40). Recent performance measures remain distinct from historical context; no scheduler, student app or automated audio assessment is introduced.
