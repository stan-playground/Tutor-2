# Stage 1 independent security/privacy review — revision 2

Reviewer: `/root/final_security_review` · 2 November 2026 (Europe/Belgrade)

Verdict: **GO for the implemented Stage 1 local synthetic security/privacy scope.**
The blocking findings in [revision 1](review-security-v1.md) are resolved with
current code and actual boundary evidence. This is not acceptance, a commit,
real-learner activation or complete HG-0003/HG-0007 integration.

## Inputs and evidence independently checked

Reviewed the Stage 1 requirements and relevant current tracked/new source,
migrations, non-secret Keycloak fixture/provisioning, HTTP handlers and tests
against base `a004bdd`, with the user's pre-existing Implementation Plan edit
preserved. No generated credentials, secrets or adjacent projects were read.

- Recomputed every hash in `input-snapshot-v2.json`: all **34 declared files
  match the current worktree**, with no drift. These cover executable source,
  migrations, tests, dependency/configuration files and the non-secret provider
  template/provisioning script.
- Read `check-v2.txt`: actual `just check` passed formatting, lint, strict mypy
  and **26 unit tests**.
- Read `integration-v2.txt` and independently parsed `integration-v2.xml`:
  **28 actual integration tests, zero failures, errors or skips**. The report
  contains the exact named regression cases discussed below.
- Inspected the native evidence import and its real check selectors. A native
  import is administrative evidence linkage; the original reports and test
  assertions establish what executed.

No full-suite rerun was needed for this review because current input hashes,
original successful reports and the relevant assertions are available. This
review did not modify implementation source.

## Findings resolved

1. **Inactive learners remain unavailable but their owner can delete them.**
   `lock_learner` in `src/tutor_copilot/evidence.py` keeps inactivity filtering by
   default and accepts an internal `allow_inactive` flag. Only the explicit
   owner deletion handler passes it (`intake.py:55`); ownership, RLS and row
   locking remain required. `test_owner_can_delete_inactive_learner_without_restoring_access`
   observes an inactive read returning 404, a successful authenticated DELETE
   and physical removal of populated learner/profile/source/activity stores.
   Existing cascade inventory tests cover all seven learner tables.

2. **The database boundary is verified beyond the application guard.**
   `test_all_child_tables_enforce_database_rls` populates all seven learner
   tables, including historical source revisions and frozen context. The real
   restricted role sees populated rows under the owner, zero rows under another
   tutor, and zero rows after transaction-local context resets. A second-tutor
   child INSERT referencing the first tutor's learner is refused with PostgreSQL
   SQLSTATE `42501`, rather than merely failing an unrelated FK assertion.

3. **Responses consistently prohibit caching.**
   `web.py:57` applies `Cache-Control: no-store` to every response, including
   sanitized failures. The current intake/lifecycle/error assertions verify it
   on private reads and expired/frozen source responses. This closes the missing
   server-side cache instruction identified during revision 1; it does not
   promise to erase copies a tutor deliberately saves outside the application.

## Additional changed boundaries checked

- Function-scoped request transactions (`intake.py:35`) complete before an HTTP
  success response. `test_commit_failure_never_returns_http_success` installs
  an actual deferred PostgreSQL constraint trigger, observes sanitized HTTP500,
  confirms rollback and verifies that private exception text never enters the
  response/log capture.
- Current and historical raw source copies are independently made unavailable
  after expiry and physically cleared by the real cleanup operation. The
  revised lifecycle case checks both stored bodies become null while qualified
  structured facts/context remain. Source-version availability is resolved again
  when reading a frozen context.
- Qualitative checked outcomes require criterion/result support without
  inventing numeric performance. The new persisted case retains an open-task
  result and an explicit unknown while confirming no recent rates are created.
  Assignment/encounter/attempt records cannot smuggle outcome fields through
  this schema.
- The earlier actual OIDC, invitation, PKCE/state/replay, CSRF/origin,
  logout/expiry/revocation, ownership, corrections/withdrawals, frozen revisions,
  deletion race and safe logging tests are included in the current successful
  run, rather than assumed from superseded reports.

## Scope and remaining limits

The fixed-loopback HTTP cookie exception and local PostgreSQL trust access are
explicitly limited to synthetic development. The review supplies no production
HTTPS/provider-terms, real-data, browser-engine, Windows or external deletion
evidence. It also does not prove statistical agent or teaching reliability.

The separate command which would run cleanup against the fixed application
database was rejected by automatic approval review and was not executed. No
bypass is part of this result. Its actual cleanup function and SQL effects are
verified against isolated real PostgreSQL databases; fixed-database CLI execution
must remain disclosed as unverified, not reported as a passed command.

HG-0003-S5's actual generation/approval/copying assertions remain for later stages
where those actions exist. HG-0007's future worker/checkpoint, exporter/provider
and backup lifecycle obligations remain open. They do not invalidate the verified
Stage 1 intake/history security slice, and this GO cannot close those broader
native contracts.

Independent security/privacy review is **complete** for the current Stage 1 slice.
