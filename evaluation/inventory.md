# Evaluation inventory

This is the E0 working inventory, not a release manifest or a claim of tutor
approval. [The dataset contract](../specs/datasets.md) owns the requirements;
[the implementation plan](../Implementation%20Plan.md) sequences them. A family
is a situation; a sample is a separately runnable input and expectation. The
compact planning targets do not replace the required 12 homework and 8 feedback
families, variants, isolated cases or per-stage gates. No reduction has been
agreed, so no requirement change is being made.

## Authored samples

| Family | Sample and revision | Job | Stage | Severity | Review | Execution / gap |
| --- | --- | --- | --- | --- | --- | --- |
| FB-01 | [FB-01-extraction-01@1](feedback/FB-01-extraction-01.json) | feedback | extraction | ordinary | draft; unassigned in case metadata | Synthetic transcript and distinct prior lesson/homework context; schema only, no extraction or complete feedback job. |
| FB-02 | [FB-02-extraction-01@1](feedback/FB-02-extraction-01.json) | feedback | extraction | ordinary | draft; unassigned in case metadata | Authored source and candidate findings; feedback extraction not implemented. |
| FB-02 | [FB-02.zero-opportunities@1](feedback/FB-02-zero-opportunities-01.json) | feedback | extraction | ordinary | draft; unassigned in case metadata | Authored transcript and candidate labels distinguish learner silence from the tutor's example; schema only, no feedback extraction runtime. |
| FB-03 | [FB-03.incomparable-history@1](feedback/FB-03-incomparable-history-01.json) | feedback | subskill_analysis | ordinary | draft; unassigned in case metadata | Real shared recent-performance calculation only; feedback job and access not exercised. |
| FB-03 | [FB-03.trend-boundaries@1](feedback/FB-03-trend-boundaries-01.json) | feedback | subskill_analysis | ordinary | draft; unassigned in case metadata | Shared fixed-clock metric calculation checks +0.15 and -0.15 in the same comparable group; feedback authorization, extraction and job are not exercised. |
| FB-04 | [FB-04.missing-current-transcript@1](feedback/FB-04-missing-current-transcript-01.json) | feedback | source_context | critical | draft; unassigned in case metadata | Missing-source stop is a static draft; no feedback runtime exists. Not in reviewer batch 1. |
| FB-04 | [FB-04.expired-current-transcript@1](feedback/FB-04-expired-current-transcript-01.json) | feedback | source_context | critical | draft; unassigned in case metadata | Expired-source stop is a static draft; no feedback runtime exists. Not in reviewer batch 1. |
| FB-05 | [FB-05.no-permission@1](feedback/FB-05-no-permission-01.json) | feedback | source_context | critical | draft; unassigned in case metadata | Permission stop is a static draft; feedback authorization and resume are not implemented. In reviewer batch 3. |
| FB-06 | [FB-06.extraction-instruction-01@1](feedback/FB-06-injection-01.json) | feedback | extraction | critical | draft; unassigned in case metadata | Synthetic imported instruction and legitimate learner responses; schema only, no injection enforcement, privacy runtime or complete job. |
| FB-SOURCE | [FB-SOURCE-01@1](feedback/FB-SOURCE-01.json) | feedback | source_context | ordinary | draft; IDs 1 and 2 assigned | Schema only; no feedback source-context task implemented. |
| HW-ARITH | [HW-ARITH-01@1](homework/HW-ARITH-01.json) | homework | subskill_analysis | ordinary | draft; IDs 1 and 2 assigned | Schema only; missing metrics input fields. |
| HW-ACCESS | [HW-ACCESS-01@1](homework/HW-ACCESS-01.json) | homework | retrieval | critical | draft; unassigned in case metadata | Real private teaching-asset search and forged-scope checks for two tutors; learner evidence and model boundaries are not exercised. In reviewer batch 3. |
| HW-LEARNER-ACCESS | [HW-LEARNER-ACCESS-01@1](homework/HW-LEARNER-ACCESS-01.json) | homework | source_context | critical | draft; unassigned in case metadata | Two-tutor local intake denies foreign learner and source access and cross-source writes, with owned-source positive controls and captured metadata checks. No identity-provider login, provider, checkpoint or complete job observed. |
| HW-01 | [HW-01.assigned-only@1](homework/HW-01.assigned-only-01.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Authenticated intake/context retains assignment without changing existing performance; approval/copy are supplied facts, and no actual-use or complete-job inference is checked. |
| HW-01 | [HW-01.encounter-only@1](homework/HW-01.encounter-only-01.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Authenticated intake/context retains a reading encounter without adding an attempt or performance observation; no model claims or complete job checked. |
| HW-02 | [HW-02.listening-unavailable@1](homework/HW-02.listening-unavailable-01.json) | homework | retrieval | critical | draft; unassigned in case metadata | Real import and search exclude a declared unavailable recording, return an eligible alternative, then report a gap after that alternative becomes unavailable. Synthetic references only; no audio checked. |
| HW-02 | [HW-02.listening-key-mismatch@1](homework/HW-02.listening-key-mismatch-01.json) | homework | retrieval | critical | draft; unassigned in case metadata | Real import and search exclude a declared recording/criteria version mismatch, return an eligible alternative, then report a gap after that alternative becomes unavailable. No actual recording or key semantics checked. |
| HW-CORRECTION | [HW-CORRECTION-01@1](homework/HW-CORRECTION-01.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real observation writes, duplicate rejection and fixed-clock metrics; not the complete history-correction variant. Not in reviewer batch 1. |
| HW-DOMAIN | [HW-DOMAIN-01@1](homework/HW-DOMAIN-01.json) | homework | retrieval | ordinary | draft; unassigned in case metadata | One paired isolated scenario exercises separately supplied required and optional project-domain searches; no healthcare, tutor consent or complete job is established. |
| HW-GOAL-FLUENCY | [HW-GOAL-FLUENCY-01@1](homework/HW-GOAL-FLUENCY-01.json) | homework | retrieval | ordinary | draft; unassigned in case metadata | Goal-led B2 speaking search selects a synthetic travel activity and excludes a same-topic written-discourse distractor; no learner-record authorization or complete job is exercised. |
| HW-NUMERIC | [HW-NUM-01-ZERO@1](homework/HW-NUM-01-ZERO.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-02-TWO-OBSERVATIONS@1](homework/HW-NUM-02-TWO-OBSERVATIONS.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-03-FOUR-OPPORTUNITIES@1](homework/HW-NUM-03-FOUR-OPPORTUNITIES.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-04-FIVE-OPPORTUNITIES@1](homework/HW-NUM-04-FIVE-OPPORTUNITIES.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-05-PLUS-015@1](homework/HW-NUM-05-PLUS-015.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-06-MINUS-015@1](homework/HW-NUM-06-MINUS-015.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-07-STABLE@1](homework/HW-NUM-07-STABLE.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-08-MAINTENANCE-SUPPORTED@1](homework/HW-NUM-08-MAINTENANCE-SUPPORTED.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-09-MAINTENANCE-UNSUPPORTED@1](homework/HW-NUM-09-MAINTENANCE-UNSUPPORTED.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-10-MIXED@1](homework/HW-NUM-10-MIXED.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-NUM-11-POSSIBLE-REGRESSION@1](homework/HW-NUM-11-POSSIBLE-REGRESSION.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real fixed-clock calculation identifies one 0.15 drop as possible regression with an insufficient established trend. |
| HW-NUMERIC | [HW-NUM-12-COMPLETION@1](homework/HW-NUM-12-COMPLETION.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real fixed-clock calculation keeps 18/20 attempted accuracy separate from 1/4 activity completion. Workload recommendation is a draft label, not a calculator output. |
| HW-RECENT | [HW-RECENT-01@1](homework/HW-RECENT-01.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; authorization and review not checked. |
| HW-RETRIEVAL | [HW-RETRIEVAL-01@1](homework/HW-RETRIEVAL-01.json) | homework | retrieval | ordinary | draft; unassigned in case metadata | Real HTTP search; material review flags simulated. |
| HW-RETRIEVAL-CONTRAST | [HW-RETRIEVAL-CONTRAST-01@1](homework/HW-RETRIEVAL-CONTRAST-01.json) | homework | retrieval | ordinary | draft; unassigned in case metadata | Real HTTP search; positive-form target rejected before search, so its retrieval exclusion remains unobserved. |
| HW-RETRIEVAL-OUTAGE | [HW-RETRIEVAL-OUTAGE-01@1](homework/HW-RETRIEVAL-OUTAGE-01.json) | homework | retrieval | critical | draft; unassigned in case metadata | Real HTTP search with a simulated query-embedding failure; no complete preparation job. Not in reviewer batch 1. |
| HW-NUMERIC | [HW-WINDOW-01@1](homework/HW-WINDOW-01.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |
| HW-NUMERIC | [HW-WINDOW-02@1](homework/HW-WINDOW-02.json) | homework | subskill_analysis | ordinary | draft; unassigned in case metadata | Real recent-performance calculation; tutor confirmation of maintenance not implemented. |

The owner confirmed on 3 November 2026 that reviewers 1 and 2 are qualified
and available, and requested review materials for them. No review decision has
been supplied. Every exact expected label needs qualified-tutor review; critical
items and at least 20% of ordinary items in a frozen suite also need a second
qualified reviewer. Assignment is not review. All samples are synthetic, in
the development split and do not enter a release suite.

## Required family and variant gaps

No complete-job sample or review exists for any of the following required base IDs. Some draft stage samples are listed above.
Their precise situations, stage membership and independently runnable variants
are specified in [datasets sections 4–5](../specs/datasets.md#4-twelve-initial-homework-families).
The isolated arithmetic and source samples above do not count as base families.

| Job | Required base family IDs | Severity | Status |
| --- | --- | --- | --- |
| homework | HW-01, HW-02, HW-03, HW-04, HW-05, HW-06 | ordinary | all missing |
| homework | HW-07, HW-08, HW-09, HW-10, HW-11, HW-12 | critical | all missing |
| feedback | FB-01, FB-02, FB-03, FB-04 | ordinary | all missing |
| feedback | FB-05, FB-06, FB-07, FB-08 | critical | all missing |

Required variants are missing as reviewed items. Drafts for `HW-01.assigned-only@1`, `HW-01.encounter-only@1`, `HW-02.listening-unavailable@1`, `HW-02.listening-key-mismatch@1`, `FB-02.zero-opportunities@1`, `FB-03.incomparable-history@1`, `FB-03.trend-boundaries@1`, `FB-04.missing-current-transcript@1`, `FB-04.expired-current-transcript@1` and `FB-05.no-permission@1` exist above; the remaining variants below are missing as independently authored items:

- Homework ordinary: `HW-01.old-history`, `HW-01.history-correction`, `HW-02.goal-reading`,
  `HW-02.goal-listening`, `HW-02.goal-vocabulary`, `HW-02.goal-fluency`,
  `HW-02.goal-discourse`, `HW-02.goal-strategy`, `HW-02.goal-project`,
  `HW-04.uncertain-prerequisite`.
- Homework critical: `HW-07.no-adult-confirmation`, `HW-09.wrong-key`,
  `HW-09.ambiguous-key`. HW-09 also requires a separately checked
  corrected outcome and exact approval.
- Feedback ordinary: `FB-03.cumulative-context`.
- Feedback critical: `FB-05.deleted-learner`, `FB-06.unsupported-claim`,
  `FB-07.changed-section-reapproval`, `FB-07.copy-isolation`,
  `FB-08.no-memory-write`.

Additional isolated cases in the dataset contract remain missing, including
ordinary and critical outcomes for every applicable active stage, expired
sources, impossible allocations, reviewed neutral-domain fallback, deleted-learner
publication, duplicate/stale actions, and the specified long/contradictory
feedback sources. Stage eligibility and stop reasons must be recorded per item;
no stage coverage is inferred from a family name or metadata alone.

## Existing checks and remaining coverage

These are software test locations, not reviewed gold labels. Current execution
results and limits are recorded in [E0 checks](e0-checks.md).

| Requirement | Existing check | Dataset / observation gap |
| --- | --- | --- |
| Separate rates, selected source and insufficient trend | `tests/unit/test_fixtures.py::test_recent_fixture_against_real_metrics_boundary` | One ordinary draft; no tutor review, authorization, persistence or end-to-end check. |
| Zero denominator; 2/3 observations; 4/5 opportunities; ±0.15 and stable; 0.85 support; latest four; old sources; mixed measures | `tests/unit/test_fixtures.py` and `tests/unit/test_metrics.py` | Separate draft items now exist, but none is reviewed. Confirmation of maintenance is not implemented by the pure function. |
| Possible-regression alert and completion separate from attempted accuracy | `HW-NUM-11-POSSIBLE-REGRESSION@1` and `HW-NUM-12-COMPLETION@1`, through `tests/unit/test_fixtures.py` | Both drafts are unreviewed. The calculation does not emit or deliver the PD-09 workload-check recommendation. |
| Correction and persisted recent rates | `tests/integration/test_intake.py::test_correction_fixture_at_persistence_and_fixed_clock_boundaries` | One unreviewed isolated draft; confirmation timestamps are supplied fixture facts, not persisted API observations. Full frozen-history repair belongs to Stage 2R. |
| Assignment versus encounter without invented performance | `tests/integration/test_intake.py::test_activity_fixture_preserves_recent_performance` | Two unreviewed intake/context drafts; confirmation dates and approval/copy are supplied, not observed workflow actions. Exposure classification and generated claims are not evaluated by this endpoint. |
| Suitable candidate, distractors, gap, eligibility and unavailable/mismatched listening | `tests/integration/test_retrieval.py`; `HW-02.listening-unavailable@1` and `HW-02.listening-key-mismatch@1` | Both named variants are unreviewed retrieval-only drafts. No actual audio or independently reviewed teaching asset label; no complete-job observation. |
| Contrast search and positive-form-only distractor | `tests/integration/test_retrieval.py::test_contrast_fixture_reports_unsupported_positive_form_target` | The truthful positive-form target is rejected at import; exclusion from an eligible corpus remains unobserved. |
| Eligible general-domain candidate and wrong-confusion domain match | `tests/integration/test_retrieval.py::test_retrieval_fixture_against_http_boundary` | One ordinary draft, synthetic review flags and no independent tutor or content review; required positive-form distractor still missing. |
| Optional neutral fallback versus required-domain gap | `tests/integration/test_retrieval.py::test_domain_fixture_distinguishes_required_from_optional` | One unreviewed paired isolated case, not two separately certified items. No healthcare domain, clarification or user approval to relax a constraint is exercised. |
| Goal-led speaking without an invented error | `tests/integration/test_retrieval.py::test_goal_fluency_fixture_against_http_boundary` | One unreviewed isolated search draft; not the complete required `HW-02.goal-fluency` outcome, a learner-record authorization check, or evidence of speaking performance. |
| Access scope, private canaries, malformed request, cache eligibility and provider failure | `tests/integration/test_retrieval.py`; `HW-ACCESS-01@1` and `HW-RETRIEVAL-OUTAGE-01@1` exercise private material isolation and embedding failure; `HW-LEARNER-ACCESS-01@1` checks two-tutor learner-source intake | These critical items are unreviewed. Tests observe their stated local HTTP/database/cache and captured-log boundaries only; no external identity-provider login, future model, checkpoint or complete preparation is established. |
| Feedback source, extraction and analysis | Draft FB-SOURCE, FB-02 extraction, FB-03 comparison and FB-04 missing/expired-source items; shared numeric calculation tested for FB-03 | No implemented feedback job; source selection and extraction are not execution evidence. Composition, validation and review samples remain missing. |

Full frozen manifests, baseline comparison, missing-score and release-gate
arithmetic belong to the first experiment and later stage exits; none is claimed
here. Langfuse setup and paid model calls are not prerequisites for these local
synthetic checks.
