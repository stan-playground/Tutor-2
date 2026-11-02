# Plan for Fixes Stage 1 — Claude backlog

## Purpose and gate

This backlog records only the two Stage 1 defects that Claude Code identified as
unsafe to defer while more persisted evidence and downstream consumers are
added. The selection was checked against [HG-0003](specs/changes/HG-0003/spec.json),
[HG-0007](specs/changes/HG-0007/spec.json), the
[Stage 1 record](docs/stage-1.md), [Product Decisions](<Product Decisions.md>)
and the [Implementation Plan](<Implementation Plan.md>).

The gate is not that these changes are literally impossible later. They should
be fixed before more data or frozen contexts exist because a later migration
would have to guess the original meaning or ownership of stored records. Only
the two non-deferrable groups below are in scope.

This is a backlog, not implementation authority. It authorizes no code change,
database migration, commit, push, activation, human acceptance, merge, release
or deployment. Each item needs a separately authorized HighGrade route,
applicable checks, independent review and a separate acceptance decision.

## Order

1. Stop metadata corrections from irreversibly erasing source bodies.
2. Decide the identity model, then enforce learner-scoped database references
   in the same migration design.

Finish and verify each implementation block before starting the next dependent
block. Items 1 and 2 may be specified independently. If both ultimately require
database migrations, keep them in separate reviewed revisions because their
rollback paths and risks differ.

## S1-FIX-01 — Preserve source bodies across metadata corrections

### Invariants

- Omitting `raw_text` from a metadata correction preserves the stored body and
  its existing expiry deadline.
- Clearing or replacing a body is distinguishable from omitting the field.
- The archived prior revision retains its exact body and expiry metadata until
  the retention process expires it.

### Why this cannot safely wait

[save_source](src/tutor_copilot/evidence.py) currently receives
`raw_text=None` both when the client omits the field and when the client sends
an explicit null. A metadata-only correction can therefore clear the current
body and assign a new deadline to the now-empty current row. The prior body is
archived before the update and remains recoverable only while that history has
not expired. The archive contains no marker that distinguishes an accidental
omission from an intentional clear. After retention removes the archived body,
no migration can recover it or prove the tutor's intent. More affected
corrections also make the replay-fingerprint repair harder to audit.

### Contract and design decision

The [HG-0003](specs/changes/HG-0003/spec.json) scope requires source
corrections to preserve provenance without extending raw expiry on metadata-only
changes. [HG-0007](specs/changes/HG-0007/spec.json) owns the 30-day raw-source
expiry policy, and the [Stage 1 record](docs/stage-1.md) says metadata-only
edits preserve the deadline. Treating an omitted body as a metadata-only change
therefore restores an existing contract and uses `highgrade-work`.

The current API accepts explicit null. Preserving that as an intentional clear
is the smallest compatible repair; omission and null must no longer collapse
into the same input. If the owner instead wants a separate clear operation,
that is a changed API requirement and needs `highgrade-spec` first. The
must-fix omission defect does not require inventing that larger API.

### Ordered implementation blocks

1. Add failing real-database cases for omitted, explicit-null and replacement
   body updates, including expiry and archived revision assertions.
2. Implement field-presence handling so omission is not converted into a clear,
   and preserve idempotent replay without treating two different intents as the
   same request.
3. Confirm that the archived prior version keeps its original body and deadline.
4. Re-run correction, replay, retention and frozen-context cases.

### Migration and compatibility

Field-presence handling may need only an application-model change, but the route
must confirm that before ruling out a schema migration. Stored request
fingerprints currently collapse omission and null, so compatibility for
already-issued retries must be stated and tested: determine whether an omitted
field from a request issued before the fix still matches its stored fingerprint
without replaying an unintended clear. A cleared current body may be restored
only when an unexpired archived revision still holds it; after retention, it
cannot be reconstructed and must not be guessed. Any required schema change
belongs in a new Alembic revision rather than the delivered Stage 1 migration.

### Required evidence

