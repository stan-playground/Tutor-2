# Golden dataset implementation plan

## Purpose and status

This is a **proposed, planning-only** simplification of the evaluation streams in [Implementation Plan.md](<Implementation Plan.md>) and [Plan_High_Level.md](Plan_High_Level.md). It does not change [Product Decisions.md](<Product Decisions.md>), [the dataset guide](specs/datasets.md), [HG-0008](specs/changes/HG-0008/spec.json), other specifications, or authorize implementation, account creation, real-data use or launch. Those sources continue to govern until a requirement change is agreed and recorded through HighGrade.

The practical target is **about 10 distinct synthetic cases per job** for an initial useful set, plus a small initial set for judge calibration. A case can carry expectations for several stages; do not create a separate ten-case dataset for every stage. Add an isolated item only when a material behavior cannot be checked clearly through a complete case. Counts are targets, not evidence of coverage or statistical reliability.

**Current status:** [evaluation/README.md](evaluation/README.md) identifies two synthetic development fixtures, neither approved gold. The homework arithmetic example is not a complete-job family, and the feedback example is a draft. Reviewer assignments are not completed reviews. No approved dataset or measured model quality is established by this plan.

## Decision needed before replacing the current release scope

The requested size is substantially smaller than today's release contract. HG-0008 and the dataset guide require **12 homework families**, **8 feedback families**, specified variants and isolated items, including ordinary and critical coverage at each applicable stage. The implementation plan estimates roughly 29 homework and 20 feedback complete-job items, plus isolated items. Ten initial cases per job therefore do **not** satisfy the current release requirements merely because a table names ten cases.

For a semantic judge, HG-0008 and the dataset guide require **at least 20 distinct human-labeled outputs overall**, both pass and fail examples per evaluated criterion, a family-aware split and a fresh holdout after tuning. The implementation plan is stricter: **20 per job plus fresh holdout**. This divergence needs an explicit decision; ten outputs cannot satisfy either current threshold. Distinct outputs, not ten outputs scored against two criteria, are the unit of count.

**Recommendation:** start with ten cases for each job and ten candidate outputs as a provisional calibration seed. Before anyone relies on a judge, retain at least the existing 20-distinct-output minimum and job/criterion coverage; decide explicitly whether the plan's 20-per-job target is justified. Retain all critical safety, privacy, authorization, evidence and review behaviors, and the real integration checks they require. If a smaller release suite is desired, map each existing required family and variant to an executable replacement or explain the gap, then use `highgrade-task`/`highgrade-spec` to agree and update the affected normative requirements and downstream plans. Do not call a proposal an approved change. A case with multiple assertions saves authoring effort but cannot make mutually exclusive inputs, outcomes, or unexecuted stages into one test result.

Ten ordinary examples at a 90% threshold allow one ordinary failure in isolation; they cannot support a broad reliability claim. Small critical subsets may still expose serious failures, but passing them does not prove their absence in production. Current no-regression and missing-score rules still apply.

## Proposed initial case inventory

These are design sketches, not authored or reviewed items. Select the highest-value boundaries first and reuse a fixed synthetic learner situation where appropriate. Each separately executed input or outcome receives its own item ID and review. A base case does not silently cover a named variant. Critical security and state assertions must be demonstrated at actual boundaries, not only scored by a language model.

### Homework: ten starting situations

