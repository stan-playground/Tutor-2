# Plan Review — evaluation, Langfuse and acceptance consistency (Claude)

Review date: 3 November 2026 · Base: `b0c9b96` (working tree has unrelated uncommitted Stage 2 edits, untouched)

Reviewed: [Implementation Plan.md](<Implementation Plan.md>) and [Plan_High_Level.md](Plan_High_Level.md), against
[Product Decisions.md](<Product Decisions.md>) (the 11 highest-priority principles, PD-31/34/37/38),
[specs/datasets.md](specs/datasets.md), [Architecture.md §10](Architecture.md), HG-0003/0005/0008/0010, the stage
records and both Stage 1 fix backlogs.

This is a review and a proposed plan only. It changes no product decision, specification or plan file, and
authorizes no implementation, provider spend, Langfuse account or real-data use.

## 1. Verdict

The plans agree with each other and with the product on **scope, job order, safety, privacy and tutor
authority**. They are not yet consistent with the acceptance criteria for either job in four places:

1. **Golden datasets are specified but not scheduled.** [datasets.md](specs/datasets.md) is a strong contract.
   But neither plan turns it into delivery work with owners, quantities, reviewers or stage exits. All of it is
   left to stage 6 (homework) and stage 9 (feedback), at the end of the critical path.
2. **Langfuse has no stage at all.** It appears in the stack list, a version note, a stage 5 "must not leak"
   line and a stage 6 "wire permitted monitoring" phrase. No stage owns hosting, tracing, dataset sync,
   experiments, scores, online evaluation or deletion. This fails principle 9 for both jobs.
3. **Extraction belongs to no stage.** PD-08, PD-34, PD-37, datasets.md and Architecture §10 all assume model
   extraction of observations from notes and transcripts. [HG-0003](specs/changes/HG-0003/spec.json) explicitly
   excludes it ("No LLM extraction"), and no later stage or spec picks it up. Without extraction, tutors
   hand-code every count. That puts the PD-31 effort target at risk and leaves the feedback learning curve
   empty unless tutors code each lesson.
4. **Some principle-level scope was narrowed without an owner decision.** Principle 5 lists lesson
   transcripts as vector-database assets, but neither plan indexes them. Neither plan names a tutor-facing UI
   or a reviewed-content stream either, and the pilot journey needs both.

## 2. What is already right (keep)

- The dataset contract has three datasets, a typed item contract, per-stage boundaries, 12 + 8 families,
  history and route variants, and frozen manifests. It also has gate arithmetic (`ceil(0.90 × N)` per job,
  stage and E2E), the critical-must-pass rule, missing score = fail, no baseline regression, judge calibration
  with fresh holdout, and production-to-gold through permission and anonymization. Nothing needs redesigning
  here. The gap is delivery.
- Gates are kept separate per job, so homework success cannot hide feedback failure.
- Privacy rules for Langfuse are right in principle: metadata only, minimum redacted excerpts, 30-day expiry
  and learner-linked deletion.
- Stage 2 already gives a cheap, LLM-free retrieval boundary that can be evaluated now: local FastEmbed with
  exact pgvector search.

## 2a. The separate golden-dataset document

The golden-dataset document is **[specs/datasets.md](specs/datasets.md)**, titled "Homework and feedback
evaluation datasets". It is the construction contract under
[HG-0008](specs/changes/HG-0008/spec.json), which owns the acceptance requirements. Related material:

| File | Role | Status |
| --- | --- | --- |
| [specs/datasets.md](specs/datasets.md) | Contract: three datasets, the item contract, stage boundaries, 12 homework + 8 feedback families, PD-39/40 variants, review and provenance, frozen manifests and gates, judge calibration, online additions. | Current text reviewed under HG-0011 ([review](specs/changes/HG-0011/evidence/review-consistency-v1.md)). Earlier GO reviews: [HG-0008 evaluation](specs/changes/HG-0008/evidence/dataset-specification/evaluation-review.md), [pedagogy](specs/changes/HG-0008/evidence/dataset-specification/pedagogy-review.md), [privacy](specs/changes/HG-0008/evidence/dataset-specification/privacy-review.md), [HG-0009](specs/changes/HG-0009/evidence/evaluation-review-v1.md). |
| [evaluation/README.md](evaluation/README.md), [item.schema.json](evaluation/item.schema.json) | Structural schema v1 and two draft items (`HW-ARITH-01`, `FB-SOURCE-01`). | Draft, unreviewed. No runner or Langfuse connection. |
| [plan-evaluation-review.md](docs/evidence/preparation-2026-11-01/plan-evaluation-review.md) | Independent GO on an **earlier** Implementation Plan revision (before feedback and PD-39/40). | GO for "text coherence" only. It found the early-start wording sufficient but did not test whether evaluation has delivery owners or stage exits. |

