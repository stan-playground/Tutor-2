# Tutor Copilot — High-Level Release Plan

Prepared with HighGrade Planner · 2 November 2026 · Synchronized with the revised Implementation Plan on 3 November 2026

Deliver four cumulative releases: **R1 homework pilot → R2 post-lesson feedback → R3 lesson planning, including first lessons → R4 urgent replanning**. Each release adds one complete tutor job and retains the shared evidence, safety, privacy and tutor-approval controls. A runnable foundation or generated draft is an internal milestone, not a tutor release.

This is an ordinary plan under a plan-only request. It proposes release boundaries around existing product decisions; it does not change those decisions, create a Goal or authorize implementation, provider spending, real-data use or activation. Release numbering describes scope, not delivery dates or production readiness.

## 1. Sources and present position

[Product Decisions.md](<Product Decisions.md>) owns product intent and the confirmed job order. Current owner decisions and delegated defaults take precedence over historical descriptions; numerical defaults remain starting policies, not measured results. [Architecture.md](Architecture.md) owns design choices. [Native specifications](specs/README.md) and the [dataset contract](specs/datasets.md) own detailed requirements and checks.

This file owns the proposed release view. [Implementation Plan.md](<Implementation Plan.md>) remains the working sequence of smaller delivery stages and parallel streams. The comparison below uses its 3 November revision, whose findings are recorded in [Plan Review_claude.md](<Plan Review_claude.md>). The product document is not changed by this plan.

Observed base: `b0c9b96`. These stages are recorded **complete for local synthetic development**:

- [Stage 0](docs/stage-0.md): startup, migrations, local services, safe observations and real checks.
- [Stage 1](docs/stage-1.md): tutor-owned evidence and history.
- [Stage 2](docs/stage-2.md): reviewed teaching retrieval.

Two Stage 1 repair backlogs gate any generation work. These are documentary status findings; this planning task does not rerun application checks.

The [two evaluation fixtures](evaluation/README.md) remain drafts, not approved gold or proof of either job's quality. The [dataset contract](specs/datasets.md) is reviewed but not yet scheduled as delivery, and no Langfuse integration exists. The revised Implementation Plan starts both now.

## 2. Release scope and completion milestones

| Release | Tutor outcome | Existing implementation scope | Completion milestones |
| --- | --- | --- | --- |
| **R1 — Invitation-only homework pilot** | Prepare personalized homework from learner and lesson evidence; review it and copy approved student material with a separate tutor guide. | Stages 0–2 (done), 2R, 3a–3f, 4, 5 and 6 build readiness; stage 7 runs and reviews the separately authorized pilot. Streams E (gold), L (Langfuse Cloud) and C (reviewed content) run alongside from now. | Stage 1 repairs → complete journey and shared controls, each model stage exiting on its approved gold → homework certification → authorized pilot launch → cohort review. |
| **R2 — Post-lesson feedback** | Prepare supported feedback from the selected transcript and saved learning curve; review sections and copy approved student feedback. | Stages 8a–8c start after stage 5, then stage 9. Reuse R1's shared controls, extraction and review. Feedback gold is authored from now. | Evidence selection/comparison → checked feedback → durable section review/copy → independent feedback certification and authorized activation. |
| **R3 — Lesson planning** | Prepare a timed lesson, including a first or returning learner's diagnostic needs, with justified objectives and usable reviewed material. | Product scope exists; detailed implementation stages/specifications remain to be prepared. | Lesson-specific contract and cases → checked lesson journey → equivalent readiness and authorized activation. |
| **R4 — Urgent replanning** | Temporarily adjust preparation for a confirmed event, preserve postponed work, and return to ordinary priorities using an explicit update. | Product scope exists; detailed implementation stages/specifications remain to be prepared. | Event/lifecycle contract and cases → checked replanning journey → equivalent readiness and authorized activation. |

### R1 — Complete homework journey

Serve independent English tutors with adult learners aged 18+, A2–B2. The first pilot starts from an existing learner's latest lesson unless another lesson is selected. Its scope includes:

