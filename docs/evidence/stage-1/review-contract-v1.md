# Stage 1 independent contract review — revision 1

Reviewer: independent `final_contract_review` subagent. Reviewed on 2 November
2026 against base `a004bdd9e96ac9bde85b989ca1ed9c73bcef0583` and the current
uncommitted Stage 1 implementation. The owner's pre-existing Implementation
Plan.md edit was read, not changed. No source/tests or generated credentials were
modified or inspected by this reviewer.

## Verdict: NO_GO pending two implementation fixes and fresh evidence

The review follows the installed HighGrade independent-review method. The scope
is Stage 1: tutor login/ownership, learner/source/observation/activity intake,
recent measures, cumulative/frozen context and lifecycle of the introduced stores.
Future artifact approval/export, graph checkpoints, model exporters and backup
deletion remain later-stage obligations, not failures of this slice. This review
does not authorize native contract integration, commit or real learner use.

### 1. Finish the transaction before reporting a saved learner or evidence record

Location: `src/tutor_copilot/intake.py:35` and
`src/tutor_copilot/evidence.py:19`.

The HTTP dependency currently uses `Depends(transaction)` with its default request
scope. The database transaction commits when that yielded dependency exits.
Installed FastAPI's `routing.py:148-154` sends the response before closing the
request dependency stack; `dependencies/utils.py:722-727` puts an unspecified
yield scope on that stack. A deferred constraint or connection error at COMMIT can
therefore occur after the client has already received a 200/201 saved response.

Use function-scoped transaction cleanup before response sending, or explicitly
complete the transaction before returning success. The smallest fix is
`Depends(transaction, scope="function")`; its FastAPI minimum is 0.121. Add a
real PostgreSQL deferred failure case asserting a sanitized non-success response
and no persisted row. Current documentation was independently fetched through
Context7 and agrees with the installed implementation:
[FastAPI dependency scope](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope).

### 2. Preserve the result of a tutor-confirmed qualitative check

Location: `src/tutor_copilot/schemas.py:105-112`.

An activity can currently be confirmed as `checked_outcome` with neither an
observation reference nor any qualitative outcome/criterion field. The numeric
observation link supports a drill score, but a fluency, discourse, reading or
project check cannot store what result was checked without misusing the purpose
field. This falls short of source-qualified checked outcomes under PD-39 and the
PD-40 distinction between task criteria and drill accuracy.

Support a small structured qualitative result with a criterion/reference, or an
existing numeric observation reference, without calculating a model judgement or
creating performance counts. Keep an explicitly unknown result qualified. Verify
the result survives real persistence/context loading and that assignment or
encounter alone does not acquire an outcome. The parent has acknowledged and is
implementing this refinement.

### 3. Refresh affected evidence after the current edits

The original `check-v1.txt` reports 26 passing unit cases. `integration-v1.xml`
contains 21 executed cases and zero errors, failures or skips, matching
`integration-v1.txt`. Their assertions cover real provider/database/worker/cache
boundaries rather than substitute services.

The independently checked `input-snapshot-v1.json` differs from the current
`web.py`, `test_intake.py`, `test_lifecycle.py` and `test_web.py`, reflecting current
no-store, permission and raw-history test additions. These original reports are
valid historical observations, but cannot establish the final edited result.
Record a new snapshot and affected/full required barriers after the final fixes.

## Confirmed parts of the implementation

- The selector caps complete source/session streams at four lessons and four
  homework submissions within 90 days before subskill filtering. It preserves
  separate evidence/task/assistance groups and excludes unknown/future/old dates.
- Exact rational arithmetic implements the positive/negative 0.15 boundaries;
  zero denominators remain unknown. Multiple answers in one lesson do not create
  several longitudinal trend points. Completion is kept separate, and maintenance
  remains a conservative unconfirmed candidate rather than mastery.
- Stable response/activity identities prevent duplicate counts. Immutable
  observation/activity revisions retain the last confirmed state during pending
  edits; an explicit confirmed withdrawal is filtered after latest-confirmed
  selection. Source metadata revisions retain one lesson identity.
- Context freezing preserves structured records and revision references without
  raw text. Source availability is resolved against the exact frozen source
  revision, and older history does not enter recent counts.
- The implementation has direct operations, typed input schemas and existing
  SQLAlchemy/async I/O. It introduces no speculative repository, memory, NLP,
  scheduler or worker framework layer.
- Documentation identifies the JSON API boundary, local synthetic OIDC/cookie
  exception, manual cleanup requirement and unimplemented future stages.

## Limits and next action

This is code/contract/evidence review, not a repeated full test run or a browser
engine exercise. Authentication/privacy receive a separate independent review.
No generated credential file was read. A final GO requires re-review of the two
fixes and the new current reports. The complete native HG-0003/HG-0007 contracts
must remain open for their explicitly deferred scenarios.
