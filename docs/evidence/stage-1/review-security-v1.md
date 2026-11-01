# Stage 1 independent security/privacy review — revision 1

Reviewer: `/root/final_security_review` · 2 November 2026 (Europe/Belgrade)

Verdict: **NO_GO pending the two fixes/checks below and refreshed evidence.**

Scope: Stage 1's local synthetic Keycloak, application sessions, learner intake,
PostgreSQL ownership/RLS, source versions, evidence corrections/withdrawals,
frozen context, expiry, inactivity, explicit deletion and metadata-only logs.
Reviewed the relevant tracked diff and new implementation/tests against `a004bdd`,
AGENTS, README, the project instruction, HG-0003, Stage 1 in Implementation Plan,
PD-28/39 and the implemented portion of HG-0007. The user's pre-existing plan-link
edit remains present and is not part of this review's proposed changes.

## Required changes

1. **Allow the owning tutor to delete an inactive learner.**
   `src/tutor_copilot/intake.py:55` calls `lock_learner` for deletion, while
   `src/tutor_copilot/evidence.py:29` unconditionally requires activity within
   twelve months. Thus an owned inactive learner returns 404 to an explicit
   deletion request even while its records remain in PostgreSQL awaiting cleanup.
   PD-28 permits tutors to delete learners at any time. Keep inactive reads and
   ordinary writes unavailable, but allow the owner-only deletion lock to include
   inactive learners. Verify immediate removal of every implemented learner table
   through a real inactive-learner DELETE request.

2. **Verify child-table RLS as the independent database boundary.**
   `tests/integration/test_evidence.py:40` checks the restricted runtime role and
   cross-tutor visibility of `learners`. The cross-tutor HTTP tests stop at the
   learner ownership guard, so they cannot detect missing/broken child-table RLS.
   The policy loop in `migrations/versions/0002_evidence.py:70` appears correct,
   but the explicit architecture boundary needs direct real PostgreSQL evidence.
   Populate profiles, source history, observations, activities and contexts; show
   all seven learner tables are invisible to another tutor and to a connection
   without tutor context, and reject a cross-owner child insert. Reuse the pool
   so transaction-local context reset is exercised.

## Correction already made during review

Initially learner/source/context responses lacked a cache prohibition even though
logout, deletion and raw expiry revoke server access. The reviewer requested a
consistent `Cache-Control: no-store` boundary. The current `web.py:57` now adds it
to all responses, and intake/lifecycle/error assertions were added. This change
still needs the refreshed final report below; this review does not treat v1
execution as verification of later code.

## Evidence checked and freshness

- `check-v1.txt`: actual `just check`; 26 executed unit tests, formatting/lint and
  strict mypy passed.
- `integration-v1.txt` and `integration-v1.xml`: actual local integration run;
  independently parsed JUnit reports 21 tests, zero failures, errors or skips.
  The named cases cover actual Keycloak authorization-code/PKCE login, invite
  refusal, CSRF/state/replay/logout/session expiry, isolated PostgreSQL, Redis,
  worker startup, source corrections, confirmed withdrawals, frozen references,
  expiry/cleanup, inactivity, deletion concurrency and log sentinels.
- `input-snapshot-v1.json`: 34 declared causal files. Recomputed hashes show
  drift in `web.py`, `test_intake.py`, `test_lifecycle.py` and `test_web.py` as
  review fixes develop. A refreshed snapshot and affected successful checks are
  required before final GO. No generated credentials or other secrets were read.

No implementation source was changed by this reviewer. This is an independent
code/evidence review, not a browser-engine test or a rerun of the full suite.

## Confirmed design boundaries and limits

The runtime engine uses the restricted local `tutor_app` role; tenant context is
transaction-local and application queries also enforce learner ownership. Input
cannot select tutor identity or SQL table names. Authlib handles the OIDC
protocol; exact issuer/subject invitations, one-use pending state, random opaque
server sessions, token hashes, HttpOnly/SameSite cookies and CSRF checks form the
implemented local boundary. HTTP cookies and PostgreSQL trust access are an
explicit fixed-loopback synthetic-development exception, not production security.

Raw text is kept in expiring source/current-history stores, not copied by the
implementation into contexts. Source metadata corrections preserve stable session
identity and metadata-only edits preserve the content deadline. Frozen contexts
resolve availability for exact source revisions. Confirmed withdrawals are
filtered after latest-confirmed selection. Explicit request deletion takes the
learner lock before cascading through implemented stores, and the real waiting
write check shows it cannot recreate the deleted learner's evidence.

HG-0003-S5's actual generation/approval/copying boundary belongs to later stages
where those actions exist. HG-0007's graph/checkpoint, exporter/provider and backup
obligations remain open. This review cannot establish either complete native
specification's integration, real-learner activation, processor terms, Windows
execution, production HTTPS, browser caching behavior beyond response headers,
human acceptance, a commit or deployment.