| # | Starting situation | Main expectations and existing coverage to map |
| --- | --- | --- |
| 1 | A2 everyday lesson, recent difficulties and an older relevant activity | Separate recent counts from historical exposure, explain priorities and timing; HW-01 and old-history. |
| 2 | B1 workplace communication with a valid alternative and missed required use | Correct denominators and attribution, adapt reviewed material without changing its purpose; HW-02. |
| 3 | B2 goal-led discussion without a visible error | Choose a suitable fluency/discourse route and criteria without inventing a deficit; HW-03 and applicable HW-02 goal variants. Other enabled routes still need actual coverage. |
| 4 | A2 sparse or conflicting evidence, with expired history | Preserve unknowns and request a useful recheck; HW-04/05. A missing-duration stop needs its own executable input. |
| 5 | B1 constrained material search, with plausible wrong-purpose distractors | Choose a suitable authorized asset or report an honest gap; HW-06 and retrieval boundary. A provider outage is a distinct failure check. |
| 6 | A2 unsafe material or missing adult permission | Block the relevant path; HW-07. Content safety and permission are separate executable outcomes. |
| 7 | B2 two tutors and learners, with foreign-data canary and hostile transcript instructions | Enforce ownership and treat instructions as data; HW-08/10. Test denial and injection independently if one prevents reaching the other. |
| 8 | B1 adapted exercise with incorrect or ambiguous teacher key | Block defective keys, independently solve, and keep keys out of student output; HW-09. Incorrect and ambiguous keys are separate inputs. |
| 9 | B1 section approval, rejection, revision and stale action | Enforce exact versions, approval invalidation and approved-only export; HW-11. |
| 10 | A2 approved timed draft changed from 20 to 15 minutes and finalized twice | Recompute timing, require appropriate reapproval and avoid duplicate effects; HW-12. Assignment and actual-use claims require separate evidence. |

Balance A2–B2, common domains and ordinary/critical outcomes across the actual authored items. Listening recording/criteria mismatches, goal-led routes, source withdrawal, history correction and numerical edge cases cannot be declared covered simply by the broad descriptions above. Map them explicitly; retain required additional items unless the contract changes.

### Feedback: ten starting situations

| # | Starting situation | Main expectations and existing coverage to map |
| --- | --- | --- |
| 1 | A2 current lesson plus relevant prior evidence | Ground strengths and difficulties in the selected source; separate student sections and tutor notes; FB-01. |
| 2 | B1 transcript with learner and tutor speech and optional paraphrase | Attribute speech correctly and preserve accuracy, use and avoidance denominators; FB-02. |
| 3 | B2 mixed assistance and limited comparable history | Qualify comparisons and retain old history outside recent counts; FB-03. |
| 4 | A2 ambiguous speakers and unavailable historical source | Express uncertainty, avoid invented historical quotes; FB-04. |
| 5 | Missing or expired selected current transcript | Stop with an explicit source gap; notes or old history cannot replace it; FB-04 variants. Missing and expired are separate inputs. |
| 6 | Two tutors/learners and a foreign canary | Deny unauthorized processing before provider calls; FB-05. Permission withdrawal and deletion require separately exercised outcomes. |
| 7 | Transcript instruction injection and unsupported candidate claim | Ignore imported instructions while using legitimate evidence; reject unsupported claims; FB-06. |
| 8 | Reviewed sections followed by substantive change and stale approval | Reapprove changed sections and reject stale actions; FB-07. |
| 9 | Private tutor-note canary in a ready draft | Actual copy/download excludes private notes and unapproved content; FB-07 copy isolation. |
| 10 | Known observation/activity rows before review and repeated export | No approval, revision or copy creates learner performance or history facts; FB-08. |

Feedback has its own transcript, claim and review expectations; it does not require a homework job, exercise, answer key or duration. A stop case does not prove stages that it never reaches.

### Judge calibration: start small, expand before use

Begin with around ten **distinct** candidate outputs only when useful real synthetic-run outputs exist. Include plausible passing alternatives and actual failures for the immediate criteria. Have a qualified tutor label each output and reason, keep related cases in the same development or holdout split, and hide labels from the judge. Expand to at least 20 distinct outputs overall before reliance, including both human pass/fail examples for every evaluated criterion and relevant job coverage. Keep a fresh human-labeled holdout after tuning and report false accepts, false rejects and missing verdicts. Feedback attribution and grounding need their own labeled examples; homework cannot establish them. Resolve the stricter per-job plan requirement before claiming its milestone complete. A deterministic assertion or tutor review can be used without creating a semantic judge.

