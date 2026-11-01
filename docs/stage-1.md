# Stage 1 — tutor-owned evidence and history

Implementation under the owner's 1 November 2026 Goal. Requirements remain in
[HG-0003](../specs/changes/HG-0003/spec.json) and the implemented portions of
[HG-0007](../specs/changes/HG-0007/spec.json). This record coordinates those tasks,
explains implementation choices and links verification. It does not authorize a
pilot, real learner data, publication or a commit.

## Blocks and barriers

1. OIDC login, restricted database role and learner/profile save/read. Check real
   Keycloak login, two tutors, CSRF and real PostgreSQL ownership independently.
2. Source intake and confirmed performance observations. Check replay, duplicate
   response identities, revisions and pending confirmation at the persisted boundary.
3. Recent comparable counts/rates/trends. Check numerical boundaries and actual
   latest-four lesson/homework source selection.
4. Independent activity facts and frozen context. Check assignment/encounter
   independence, qualified unknowns, corrections and unchanged frozen references.
5. Lifecycle and integration. Check expiry without cleanup, physical cleanup,
   inactivity, deletion, private-content logging and independent review.

## Implementation decisions

- Local Keycloak with a public OIDC client and PKCE was selected by the owner.
  Authlib handles the protocol. Exact issuer/subject invites and server-side
  sessions establish tutor identity; request fields cannot select it.
- A restricted PostgreSQL runtime role uses transaction-local tutor context and
  row-level security, in addition to application ownership checks. The migration
  and cleanup account is separate. Local trust access remains synthetic-only.
- Profiles, source metadata, observations and activity facts retain revisions. Pending
  corrections do not erase prior confirmed evidence. Writes lock the learner
  before checking revisions, sources or deletion state.
- Stable source IDs and response/activity references are supplied by tutor intake.
  Replays are idempotent; conflicting duplicate identities are rejected. The
  application cannot recognize the same response given unrelated false identities.
  A source correction preserves its session identity and archives the prior version.
  Metadata-only edits preserve its raw expiry deadline. A confirmed `withdrawn`
  revision excludes a false observation/fact from new context; pending withdrawal
  preserves the last confirmed state. Audit reads and prior snapshots retain it.
- A checked open-task outcome records a criterion reference and `met`,
  `partially_met`, `not_met` or explicitly `unknown`, unless it references an
  existing numeric observation. Assignment/encounter/attempt facts cannot claim
  outcomes. Qualitative results remain structured facts, not performance rates.
- Notes/transcripts stay in an expiring source body. Structured assessment and
  evidence fields are tutor-authored nonverbatim facts; no model extraction,
  embedding, text classifier or automatic linguistic assessment is introduced.
- Recent selection uses event dates, excluding unknown/future dates, with UUID
  tie-breaks. Select up to four lesson sessions and four homework submissions
  before filtering by subskill. Compare the same task reference/type and assistance.
  Aggregate observations within a session before checking trends so multiple
  answers in one lesson do not become several longitudinal observations.
- Cumulative context uses separately confirmed activity facts, including historical
  facts, and explicit selection coverage. It creates no performance observations,
  forgetting score, schedule or mastery assertion. Frozen contexts retain revisions,
  while source availability is always resolved at read time.
  Exact subskill and purpose filters are combined with OR; an empty filter selects
  all confirmed facts up to the visible 200-fact limit. Goal-led input facts need
  no subskill. Purpose selection is supplied by the caller; automatic teaching
  purpose selection belongs to stage 3.
- Deliberate tutor writes and context creation refresh activity. Reads/polling do
  not. Structured records expire after 12 calendar months of inactivity. Cleanup
  physically removes expired raw bodies and inactive learners. Explicit deletion
  synchronously removes every implemented learner store in one transaction.
  The owning tutor can explicitly delete an inactive learner while all ordinary
  reads and writes remain unavailable.
