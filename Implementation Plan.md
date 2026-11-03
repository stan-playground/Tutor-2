# Tutor Copilot — High-Level Implementation Plan

Prepared with HighGrade Planner · 1 November 2026 · Revised 3 November 2026; evaluation sequencing updated

Deliver the complete homework journey for adult A2–B2 English learners first. Then deliver post-lesson
feedback, before lesson planning and urgent replanning.

- **Homework** moves from evidence to checked practice and a tutor-approved handoff.
- **Feedback** moves from the selected transcript and saved learning curve to supported, tutor-approved
  feedback sections. It needs no preceding homework request.

PD-39/40 extend preparation now. Preparation uses qualified cumulative learning history alongside unchanged
recent performance, and chooses input, practice and task routes beyond visible errors. It reconsiders
important-now and worth-revisiting needs on each tutor request. These changes fit the stages below. They add
no scheduler, student app, automated audio assessment or new workflow system.

**3 November revision.** At the owner's request, this revision:

- starts evaluation and golden-data work now, in its own stream, as early as dependencies allow
- adds Langfuse as a delivered stream, hosted on **Langfuse Cloud**
- adds model **extraction** from tutor notes, transcripts and homework responses, with mandatory tutor
  confirmation
- adds a **learner-scoped private transcript index**
- adds the **tutor interface**, a **reviewed-content stream** and the **Stage 1 repair gate**
- decides when feedback starts and how production cases reach gold (see [Decisions](#decisions-in-this-revision))

The earlier review is in [Plan Review_claude.md](<Plan Review_claude.md>); the current evaluation sequence incorporates the later [golden dataset plan](<Golden Dataset Implementation Plan.md>).

This plan grants no execution, provider-spend, account-creation or launch authority. Owner requests
implemented the local slices in [Stage 0](docs/stage-0.md), [Stage 1](docs/stage-1.md) and
[Stage 2](docs/stage-2.md). Those records own observed behavior and limits. The remaining rows describe
future work.

## Sources and scope

| Document | Owns |
| --- | --- |
| [Product Decisions](<Product Decisions.md>) | Policy |
| [Architecture](Architecture.md) | The design proposal |
| [Native specs](specs/README.md) | Requirements. HG-0003–0008 cover the homework foundation and shared controls, HG-0009 records the product update, HG-0010 adds feedback and HG-0011 adds history and routes. |
| [Dataset contract](specs/datasets.md) | Each job's gold cases and gates |
| [Golden Dataset Implementation Plan](<Golden Dataset Implementation Plan.md>) | Initial case inventory, stage samples, review sequence and dependencies |
| [Repository Structure](<Repository Structure.md>) | Planned modules, Justfile and tools |
| The two Stage 1 fix backlogs ([1](<Plan for Fixes Stage 1.md>), [2](<Plan for Fixes Stage 1_claude.md>)) | The repairs that gate stage 3 |

This plan coordinates delivery order rather than duplicating those contracts.

**New allocations need native specifications before implementation.** This revision allocates work that no
current specification owns:

- extraction and confirmation (stage 3b)
- the private transcript index (3c)
- tutor-interface flows (4)
- the Langfuse integration and online-evaluation obligations (stream L)
- dataset-contract additions: a planned item inventory, the reviewer-qualification definition and the
  Langfuse score/run mapping (E0)

Create these through `highgrade-spec`. HG-0003's "No LLM extraction" remains true for the delivered Stage 1;
extraction is a later, separate change.

Stack:

- one Python codebase with FastAPI/Jinja
- a separate LangGraph worker
- PostgreSQL/pgvector
- Redis for generic query embeddings
- Pydantic output schemas
- Langfuse Cloud for traces, datasets, experiments and scores

Application records own evidence, decisions and export. Graph checkpoints own execution position. Langfuse
holds copies for evaluation, never the authoritative record. Finish a small coherent block, integrate it and
check its real boundary before another block depends on it.

## Delivery order

Three streams run alongside the build stages, starting now:

- **E** — evaluation and golden data
- **L** — Langfuse
- **C** — reviewed teaching content

The build path is 2R → 3a–3f → 4 → 5, then homework certification (6) and the separately authorized pilot
(7). Feedback implementation (8a–8c) starts after stage 5 and runs alongside stages 6–7. Feedback release
waits for its own stage 9. Lesson planning follows feedback.

```text
Build:  0–2 local → 2R → 3a → 3b → 3d → 3e → 3f → 4 → 5 → 6 → 7
        2R → 3c (optional evidence questions); 5 → 8a → 8b → 8c → 9
Gold:   E0 first case/inventory → E1 homework stage labels → E4 homework (6) → E5 (7)
        E0 feedback inputs → E3 feedback stage labels → E4 feedback (9)
Judge:  E2 homework outputs from 3f; feedback outputs from 8b; calibrate before judge use
Cloud:  L0 before 3a/first required experiment → L1 at 3a → L2 at 4 → L3 at 5 → L4 at 6
Content: C0 first relevant assets/gaps → C1 for enabled routes before 3e and cohort use
```

Synthetic authoring and early local checks can run alongside 2R. Feedback implementation starts after 5,
not after the homework cohort. Stage 3c may answer optional evidence questions; it does not select recent
observations or replace full selected-transcript coverage.

**Exit rule for every model stage (3b, 3d–3f, 8a–8b).** The stage exits only when its boundary's
**approved** gold items pass a recorded Langfuse experiment against the accepted baseline under the
[dataset gates](specs/datasets.md#7-frozen-experiments-and-release-decisions). Runs on draft labels guide
development but do not satisfy an exit. Stages 6 and 9 therefore freeze and certify suites that already
exist; they do not build evaluation from scratch.

### Evaluation, golden data and Langfuse

The [golden dataset plan](<Golden Dataset Implementation Plan.md>) describes the initial cases and the
small-block workflow. Use three datasets: homework gold, feedback gold and judge calibration. Each job
contains complete-job and focused samples tagged by stage, severity and stable ID. A learner situation can
supply multiple runnable samples; report counts by job, stage and end to end. The teaching bank is the corpus
being searched, not the golden dataset. No separate dataset per stage is needed.

Begin with about 10 synthetic learner situations for each job and add isolated stage samples where needed.
These are starting targets, not release counts. The current [dataset contract](specs/datasets.md) still
requires all 12 homework and 8 feedback families, mandatory variants and isolated stage coverage; it also
requires ordinary success and relevant critical cases for each active stage. Qualified English tutors
review each expected label and reason; a second reviews every critical item and at least
`ceil(0.20 × ordinary)` items in each frozen suite. The existing two fixtures are drafts, not approved gold.

| Milestone | Small deliverable and completion | Depends on → unblocks |
| --- | --- | --- |
| **E0 — First case, inventory and local checks** | Inventory family IDs, runnable sample IDs, job, stage, severity, review and gaps against the contract. Author one synthetic case with its expected result and provenance; validate and seek qualified review. Use existing schema and a real available boundary to check it. Then expand toward the starting targets. Add Stage 1 numeric and Stage 2 retrieval checks incrementally, including the contract's boundary cases and real authorization/failure observations. Create only the local loading/results needed for real checks; add the full frozen manifest and gate arithmetic when required for experiments. `just eval <job>` is a proposed command, not an existing one. | Schema and available Stage 1/2 boundaries; no Cloud or 2R needed to draft → early E1/E3 inputs and first local checks. |
| **C0 — First reviewed content** | Identify suitable rights-cleared material and versions for the first retrieval/adaptation cases. Track route, level, domain and recording/criteria gaps as they arise; grow coverage for enabled routes rather than blocking the first case on a full matrix. | Stage 2 bank and qualified content review → relevant E1 labels; C1 before 3e and pilot. |
| **L0 — Synthetic Langfuse project** | When the first recorded experiment is ready, create an authorized synthetic-only EU-region project; verify the SDK and version-matched documentation through Context7. Mirror the reviewed Git items needed for the experiment and record their versions in the experiment manifest. Run an initial deterministic experiment before model spend. | Authorized account and executable E0 samples → L1/3a. Draft authoring and local checks do not wait for Cloud; 3a and the model-stage exits still do. |
| **E1 — Homework stage gold** | Review extraction before 3b, selection before 3d, retrieval/adaptation before 3e, composition/validation before 3f and scripted review/revision before 4. Independently solve closed answers. Reuse a family across boundaries but identify each runnable input and reviewed expectation separately. | E0 inputs; reviewed content for retrieval/adaptation; 3a schemas for composition/validation/review → respective stage exits. |
| **E2 — Judge calibration** | Start with around 10 distinct candidate outputs, then use at least **20 distinct human-labeled outputs overall** before relying on a judge. Cover both human pass/fail for every evaluated criterion and the applicable job, keep related outputs together in development or holdout, and obtain a fresh labeled holdout after tuning. Report false accepts, false rejects and missing results. Add feedback-specific grounding and attribution labels before judging feedback. | Candidate outputs from 3f for homework and 8b for feedback; tutor review → calibrated judge for the relevant criteria. If homework is calibrated before feedback outputs exist, at least 20 distinct homework outputs are needed before that judge is relied upon. Feedback later needs its own applicable criterion coverage, without an automatic extra 20-output quota. |
| **E3 — Feedback gold** | Author synthetic source/extraction/analysis inputs alongside E0. Add composition, validation and review samples after the 3a `FeedbackDraft` schema. Keep feedback independent of homework retrieval and results. | E0 and 3a → respective 8a–8c checks. |
| **E4 — Freeze and certify each job** | Freeze the applicable reviewed revisions and manifest; run stage and end-to-end gates and actual privacy, review, export and lifecycle checks. Report the applicable judge calibration and fresh holdout. | Homework stage 6: E1 and homework E2 plus stage 5. Feedback stage 9: E3, feedback E2 and 8a–8c. Feedback labels do not block homework certification. |
| **E5 — Pilot curation** | Review failures and add reviewed synthetic reproductions; handle any permitted production-derived item under the separate reuse/deletion rules below. | Stage 7 → later manifests. |

The 20-output judge target is the minimum in HG-0008, not a reliability guarantee or a fixed 10-per-job
allocation. Expand where criterion or job coverage is missing. Related outputs sharing a family/source stay
in one split, including across jobs. Human review and deterministic checks can evaluate early samples without
a semantic judge; model-stage exits still require the recorded Langfuse experiment. Freeze exact case versions,
fixture and corpus hashes, evaluator definitions, application/model versions and baseline as required by the
dataset contract. Missing scores, critical failures and accepted-baseline regressions fail their gates.

### Build stages

| Stage | Deliverable and small implementation blocks | Dependencies / requirement owner | Completion barrier |
| --- | --- | --- | --- |
| **0–2. Done (local, synthetic)** | Foundation, tutor-owned evidence/history and reviewed teaching retrieval. See the stage records. | HG-0003/0004/0007 portions | Recorded in [Stage 0](docs/stage-0.md), [Stage 1](docs/stage-1.md) and [Stage 2](docs/stage-2.md). HG-0003's approval/copy scenario remains future. |
| **2R. Stage 1 repairs** | Reconcile the two fix backlogs into one route. They cover source-body preservation across metadata corrections, learner-scoped identities/references, exact source-version provenance and a versioned frozen-context contract. Implement as separately reviewed migrations. | Fix backlogs, HG-0003; now | No generated artifact or new frozen-context consumer exists before these pass with real checks and independent review. Stage 3 cannot start while any item is open. |
| **3a. Model, graph and trace foundation** | Choose one generation-model candidate by comparing candidates on available reviewed E0 and early E1 items. Integrate the provider and the LangGraph worker with the PostgreSQL checkpointer (initial HG-0006 persistence). Add **Langfuse tracing (L1)** with a masking function: full capture in the synthetic project only. Draft the `HomeworkDraft` and `FeedbackDraft` schemas so labels can be written. Run the **naive baseline candidate** (one prompt with retrieved context), explicitly recording that there is no previous baseline. Adopt it as the first accepted baseline only after the applicable review and gates; never promote it automatically. Record cost/latency per active segment (PD-26/36). | 2R, L0; HG-0005/0006 | Every model call is traced with versions, usage and latency. Masking passes synthetic canaries. Routine checks make no live calls. The baseline experiment is recorded in Langfuse and accepted through the applicable gates before later stages use it. |
| **3b. Extraction and evidence confirmation** | The model proposes candidate observations (attempted/required/inappropriate opportunities, correctness, task/assistance) and candidate encounter/attempt/check facts from tutor notes, authorized transcripts and homework responses. Each candidate carries source-span/speaker references and uncertainty. The tutor confirms, corrects or rejects each through the existing Stage 1 intake operations; only confirmed facts enter rates or history. | 3a, E1 extraction labels; new spec (shared by homework and feedback) | Unconfirmed candidates never change rates, trends or history (PD-08). Re-extraction of the same source revision creates no duplicates. Expired or unauthorized sources are not extracted. Imported instructions stay evidence text. Extraction gold passes the exit rule. |
| **3c. Private transcript index** | Embed source-linked transcript/note segments with the **local pinned embedding model**, so no external processor is involved. Store them in a learner-scoped table under RLS, never in the shared bank or the Redis cache. Expire with the raw source after 30 days and delete with the learner. Search answers evidence questions within one owner/learner only. | 2R and the Stage 2 embedding; runs alongside 3a/3b; new spec | Foreign-learner canaries never match. Expiry and deletion remove vectors. The index cannot select recent-window observations, replace feedback transcript coverage or reach shared retrieval. |
| **3d. Objective and route selection** | Freeze recent evidence, history and goal references. Select explained important-now/revisit purposes and PD-40 routes, with no compulsory remediation, review quota or invented error. | 3b, with 3c for optional evidence questions; HG-0005-T1 | Analysis/selection gold passes the exit rule. No history facts are created by selection. |
| **3e. Material use and adaptation** | Use Stage 2 retrieval per selected purpose. Add input, vocabulary, fluency, discourse, strategy and task/project adaptation as small route blocks, with an independent solver for closed answers. | 3d, C1 for enabled routes; HG-0005 | Retrieval/adaptation gold passes the exit rule. Recording correspondence holds and gaps stay honest. Exposure/drill scores prove no unrelated ability. |
| **3f. Composition, validation and review versions** | Compose timed outputs, validate route-specific criteria and save review versions through the same graph. | 3e; HG-0005, initial HG-0006 | Composition/validation gold passes the exit rule against the baseline. Minutes sum exactly. Student content and keys stay separate. E2 judge labeling starts on these outputs. |
| **4. Tutor review, handoff and tutor interface** | Add bounded clarification, exact part decisions, full regeneration, approval invalidation, the final manifest and a student-copy read.<br>Build the **Jinja tutor interface** for: profile/permission; source intake; extraction confirmation; preparation request; part review (clarify, alternatives, edits, regeneration); approved copy; assignment/actual-use confirmation; effort self-report.<br>Persist the **trace ID** on each draft version and decision, and send tutor decisions to Langfuse as scores (L2). | 3f, E1 review scripts; HG-0006 | Restart/resume preserves the exact pause, and stale/duplicate actions change nothing extra. Part approval makes no model call. The copy contains only valid approved student content. Approval or copying creates no activity facts. Each interface flow is checked in a real browser against persisted state. Review/revision gold passes. |
| **5. Failure, data lifecycle and Langfuse Cloud readiness** | Complete lease/queue/checkpoint reconciliation, timeouts, manual restart and expiry. Complete retention/deletion across sources, the private index, derived records, checkpoints, evaluations and Langfuse objects. Add late-worker fencing and backup/restore deletion.<br>**L3:** Langfuse Cloud processor terms (DPA, EU region, no-training, retention). A separate **pilot project** with masking and no automatic input/output capture. Retention configured to PD-28 where the plan tier supports it, otherwise an enforced deletion job. | 4; HG-0006/0007 | Crash and concurrent-action cases preserve decisions. Deletion blocks access immediately. Copies, vectors and Langfuse traces/scores/dataset and run items for a deleted synthetic learner are removed within policy, verified with canaries. Restores cannot revive deleted learners. Logs, Langfuse and Redis leak no private content. |
| **6. Homework certification and pilot readiness** | **E4** freeze and full gates, with the fresh-holdout judge report.<br>**L4** online evaluation in the pilot project: deterministic gates on every request, every tutor decision captured, 10% sampled advisory judge, a weekly review queue (every critical flag/failure plus 5 random unflagged), cost/latency dashboards.<br>Pilot measurement: effort with the 3-task manual baseline, 7-day assignment, once-only allowance. | 5, E1–E2; HG-0008 | All critical cases pass, and at least `ceil(0.90 × N)` ordinary cases pass per stage and E2E, using every declared variant. No missing scores or baseline regressions. Real access/review/recovery/deletion checks pass. Judge calibration and the allowance do not establish learning benefit or feedback readiness. |
| **7. Invitation-only homework pilot** | After separate launch authorization, invite five tutors, collect manual-effort baselines and monitor assignment, effort, failures and review burden. Free, with 20 completed preparations per tutor. Operate the weekly online review and the **E5 curation queue**. | PD-31/36/37, HG-0008; after 6, C1 and operational/provider readiness | Review after at least five requests per tutor, or sooner after a critical defect. Report tutor/task counts, effort including retries/fallback, and assignment including failures/unknowns. The ≥25% effort and ≥80% assignment figures are management targets. A critical defect stops the affected feature. |
| **8a. Feedback transcript and learning-curve comparison** | Freeze the authorized selected transcript, recent observations and relevant PD-39 references. Reuse the unchanged PD-08/09 metrics and separate cumulative context. Cover source-linked segments directly, with no embedding. Reuse 3b for **candidate findings**: they stay unconfirmed and are marked as such, and confirmation remains a separate intake action. The 3c index may answer optional evidence questions. | HG-0010-T1; **after stage 5**, alongside 6–7; E3 labels | Measures, attribution and unknown/mixed status are kept. Older facts never enter recent denominators. Top matches cannot replace coverage. A missing/expired/unauthorized transcript cannot be replaced. Activity facts and performance rows stay unchanged. Feedback source/extraction/analysis gold passes. |
| **8b. Feedback generation and validation** | Compose student sections (strengths, difficulties, supported progress, suggested next steps) with private tutor notes kept separate. Apply feedback grounding/suitability checks before the review draft. Trace through the same Langfuse integration. | HG-0010-T2, after 8a | No exercise, key, duration or prior homework request is needed. Unsupported claims and imported instructions cannot bypass checks. Feedback composition/validation gold passes. Feedback judge labeling starts. |
| **8c. Feedback review and approved handoff** | Connect section decisions, substantive full revision, durable waits and the exact approved copy to the existing review interface, records and Langfuse decision scores. | HG-0010-T2, after 8b; reuse HG-0006 and the stage 4 interface | Revisions retain frozen evidence and invalidate affected approvals. Stale/duplicate actions repeat no effects. Private notes never reach the copy. Approval/revision/export never writes performance evidence or homework allowance. |
| **9. Feedback certification and controlled activation** | **E4** for feedback: frozen families/variants, per-job gates, a feedback judge holdout and real privacy/export/no-performance-write checks. Add feedback online evaluation to the pilot project. Record feedback effort and use separately, and agree operating terms before separately authorized activation. | HG-0010-T3 and HG-0008 feedback rules, after 8a–8c | Same gates as stage 6, applied to feedback independently. Feedback stays disabled on any failed or missing gate. No homework target or allowance transfers. |

Stage barriers describe delivery slices. They do not complete a native specification while its scenarios are
unverified. Real homework use waits for stage 6 and launch authority; real feedback use waits for stage 9 and
launch authority. Only after feedback should lesson planning be prepared, then urgent replanning.

## Decisions in this revision

1. **Langfuse Cloud (owner decision).** Cloud removes the need to self-host several stateful services. In
   exchange, it becomes a named processor under PD-28.
   - Synthetic development uses a project that holds no learner data (L0), before 3a and the first required experiment.
   - Real excerpts wait for stage 5: processor terms, EU region, no-training confirmation, retention and
     canary-verified deletion.
   - If required deletion cannot be enforced, production-derived items stay out of Langfuse.
2. **Feedback starts after stage 5 (delegated decision).** Logic:
   - 8a technically needs only Stage 1 data, 3a and 3b. 8c needs stage 4 records and stage 5's lifecycle
     (checkpoints, deletion, fencing). Starting earlier would build feedback on unfinished shared controls and
     reopen them twice.
   - Stage 6 may involve reviewer labeling, freezing and holdout rounds. Feedback can proceed in parallel
     once the shared controls are ready, subject to available capacity.
   - Feedback gold (E3) starts in E0; 8a waits for its approved applicable labels, which may not yet be available.
   - Guardrail: fixes for homework gate failures in stages 6–7 take priority over feedback work, which keeps
     PD-03's homework-first priority.
3. **Production-to-gold runs during the pilot, in two lanes (delegated decision).** Logic:
   - Five tutors × up to 20 preparations is the only real distribution available before scaling, and weekly
     review will surface failure patterns that synthetic families miss.
   - Copying real learner content needs separate permission and reviewed anonymization (PD-28), and aliases
     do not anonymize.
   - **Default lane (from the first pilot week):** weekly review flags a failure pattern. A reviewer authors a
     new *synthetic reproduction* containing no copied learner content. It goes through normal review into
     the next manifest version.
   - **Exceptional lane:** a production-derived item is admitted only with separate reuse permission,
     reviewed anonymization and the stage 5 Langfuse deletion check. It is never promoted automatically from
     a score or a tutor approval.
   - This satisfies principle 9 during the pilot while keeping real learner text out of gold by default.
4. **Extraction with mandatory confirmation (owner assumption).** Without extraction, tutors hand-code every
   count. That threatens PD-05 and the PD-31 effort target, and leaves the feedback learning curve empty.
   Confirmation keeps PD-08's rule that uncertain extracted observations await the tutor.
5. **Private transcript index (owner assumption).** This satisfies principle 5 and PD-33 without weakening the
   rule that feedback covers the selected transcript directly. Local embeddings keep private text away from
   external providers.
6. **Reviewers** are a role (a qualified English tutor, defined in E0), not named people in this plan.

## Work across stages

**Privacy.**

- Ownership, permission, minimization and safe logging begin in stages 0–1.
- Deletion/expiry handling arrives with every learner-linked store: the private index, checkpoints, permitted
  evaluation excerpts and Langfuse objects. Stage 5 verifies the combined lifecycle.
- Real learner data waits for all controls and verified processor terms for the model provider and Langfuse
  Cloud.
- Cumulative facts inherit the same lifecycle and unavailable-source behavior. No verbatim learner passages are
  retained to bypass raw-source expiry.
- Reviewed listening sources are teaching-material references, not learner recordings. Do not import business
  archives or assume historical assignments were encountered without a separately authorized, source-qualified
  intake task.

**Verification.**

- Fixed clients check local contracts and failure paths. They cannot prove model quality or external deletion.
- Exercise the real PostgreSQL, checkpointer, worker, API, Redis and Langfuse boundaries where their behavior
  matters, then run reviewed model experiments in an authorized environment.
- Record versioned inputs, outcomes, usage and sanitized failure categories.
- Do not log private prompts or keys, add placeholder tests, or claim that a simulated service proves the real
  integration.

## Choices that keep the implementation small

| Choice | Reason and trade-off |
| --- | --- |
| Homework first; feedback after shared controls | Homework reaches stage 5 before feedback implementation. Feedback can proceed alongside homework certification and the pilot; later jobs need their own coverage. |
| Gold before each model block | Labeling time comes earlier, but model, prompt and route choices rest on evidence, and stage 6 does not become a long serial surprise. |
| Git is canonical for gold; Langfuse mirrors it | Review diffs, rights and provenance stay auditable; Langfuse supplies experiment comparison and UI. Using Langfuse as the primary store is simpler, but does not version schemas or keep review history. |
| Naive one-prompt baseline | Cheap first candidate for comparison after review and acceptance; shows whether the staged graph earns its complexity. |
| Extraction proposes; the tutor confirms | Adds one model stage and its gold, but is the only plausible route to lower intake effort without unconfirmed evidence entering rates. |
| Add feedback by reusing evidence, metrics, extraction and review | A job-specific schema/branch avoids a second agent system. Feedback needs its own claim checks and gold, and cannot turn generated text or approval into evidence. |
| Keep recent measures and cumulative context separate | Old exposure informs review without changing rate windows or becoming a forgetting/mastery score. No memory service or scheduler. |
| Select teaching purpose before material | Non-error routes need suitable input/frameworks and their own criteria, not invented confusions or an agent per route. |
| LangGraph waits; PostgreSQL domain records | Avoids a custom pause engine. Requires exact pause identities, replay-safe effects and reconciliation. |
| One web/worker codebase | Ordinary functions connect stages. Services, a broker and agent crews add coordination without a present need. |
| Exact search of eligible pgvector material and learner-scoped private segments | Permission/relevance failures stay inspectable; local embeddings keep private text in-house. Approximate indexes and rerankers wait for measured problems. |
| Redis for generic query embeddings only | Disposable: 24-hour TTL, versioned keys, no private text, no result-list cache, no persistence. |
| Bounded async I/O for provider/database waits | Fits external waits without sharing sessions. Dependent stages stay sequential; threads only for blocking parsing, processes only for measured CPU work. |

## Next implementation tasks and deferred choices

When implementation is requested, start **2R** and, independently, **E0**: inventory coverage and author
one synthetic case. Begin **C0** with the first material that needs review. Prepare **L0** with authorized
account access before 3a and the first required recorded experiment. Prepare the specifications listed under
[Sources and scope](#sources-and-scope) before their stages; do not scaffold the entire backlog first.

Choose the model provider, compatible versions, permitted execution environment and hosting/backups when their
first integration needs them. Fetch current Context7 documentation before using new framework or library
features. Compare model candidates on reviewed fixtures; no quality winner, cost budget or delivery date is
assumed here. Stage 7 additionally needs C1 material for the cohort, operator recovery/deletion procedures and
explicit launch authority.

This plan covers homework and feedback. Lesson planning and urgent replanning follow later with their own
specifications and coverage. These remain excluded:

- live student tutoring
- unrelated original authoring
- MCP/email/calendar delivery
- paid billing
- extra agent frameworks
- automatic mid-generation recovery

Requirements and execution evidence stay with their specifications.
