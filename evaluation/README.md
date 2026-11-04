# Synthetic evaluation fixtures

These wholly synthetic development items have draft expectations. They are not
approved gold, a release suite, a provider experiment or evidence of complete
homework or feedback behavior. [The inventory](inventory.md) lists every case
and maps remaining gaps to [the dataset contract](../specs/datasets.md).

- `homework/HW-RECENT-01.json`, `HW-NUM-*.json` and `HW-WINDOW-*.json` exercise
  the existing recent-performance calculation with separately identified draft
  inputs and expectations. `HW-ARITH-01.json` is an earlier structural draft
  without all fields needed by that calculation. `HW-CORRECTION-01.json` also
  exercises observation replay, duplicate rejection and correction through HTTP
  and PostgreSQL before applying the fixed fixture clock to the saved record.
- `homework/HW-RETRIEVAL-01.json` and `HW-RETRIEVAL-CONTRAST-01.json` exercise
  local HTTP search. The latter records that a positive-form-only target cannot
  currently be imported truthfully; exclusion from an eligible corpus has not
  been observed. Material review flags are synthetic test setup, not human review.
- `homework/HW-RETRIEVAL-OUTAGE-01.json` observes a healthy result and then a
  failed HTTP search when the query embedding is unavailable.
- `homework/HW-ACCESS-01.json` exercises private teaching-asset isolation for
  two synthetic tutors and rejects caller-supplied scope before query embedding.
- `feedback/FB-SOURCE-01.json` and `FB-02-extraction-01.json` contain authored
  source and extraction expectations; those feedback operations do not exist
  yet. `FB-03-incomparable-history-01.json` checks its numeric subset against the
  shared calculation, not the feedback job or its authorization boundary.
  `FB-04-missing-current-transcript-01.json` and its expired-source counterpart
  are static drafts for required source stops. `FB-05-no-permission-01.json`
  drafts a denied-permission stop. None establishes feedback-runtime behavior.

The owner confirmed on 3 November 2026 that reviewers `1` and `2` are qualified
and available. The two original items list those assignments; the newer case
metadata remains unassigned until review is recorded. No review dates, decisions
or approvals have been supplied. All samples remain `draft`, with
`reviewed: false` and empty decisions. Each label needs review by a qualified
English tutor; critical items and the required portion of ordinary items need
second review. [Reviewer instructions](reviewer-instructions.md) explain the
review and its independence requirements. The first pair of private reviewer
workbooks and handoff status are recorded in [review handoff](review-handoff.md).

`item.schema.json` is the initial structural contract, version `1`. Schema
validation cannot establish teaching correctness, source rights or human
qualifications. The task receives only `input`; the tests use `expectedOutput`
after the call for comparisons. The metrics function receives already
validated observations and does not establish authorization; retrieval checks
use isolated synthetic HTTP/database state. [E0 checks](e0-checks.md) record
executed checks and their limits. These isolated examples are not complete-job
families or release gates. No provider credentials or production data are used.
