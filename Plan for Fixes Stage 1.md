# Plan for Fixes Stage 1

Status: selected repair backlog; no fix is implemented or accepted by this document.

Audit date: 2 November 2026
Stage 1 baseline: `cb699151c39b7f9fc3594afd52a85a9a97c0fc5c`
Current-head check: the affected Stage 1 migration, source modules and tests are unchanged at
`35988f6deaddf8493f04e2836549986add897ee1`.

Contract sources: [HG-0003](specs/changes/HG-0003/spec.json) and
[Product Decisions](<Product Decisions.md>) PD-06–09, PD-28 and PD-39.

## Selection rule

Nothing here is literally impossible to change later. “Fix now” means **before Stage 3 creates
jobs, generated artifacts or additional frozen contexts that depend on these identities and
snapshots**. After that point, a repair needs ambiguous data reconstruction, multi-store re-keying
or compatibility support for already-frozen artifacts.

An item is included only when all of these are true:

1. The current behavior was reproduced from the untouched Stage 1 commit, rather than inferred
   from a completion report.
2. The defect affects a durable identity, exact provenance or frozen context contract.
3. Deferral makes safe repair materially harder because existing records cannot be reconstructed
   or automatically merged, or because immutable artifacts would keep the old meaning.

Small validation bugs, presentation work, production-provider hardening and the Stage 5 worker,
backup and telemetry obligations are outside this backlog.

Stage 3 must not start while any item below is open.

## Backlog

### S1-FIX-01 — Repair evidence identity and exact source-version provenance

Priority: P0
Depends on: none
Blocks: S1-FIX-02 and every later learner-linked job or artifact

#### Observed failure

- `sources.id` and the `(id, revision)` keys for observations and activities are global even
  though their UUIDs come from clients. A source UUID already used by Tutor A makes Tutor B's
  otherwise valid write fail with `409`. The hidden row therefore changes another tutor's
  behavior.
- Observation and activity revisions store only `source_id`. They do not store the source
  revision used when the evidence was recorded. After source revision 1 is corrected to revision
  2, `GET /evidence?history=true` presents the old evidence with revision-2 source metadata.
- The database foreign key checks only `source_id`. It cannot prove that evidence and source
  belong to the same learner. The HTTP helper currently checks this, but future writers could
  create cross-learner provenance while still satisfying row-level tutor ownership.

Relevant code:

- [Evidence migration, lines 29–59](migrations/versions/0002_evidence.py#L29-L59)
- [Intake schemas, lines 50–108](src/tutor_copilot/schemas.py#L50-L108)
- [Source persistence, lines 90–160](src/tutor_copilot/evidence.py#L90-L160)
- [Evidence persistence and reads, lines 190–295](src/tutor_copilot/evidence.py#L190-L295)

The missing source revision is not recoverable from existing rows: observation/activity revisions
have neither `source_revision` nor a creation time that can be matched reliably to source-history
revisions. Re-keying after later tables and JSON snapshots refer to these IDs would require a
multi-store migration.

#### Architecture decision

Use learner-scoped client identities and one append-only source-version table:

```text
sources
  (learner_id, source_id) primary key
  tutor_id, current_revision

source_versions
  (learner_id, source_id, revision) primary key
  tutor_id, kind, occurred_at, qualification, raw_text, expires_at, fingerprint
  foreign key (learner_id, source_id) -> sources

observations
  (learner_id, observation_id, revision) primary key
  tutor_id, source_id, source_revision, confirmed, data
  foreign key (learner_id, source_id, source_revision) -> source_versions

activities
  (learner_id, activity_id, revision) primary key
  tutor_id, source_id, source_revision, confirmed, data
  optional normalized (observation_id, observation_revision)
  composite foreign keys keep every reference inside one learner
```

Keep the public UUID stable inside one learner. The same client UUID must be valid for another
learner or tutor. Server-generated learner and context IDs may remain global.

The common alternative is to keep mutable `sources` plus `source_history` and add triggers that
validate a source revision across their union. That preserves fewer table changes, but every
provenance read needs union logic and PostgreSQL cannot provide one ordinary composite foreign key
to the union. The append-only version table is simpler and gives the database one enforceable
reference target.

Implement this as a forward migration after `0004`; do not rewrite committed migration history.
Do not guess source revisions for ambiguous existing evidence. Because the database is explicitly
synthetic and real-data activation is unverified, reset synthetic records or stop the migration
with a clear diagnostic when an exact backfill cannot be proven.

#### Edible implementation blocks

1. Add the source head/version tables and migrate unambiguous source rows. Verify create, correct,
   exact-version read and 30-day raw expiry before continuing.
2. Add learner-scoped observation keys and exact source-version foreign keys. Verify one
   observation create/correct/withdraw path.
3. Apply the same keys to activities and normalize their optional observation reference. Verify
   one activity create/correct/withdraw path.
4. Update row-level security and direct database constraints. Verify two tutors and two learners,
   including direct cross-learner insert attempts.
5. Update context/evidence reads to resolve the recorded source revision, then remove the obsolete
   split-history path only after all checks pass.

#### Required real checks

- Two tutors and two learners can reuse the same client source, observation and activity UUIDs;
  all writes succeed and neither tutor learns that the other used the UUID.
- A direct `tutor_app` insert that combines learner B with learner A's source fails at the database
  constraint.
- Evidence saved against source revision 1 still resolves revision 1 after the source head advances
  to revision 2.
- A frozen context keeps its exact source/evidence revisions; a new context uses the intended
  corrected revision without changing the old one.
- Raw expiry and cleanup still remove source text from every version without removing permitted
  structured evidence.
- Every learner table remains unreadable under another tutor or an unset tutor context.

Definition of done: the migration, API operations, RLS checks and exact-provenance scenarios pass
against real isolated PostgreSQL. No stored record relies on an application-only same-learner
check.

### S1-FIX-02 — Version and correct the frozen-context contract before generation consumes it

Priority: P0
Depends on: S1-FIX-01
Blocks: Stage 3 preparation jobs and Stage 8 feedback artifacts

#### Observed failure

- A confirmed performance observation on a 120-day-old lesson is correctly excluded from recent
  rates, but it also disappears from cumulative context because `build_context` builds history
  only from activities.
- A checked-outcome activity remains in every new context after its referenced observation is
  confirmed as withdrawn. The activity and observation are selected independently.
- Frozen context JSON has no schema version. If generation starts now, later corrections would
  create old and new immutable snapshots with different meanings but no explicit compatibility
  boundary.

Relevant code:

- [Context construction, lines 34–89](src/tutor_copilot/context.py#L34-L89)
- [Context freeze/read, lines 92–138](src/tutor_copilot/context.py#L92-L138)
- [Checked-outcome validation, lines 237–250](src/tutor_copilot/evidence.py#L237-L250)
- [Context persistence, lines 60–63](migrations/versions/0002_evidence.py#L60-L63)

Stored observations still make the first omission repairable today. It becomes expensive after
generated artifacts cite incomplete frozen contexts. Recomputing old contexts would violate their
immutability; keeping both meanings without a version would make consumers guess.

#### Architecture decision

Define the first explicit context schema version before adding a generation consumer. Keep recent
performance and cumulative history separate:

```text
schema_version
learner_id, profile_revision, as_of, selection
recent
history:
  observations: bounded exact observation + source revision references
  activities: bounded exact activity + source revision references
history_coverage: separate matching/selected/omitted counts for each record type
sources: exact referenced source versions with availability resolved at read time
```

Older observations belong in cumulative history without entering recent counts, trends or
maintenance candidates. A numeric checked outcome belongs in a new context only while its exact
observation reference is the current confirmed, non-withdrawn evidence. A pending correction keeps
the last confirmed reference usable; a confirmed correction requires the activity to be corrected
or marked stale. Existing frozen selections remain unchanged; source availability continues to be
resolved dynamically when they are read.

Mixing observations and activities in one untyped list is the common smaller alternative. It saves
one field but forces every consumer to inspect record-specific JSON and makes coverage ambiguous.
Separate typed collections are clearer and match the product distinction between performance and
learning-activity facts.

#### Edible implementation blocks

1. Add `schema_version` and typed response models without changing selection behavior. Verify one
   current and one frozen read.
2. Add bounded historical-observation selection using exact revisions from S1-FIX-01. Verify that
   old evidence appears without changing any recent denominator.
3. Validate checked-outcome dependencies for new contexts. Verify pending correction, confirmed
   correction and confirmed withdrawal separately.
4. Update freeze/read handling and coverage counts, then run consumer-contract tests before Stage 3
   is allowed to load the new shape.

`build_context` remains one request-scoped async database operation used by current reads and
freezing. A small historical-observation selector is justified because it has different eligibility
and coverage rules from activities; its inputs are the transaction, learner and selection, and its
output is exact structured references. Missing or stale linked evidence is an explicit qualified
result, not an exception or an invented outcome.

#### Required real checks

- A 120-day-old confirmed observation appears in cumulative history with exact observation and
  source revisions while recent groups and denominators remain empty.
- Pending and withdrawn observation revisions do not appear as cumulative performance.
- A frozen context containing a valid checked outcome is unchanged after withdrawal, while every
  new context excludes or marks that outcome stale.
- Missing dates and amounts remain unknown; no history row creates an opportunity, mastery or
  forgetting claim.
- Context limits and coverage counts are deterministic for both observations and activities.
- A consumer rejects an unknown `schema_version` instead of interpreting it as the current shape.

Definition of done: current and frozen contexts have one explicit, tested schema; retained old
performance is visible only as cumulative evidence; retracted evidence cannot support a new
context.

## Fresh audit evidence

The stored Stage 1 evidence reports were not used as proof. The untouched commit was extracted to
a disposable directory and checked again:

```text
just check       -> Ruff format/lint passed; strict mypy passed; 26 unit tests passed
just integration -> 28 real PostgreSQL/Redis/worker/Keycloak tests passed
```

Four additional disposable real-API/PostgreSQL critic scenarios were then run. They are acceptance
tests for this backlog, not committed fake-success tests:

```text
test_evidence_keeps_the_exact_source_revision                         FAILED
test_old_confirmed_performance_remains_in_cumulative_context          FAILED
test_new_context_drops_checked_outcome_after_observation_withdrawal   FAILED
test_client_ids_are_isolated_per_tutor                                FAILED
```

The normal suites passing alongside these targeted failures shows that the gaps are absent from the
existing test contract; it does not cancel the reproduced failures.

## Completion order

1. S1-FIX-01 — identities and exact provenance.
2. S1-FIX-02 — versioned context built on exact references.
3. Re-run normal checks plus every required real scenario, then perform an independent security and
   contract review of the complete repair diff.

This backlog is complete when both definitions of done are met with fresh evidence. That
technical completion still does not imply human acceptance, commit, push, activation or launch.