- **Learner information and intake:** dated assessment or provisional tutor estimate, preferences, goals, adult confirmation, opt-in/upload permission, tutor-owned lesson notes or an authorized transcript, homework evidence and separately confirmed corrections. Keep supplied profile information distinct from observed performance.
- **Extraction and private transcript search:** the model proposes candidate observations and encounter/attempt/check facts from notes, transcripts and homework responses, with source spans and uncertainty. Only tutor-confirmed facts enter rates or history (PD-08). A learner-scoped private transcript index, built with local embeddings, answers evidence questions within one owner/learner. It never feeds the shared bank or recent-window selection.
- **Tutor interface:** browser flows for profile/permission, intake, extraction confirmation, request, part review, approved copy, assignment confirmation and effort reporting. Intake effort counts toward the pilot's effort outcome.
- **Personalization:** confirmed subskill accuracy, required use and correct avoidance; comparable recent lesson/homework trends; qualified cumulative assignment, encounter, attempt and checked-outcome facts. Select and explain what is important now and worth revisiting. Old history must not change recent denominators; elapsed time proves no forgetting and exposure proves no mastery.
- **Teaching material and draft:** reviewed, permissioned exercises, explanations, reading/listening input, vocabulary/fluency activities, discourse/strategy models and task/project frameworks, with checked adaptation. Select by purpose and task demands, including exact confusion when relevant. A supported goal needs no invented error. Listening needs an available permitted recording and matching reviewed criteria. Missing material remains a visible gap.
- **Tutor-controlled handoff:** usable homework whose planned minutes sum to the requested duration; separate student content and tutor answers/criteria; safety, grounding and suitability validation; per-part approval/rejection, meaningful clarification, alternatives, edits, full substantive regeneration and durable return. Only valid approved student parts become copyable; the tutor shares them manually.
- **Operational completion:** authenticated ownership isolation, data lifecycle, visible status/failure, manual restart, replay-safe decisions, approved-copy isolation, permitted monitoring, reviewed evaluations and pilot measurements. Privacy and recovery are prerequisites for real use, not later enhancements.

PD-39 cumulative history and PD-40 teaching beyond visible errors are **already R1 requirements**. R1 cannot be reduced to a grammar-error demo and still satisfy the current product scope. Generation, approval and copying never establish actual assignment, exposure or performance; tutor intake supplies those facts separately.

**Readiness milestone:** finish the applicable contracts and their real access, review, recovery and lifecycle checks, plus the homework-specific evaluation gates in section 3. The contracts are HG-0003–HG-0008, HG-0011 and the new specifications for extraction, the private index, tutor-interface flows and the Langfuse obligations.

Gold is built ahead of each model stage rather than at the end. Stage 6 freezes and certifies suites that already pass at their stage exits. Start from synthetic learners.

Before real learner use, these must be ready:

- named processors: the model provider and Langfuse Cloud
- the permitted environment and hosting/backups
- recovery/deletion procedures
- usable reviewed material (content stream C1)

**Launch milestone:** after separate launch authorization, invite five tutors. Keep the pilot free with 20 completed homework preparations per tutor; failed runs and within-request revisions consume no allowance. There is no automatic paid conversion.

**Cohort-review milestone:** review after at least five requests per tutor, or earlier after a critical defect. Compare active effort with three comparable manual tasks per tutor; include setup, clarification, revisions, retries and manual fallback. Report confirmed assignment within seven days against all eligible started requests, including failures/abandonment; unknown use is not success. The ≥25% lower median effort and ≥80% assignment figures are management targets, not technical gates or proven benefits. A critical safety, access or approval defect stops the affected feature.

### R2 — Independently usable post-lesson feedback

Add feedback from an available authorized selected transcript, frozen confirmed observations/learning curve and relevant qualified history. Cover the transcript with source-linked findings; a few semantic matches cannot substitute for coverage. Keep accuracy, required use, avoidance and task/assistance context distinct, with insufficient or mixed evidence visible.

Produce concise student sections on demonstrated strengths, difficulties, supported progress and suggested next steps, alongside private tutor evidence notes. Validate claims and attribution, then reuse durable exact-version section review, full substantive revision and approved manual copy. Missing/expired transcript content stays unavailable. Feedback generation, review and export cannot confirm observations, update rates/trends/preferences or create learning-activity facts. New evidence starts a new request; wording revisions retain the frozen evidence.

