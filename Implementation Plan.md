# Tutor Copilot — High-Level Implementation Plan

Prepared with HighGrade Planner · 1 November 2026 · Revised 3 November 2026

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

The findings behind these changes are in [Plan Review_claude.md](<Plan Review_claude.md>).

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
Build:     [0 ✓][1 ✓][2 ✓] → 2R → 3a → 3b → 3d → 3e → 3f → 4 → 5 → 6 → 7 (homework pilot)
                              └→ 3c ────────┘                  └→ 8a → 8b → 8c → 9 (feedback)
Gold (E):  E0 now → E1 (before each 3x) → E2 (judge labels from 3f) → E4 freeze (6) → E5 pilot curation (7)
           E0 now → E3 feedback gold (inputs now; composition labels after 3a) → 8a–8b exits → E4 freeze (9)
Langfuse:  L0 now → L1 (3a tracing) → L2 (4 scores) → L3 (5 Cloud terms, masking, deletion) → L4 (6 online)
Content:   C0 now → C1 (route × level × domain coverage before 3e and 7)
```

**Exit rule for every model stage (3b, 3d–3f, 8a–8b).** The stage exits only when its boundary's
**approved** gold items pass a recorded Langfuse experiment against the accepted baseline under the
[dataset gates](specs/datasets.md#7-frozen-experiments-and-release-decisions). Runs on draft labels guide
development but do not satisfy an exit. Stages 6 and 9 therefore freeze and certify suites that already
exist; they do not build evaluation from scratch.

### Evaluation, golden data and Langfuse

Each milestone starts as soon as its listed dependency exists. **Reviewer** means a qualified English tutor as
defined in E0; second review follows the dataset contract (all critical items and `ceil(0.20 × ordinary)`).

| Milestone | Deliverable | Depends on → unblocks |
| --- | --- | --- |
| **E0 — Harness, inventory and retrofit gold (now)** | **Contract.** Add to datasets.md/HG-0008 a planned item inventory (items × stage × severity × review passes), the reviewer-qualification definition, and the Git-canonical/Langfuse-mirror rule.<br>**Harness.** Build a local `just eval <job>` harness: item loader on the existing schema, manifest freeze (Git SHA, item revisions/hashes, evaluator versions), deterministic evaluators and the gate arithmetic.<br>**Retrofit gold** for delivered boundaries: Stage 1 confirmed-count/recent-selection numerics (datasets §3: zero denominators, 2 vs 3 observations, 4 vs 5 opportunities, ±0.15, 0.85 with/without support, the 90-day boundary, the corrected duplicate) and **Stage 2 retrieval**: suitable-candidate coverage, honest gaps, contrastive distractors, private-text canaries, embedding-outage failure. Both run locally with no LLM cost.<br>**Authoring starts** for all 12 homework and 8 feedback family *inputs* (synthetic learners, notes, transcripts, homework responses) and their extraction, source-context and analysis labels. | Item schema (exists) and Stage 1/2 code → L0, E1, 3a model comparison |
| **L0 — Langfuse Cloud dev project (now)** | Create a **synthetic-only** Langfuse Cloud project, EU data region, holding no learner data, with full input/output capture allowed. Pin the SDK after rechecking the release and version-matched docs through Context7 (Architecture names `langfuse==5.1.0`). Sync Git `evaluation/` items into Langfuse datasets (`tutor-copilot/homework-gold`, `feedback-gold`, `judge-calibration`), recording the item-version timestamp in each manifest. Run the E0 items as the first Langfuse experiment, with deterministic scores, to prove the path before model spend. | Owner-authorized account and E0 harness → L1 |
| **C0 — Content coverage (now)** | Build a coverage matrix for PD-40 routes × A2/B1/B2 × pilot domains, including listening recordings with version-matched criteria. Set up the rights intake and reviewer review for the shared bank (PD-33). The E0 retrieval run reports gaps. | Stage 2 bank → E1 retrieval/adaptation labels, 3e, C1 |
| **E1 — Stage gold before each model block** | Approved labels for each homework boundary, authored before the code that answers it:<br>• extraction → 3b<br>• analysis and route selection → 3d<br>• retrieval and adaptation, with closed answers independently solved → 3e<br>• composition and validation, with seeded defects and valid alternatives → 3f<br>• review/revision scripts → 4<br>Complete-job E2E items are assembled from these stage labels. | E0 inputs; C0 content for retrieval/adaptation labels; 3a schemas for composition, validation and review labels → each stage exit |
| **E2 — Judge calibration** | Human pass/fail labels on real candidate outputs from 3f onward: at least 20 distinct outputs per job, covering every criterion. Fix the development/holdout split by family. After tuning, a fresh holdout round. | First 3f outputs → E4 |
| **E3 — Feedback gold** | Feedback family inputs and source/extraction/analysis labels start in E0. Composition, validation and review labels follow the `FeedbackDraft` schema drafted in 3a. Separate feedback judge labels from 8b outputs. | E0, 3a → 8a–9 exits |
| **E4 — Freeze and certify (stage 6, then 9)** | Freeze the release manifests, run the full per-job/stage/E2E gates and report the fresh-holdout judge results. | E1–E3 → 7 and 9 |
| **E5 — Pilot curation** | Weekly review feeds a curation queue (see [Decisions](#decisions-in-this-revision)). | 7 → later manifests |

**Planned volume (estimate, to be replaced by the E0 inventory).**

- Homework: about 29 complete-job items (12 base families + 17 required variants), each with intermediate
  stage labels, plus about 20–25 isolated stage and numeric items.
- Feedback: about 20 complete-job items (8 + 12 variants) plus isolated items.
- Judge calibration: at least 20 outputs per job, plus a fresh holdout.

Together these are hundreds of reviewer label decisions, which makes them the main human critical path. Hence
the stream starts now.

### Build stages

| Stage | Deliverable and small implementation blocks | Dependencies / requirement owner | Completion barrier |
| --- | --- | --- | --- |
| **0–2. Done (local, synthetic)** | Foundation, tutor-owned evidence/history and reviewed teaching retrieval. See the stage records. | HG-0003/0004/0007 portions | Recorded in [Stage 0](docs/stage-0.md), [Stage 1](docs/stage-1.md) and [Stage 2](docs/stage-2.md). HG-0003's approval/copy scenario remains future. |
| **2R. Stage 1 repairs** | Reconcile the two fix backlogs into one route. They cover source-body preservation across metadata corrections, learner-scoped identities/references, exact source-version provenance and a versioned frozen-context contract. Implement as separately reviewed migrations. | Fix backlogs, HG-0003; now | No generated artifact or new frozen-context consumer exists before these pass with real checks and independent review. Stage 3 cannot start while any item is open. |
| **3a. Model, graph and trace foundation** | Choose one generation-model candidate by comparing candidates on E0/E1 items. Integrate the provider and the LangGraph worker with the PostgreSQL checkpointer (initial HG-0006 persistence). Add **Langfuse tracing (L1)** with a masking function: full capture in the synthetic project only. Draft the `HomeworkDraft` and `FeedbackDraft` schemas so labels can be written. Build the **naive baseline** (one prompt with retrieved context) and record its run as the first accepted baseline. Record cost/latency per active segment (PD-26/36). | 2R, L0; HG-0005/0006 | Every model call is traced with versions, usage and latency. Masking passes synthetic canaries. Routine checks make no live calls. The baseline experiment exists in Langfuse. |
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
   - Synthetic development starts now in a project that holds no learner data (L0).
   - Real excerpts wait for stage 5: processor terms, EU region, no-training confirmation, retention and
     canary-verified deletion.
   - If required deletion cannot be enforced, production-derived items stay out of Langfuse.
2. **Feedback starts after stage 5 (delegated decision).** Logic:
   - 8a technically needs only Stage 1 data, 3a and 3b. 8c needs stage 4 records and stage 5's lifecycle
     (checkpoints, deletion, fencing). Starting earlier would build feedback on unfinished shared controls and
     reopen them twice.
   - Stage 6 is dominated by reviewer labeling, freezing and holdout rounds, while engineering capacity is
     mostly free. Waiting for stage 6 would idle that capacity and delay R2 with no quality benefit.
   - Feedback gold (E3) is authored from E0 onward, so 8a has labels on day one.
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
| Complete homework before other jobs | Exposes evidence, material and approval problems early. Lesson planning and urgent replanning wait for equivalent coverage. |
| Gold before each model block | Labeling time comes earlier, but model, prompt and route choices rest on evidence, and stage 6 does not become a long serial surprise. |
| Git is canonical for gold; Langfuse mirrors it | Review diffs, rights and provenance stay auditable; Langfuse supplies experiment comparison and UI. Using Langfuse as the primary store is simpler, but does not version schemas or keep review history. |
| Naive one-prompt baseline | Cheap. Gives the first accepted baseline and shows whether the staged graph earns its complexity. |
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

When implementation is requested, start **2R** together with the stream starts **E0**, **L0** (after the
owner creates the synthetic Cloud project) and **C0**. These have no mutual dependency. Prepare the new
specifications listed under [Sources and scope](#sources-and-scope) before their stages. Do not scaffold the
entire backlog first.

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