## Small, ordered implementation stages

Each block ends with a concrete reviewable result before dependent work begins. This ordering is a proposal; the current plan's stage-exit and release requirements remain in force.

1. **Inventory and contract decision.** Make one small table of existing requirements, proposed case IDs, stage memberships, criticality and explicit gaps. Confirm which proposed consolidations preserve each required observable result. Record the reviewer qualification and assign qualified tutors; determine availability, but do not mark an assigned review complete. If reducing release requirements, agree and update the product/specification owners first. No change to the contract is needed merely to prepare an initial tranche. Completion: inventory and decisions are reviewable; existing obligations remain visible.
2. **First authored case.** Use the existing `evaluation/` structure and item schema. Write one wholly synthetic homework input with source/version/time, expected facts, forbidden outcomes, rubric and provenance; resolve referenced fixtures. Ask a qualified tutor to review the exact revision, and a second reviewer for critical items and the required ordinary sample. Fix disagreements before approval. Check the JSON and schema and inspect whether the expected result is actually decidable from the input. Completion: one reviewed case, or a clearly labeled draft if reviewers are unavailable. Avoid designing a new platform first.
3. **Expand the two job sets.** Repeat the same small author-review-verify cycle toward the ten starting situations per job. Author feedback source/extraction/analysis inputs in parallel with homework where independent. Reuse cases for applicable stage labels, but record each input, expected outcome, reached stage and review. Add focused numerical, route, failure and state items only for uncovered requirements. Content used in retrieval/adaptation needs reviewed rights and suitable versions; do not invent licensed source content. Completion: an explicit coverage and gap list, item counts and exact reviewed revisions. The target is not a substitute for the current full release inventory.
4. **Minimal local execution.** Once a real case and a real boundary can be exercised, load its fixed input and check deterministic expected facts using existing project tools and tests; write a small manifest/results record only to the extent needed to identify the case revision, inputs, expected result and observed outcome. Do not expose expected answers to the application. Run an ordinary and a relevant critical check at each active boundary; retain real authorization, deletion, persistence and export tests separately. Add the complete frozen manifest, gate arithmetic and baseline comparison when an actual experiment needs them, as required by the current contract. Do not assume `just eval <job>` exists: it is proposed in the existing plan.
5. **Follow implementation, then evaluate.** Prepare and review boundary labels before the corresponding model stage: extraction 3b; selection 3d; retrieval/adaptation 3e; composition/validation 3f; review/revision 4. Feedback source/extraction/analysis are used by 8a, composition/validation by 8b, review by 8c. Current plan exits for model stages require approved boundary gold and a recorded Langfuse experiment against the accepted baseline; draft-only and local-only runs do not meet that exit. Set up the Langfuse mirror when that first actual experiment is ready, subject to authorized account access and the existing plan. Deferring the setup does not remove its current exit requirement.
6. **Calibrate only when needed.** Label candidate outputs from homework 3f and feedback 8b, then perform the calibration and holdout checks above before relying on semantic judging. Prefer deterministic checks for counts, access, state and exact export. A judge cannot waive hard gates or replace tutor decisions.
7. **Certify separately.** At homework stage 6 and feedback stage 9, freeze each job's full applicable reviewed suite and manifest; run critical, ordinary, missing-score and accepted-baseline gates, plus actual integration/privacy/recovery checks. Homework results do not qualify feedback. Current planned Langfuse and online-monitoring obligations remain. Real use and activation need separate authority. Pilot curation is a later activity, using synthetic reproductions by default; production-derived reuse needs separate permission, reviewed anonymization and deletion controls.

Lesson planning and urgent replanning are later product stages, not ready-made datasets. Define each job's actual contract and a small representative set when that job is prepared; do not create speculative suites now. They require their own reviewed cases and readiness before activation.

## Dependency and blocker map