So the golden-dataset **design** exists and is reviewed. This review's finding is narrower: neither plan turns
that contract into scheduled delivery (F1), and nothing integrates Langfuse (F2). The dataset document
itself has these gaps:

1. **No inventory.** It never totals the items per job and stage. "Release counts follow each frozen
   manifest" means the labeling workload stays unknown until the end. Add a planned inventory table: items ×
   stage × severity × reviewer passes.
2. **"Qualified English tutor" is undefined.** HG-0008 and the evaluation README do not define the
   qualification, its evidence or reviewer independence. Reviewers `1` and `2` therefore cannot yet approve
   anything.
3. **Langfuse mapping stops at dataset items.** §1 maps `input`/`expectedOutput`/`metadata`. Nothing names:
   - score names and types for deterministic assertions and judge criteria
   - experiment and run naming, and the run metadata that links to the manifest
   - how online tutor decisions become scores
   - which store is canonical, Git or Langfuse (recommendation: Git)
4. **The extraction stage is assumed.** Homework and feedback extraction boundaries are defined, but no build
   spec delivers extraction (F3). As written, those stages would count as coverage gaps at gate time.
5. **The online section lacks operating details.** It specifies 10% sampling and weekly review but not:
   - who reviews
   - the review queue or tool
   - how results feed back into gold candidates
   - cost and latency observation (PD-26/36), which belongs with the Langfuse work even though it is not
     gold
6. **Retrieval fixtures are still unwritten** although Stage 2 is implemented. The §3 "search construction"
   cases (contrastive distractors, private canaries, embedding outage) are planned only, while the code they
   test already exists.

None of these needs a new dataset platform. Items 1–3 are additions to datasets.md and HG-0008, through
`highgrade-spec` because they change the contract. Items 4–6 belong to the delivery plan.

## 3. Findings

Ordered by impact on acceptance.

### F1 — Golden data is a contract without a delivery stream (high)

Evidence:

- [evaluation/](evaluation/README.md) holds two **draft** items. Neither is reviewed. The reviewer IDs `1` and
  `2` have no recorded qualification. HG-0008 tasks T1–T5 are all `done: false`.
- The Implementation Plan says "prepare reviewed fixtures before implementing each model stage". Stage 2
  shipped retrieval without retrieval gold items, so the rule was already skipped once.
- Model choice ("compare model candidates on reviewed fixtures") and the first stage 3 work both need gold
  *before* stage 3. The plan only assembles gold at stage 6.
- The labeling effort is not sized. A rough estimate from datasets.md: homework has 12 base families plus
  about 17 required variants (about 29 complete-job items), each with intermediate stage labels. It also has
  about 20–25 isolated stage and numeric items. Feedback has 8 base families, about 12 variants and isolated
  items. Judge calibration needs at least 20 distinct outputs per job plus a fresh holdout. Second review
  covers every critical item and 20% of ordinary ones. That adds up to **hundreds of qualified-tutor label
  decisions**. This is the slowest human dependency in R1 and R2, and no stage plans for it.
- Fixtures need rights-cleared teaching text and listening recordings. Both are the same content the pilot
  bank needs, and no stage covers that content either (see F6).

Consequence: stage 6 becomes a long serial wait, model and prompt choices get made without evidence, and the
stage barriers for 3, 4, 8a and 8b can be "passed" with deterministic tests only.

### F2 — Langfuse is named but never delivered (high)

Evidence: no Langfuse, LangGraph or LLM dependency exists yet ([pyproject.toml](pyproject.toml)), which is
expected at this point. [Stage 0](docs/stage-0.md) deferred Langfuse "before the first model/evaluation
integration", which is stage 3. Stage 3's row does not mention it.
[Repository Structure](<Repository Structure.md>) promises `just eval homework|feedback`. The
[Justfile](Justfile) has no such recipe, and no stage builds one.

These pieces have no owner:

| Missing piece | Why it matters for acceptance |
| --- | --- |
| **Hosting decision**: Langfuse Cloud with processor terms, or self-hosted. Self-hosting adds services such as ClickHouse, blob storage and a queue; verify for the pinned release. | PD-28 needs named-processor purpose, retention and no-training terms. datasets.md §6 needs verified deletion before any production-derived item. This decision blocks real-data monitoring. |
| **Environment separation**: a synthetic dev/eval project with full trace capture, and a pilot project with masking and no automatic I/O capture. | Full traces on synthetic data make debugging possible. The blanket "no raw prompts" rule should apply to real data, not to synthetic experiments. |
| **Tracing and a masking function**, tested with privacy canaries (HW-08, FB-05). | Stage 5's "Langfuse leaks no private content" cannot be checked if tracing was never built. |
| **Dataset sync**: Git `evaluation/` is canonical and Langfuse datasets mirror it. Manifests record the Git SHA and the Langfuse item-version timestamp. | Langfuse does not version dataset schemas (datasets.md §1). A reviewed Git source keeps review history and diffs. |
| **Experiment runner and evaluators**: deterministic assertions as scores, the independent solver, and calibrated judges. Plus `just eval <job>`. | This is how "offline experiments compare changes" (principle 9) actually works. Gates need raw scores per frozen manifest. |
| **Online signals**: tutor part approve/reject and substantive-edit flags as scores on the generating trace, 10% sampled judge runs, a weekly review queue (all critical items plus 5 random), and cost and latency per active segment. | This covers principle 9 "online evaluation … tutor feedback", PD-34 weekly review, PD-26 latency targets and PD-36 cost assumptions. The draft-version record must store its trace ID **when stage 4 is designed**. Retrofitting it later is costly. |
| **Deletion and retention for Langfuse objects**: traces, scores, dataset items, run items. Checked with canaries. | PD-28 and datasets.md §6. Archiving an item does not erase it. |

### F3 — Extraction belongs to no stage (high, needs an owner decision)

- Product assumes extraction exists:
  - PD-08: "uncertain extracted observations await tutor confirmation".
  - PD-34: gold covers "extraction".
  - PD-37 journey: "tutor lesson notes or authorized transcript → draft".
  - PD-38: "Feedback approval does not confirm extracted observations".
- Design and evaluation assume it: datasets.md defines extraction boundaries for both jobs, and Architecture
  §10 lists a cheaper extraction model.
- The delivered and planned specs exclude it. HG-0003 says "No LLM extraction". HG-0005 and HG-0010 tasks do
  not mention it, and neither plan has an extraction row.
- Impact on homework: tutors must hand-enter structured counts per subskill, for example `6/8`, `5/10`,
  `3/4`. This conflicts with PD-05 (few interactions) and makes the PD-31 target of at least 25% lower median
  effort unlikely, because effort explicitly includes setup.
- Impact on feedback: the learning curve only grows if tutors hand-code each lesson. Feedback then falls back
  to transcript-only findings, with no supported comparisons. The "candidate findings" in stage 8a have no
  route to become confirmed observations.

Recommendation: add an **extraction-and-confirmation slice**. A model proposes candidate observations and
activity facts with source spans. The tutor confirms, corrects or rejects them through the existing Stage 1
intake. Only confirmed facts count. Homework uses it in stage 3 and feedback reuses it in stage 8a. This needs
a new spec through `highgrade-spec`, since it allocates an unowned requirement. The alternative is an explicit
owner decision that the pilot uses manual coding and accepts the effort risk.

### F4 — Principle 5's transcript indexing was silently narrowed (medium, owner decision)

Principle 5 and PD-33 list lesson transcripts as vector-database assets. PD-28 sets a 30-day expiry for
transcript *embeddings*. The plans decide that feedback loads the transcript directly, which is better than
top-k similarity for coverage. But no stage indexes transcripts at all, and Stage 2 excludes private text by
design.

Options:

- (a) A small learner-scoped private transcript index: owner and learner RLS, 30-day expiry, never in the
  shared bank. It answers evidence questions such as "earlier lessons where this confusion appeared" for both
  jobs.
- (b) An owner-recorded deferral.

Either is acceptable. Today's silent omission is not.

### F5 — No tutor-facing UI is planned (medium)

[web.py](src/tutor_copilot/web.py) serves JSON only. Stage 4 mentions "browser actions" for review only. The
pilot journey (PD-37) also needs tutors to:

