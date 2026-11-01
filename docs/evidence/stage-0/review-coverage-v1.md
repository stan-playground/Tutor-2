# Stage-0 milestone and evidence review

Verdict: **GO** for the local synthetic stage-0 foundation. No blocking finding in this review scope. This is independent technical review, not human acceptance, fixture-label approval, product readiness or commit authority.

Reviewed on 1 November 2026 against the current uncommitted implementation and the 23 causal file hashes in [inputs-v2.json](inputs-v2.json). I recomputed every declared hash and confirmed that all matched. I read the HighGrade independent review method before assessing the result. The runtime/privacy review is separate.

## Coverage and claims

- The first milestone is the stage-0 row in [Implementation Plan.md](<../../../Implementation Plan.md>), not stage 1's authenticated learner intake. The implementation provides an installed package and lockfile, real Just targets, local PostgreSQL/pgvector and Redis, migration `0001`, both process entry points and safe observation boundaries. README and the stage record explicitly limit the worker to startup/shutdown; queue and graph behavior are not represented as implemented.
- [Justfile](../../../Justfile) uses actual commands. Its default lists recipes. The routine check has no migration, service startup, model/embedding call or Langfuse write. The documented integration command exercises actual services, creates random test databases and removes only those databases and its own keys. No evaluation recipe pretends that an experiment target exists.
- [evaluation/README.md](../../../evaluation/README.md) correctly describes two initial draft items rather than complete family coverage or approved gold. Both items have actual synthetic input, explicit nonempty expectations, immutable source/state references and review assignments `1`/`2`, matching the owner's reply. Neither fabricates reviewer qualifications, review decisions or approval. Schema and collection tests check structural rules; they make no claim to perform the unimplemented arithmetic, source selection, pedagogical review or release admission.
- The scope avoids learner-linked persistence, real-data access, providers and deployment. Full HG-0003/0007/0008 scenarios remain open. Product Decisions.md is not changed by this task. The separate Implementation Plan.md link-formatting edit remains outside the reviewed implementation scope.

## Verification reviewed

- I independently ran `just check`: Ruff formatting and lint passed, mypy found no issues in nine source files, and all nine unit checks passed in 0.64 seconds with no warnings.
- [integration-v2.xml](integration-v2.xml) and [integration-v2.txt](integration-v2.txt) report six executed checks, zero failures/errors/skips. I compared their assertions with migration round-trip/vector operation, pre/post-migration API readiness, actual Redis TTL and no-persistence configuration, bounded cache outage, unmigrated-worker refusal and worker shutdown.
- [process-v2.json](process-v2.json) and the original [web](web-process-v2.txt)/[worker](worker-process-v2.txt) outputs show the actual console entry points, ready HTTP, response/log correlation and lifecycle completion. The synthetic request's path/query/body/header text is absent from the stored console outputs.
- The original [process-v1 failure](process-v1-failure.json) and logs remain visible. Accepting Uvicorn's SIGTERM exit in v2 is justified by the installed server's signal re-raise behavior and the added post-cleanup observation; it does not weaken a product requirement or disguise the prior failed assertion.
- Public dependency resolution is locked, service images are digest-pinned, and current API/tool documentation was checked during implementation. The final test-client dependency no longer produces the earlier deprecation warning. The real test results establish compatibility only for the tested local Python 3.12/macOS environment.
- HighGrade inspection reports only explicitly unagreed budgets after source ownership/caches were classified. The historical survey remains structurally valid and stale, as the stage record states. Neither result is misreported as application verification.

## Limits

I inspected the existing real-service reports rather than rerunning those service exercises in this coverage review. I independently reran deterministic checks and verified report input freshness. Fresh service initialization and original package installation were observed in the executor's tool history; I did not create another environment or remove the retained development volume. Actual qualified-tutor review, all future product contracts, real provider/processor behavior, production deployment and Windows execution remain unverified. None is a stage-0 completion claim.

Recommended next action: combine this verdict with the separate runtime review, resolve any runtime findings, then present the stage-0 result for the owner's separate commit decision. The next product implementation block is stage 1's authenticated learner-save operation under HG-0003/0007.