- Async database and OIDC I/O use existing process-lifetime pools. Dependent
  operations remain sequential inside one short request transaction. Threads and
  processes offer no benefit for these bounded calculations and I/O operations.
  FastAPI uses a function-scoped transaction dependency (minimum 0.121), so commit
  completes before an HTTP success is sent. The actual PostgreSQL deferred-error
  check verifies that a failed commit returns a sanitized error and rolls back.
  One bounded thread is used only by the test that races a write against deletion.

Local PostgreSQL, API and Keycloak observations cannot prove external provider
terms, backup deletion or future graph/exporter behavior. Those HG-0007 boundaries
remain open for later stages.

## HTTP operations

The Stage 1 interface is JSON. Authentication is browser OIDC; learner-management
forms are not implemented in this slice. Schemas are defined in
[schemas.py](../src/tutor_copilot/schemas.py); unknown fields are rejected rather
than silently stored. Profile intake requires an alias, adult confirmation,
informed learner opt-in, tutor upload permission, dated assessment/source/level/
uncertainty, goals and preferred domains. No birth date or contact field exists.

| Operation | Input → output |
| --- | --- |
| `GET /auth/login`, `GET /auth/callback` | OIDC authorization/response → server-side invited tutor session. |
| `GET /auth/me`, `POST /auth/logout` | Session → tutor ID/CSRF token, or invalidate the session. |
| `POST /learners` | Profile with `expected_revision: 0` → learner ID, revision and saved profile. |
| `GET /learners/{id}`, `PUT /learners/{id}` | Learner ID, or profile and current expected revision → current/new profile revision. |
| `POST /learners/{id}/sources` | Stable source UUID, lesson/homework/actual-use kind, event date or null, source qualification, optional raw text and expected revision → source UUID/revision. |
| `GET /learners/{id}/sources/{source}` | Optional `revision` → that source version and raw text only while available. |
| `POST /learners/{id}/observations` | Source, stable response reference, subskill/task/assistance, confirmation, three independent count pairs and optional completion → saved revision. |
| `POST /learners/{id}/activities` | Independent assignment/encounter/attempt/checked-outcome fact, stable activity reference, source, nullable date/amount, purpose/context, confirmation, and checked observation revision or qualitative criterion/result → saved revision. |
| `GET /learners/{id}/evidence` | Optional `history=true` → latest pending/confirmed/withdrawn records, or all audit revisions. |
| `GET /learners/{id}/context` | Authorized learner → current recent measures and separate bounded cumulative history. Read creates no evidence. |
| `POST /learners/{id}/contexts` | Optional exact `subskills`/`purposes` → frozen context ID and selected structured revisions. Creates no activity/performance facts. |
| `GET /learners/{id}/contexts/{context}` | Frozen ID → unchanged selection with source-version availability resolved now. |
| `DELETE /learners/{id}` | Authorized learner → immediate synchronous deletion of all implemented learner stores. |

All unsafe methods require the session's `X-CSRF-Token`. The server determines
tutor identity. Authentication failure is 401, CSRF/invitation refusal 403, an
unavailable/other-tutor learner 404, stale/duplicate identity conflict 409, malformed
intake 422, provider unavailability 503 and an unexpected failure a sanitized 500.
Validation and database errors never echo input values.
All responses use `Cache-Control: no-store`, including failures and deletion, to
avoid browser/shared caches retaining a learner response after its access expires.

`expected_revision` starts at zero for a new source/observation/activity; corrections
name the current revision. Repeating the same write with its original expected
revision returns the previously saved revision. Pending evidence is visible through
intake, while context uses the newest confirmed non-withdrawn revision. To correct
a mistaken subskill/kind, withdraw the false record and create the correctly
identified record. Assignment, encounter, attempt and checked outcome are not
mandatory sequential states. A reading encounter can have no answer or amount.