- enter profile and intake data
- confirm evidence (and confirm extraction output, if F3 is adopted)
- start a request
- review parts
- copy approved content
- confirm assignment within 7 days
- self-report effort

Assignment confirmation and effort reports feed PD-31 directly, and UI effort is part of measured tutor
effort. Make this an explicit deliverable, split across stages 4 and 6.

### F6 — Reviewed teaching content and rights have no stream (medium)

R1 needs reviewed, rights-cleared material for seven PD-40 routes. That includes listening recordings with
version-matched criteria, at A2–B1–B2, across pilot domains. The gold fixtures need the same material. The
plans list "usable reviewed material" only as a stage 7 precondition. Make it a parallel stream (C) with a
named qualified reviewer, a coverage matrix (route × level × domain) and a gap report from the Stage 2
retrieval eval.

### F7 — The Stage 1 repair gate is missing from both plans (medium)

[Plan for Fixes Stage 1.md](<Plan for Fixes Stage 1.md>) says "Stage 3 must not start while any item below is
open". [Plan for Fixes Stage 1_claude.md](<Plan for Fixes Stage 1_claude.md>) is a second, partly different
backlog. One covers identity and provenance plus a versioned frozen context. The other covers source-body
erasure plus learner-scoped references. Neither plan has a row for this gate. Add **stage 2R**: reconcile the
two backlogs into one route, implement, review, and then unblock stage 3.

### F8 — Evaluation has no naive baseline (medium)

Architecture names "one large prompt with retrieved context" as the evaluation baseline. No stage builds it.
Without it:

- the first gate run has no comparator
- "no regression versus the accepted baseline" starts empty
- nothing shows that the multi-stage graph beats a simple approach

Build it in stage 3a. It is cheap and makes later complexity defensible.

### F9 — Judge calibration and feedback gold are scheduled too late (medium)

- Calibration needs real candidate outputs, so labeling can only start after stage 3 produces drafts. A fresh
  holdout needs a second labeling round. Leaving all of this to stage 6 serializes two human rounds at the end.
- Feedback transcripts and labels are independent of homework code. Their authoring can start now, but the
  plan implies "before its branch", which follows stage 6.
- 8a depends on "after stage 6". It technically needs only stage 1 data, the stage 3 model integration and
  extraction. 8c needs stages 4–5. Feedback build can start after stage 5 while stage 6 labeling runs, and
  release stays gated by stage 9. This is a priority trade-off for the owner. "Homework first" is about
  delivery priority, not a technical dependency (PD-03).

### F10 — Online evaluation and production-to-gold have no operating owner (medium)

Principle 9 ends with "Production examples enter the golden datasets after review". Stage 7 lists cohort
metrics but not:

- the weekly review operation
- the tutor-decision score stream
- a curation queue (permission → anonymization → label → review → admission)

Either add these to stage 7, or record an owner decision that promotion waits until after R1.

### F11 — Stage barriers have no evaluation exits (medium)