R2 needs no preceding homework request, exercise retrieval, answer key or homework duration. It adds HG-0010 with the shared HG-0003/0006/0007 controls and feedback-specific evaluation. Before activation, pass its own gates, settle feedback operating terms and define effort/use reporting separately. Do not transfer homework assignment targets or consume homework allowance by default.

**Dependency:** R2 implementation starts after stage 5 and proceeds alongside homework certification (6) and the pilot (7). It does not wait for the cohort report.

Logic:

- 8a needs only Stage 1 data, model integration (3a) and extraction (3b). 8c needs stage 4 records and stage 5's lifecycle controls.
- Stage 6 is dominated by reviewer labeling, so engineering capacity is otherwise idle.
- Feedback gold is authored from now on.

Fixes for homework gate failures take priority over feedback work, which keeps homework first. Real feedback use still waits for stage 9 and separate activation authority.

### R3 — Lesson planning, including first lessons

Extend the existing preparation/review path to ordinary, first and returning-learner lessons. Produce a coherent timed sequence, objective reasons, activities and appropriate teaching support, preserving current goals, qualified history and important-now/worth-revisiting selection. Use reviewed material and checked adaptations under the same content boundary.

First lessons start from assessment/preferences and proportionate diagnosis of uncertainty that matters to preparation. Returning learners use available evidence or qualified rechecks; missing history remains missing. This does not introduce a placement-testing product or require a recheck before every goal-led activity.

**Completion barrier:** formalize lesson-specific inputs, artifact/review behavior and scenarios before implementation. Add reviewed first/returning/ordinary lesson cases, timing/constraint conflicts, uncertain prerequisites and relevant teaching-route coverage; verify the complete job and shared controls before activation. Existing homework checks alone do not establish lesson-planning readiness. Detailed contracts and stage numbers remain future preparation, not adopted by this plan.

### R4 — Urgent-event replanning

Add a tutor-confirmed event, date and goal. Initially flag dates within 14 days as urgent, with tutor override outside that window. Promote event-related objectives temporarily, preserve postponed objectives and explain the trade-off; a dated multi-lesson plan is specific to a confirmed deadline goal.

Handle changed dates and cancellation. At the next request after the event, ask for the outcome/update and recompute ordinary priorities without assuming success. Reuse reviewed content, evidence boundaries, timing, validation and tutor approval. R1–R3 may respect an explicit current goal without claiming this complete event lifecycle.

**Completion barrier:** specify and evaluate missing/conflicting event details, urgent overrides, postponement, date changes, cancellation and post-event return, including stale revisions and shared-control regressions. Enable only after equivalent job-specific readiness and authorization. No background scheduler, reminders or calendar integration is implied.

## 3. Gates inherited by every release