| Work | What blocks it | What does not block it |
| --- | --- | --- |
| Draft synthetic homework/feedback inputs and expected outcomes | No technical stage is inherently required. Authoring time and a clear expected behavior are needed; check existing schema and contracts. | 2R, generation, cloud account, a completed harness, real learner data and pilot launch. |
| Approved gold | Qualified English tutor review of every exact label; second qualified review for all critical and at least `ceil(20% × ordinary)` per frozen suite; resolved disagreements, provenance and suitable rights. Availability has not been verified. | Model execution is not intrinsically needed for an authored expected outcome. |
| Retrieval/adaptation gold | Suitable reviewed, rights-cleared asset versions and correct expected outcomes; closed answers independently solved. | A full route × level × domain cross-product is not intrinsically necessary for the first case; current C0/C1 requirements still apply to their stated milestones. |
| Composition/validation/review labels under the existing plan | Stage 3a's drafted job schemas and, where applicable, specific content and review behavior. | Waiting for all later feedback implementation is unnecessary for authoring earlier feedback inputs. |
| Model stage implementation | Existing plan makes Stage 2R repairs a prerequisite for Stage 3; 3a also depends on L0. Stage exits additionally need approved gold and recorded Langfuse baseline experiments. | These dependencies do not prevent offline synthetic authoring. |
| Judge calibration | Candidate outputs, qualified human labels, criterion coverage and uncontaminated split/holdout. 3f and 8b produce the planned job outputs. | It is not needed to write the first fixtures or perform deterministic checks. |
| Homework certification / feedback certification | Respective implemented job boundaries, reviewed full required suites, baseline and judge evidence, plus stage 5 controls and real integration checks; feedback also needs 8a–8c. | Homework pilot cohort results are not a prerequisite for beginning feedback implementation under the current plan. |
| Real-data processing, production cases and activation | Separate permission, privacy/processor and deletion readiness, applicable release gates and separate activation authority. | None is needed for wholly synthetic drafting. |

Stage 2R is described in the two Stage 1 fix plans and [Implementation Plan.md](<Implementation Plan.md#build-stages>); this review does not independently certify its current runtime status. Stage 2 changes were in progress when this plan was reviewed; check the current commit, worktree and stage reports before relying on a specific implementation revision. A missing available tutor or rights-cleared content is a potential blocker until confirmed, not an observed staffing or licensing failure.

## Review of the existing plans

- **Keep:** gold before the affected model stage, synthetic initial data, stage-specific expectations, human review, explicit critical outcomes, actual integration checks, frozen comparisons and job-specific certification. These address concrete errors that a single end-to-end quality score can hide.
- **Simplify first work:** author and review one real example, then grow to approximately ten per job; use one case at multiple applicable boundaries and add isolated examples for real gaps. A small inventory replaces a speculative large matrix as the first deliverable, but must expose omitted mandatory cases.
- **Avoid front-loading:** the existing E0 bundles the full family inventory, all numerical/retrieval coverage, a generic evaluation harness, Langfuse synchronization and a large content matrix. These can be sequenced around the first working case and first experiment. This changes ordering only unless requirements or stage exits are formally revised.
- **Do not count integrations as dataset samples:** authorization, lifecycle and stale-state tests can use the same synthetic situations but require observations of actual boundaries. A model's judgment alone cannot establish them.
- **Resolve the judge count divergence:** 20 overall in HG-0008 versus 20 per job in the implementation plan. Treat both as current until explicitly reconciled; do not quietly substitute ten.
- **Historical review:** [Plan Review_claude.md](<Plan Review_claude.md>) reviews an earlier plan. Check its suggestions against the present implementation plan before adding work; its call to schedule gold early has since been addressed by E0–E5. Its critique is not proof that a later stage is implemented.

**Next authorized implementation request:** begin Stage 1 of this plan, then author one synthetic case and arrange its review. If the intended outcome is a release suite of approximately ten cases per job rather than a ten-case starting tranche, first agree the specific requirements to change and reconcile the product decision, HG-0008, dataset guide and affected plans.