The barriers for stages 3, 4, 8a and 8b are written as behaviors, checked deterministically. Add one rule:
**each model stage exits only when its boundary's reviewed gold items exist and pass a recorded Langfuse
experiment against the frozen baseline.** Stages 6 and 9 then *freeze and certify* rather than build
evaluation from scratch. The Implementation Plan already intends this ("stage 6 assembles the full gate
rather than starting evaluation from scratch"), but no barrier enforces it.

### F12 — Document hygiene (low)

- [Implementation Plan.md:13](<Implementation Plan.md:13>) has two broken links, `(Product Decisions.md)` and
  `(Repository Structure.md)`, which need angle brackets. They were introduced in `c7dff4e`.
- [Plan_High_Level.md:15](Plan_High_Level.md:15) and [:145](Plan_High_Level.md:145) are stale. They say "Base
  `a004bdd`, Stage 1 in progress" and "next milestone: complete Stage 1", but Stages 1 and 2 are recorded
  complete.
- The §4 discrepancy note is half-stale. Implementation Plan line 9 was updated; line 66 ("start with stage
  0") was not.
- Plan_High_Level restates gate arithmetic and policy owned by datasets.md and PD-28/34, which invites drift.
  Keep a one-line reference plus release-level deltas.
- Neither plan mentions measuring PD-26 latency or PD-36 cost. Langfuse captures both. Assign them to stream
  L.

## 4. Consistency with acceptance criteria

Legend: ✅ planned and consistent · ⚠️ partial or at risk · ❌ missing.

| Acceptance criterion (source) | Homework (R1) | Feedback (R2) | Note |
| --- | --- | --- | --- |
| Job order (P1, PD-03) | ✅ | ✅ | Both plans agree. |
| Subskill accuracy / required use / avoidance (P2, PD-08) | ✅ Stage 1 done | ✅ 8a reuses | ⚠️ Values come only from manual tutor coding (F3). |
| Lesson + homework evidence change priorities (P3, PD-09) | ⚠️ | ⚠️ | Arithmetic is done. Evidence ingestion has no extraction (F3). |
| Distinct learner information (P4, PD-06/07) | ✅ | ✅ | |
| Vector DB: exercises, speaking, explanations, transcripts (P5, PD-33) | ⚠️ | ⚠️ | Teaching bank is done. Transcripts are not indexed anywhere (F4). |
| Domain adaptation (P6, PD-13/14) | ✅ stage 3 | n/a | |
| Safety, age and quality validation (P7, PD-17) | ✅ stage 3 | ✅ 8b | |
| Per-part tutor approval (P8, PD-18) | ⚠️ stage 4 | ⚠️ 8c | Logic is planned. Tutor UI is not (F5). |
| **Golden datasets for every stage (P9, PD-34)** | ❌ | ❌ | Contract exists, delivery does not (F1, F11). |
| **Langfuse offline + online, tutor feedback (P9, PD-34)** | ❌ | ❌ | No stage (F2). |
| **Production → gold after review (P9)** | ❌ | ❌ | No owner (F10). |
| Cumulative history, important-now / revisit (P10, PD-39) | ✅ stages 1, 3 | ✅ 8a | |
| Teaching beyond errors, 7 routes incl. listening (P11, PD-40) | ⚠️ | n/a | Logic is planned. Reviewed content per route is not (F6). |
| Complete journey: notes/transcript → draft → validation → review → handoff (PD-37) | ⚠️ | — | The "notes/transcript →" step has no extraction (F3). UI (F5). |
| Real-use prerequisites: auth, material, privacy, recovery, stage/E2E eval (PD-37) | ⚠️ | ⚠️ | Eval and material are missing (F1, F6). Langfuse deletion is untested (F2). |
| Pilot targets: ≥25% effort reduction, ≥80% assignment (PD-31) | ⚠️ | n/a | Measured in stages 6–7, but achievability is threatened by manual intake (F3, F5). |
| Transcript + learning curve, sections, private notes, linked claims, no writes, no homework prerequisite (PD-38) | n/a | ✅ 8a–8c | Candidate-finding extraction is unowned (F3). The 8a "after stage 6" dependency is over-constrained (F9). |
| Per-job independent gates (PD-34 feedback extension) | ✅ | ✅ | |
| Latency and cost observed (PD-26, PD-36) | ❌ | ❌ | Assign to Langfuse stream (F12). |

The two plans are **consistent with each other**: the same order, the same stage mapping, and no
contradictions except the stale status lines. They share the same four gaps, because Plan_High_Level was
derived from the Implementation Plan's stages.

## 5. Proposed high-level plan

Keep the release view (R1–R4) and stages 0–9. Add three parallel streams that the build stages depend on at
named exits. Their milestones are dependency gates, not dates.

```text
Stream A — Build:   2R → 3a → 3b → 3c–3e → 4(+UI) → 5 → 6 → 7 (pilot)
                                         └────────── 8a → 8b → 8c → 9 (feedback)
Stream E — Gold:    E0 ──→ E1 ──→ E2 ──→ E3 ──→ E4 (freeze + certify) ──→ E5 (pilot curation)
Stream L — Langfuse:     L0 ──→ L1 ──→ L2 ──────→ L3 (online) ──→ L4 (deletion verified)
Stream C — Content: C0 (coverage matrix, rights, reviewer) ──→ C1 (route × level × domain filled)
```

| Milestone | Deliverable | Must exist before |
| --- | --- | --- |
| **2R** | Reconcile both Stage 1 fix backlogs into one route; implement, review. | 3a |
| **E0** | Qualified reviewers named, with recorded qualification. Item counts sized per job and stage. Review workflow chosen (Git PR review of JSON, or Langfuse annotation). Local `just eval` runner with deterministic evaluators and manifest freezing. Retrofit gold: Stage 1 numeric fixtures (datasets.md §3) and **Stage 2 retrieval items**: suitable-candidate recall, honest gaps, contrastive distractors, private-canary exclusion. Runs today with no LLM cost. Start feedback transcript authoring now. | 3a |
| **C0** | Content coverage matrix and rights process. Gaps reported from the E0 retrieval run. | E1, 3d |
| **L0** | Owner decision on Langfuse hosting (Cloud with processor terms, or self-host). Pin the SDK after a Context7 check. Synthetic dev project. Git → Langfuse dataset sync. First experiment on the E0 items, which proves the whole path before LLM spend. | 3a |
| **3a** | Model client, graph skeleton, tracing with masking, **naive one-prompt baseline** (run on E0/E1 items as the first accepted baseline), model candidate comparison. | 3b |
| **3b** *(new spec)* | Extraction of candidates with source spans → tutor confirm/correct/reject through Stage 1 intake. Extraction gold (E1). | 3c, 8a |
| **E1** | Stage gold for extraction, analysis/selection, retrieval, adaptation and composition, authored just before each sub-stage. | each 3x exit |
| **3c–3e** | Selection, adaptation, composition and validation, as in the current stage 3. **Exit = stage gold passes in a recorded Langfuse experiment versus the baseline.** | 4 |
| **4 + UI** | Review, handoff, **tutor UI** for intake, confirmation, review and copy. Persist trace ID per draft version. Part decisions emitted as Langfuse scores (L1). | 5 |
| **E2** | Judge-calibration labeling begins on real stage 3–4 outputs, per job and criterion. Development and holdout splits fixed. | E4 |
| **5** | As planned, plus **L4**: canary-verified Langfuse retention and deletion, and masked pilot project config. | 6 |
| **6 / E4** | Freeze manifests, run full homework gates, fresh-holdout judge report. **L2/L3**: 10% sampled judge, weekly review queue, cost and latency dashboards, assignment and effort capture. | 7 |
| **7 / E5** | Pilot, plus operating the weekly review and a production → gold curation queue (permission → anonymization → label → review), or an explicit owner deferral. | R1 review |
| **8a–8c** | As planned, reusing 3b extraction and L1 tracing. **Start after stage 5** (owner choice; see F9). Each sub-stage exits on feedback stage gold (E3). | 9 |
| **9** | Feedback freeze, gates and judge calibration on feedback criteria, as planned. | R2 activation |

Implementation choices and their trade-offs:

- **Git as the canonical gold store, Langfuse as a mirror.** Review diffs, rights and provenance stay
  auditable in Git, and Langfuse provides experiment comparison and UI. The alternative, Langfuse as the
  primary store, is simpler, but loses schema versioning and Git review history.
- **Langfuse hosting.** Cloud is fastest and suits synthetic dev immediately. It needs a DPA, no-training and
  verified deletion before any pilot excerpts. Self-hosting keeps data in-house but adds several stateful
  services to operate, back up and delete from. Decide at L0, because PD-28 makes this a processor choice.
- **Eval-driven stage exits.** They cost labeling time earlier, but stop stage 6 from becoming a long serial
  surprise, and let model and prompt choices rest on evidence.
- **Extraction with mandatory tutor confirmation.** It adds a model stage and gold, but is the only plausible
  way to meet the PD-31 effort target and keep the feedback learning curve populated. Unconfirmed candidates
  never enter rates (PD-08).

## 6. Owner decisions needed

1. Extraction (F3): add an extraction-and-confirmation slice to R1 and R2, or accept manual coding for the
   pilot.
2. Transcript indexing (F4): a learner-scoped private index, or a recorded deferral.
3. Langfuse hosting (F2/L0): Cloud with processor terms, or self-hosted.
4. Feedback start (F9): after stage 5, in parallel with stage 6 labeling, or after stage 6 as now.
5. Production-to-gold during the pilot (F10): operate it in stage 7, or defer it until after R1.
6. Qualified reviewers and the content owner (F1/F6): who they are, and how much time they have.

Once these are decided, update the two plans: rows 2R and 3a–3e, streams E/L/C, the UI, and the stale status
lines. Allocate new requirements (extraction, possibly transcript indexing, the Langfuse integration
obligations) through `highgrade-spec` rather than editing plans alone.