For performance, each count pair is `correct`/`opportunities`; denominators are
attempts, required-use opportunities and meaningful avoidance choices respectively.
The tutor supplies clear observed counts. There is no transcript extraction or
automatic audio assessment. An actual-use report alone cannot create a performance
observation; lesson/homework evidence is required. Completion is separate. Missing
and zero denominators stay unknown. Trends need three comparable sessions with at
least five opportunities each; thresholds use exact rational arithmetic. A single
qualified adjacent-session drop of at least 0.15 is only a possible-regression
alert. A maintenance candidate conservatively requires all three measures to
support it; no mastery or tutor-confirmed maintenance is inferred.

## Functions, ownership and lifetime

The engine/cache live for one application process and close on shutdown. All
connections, authorization state, loaded records and calculations below live for
one request/transaction. No ORM session is shared across tasks. Ordinary HTTP
handlers stay separate because they expose different validation and response
contracts; the dependency supplies each with one transaction/tutor pair.

| Method | Purpose, inputs/output, caller and reason for separation |
| --- | --- |
| `Settings.runtime_database_url` | Settings → fixed restricted local URL; called by `db.create_engine`, separating request access from migration/maintenance authority. |
| `Intake` and concrete schemas | FastAPI body → validated typed data; bound text/count/date sizes and independent concepts before persistence. Pydantic raises validation errors. |
| `Count.valid_counts` | Validated pair → pair, rejecting numerator above denominator. Called by schema validation because this is a cross-field invariant. |
| `Activity.complete_reference` | Activity → activity; requires paired observation references, a checked result/criterion when no numeric reference exists, and prevents other kinds from claiming outcomes. Called by schema validation. |
| `tenant_transaction` | Engine/tutor → transaction-scoped connection; called by the HTTP dependency and database checks to set/reset RLS context and commit/rollback atomically. |
| `lock_learner` | Connection/learner/tutor → profile revision or 404; shared by reads/mutations/freezing/deletion for one lock order. Only owner deletion passes the internal `allow_inactive` flag; it cannot bypass ownership. |
| `touch_learner` | Connection/learner → no return; successful deliberate writes/freezes refresh inactivity independently of reads. |
| `save_profile`, `read_profile` | Typed profile/current revision or learner ID → saved/current profile; called by learner handlers. Separate write/read operations retain history and enforce 409/404 respectively. |
| `save_source`, `read_source` | Typed source/expected revision or source/version IDs → saved revision or qualified source; source handlers and evidence intake use these to preserve one session identity and enforce raw expiry. |
| `save_revision` | Observation/activity → revision receipt; their handlers share the same source ownership, stable identity, replay and correction transaction. It is one helper for two current record types, with no plugin/repository framework. |
| `current_records` | Learner and fixed table name → newest confirmed revisions for context, latest pending/withdrawn records for intake, or audit history. Called by context/evidence handlers; confirmation filtering happens before latest-revision selection, withdrawal filtering after it. |
| `source_metadata` | Learner → nonverbatim current source metadata; called by context construction so latest-four selection considers sessions even without target observations. |
| `summarize_recent` | Confirmed current observations, all authorized source metadata and aware time → recent qualified counts/rates/trends. Called by context construction; pure and synchronous, with no application resources. Naive time raises `ValueError`. |
| `_counts`, `_measure` | Comparable rows/session points and measure name → count totals or trend/support fields; summary internals share exact arithmetic across three measures. |
| `build_context` | Active learner/tutor and filter → current structured context; current read and freeze share identical selection/calculation logic. It locks the learner to avoid mixing concurrent revisions. |
| `freeze_context` | Context request → persisted ID/structured selection; create-context handler uses it to preserve references without raw text. |
| `resolve_availability` | Frozen/current structured context → same selection with current availability for each exact source revision; reads cannot revive expired text. |
| `read_context` | Learner/tutor/context ID → frozen selection or 404; frozen-read handler rechecks access and source availability. |
| `transaction` | FastAPI request/authenticated tutor → connection/tutor pair; one function-scoped HTTP dependency owns transaction lifetime and commits before response success. |
| `create_learner`, `get_learner`, `update_learner`, `delete_learner` | Learner HTTP operations → corresponding persistence response. Delete locks first and cascades synchronously; no deletion worker is needed for the currently small store. |
| `add_source`, `get_source`, `add_observation`, `add_activity`, `get_evidence` | Typed intake/read request → revision/source/audit response; each calls the corresponding evidence operation without deriving facts from another kind of fact. |
| `get_current_context`, `create_context`, `get_context` | Read/freeze request → current/frozen context; separate handlers expose the different persistence effects explicitly. |
| `invalid_input`, `conflict` | Request validation/database integrity exception → fixed 422/409 response; app-level handlers prevent private values in error bodies. |
| `cleanup` | Maintenance transaction → counts of physically purged expired source versions/inactive learners; CLI and actual database tests share one operation. Also deletes expired login sessions. SQL/connection failure aborts the transaction. |
| `run_cleanup`, `main` in lifecycle | No user input → short-lived fixed local maintenance engine, JSON counts, then shutdown. CLI entry point calls the async operation; no background scheduler or permanent engine is added. |
| Migration `upgrade`/`downgrade` methods | Alembic connection → schema changes; called by Alembic, with deployment/migration lifetime only. Role creation is serialized for isolated database tests. Cluster role remains after downgrade because another test database may use it. |