The [dataset contract](specs/datasets.md#7-frozen-experiments-and-release-decisions) owns the exact gate arithmetic and manifests. At this level, a release is technically ready only when:

1. **The complete tutor journey works at real boundaries.** Check actual persistence, authorization, worker/checkpoint transitions, API/UI decisions and approved export where relevant. Mocks can isolate failures; they do not prove real integrations, provider behavior or teaching quality. Significant work needs independent review under HighGrade.
2. **Applicable reviewed suites pass.** R1 has twelve homework base families; R2 has eight feedback base families. Both also require applicable history/route variants, isolated cases and intermediate-stage labels. Every critical item passes; ordinary passes reach `ceil(0.90 × N)` separately per job, active stage and end-to-end; all required scores are present/valid; no accepted passing baseline case regresses. Missing/error scores fail. Each model stage must already have passed its approved boundary gold in a recorded Langfuse experiment against the accepted baseline. The first accepted baseline is a naive one-prompt run. The release gate freezes and certifies these suites rather than first creating them. R3/R4 need equivalent job-specific suites before activation, without an invented case count here.
3. **Gold and judges have distinct evidence.** Qualified tutors review every gold label; second review covers all critical items and at least `ceil(0.20 × ordinary items)` per frozen suite, with disagreements resolved. Initial judge calibration uses at least 20 distinct human-labeled outputs, criterion/job coverage and fresh holdout after tuning. Model-written expectations and assigned reviewer IDs alone are not approved gold.
4. **Privacy and failure behavior are complete.** Enforce tutor/learner isolation and permissions; raw sources/embeddings expire after 30 days, structured records after 12 months of inactivity. Deletion blocks access immediately, removes active/derived copies within seven days and backups within 30, including history, checkpoints and permitted evaluation records. Late workers and restores cannot revive deleted data. Named processors need compatible purpose, retention and no-training terms.
5. **Review and monitoring remain mandatory.** Hard failures cannot be waived; exact approved student content excludes keys/private notes. Keep two clarification rounds, five substantive revisions, seven-day pause expiry and the five-minute active-segment cap under the existing policies. Show saved status and recoverable failures; manual retry creates a new request with current evidence and no approvals. Per-request validation is mandatory; additional advisory judging samples 10% of permitted runs. Weekly review covers all critical flags/failures and five random unflagged permitted outputs, with coverage reported. Tutor decisions are recorded as Langfuse scores linked to the draft version's trace ID; PostgreSQL remains the authoritative record.
6. **Langfuse Cloud is a verified processor before real data.** Synthetic development uses a project with no learner data and full capture. The pilot uses a separate masked project with no automatic input/output capture: metadata and the minimum permitted redacted excerpts only. Before any real excerpt, settle:
   - processor terms: EU region, no-training, retention
   - deletion of traces, scores and dataset/run items, verified with test markers
   If deletion cannot be enforced, production-derived items stay out of Langfuse.
7. **Production cases reach gold only through review.** During the pilot, failure patterns found in weekly review become new synthetic reproductions with no copied learner text, reviewed normally. A production-derived item additionally needs separate reuse permission, reviewed anonymization and verified deletion. Nothing is promoted automatically from a score or an approval.

Technical readiness, activation, pilot review, human acceptance, commit and deployment are distinct outcomes. Passing scores or tutor approval do not establish learning gain. Latency, escalation, effort and cost targets remain targets until measured; historical model-cost estimates are not current prices.

## 4. Comparison with Implementation Plan.md

The existing file is more detailed about **how to build homework and feedback**. This plan adds the **four-release product view**, explicit launch/review boundaries and later-job gaps. Its stages run from **0 to 9**, with 2R, stage 3 split into 3a–3f and stage 8 split into 8a/8b/8c. There is no stage 10. Three streams run alongside the stages:

- **E — gold:** E0 starts now; E1 lands before each model stage; E2 judge labels start from 3f; E3 feedback gold starts now; E4 freezes at 6 and 9; E5 is pilot curation.
- **L — Langfuse Cloud:** L0 synthetic project now; L1 tracing at 3a; L2 decision scores at 4; L3 processor terms, masking and deletion at 5; L4 online evaluation at 6.
- **C — reviewed content:** C0 coverage matrix now; C1 before 3e and 7.

| Existing stage and scope | Release/milestone here | Assessment |
| --- | --- | --- |
| **0–2. Foundation, evidence/history, teaching retrieval** | Shared internal foundation; R1 evidence and material foundation | Recorded complete locally. Neither an R1 release nor approved gold. Profile/permission, recent measures, cumulative facts and reviewed retrieval are inherited by later jobs. |
| **2R. Stage 1 repairs** | R1 prerequisite | Identity, provenance and frozen-context repairs before any generated artifact depends on them. Runs alongside E0/L0/C0. |
| **3a–3f. Model/trace foundation, extraction, private index, selection, adaptation, composition/validation** | R1 draft milestone | Necessary internal result, with each model stage exiting on approved gold against the naive baseline. Extraction (3b) and the private index (3c) are shared with R2. Insufficient for release without review, lifecycle and certification. Includes PD-39/40 scope. |
| **4. Tutor review, handoff and tutor interface** | R1 tutor journey | Exact decisions, full revision, approved copy and the tutor-facing flows. Trace IDs link tutor decisions to Langfuse scores. Still depends on the combined failure/privacy and release gates. |
| **5. Failure, data lifecycle and Langfuse Cloud readiness** | R1 shared-control completion | Must precede real use. Includes verified Langfuse Cloud terms, masking and deletion. Later jobs extend these checks to their added records. |
| **6. Homework certification and pilot readiness** | R1 technical readiness | Freezes and certifies homework gates and wires online evaluation, not pilot launch or measured product benefit. |
| **7. Invitation-only homework pilot** | R1 authorized launch and cohort review | Two distinct milestones: operational readiness and launch authority precede real use, then cohort reporting. Also operates weekly online review and gold curation. |
| **8a. Feedback transcript and learning-curve comparison** | R2 evidence milestone | Starts after stage 5. Direct coverage of the selected source and confirmed state, with unconfirmed extraction candidates. No homework dependency per request. |
| **8b. Feedback generation and validation** | R2 draft milestone | Job-specific supported claims and private-note separation; no mandatory exercise stages. |
| **8c. Feedback tutor review and approved handoff** | R2 tutor journey | Reuse exact-version review; feedback actions cannot write learner performance/history. |
| **9. Feedback readiness and controlled activation** | R2 readiness and authorized activation | Separate feedback gates, operating terms and measurements; homework success does not qualify feedback. |
| **Later lesson planning** | R3 | Order is mentioned, but detailed stages, job contract and reviewed cases are absent. |
| **Later urgent replanning** | R4 | Order is mentioned, but event lifecycle implementation and job-specific coverage are absent. |

**Scope agreement:** both plans:

- prioritize homework → feedback → lessons → urgent replanning
- put history/non-error teaching into the current homework foundation
- reuse evidence, extraction, review and privacy infrastructure
- start golden data and Langfuse work now rather than at certification
- start feedback implementation after stage 5, without waiting for the homework cohort report

**Coverage difference:** the existing implementation plan explicitly details only homework and feedback. This plan makes R3/R4 outcomes and preparation barriers visible without pretending those jobs are implementation-ready. It also distinguishes release scope from smaller technical stage completion.

**Status:** Implementation Plan.md now records Stages 0–2 and starts with 2R and the E0/L0/C0 streams. [Repository Structure.md](<Repository Structure.md#4-future-justfile-command-contract>) still describes the commands as wholly proposed, while README and the stage records record real commands. Use the execution records for current progress and the design documents for intended scope.

## 5. Requirements coverage and exclusions

This index assigns each PD-01–PD-40 requirement to a release or shared boundary; its linked owners retain the full rules.

| Product decisions | First delivery / treatment |
| --- | --- |
| **PD-01–06** — tutor audience, adaptation, four jobs, tutor authority, interaction burden, profile/evidence separation | R1 shared baseline; PD-03's job scope completes cumulatively through R4. |
| **PD-07** — initial assessment and first/returning diagnosis | Assessment/uncertainty intake in R1; first-lesson preparation in R3. |
| **PD-08–10** — subskill measures, both evidence streams, justified objectives | R1, inherited. Extraction proposes candidates and only tutor-confirmed observations count. Timing/share rules apply to teaching plans, not feedback prose. |
| **PD-11** — temporary urgent goals | Full event lifecycle in R4. |
| **PD-12–17** — usable artifact, fit, reviewed adaptation, gaps, provenance and validation | R1, then job-specific application; R2 validates evidence claims rather than imposing homework timing/keys. |
| **PD-18–25** — review, questions, alternatives, edits, regeneration, durable waits, notices and tutor judgments | R1 shared review; R2 extends it to feedback sections. Notices appear in review; external delivery is excluded. |
| **PD-26–28** — asynchronous status, visible/manual recovery, privacy | R1 real-use gates, inherited and rechecked for each new job/store. |
| **PD-29–30** — external assistant access and live tutoring | Deferred/excluded from R1–R4 in this proposal. |
| **PD-31–32** — useful tutor outcomes and attention | R1 effort/assignment/review burden; later jobs need their own outcomes. Retention/conversion/capacity are downstream measurements. |
| **PD-33** — reviewed teaching assets and private transcripts | R1 shared teaching retrieval (done locally), plus a learner-scoped private transcript index (3c). Reviewed content grows through stream C, without sharing private learner evidence. |
| **PD-34–35** — stage/job gold, offline/online evaluation and qualified quality claims | Every release. Gold starts now and gates each model stage. Langfuse Cloud runs offline experiments from L0 and online evaluation from stage 6. Production-to-gold follows section 3 item 7. Independent job gates; no learning-gain claim. |
| **PD-36** — free pilot and commercial boundary | R1 homework allowance; later operating terms explicit. Monthly subscription is chosen for a future commercial offering; price/billing/paid launch stay separate. |
| **PD-37** — complete pilot versus runnable stages | R1 complete journey, then R2–R4 with equivalent checks. |
| **PD-38** — post-lesson feedback | R2. |
| **PD-39–40** — cumulative history and teaching beyond errors | R1 requirements, inherited by R2–R4 with job-appropriate outputs/criteria. |

No Release 5 is specified: the requirements do not justify inventing another committed milestone. Live student tutoring, unrelated original exercise/project authoring, automated pronunciation/listening assessment, a student app, MCP/email/calendar integrations, automatic sending, background scheduling, selective regeneration, automatic mid-generation recovery and paid billing remain outside this plan. Any later expansion needs a concrete product decision and appropriate specification/evaluation; existing proposals are not adopted by being mentioned here.

## 6. Implementation approach, trade-offs and next action

Retain the selected **one Python codebase with web and worker roles**: FastAPI tutor interface, a small LangGraph for durable pauses, PostgreSQL domain records/pgvector, disposable Redis query-embedding cache, typed job outputs and Langfuse Cloud evaluation. Job-specific composition/validation extends shared records, extraction and review; it does not need another agent system or service.

Git holds the canonical reviewed gold, and Langfuse datasets mirror it for experiments. This keeps review history and schema versions auditable, at the cost of a sync step. Private transcript embeddings use the local pinned model, so private text never reaches an external embedding provider. The architecture's documented Langfuse baseline is `langfuse==5.1.0`; recheck the compatible release and version-matched documentation at integration, rather than treating this plan as an installation lockfile.

Keep profile facts, confirmed performance observations and independent learning-activity facts distinct. Recent measures and cumulative context are derived views; frozen request references support reproducible revisions, while exact draft/decision records determine student copy. Graph checkpoints own execution position, not permissions or learner truth. These distinctions prevent double counting, invented progress and approval of the wrong version; a separate memory database would add synchronization/deletion work without a present need.

The alternative of a small simulated draft ships sooner but fails the complete R1 tutor journey. Building all four jobs together delays validation and mixes failure causes. Separate services or specialist-agent crews add coordination before a demonstrated need. A custom saved-state pipeline is a viable orchestration alternative, but the selected LangGraph avoids implementing durable human pauses ourselves; application-level authorization, replay safety and deletion still require real checks.

Use bounded async I/O for database/provider waits and keep dependent stages sequential. Pools, model clients and the compiled graph live for a process; transactions and loaded context live for a request/active segment, with no resources held while waiting days for a tutor. Threads belong only to a concrete blocking parser; processes require measured CPU work. Release planning adds no new concurrency mechanism, layer or module.

Do not assign dates, effort estimates or a model-quality winner without evidence. Resolve provider/processor/environment and hosting/backup choices at the relevant integration; obtain qualified material/gold reviews before claiming readiness. Feedback operating terms precede R2 activation; R3/R4 need their detailed contracts before implementation. These are remaining implementation/activation decisions, not a reopening of delegated pilot defaults.

**Next project milestones:** stage 2R (Stage 1 repairs) together with E0 (eval harness, inventory and retrofit gold for Stages 1–2), L0 (synthetic Langfuse Cloud project and first experiment) and C0 (content coverage matrix). These have no mutual dependency.

Before the stages that need them, prepare new specifications through `highgrade-spec` for:

- extraction and confirmation
- the private transcript index
- tutor-interface flows
- the Langfuse obligations
- the dataset-contract additions

This file authorizes none of that execution. Ask separately whether to commit; a commit does not launch a release.
