# Stage 1 executor completion audit

2 November 2026. Base `a004bdd`; result is the uncommitted working tree identified
by [input-snapshot-v2.json](input-snapshot-v2.json). This audit checks the requested
Stage 1 barrier, not readiness for a real learner pilot or completion of every
later scenario in HG-0003/HG-0007.

| Required result | Authoritative current evidence |
| --- | --- |
| Small coherent blocks, existing workflow and preserved sources | [Stage 1 record](../../stage-1.md), HG-0003 tasks/checks, original v1/v2 reports and independent review history. Product Decisions.md and Architecture.md are unchanged. The pre-existing Implementation Plan.md edit and separately appearing Plan_High_Level.md remain outside this task's edits. |
| Two tutors, actual login, invite-only identity and CSRF | `test_auth.py`: four actual Keycloak authorization-code/PKCE and PostgreSQL session checks. `test_every_learner_operation_is_owned_and_csrf_protected` exercises all learner routes with another tutor. |
| Assessment, preferences, adult/learner/upload permission and source qualification | Profile save/read/revision, explicit false-permission rejection and no-extra-contact-field cases use real API/PostgreSQL. Lesson notes need no transcript. |
| Runtime database isolation | `test_all_child_tables_enforce_database_rls`: all seven populated learner tables return zero rows for the second tutor and an unset tenant context; a cross-owner child insert is rejected with PostgreSQL SQLSTATE42501. |
| Persistence succeeds before HTTP success | `test_commit_failure_never_returns_http_success`: actual deferred PostgreSQL trigger failure produces sanitized HTTP 500 and rolls back both new learner/profile records. Dependency uses FastAPI function scope, with a compatible declared minimum. |
| Three distinct performance measures and qualified trends | Sixteen pure metric cases cover zero/unknown counts, two/three-session and four/five-opportunity thresholds, exact ±0.15 and 0.85 boundaries, mixed trends, completion, task/assistance distinction and date/selection boundaries. Persisted selection checks confirm latest four lessons/four homework submissions before subskill filtering. |
| Independent activity facts without fabricated performance | Actual intake/history cases preserve assignment-only and encounter-only facts, nullable dates/amounts, pending reports and qualitative checked fluency/project outcomes. Actual-use facts create no performance observation or inferred rates. |
| Corrections, deduplication and immutable frozen selection | Stable source sessions retain metadata revisions; duplicate response/activity identities conflict; identical retries add no revisions; pending edits retain prior confirmation; confirmed corrections/withdrawals affect only new context. Source/observation/activity revisions remain in earlier snapshots. |
| Relevant cumulative context separate from recent rates | Historical facts outside 90 days leave recent selected IDs/counts unchanged. Exact purpose/subskill filters use OR and display the 200-fact limit and omissions. Goal-led facts need no invented subskill. |
| Source expiry, minimization and physical cleanup | Actual current/history version expiry guards hide raw text before cleanup; cleanup physically clears both current/history bodies. Snapshots contain structured facts/references, no raw notes, and reread source-version availability. Metadata-only source edits preserve the expiry deadline. |
| Inactivity and owner deletion | Reads/polling do not refresh activity; 12 calendar months of inactivity block normal access. Operator cleanup and owner deletion both physically remove implemented child records. A real waiting write cannot recreate deleted data. |
| Safe responses/logging | All responses use no-store; validation/database/commit failures return fixed bodies. Sentinel inputs and exception text stay out of captured routine logs. |
| Reproducible local setup/checks | `just setup`, `just auth-up` and `just migrate` ran successfully. [check-v2.txt](check-v2.txt): Ruff format/lint, strict mypy and 26 unit tests pass. [integration-v2.txt](integration-v2.txt) and [JUnit](integration-v2.xml): 28 real integration cases pass, no failures/errors/skips. Declared input hashes were compared before native import. |
| Affected document/configuration checks | Affected links exist; registry/realm JSON, provisioning Python and launcher syntax pass; `git diff --check` passes. [Registry v2](registry-v2.json) has no structural/link error; its three `BudgetNotAgreed` findings remain unknown rather than PASS. |

## Evidence history and limits

V1 is preserved. Its 26 unit/21 integration passes predate later review fixes and are
not current confirmation. Independent v1 NO_GO reviews identified missing cache
controls, inactive deletion, child-policy coverage, commit ordering, qualitative
results and evidence drift. V2 checks include their fixes and additional cases.

Twelve HG-0003 automatic bindings were imported from the actual v2 JUnit report
using pre-run snapshots; [native-import-v2.json](native-import-v2.json) preserves
the CLI results. HG-0003-C9 remains a manual future-stage gap: approving/copying an
actual generated artifact cannot be exercised before stages 3–4 implement it.
The current intake/context checks establish evidence independence, not those
future actions. HG-0007's future graph/worker/checkpoint, exporter/provider and
backup obligations remain open. No full native integration or acceptance is claimed.

The initialization survey remains historically completed with stale source hashes
from later project changes; [survey-v1.json](survey-v1.json) is unknown, not fresh
initialization certification. Task evidence and current independent review own
this implementation. Document budgets are still unagreed; no ceiling was invented.

Automatic approval review rejected running `just cleanup` on the fixed existing
development database because it could permanently delete pre-existing records.
That command was not executed or bypassed. The same cleanup operation is verified
against disposable real PostgreSQL databases, including physical deletion of both
raw-source versions and inactive learner stores. No production/real-account secrets
were inspected. Generated disposable Keycloak credentials are used internally by
the fixture, never displayed or included in reports/snapshots.

No learner-management HTML form, real-learner activation, teaching-quality/model
experiment, production HTTPS/provider terms, backup deletion, deployment, push,
commit or human acceptance is part of this result. The local interface is JSON
with browser OIDC. Separate authorization is required for a local commit.

Independent re-review is complete: [security/privacy GO](review-security-v2.md)
and [contract/maintainability GO](review-contract-v2.md) both confirm the implemented
Stage 1 scope and unchanged current inputs. They do not accept the product or
close later-stage specification obligations.