- Real PostgreSQL cases proving omission preserves body and expiry.
- Separate explicit-clear and replacement cases under the agreed contract.
- An idempotent replay case and an exact archived-revision read.
- Clean applicable commands from [README](README.md#local-commands), including
  `just check` and the real `just integration` path when services are
  available.

## S1-FIX-02 — Make identity and references learner-scoped

### Invariants

- A tutor cannot learn whether a supplied evidence ID belongs to another
  learner or tutor.
- An observation, activity or archived source revision can reference only a
  source owned by the same learner.
- The database enforces the learner match; application checks remain a second
  boundary.
- Idempotent replay within the owning learner continues to work.

### Why this cannot safely wait

The delivered schema in
[0002_evidence.py](migrations/versions/0002_evidence.py) uses globally supplied
source and evidence UUIDs. The write path can return a distinguishable conflict
when another learner already owns a supplied ID, creating an existence oracle.
That check compares learner IDs; treating it as cross-tutor protection assumes
learner IDs are globally unique. The new identity spec must state and verify
that assumption or remove it through the selected scoped key.

The child tables store both `learner_id` and `source_id`, but their foreign
keys constrain only `source_id -> sources.id`. Application reads currently
check ownership, yet the database does not prove that both columns name the
same learner. A missed write check could therefore store a cross-learner
reference even when both learners belong to one tutor.

Adding the constraint later requires validating every stored row and deciding
which side of each mismatch is correct. Changing the identity namespace after
Stage 3 stores IDs in generation or frozen-context records would also require a
mapping and compatibility reader for every old reference. That is the expensive
part; error-message cleanup alone does not solve it.

### Contract and design decision

This item is `highgrade-spec` first because the public identity contract is not
settled. The main alternatives are:

- **Learner-scoped client IDs — recommended by Claude.** Keep client-supplied
  UUIDs, but make uniqueness and lookup include `learner_id`. This preserves
  the current intake/replay shape while changing database keys.
- **Server-generated IDs.** This removes client collisions but needs a separate
  idempotency key or external reference and changes the intake API.
- **Global IDs with uniform errors.** This is the smallest patch, but a foreign
  collision can still block a valid write and timing may still reveal the
  global namespace. It is not the recommended durable fix.

The selected spec must define the identity key, replay key, frozen-reference
shape and indistinguishable response for foreign and nonexistent IDs. It must
preserve the non-disclosure rule in
[HG-0003](specs/changes/HG-0003/spec.json) and the tutor/learner isolation policy
in PD-28 of [Product Decisions](<Product Decisions.md>).

The spec must also decide whether the physical key needs `tutor_id` as well as
`learner_id`. Learner scope is narrower when learner IDs are already unique;
including tutor scope makes the ownership boundary explicit but widens every
key and foreign key. Either design must enforce the same-learner reference in
the database and avoid foreign-ID disclosure.

### Ordered implementation blocks

1. Specify and approve the identity model before writing a key migration.
2. Add failing cross-tutor and same-tutor/cross-learner cases using the same
   supplied IDs. Compare both status and response body with an unknown ID.
3. Run a read-only audit for mismatched learner/source pairs in an isolated
   database. Stop and report any mismatch; do not rewrite it automatically.
4. Add a new Alembic revision for the selected key shape and composite
   learner/source foreign keys. Include `source_history`, `observations` and
   `activities`.
5. Update every read, write, replay and delete lookup to use the complete
   identity. Keep the application ownership checks.
6. Verify migration upgrade and downgrade on isolated databases, then verify
   deletion and frozen-reference resolution.

Implement and review this identity migration separately from any schema change
selected for S1-FIX-01.

### Migration and compatibility

The identity decision affects primary/unique keys, indexes and all dependent
foreign keys, so it must precede the referential-integrity migration design.
Existing frozen contexts and observation references need an explicit reader or
migration rule; do not infer learner ownership from an unscoped ID when the
owning record is unavailable. Current project use is synthetic-only, but that
does not authorize destructive cleanup of any shared development database.

### Required evidence

- Cross-tutor and same-tutor/cross-learner collision and non-disclosure cases.
- A direct restricted-role database case proving a cross-learner child/source
  pair is rejected.
- Read-only mismatch-audit output from an isolated database.
- Upgrade, constraint validation and downgrade evidence.
- Existing replay, correction, deletion, recent-context and frozen-reference
  checks.
- Clean applicable README commands and independent security/contract review.

## Completion rule

An item is complete only when its selected HighGrade route, implementation,
real checks, migration evidence where applicable, independent review and
recorded results are complete. Completion of this backlog does not establish
production readiness, teaching quality, human acceptance or authority for any
later delivery action.
