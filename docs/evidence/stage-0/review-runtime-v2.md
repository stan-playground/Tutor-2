# Independent runtime delta review — stage 0

Verdict: **GO** for the final local synthetic stage-0 foundation. This report preserves and updates review-runtime-v1.md; its unchanged scope limits still apply.

Reviewed on 1 November 2026. Compared inputs-v3.json with inputs-v2.json: the only changed causal files are src/tutor_copilot/web.py and tests/unit/test_web.py. All current v3 hashes match the working files; no drift was found.

The lifespan now emits `stopped` only after open_resources has exited successfully. This removes the previous possibility of a cleanup exception producing a successful-stop observation. The added cleanup-failure test injects an exception after the real resource context exits and checks that TestClient propagates that failure and that no stopped observation is emitted. The normal-lifecycle sentinel test still requires the matching stopped observation. Independently ran `UV_CACHE_DIR=.uv-cache uv run --locked pytest tests/unit/test_web.py -q`: all three affected tests passed.

Read the current original reports: local-check-v3.txt confirms Ruff formatting/lint, strict mypy and ten unit tests pass; integration-v3.xml/txt confirms the same six real-service checks pass with zero errors/failures/skips. Process-v3.json and web/worker-process-v3.txt confirm both actual entry points run and stop, response/log correlation matches, private query text is absent, and the tightened successful-cleanup observation is present before Uvicorn's expected SIGTERM exit. The unchanged payload logging boundary retains the broader original v2 process canary observation and the current exception/header/body/path/query/library sentinel unit check.

Also reviewed fresh-setup-v1.json/txt: the unchanged lockfile installed 53 packages into a new temporary environment, both modules imported, and the installed worker entry point reported ready against the local services. This uses an existing public-package cache (`--offline`), so it proves fresh environment installation and startup, not fresh network download availability. The web lifespan change does not alter dependency resolution or entry-point packaging.

No new blocking runtime, logging-privacy, lifetime or data-preservation finding. Service integration and fresh setup were assessed from the supplied current original reports rather than rerun independently. No production, full product-contract, human fixture-review, provider, acceptance or commit authority is implied.
