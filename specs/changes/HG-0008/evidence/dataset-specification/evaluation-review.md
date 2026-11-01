# Dataset specification — independent evaluation-content review

Date: 1 November 2026. Verdict: **GO for specification content in the assigned scope**.

This verdict does not approve a dataset, label, experiment, application release or live evaluator. All described execution and verification remain future work.

## Reviewed inputs

Before semantic review, independently recomputed the five hashes in draft-inputs.json; every value matched the actual file:

| Input | SHA-256 |
| --- | --- |
| specs/datasets.md | `90805e46e135dbdea0b254222b4e7cc4d10daa184e997c9ba4da62eb4c76cf6d` |
| specs/README.md | `5ff8e70d7c29178d7bd81962839502792f8ab774b47066b8f78f14453ae25203` |
| specs/changes/HG-0008/spec.json | `70f2ecb5746062a368a2dcd666ee27da7808f13ae24b38ba187e9aa13686f4f9` |
| Product Decisions.md | `dda62c0835e507fa48b59197090ae86888e48e05b11cccca2952ec18a7db9164` |
| Architecture.md | `ca54755bb6367f8132d222a9351b4d69dc6f83161e161e8c5e9220367c215e80` |

Read the complete dataset guide and HG-0008 requirements/scenarios/tasks, the updated index, PD-34/35 and Architecture §10. Checked privacy and integration references against the relevant source boundaries. Applied the active HighGrade independent-review distinction between normative content and observed execution. Earlier research/advice was not treated as review of the final text.

## Findings by priority

No P0, P1 or P2 actionable content findings in the assigned scope. No preference-only changes are required for this verdict.

## Evaluation observations

- **Fields and label isolation — datasets.md:18–32; HG-0008-R2/S4–S6:** The guide defines input/expectedOutput/metadata responsibilities, identity/revision, fixture resolution, stage vocabulary and evaluator-only information. Invalid/missing fields or references prevent execution. Provider-payload observations are explicitly future checks. Open valid alternatives are assessed by criteria, while task gold, proposed solver keys and judge human verdicts remain withheld. The numeric example demonstrates arithmetic without inventing response-level extraction evidence.
- **Family versus stage coverage — datasets.md:34–70; HG-0008-R3/S7–S9:** Twelve families are distinguished from executable variants/stage items and independent examples. The level/severity matrix matches the native requirement: four A2, four B1, four B2; six ordinary and six critical base families. Required no-adult-confirmation, wrong-key and ambiguous-key variants cannot be replaced by a safe base case. Every active stage requires ordinary-success and relevant critical coverage, with isolated cases filling gaps. Expected early stops neither become fabricated stage results nor replace stage coverage. The PD-08/09 numeric, recency, correction and comparable-evidence boundaries are stated as planned fixtures.
- **Review and provenance — datasets.md:72–78; HG-0008-R4/S10–S12:** Each item revision/variant/intermediate label requires first review; every critical item and ceil(20% of ordinary items) require second review. Unresolved disagreements block admission. Synthetic initial learner fixtures, teaching rights and separately permitted/anonymized production reuse preserve source policy. Retirement or a frozen manifest does not claim to erase historical/private content; required deployment deletion behavior remains to be verified.
- **Frozen definitions and baseline — datasets.md:80–84; HG-0008-R5/S15:** The manifest pins item IDs/revisions/hashes, fixtures/corpus, clock, stops, severity, schema/rubric/evaluator definitions and model/application configuration. Pinning schemas separately correctly addresses the documented item-version/schema distinction. Candidate results do not auto-create an accepted baseline. A first run without a prior baseline is explicitly identified; later definition/label/retirement changes need visible review rather than silent regression removal.
- **Denominators and strict gates — datasets.md:84–93; HG-0008-R5/S13–S15:** A case requires all mandatory assertions/criteria; individual criteria cannot inflate passing-case counts. Ordinary rates use all required ordinary items separately per stage and end-to-end, with ceil(0.90 × N) passes; zero ordinary coverage is a gap. Six initial ordinary complete-job base cases therefore require six passes, not five. All critical cases/variants and accepted previously passing cases remain protected. Missing/invalid scores and execution errors fail the gate independently of the ordinary semantic-failure allowance. A correct expected refusal/incomplete result can pass; an infrastructure exception cannot impersonate it.
- **Judge calibration independence — datasets.md:95–99; HG-0008-R6/S16–S17:** The calibration collection remains distinct from homework release coverage. At least 20 distinct human-labeled outputs, unique-output/per-criterion reporting, both human classes per criterion, qualified review and withheld human labels prevent straightforward count/answer leakage. Related family/variant outputs stay in the same partition. Tuning on holdout content invalidates its independence and requires fresh human-labeled outputs before a fresh claim. False acceptance, false rejection and invalid/missing verdicts remain visible. No universal accuracy cutoff or statistical reliability guarantee is invented.
- **Online separation — datasets.md:101; HG-0008-R1/S2 and R6/S18:** Mandatory preparation validation applies to every request; the 10% permitted-run semantic sample is additional. Eligible/sampled/completed/missing counts and weekly critical-plus-random review preserve coverage visibility and avoid presenting a flagged-case prevalence as a random rate. Live-to-gold admission requires its own permission and full review. Model agreement and tutor approval do not prove learning gains.
- **Guide/native/index consistency:** The six native requirements and eighteen scenario examples substantively cover the guide's construction, coverage, admission, freezing/gating and calibration duties. The index identifies the expanded dataset contract and preserves deferred application design. The guide assigns acceptance ownership to the native requirement and construction details to the guide; neither claims actual created datasets or measured outputs. HG-0008 tasks remain unfinished, executable checks remain unbound and no results file claims runtime PASS.

## Limits and remaining verification

This is static specification-content review. It confirms explicit, mutually consistent planned behavior; it does not establish that future fixtures contain valid English teaching content, that reviewers supplied genuine gold labels, or that loader/gate/judge implementations comply. Actual source/response annotations, allowed answers, JSON schemas, frozen item membership and reviewed labels are to be authored later under these contracts.

Future verification must observe real evaluator aggregation, provider payloads, database/worker/export boundaries, independent held-out labeling and the chosen deployment's deletion behavior. Reading scenario text or passing native structural validation cannot establish those outcomes. No runtime, model, SDK, service, dataset, release or native evidence mutation occurred. Only this original review report was written.