[Authentication methods and alternatives](evidence/stage-1/auth-methods.md) document
the Authlib/session/provisioning methods, their lifetimes and exact local checks.
SQL/database errors roll back request mutations; no private exception strings are
logged. Debugging uses existing metadata observations and targeted assertions;
printing private method arguments/results would be harmful here.

The implementation uses established Authlib, Pydantic, FastAPI and SQLAlchemy
features, checked through current Context7 documentation. Standard-library exact
arithmetic handles the small numerical calculation; language-processing packages
would add no value because this stage accepts explicit tutor observations.

## Reproduction and evidence

From a locked environment, with Docker running:

```bash
just setup
just up
just auth-up
just migrate
just check
just integration
just cleanup
```

`just auth-up` prepares only disposable synthetic identities and starts the
loopback provider; `just cleanup` permanently removes eligible synthetic records.
Raw source history shares the 30-day deadline; structured history is removed after
12 calendar months of inactivity. Run cleanup at least daily while local services
are active. Raw text is unavailable immediately at expiry even before cleanup.
Application backups, future graph checkpoints and third-party model copies do not
exist in this slice; later stages must implement their lifecycle before real use.

## Continuation

Stage 1 is complete. Observed base: `a004bdd`, with the owner's pre-existing edit
to Implementation Plan.md and separately appearing Plan_High_Level.md preserved.
All five blocks have real verification and independent GO. Next: none for this
implementation Goal; a local commit awaits a separate owner decision.

[Executor completion audit](evidence/stage-1/executor-review-v1.md) maps the Stage 1
barrier to current evidence. [Final deterministic checks](evidence/stage-1/check-v2.txt)
pass Ruff, strict mypy and 26 unit tests; [final integration checks](evidence/stage-1/integration-v2.txt)
pass 28 actual local-service cases with no skips. [Security review](evidence/stage-1/review-security-v2.md)
and [contract review](evidence/stage-1/review-contract-v2.md) give GO for this scope.
Original failed/replaced reports remain in [stage-1 evidence](evidence/stage-1/).

HG-0003 retains its future actual artifact-approval/copy scenario gap; HG-0007
retains future graph/exporter/backup obligations. Neither entire specification is
integrated or accepted by this milestone. Registry budgets remain unknown; the
initialization survey is historical and stale after later project changes.

Automatic approval review rejected invoking `just cleanup` on the existing fixed
development database because it could delete pre-existing records. It was not
executed or bypassed; the shared operation is verified in isolated real PostgreSQL,
including physical cleanup of current/historical sources and inactive learners.
