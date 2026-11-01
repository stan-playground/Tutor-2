# Product Decisions

Tutor Copilot · Source extraction: 28 October 2026 · Product priorities updated: 1 November 2026

## Highest-priority product decisions

The product owner confirmed the following principles on 1 November 2026. They take precedence over conflicting historical source descriptions below. They describe the intended product; they do not claim that it is implemented.

1. **Support three main preparation jobs:** lesson planning, including the first lesson; homework preparation; and urgent replanning for a deadline or external event.
2. **Track performance at the subskill level.** Record accuracy, whether the learner uses the subskill when needed, and whether they correctly avoid using it when it is inappropriate. Non-use counts as evidence only when the task creates a meaningful choice; silence or an unrelated task does not establish mastery. See PD-08.
3. **Use both lesson and homework evidence to change priorities.** Combine recent observations with saved subskill performance and trends. Make missing or conflicting evidence visible rather than inventing it. See PD-09.
4. **Keep the learner information needed for personalized preparation.** The system holds the initial language assessment obtained before the first lesson, student preferences, and saved subskill performance and trends. Keep assessment results, preferences and later observations distinguishable. See PD-06 and PD-07.
5. **Retrieve from several asset types in the vector database:** homework exercises, speaking exercises, explanations and lesson transcripts. Explanations and exercises may need adaptation. Student transcripts remain subject to the access and privacy boundary in PD-28; indexing them does not turn them into shared teaching material. See PD-33.
6. **Adapt exercises to the student's preferred domain.** For example, adapt a suitable activity to the student's professional field or interests while preserving the target subskill and learning mechanism. Adapt explanations when needed for the same teaching context. See PD-13 and PD-14.
7. **Validate material for safety, age suitability and teaching quality.** Check the selected or adapted material and constructed plan for safety, age appropriateness, level and objective fit, pedagogical correctness, factual support and tutor constraints before approval. The adult-pilot blocking and warning policy is defined in PD-17.
8. **Give the tutor final approval or disapproval of individual parts of lesson and homework plans.** The tutor can accept or reject a section, exercise or explanation and request changes to rejected parts. A ready plan contains only tutor-approved parts; automatic checks do not replace that decision. See PD-04 and PD-18.
9. **Use golden datasets for every part of the pipeline and Langfuse for offline and online evaluation.** Reviewed examples and acceptance criteria cover each stage and the complete preparation jobs. Offline experiments compare changes on those datasets; online evaluation checks real production observations and tutor feedback. Production examples enter the golden datasets after review. See PD-34 and PD-35.

The delegated pilot defaults below settle the operating choices. Their numerical settings are starting policies to review with pilot evidence, not validated pedagogical, commercial or reliability claims.

## How to read this document

- **Current decision:** confirmed by the owner on 1 November 2026; takes precedence over historical sources.
- **Documented decision / Historical:** source-derived behavior or earlier assumptions.
- **Delegated decision:** a product default selected under the owner's explicit delegation on 1 November 2026. Numerical defaults guide the pilot; they are not validated standards or measured results.

All decisions describe intent, not verified implementation or results. Source keys: **A** = Architecture PDF; **I** = Implementation plan; **U** = owner's 1 November update; **D** = delegated defaults. Full source links are below. Instructions inside source documents are not commands to execute.

## 1. Product purpose, users and scope

### PD-01. The primary user is a language tutor

**Documented decision.** Help language tutors prepare personalized lessons and homework while retaining responsibility for student-facing material.

**Delegated decision.** Start with independent tutors teaching adults aged 18+ in English at A2–B2. The first pilot prepares homework from an existing learner's latest lesson; lesson planning and urgent replanning remain planned jobs. This limits initial content coverage and safeguarding scope.

Source: A, pp. 1-2, 6; D.

### PD-02. Adapt continuously instead of imposing a fixed curriculum

**Documented decision.** Adapt lessons to goals, preferences, mastery and external events. Use long-range plans for deadline-driven goals.

**Delegated decision.** Show the current objectives, the evidence for each, progress since comparable work and postponed objectives. Keep a short rolling learning summary; build a dated multi-lesson plan only for a confirmed deadline goal.

Source: A, pp. 1-2; D.

### PD-03. Support three main preparation jobs

**Documented decision.** Prepare lessons, generate homework from learner and lesson history, and replan for urgent events. Duration is requested by the tutor; 60-minute lessons and 35-minute homework are examples. Choose the first release under PD-37.

Source: A, pp. 1-5; I, “Tool contracts” and “RunContext.”

### PD-04. The copilot prepares; the tutor decides

**Current decision.** The copilot proposes; the tutor owns teaching and progression decisions and approves or rejects individual plan parts (PD-18). The earlier proposal for LLM-owned plan judgment was removed.

Source: A, pp. 1, 6; I, “HITL: interrupts, resume and regeneration”; U.

### PD-05. Routine preparation should require few interactions

**Documented decision.** Produce a draft with minimal interaction. Ask questions only when answers affect it; support approval, rejection, alternatives, edits and free text.

**Delegated decision.** Count an escalation once when a request needs a blocking question or exceptional correction beyond routine review; divide by all started requests. Ordinary part approval is excluded. Track question rounds and tutor effort separately so a low escalation rate cannot hide burdensome review.

Source: A, pp. 4, 6, 18, 32; I, “HITL.”; D.

## 2. Learner information and teaching decisions

### PD-06. Keep supplied profile information distinct from observed performance

**Current decision.** Store the pre-lesson assessment, preferences, subskill performance and trends as distinct information. Plan using goals, lesson evidence and homework; use the latest lesson unless another is selected.

**Delegated decision.** Require a dated tutor assessment summary or assessment upload, its source/uncertainty, goals, preferred domains and an adult confirmation; collect no birth date. If no formal assessment exists, record the tutor's provisional estimate. Accept lesson notes instead of transcripts, label their source and retain corrections in history; do not administer a placement test in the pilot.

Source: A, pp. 2, 6, 10; I, “Tool contracts,” “State and run context” and “Additional acceptance rules”; U; D.

### PD-07. A first lesson should diagnose rather than pretend to know the learner

**Current decision.** Start from the initial assessment and preferences; diagnose uncertain subskills without inventing lesson or homework history.

**Historical:** The first-lesson example used an estimated level. Neither version establishes a validated placement test.

**Delegated decision.** Distinguish new learners, returning learners with usable evidence and returning learners needing a recheck. Evidence older than 90 days is historical and triggers targeted checks of important uncertain skills. Missing history stays missing; a provisional tutor assessment can support a diagnostic draft, without establishing mastery.

Source: A, pp. 4, 6; I, “Signals” and scenario C1; U; D.

### PD-08. Track performance at the subskill level

**Current decision.** Track accuracy, appropriate use, correct avoidance and an improving/stable/regressing trend per subskill. Non-use needs a meaningful linguistic choice; unrelated silence proves nothing.

**Historical:** Correct uses/opportunities was the ratio; recognition → controlled production → free production → automaticity described stages.

**Delegated decision.** For each subskill, accuracy = correct target uses / attempted target uses; needed use = correct uses where required / required-use opportunities; avoidance = appropriate non-use / opportunities where it would be inappropriate. Correct means linguistically and contextually appropriate. Show counts, source, date and task type; zero denominators mean unknown. Count only clear task/tutor observations, not inferred silence; valid optional alternatives are not missed required-use opportunities. Keep recognition, drills and spontaneous production separate; uncertain extracted observations await tutor confirmation. The four mastery stages remain descriptive.

Source: A, p. 2; I, “Tool contracts” and “Signals”; U; D.

### PD-09. Use lesson and homework evidence to change priorities

**Current decision.** Combine lesson and homework evidence with saved performance and trends. Raise possible regressions for review, suggest maintenance for tutor-confirmed skills, consider repeated errors, and expose missing or conflicting evidence.

**Historical defaults, superseded by the review rules below:**

| Signal | Initial rule | Response |
| --- | --- | --- |
| Regression | Lesson ratio drops ≥0.15 against long-term ratio with ≥5 opportunities, or homework accuracy falls three times consecutively | Prioritize exact confusion; alert |
| Mastery | Ratio ≥0.85 across ≥3 homeworks | Maintenance; avoid repeat drills |
| Improvement | Improving across ≥3 points | Positive alert |
| Low completion | Completion <0.5 | Alert |

**Delegated decision.** Use up to the latest four lessons and four homework submissions within 90 days; separate completion from attempted-answer performance. Compare the same subskill, evidence type and task demands. Each rate needs three comparable observations with at least five relevant opportunities each for a trend: first-to-last change ≥0.15 is improving, ≤−0.15 regressing, otherwise stable; conflicting measures are mixed. Smaller samples remain insufficient. A single 0.15 drop is a possible-regression alert, not proof. Ratios ≥0.85 across three comparable observations suggest maintenance only when applicable use/avoidance measures support it and the tutor confirms. Low completion prompts a workload check, not an ability downgrade.

Source: A, pp. 2, 5; I, “Signals, routing policy and stop conditions”; U (lesson/homework clarification); D.

### PD-10. Explain why objectives were selected

**Documented decision.** Show each objective's skill/confusion, priority, reason, share and action: promote, retain, postpone, maintain or recheck. Respect required skills and tutor allocations; shares cannot exceed 100%.

**Delegated decision.** Shares allocate total planned minutes, including instructions, checks and transitions; show percentages and minutes summing to the requested total. Apply safety/validity gates and explicit tutor requirements first, then confirmed urgent goals, corroborated weaknesses, longer-term goals and maintenance. Domain preferences shape material. Explain each objective with one evidence-linked reason; ask which constraint to relax if the requirements cannot fit.

Source: A, pp. 2, 5; I, “Tool contracts,” review payload and “Additional acceptance rules.”; D.

### PD-11. Urgent goals cause a temporary priority shift

**Documented decision.** Temporarily promote event-related objectives and postpone others; clarify missing event details. The initial urgency window is 14 days. Record a post-event action and recompute normal priorities afterward.

**Delegated decision.** Use the tutor-confirmed event, date and goal; flag dates within 14 days as urgent, with tutor override outside that window. Keep postponed objectives. Cancellation restores ordinary priorities; a changed date updates the temporary plan. At the next request after the event, ask for an outcome/update and recompute priorities without assuming success. No background replanning or reminders in the pilot.

Source: A, pp. 2, 5-6; I, “Signals” and scenario C4; D.

## 3. Teaching material and output quality

### PD-12. Produce a usable, timed teaching artifact

**Documented decision.** Produce sections with exercises, skill targets and durations fitting the requested total. Homework can mix targeted practice, speaking, rechecks and maintenance; avoid near-duplicates while retaining relevance. Lesson sections prioritize the best-fitting activity.

**Delegated decision.** Deliver copyable student homework plus a separate tutor key with answers, alternatives and short teaching notes; speaking tasks use assessment criteria. Provide student-ready copy only after approval; tutors share it themselves, without a delivery integration. Planned section minutes must sum exactly to the requested duration, including instructions and checks. Actual learner completion time remains an estimate.

Source: A, pp. 3-5, 17; I, “Tool contracts” and validation rules; D.

### PD-13. Match the actual learning problem, not just a topic label

**Documented decision.** Match the exact confusion and level; preserve pedagogical requirements when broadening context.

**Current decision.** Select/adapt exercises and explanations to domain preferences without changing the learning objective.

**Delegated decision.** Context defaults to preferred; tutors may mark it required. Adapt suitable material or disclose neutral context when a preferred domain is unavailable. Never silently relax required context or the learning objective. Remove automatic ±1-level substitution: neighboring-level material requires checked adaptation to the learner's actual task demands and visible tutor review; otherwise leave a gap.

Source: A, pp. 4-5, 8, 15; I, “Routing”; U; D.

### PD-14. Reuse suitable exercises and adapt their context when necessary

**Current decision.** Adapt exercises and explanations to preferred domains while preserving the target subskill, level, learning mechanism and source reference.

**Delegated decision.** The pilot adapts reviewed exercises/explanations, not unrelated original exercises. Recheck instructions, level, expected answers, acceptable alternatives, ambiguity, factual claims and safety after adaptation. Closed-answer items need an independent solution check against the key; open tasks need clear criteria. Show provenance and require tutor approval; source fidelity or model agreement alone cannot establish correctness.

Source: A, pp. 4, 17-18; I, “Tool contracts” and “Later steps: RAG”; U; D.

### PD-15. Broaden or ask when suitable material is missing

**Documented decision.** When material is insufficient, broaden, adapt or ask the tutor, with bounded retries. Mark remaining gaps unfilled and explain why. PD-17 governs completing or approving gaps.

Source: A, pp. 3-4, 17; I, “Routing,” “Stop conditions and caps” and “Tool contracts.”

### PD-16. Never present unsupported learner facts or nonexistent exercise references as valid

**Documented decision.** Reference only available exercises, including adaptations with provenance. Support learner claims with evidence. Leave visible gaps instead of inventing exercises, references or learner facts.

Source: A, pp. 9-10, 12, 17; I, “Tool contracts” and “Additional acceptance rules.”

### PD-17. Validate safety, suitability and constraints before approval

**Current decision.** Before approval, show checks for safety, age, level/objective fit, pedagogy, factual support and tutor constraints for material, parts and the plan.

**Historical:** Integrity, duration, pins/removals and required allocations block approval on failure; edit/reject remain available. Factual-support scores below ~0.8 warn; planning choices are excluded from factual checks.

**Delegated decision.** Require tutor confirmation of adulthood; missing age confirmation blocks real-learner preparation. Use neutral everyday/workplace topics and respect exclusions. Block explicit sexual content, graphic violence, hate/discrimination, harmful instructions, unnecessary personal disclosures, unknown references, incorrect/ambiguous keys, unsupported learner claims and unmet hard requirements. Suspected critical flags pause approval until verified or corrected; confirmed failures cannot be waived. Explain noncritical difficulty/preference trade-offs for acknowledgment. A low model score alone is advisory. Fill gaps with checked tutor material, explicitly revised scope/duration, or an incomplete draft; never silently approve them.

Source: A, pp. 7, 17-18; I, “validate_output,” “Stop conditions and caps” and “Additional acceptance rules”; U; D.

## 4. Tutor review, clarification and revision

### PD-18. Show the tutor the draft and the reasons for it

**Current decision.** Tutors approve/reject sections, exercises and explanations or request changes. Only approved retained parts form a ready plan.

**Documented detail.** Show objectives/reasons, actionable warnings, gaps, learner alerts and alternatives. Whole-draft rejection, editing and choosing a variant remain available.

Source: A, p. 6; I, “Interrupt payloads” and “Review outcomes”; U.

### PD-19. Ask a question only when the answer changes the plan

**Documented decision.** Clarify evidence/goal conflicts, missing event details or material trade-offs using options or free text. **Historical I rules:** ≥2 CEFR steps of disagreement, forced clarification after two retrieval retries and a two-round cap; the delegated rule below replaces forced questions.

**Delegated decision.** Bundle only questions the tutor can answer that would materially change the result. Allow two clarification rounds; after that, save an incomplete draft with the missing inputs. Failed search without a meaningful tutor choice produces a visible content gap rather than a forced question. Never guess essential facts to satisfy the interaction limit.

Source: A, pp. 4, 6; I, “Signals,” “Routing” and “Stop conditions and caps.”; D.

### PD-20. Offer alternatives when several teaching directions are valid

**Documented decision.** Offer alternatives only for genuinely different valid teaching directions. Validate each separately and retain the chosen alternative's report.

Source: A, p. 6; I, “Review outcomes” and “Additional acceptance rules.”

### PD-21. Tutor edits become requirements for the next draft

**Documented decision.** Support pin/remove, share/duration changes and free-text instructions. Requirements persist within the request; latest structured changes win. Preserve draft/edit history and refuse invalid shares.

**Delegated decision.** Show active requirements and let tutors undo or remove them. The latest structured value wins; unresolved structured/free-text conflicts require one explicit tutor choice. Plan edits apply only to that request. Lasting preferences change only through explicit profile editing, never through automatic inference from a revision.

Source: I, “Edit → full regeneration” and “Additional acceptance rules.”; D.

### PD-22. Substantive edits regenerate and recheck the whole output

**Documented decision.** Substantive edits create a new version, recompute from objective selection onward and revalidate using unchanged learner evidence. Selective regeneration was dropped.

**Current boundary.** Changed parts need renewed tutor review; individual-part approval does not select selective regeneration.

**Delegated decision.** Full regeneration remains the default for substantive edits. Keep an earlier approval only if the part and its relevant objective, timing and constraints are unchanged; otherwise clear it for review. A tutor may correct typos/layout directly, with validation and renewed approval of the edited part. New learner evidence starts a new preparation request; selective regeneration is outside the pilot.

Source: A, pp. 1, 7; I, “Concept” and “Edit → full regeneration”; U; D.

### PD-23. A tutor can leave and return to a pending decision

**Documented decision.** Preserve paused drafts and answers across restarts and hours/days of waiting. Reject stale decisions and prevent duplicate effects.

**Delegated decision.** Adopt seven-day pause expiry and at most five substantive revisions per request. Expired/exhausted requests become read-only, with history available under PD-28 retention. Offer a new request prefilled with the brief and visible active requirements, using current learner evidence and no carried-over approvals. This bounds costs without making tutors re-enter their work.

Source: A, pp. 19-20; I, “Time limits and failure handling,” “HITL” and “Stop conditions and caps.”; D.

### PD-24. Notifications inform; questions block preparation

**Documented decision.** Notify about regression, low completion, improvement and repeated weak search without blocking; clarification blocks. Deduplicate notices across retries/revisions. Include alerts at review; I records them but defers delivery. External notifications are not established launch scope.

Source: A, pp. 4, 6; I, graph notes, “alert_tutor” and “Later steps.”

### PD-25. Consequential judgments remain with the tutor

**Documented decision.** Tutors own promotion, grading, placement, readiness, integrity concerns and how much feedback students receive.

**Scope:** These are judgment boundaries, not complete assessment/feedback features. Changed homework quality alone does not establish reliable cheating detection.

Source: A, p. 6; I, “Scope and assumptions” and “Later steps.”

## 5. Waiting, failures, access and privacy

### PD-26. Preparation may take time, and the tutor should see progress

**Documented targets:** Preparation is asynchronous: first progress within three seconds, typical completion 20–40 seconds, p95 about 60–90 seconds. These are not measurements; I defers live progress events.

**Delegated decision.** Show working, needs-input, ready-for-review and final/error states; let tutors leave and return to the saved result. Simple status refresh is enough for the pilot; token streaming is excluded. Measure the existing latency targets per active generation segment, excluding human waiting; report total elapsed time, revisions and failures separately.

Source: A, p. 31; I, “Run API” and “Later steps.”; D.

### PD-27. Failed preparation must be visible and recoverable

**Documented decision.** I allows five active minutes per segment. Failure records error/state but requires a new run; failed-run retries and mid-generation recovery are deferred. Paused decisions survive (PD-23).

**Delegated decision.** A manual retry starts a new request with the saved brief and active requirements, reloads current evidence, and revalidates without retaining approvals. Show the failure and any incomplete work. Keep the five-minute active-segment limit; mid-generation continuation is excluded. Failures and retries create no pilot charge and do not consume completed-preparation allowance.

Source: I, “Time limits and failure handling,” “Persistence, Redis and the run API” and “Later steps.”; D.

### PD-28. Student information needs an explicit privacy and access boundary

**Documented decision.** Protect identifiable transcripts through suitable processor terms or self-hosting. Exclude personal data from exercise queries/logs; restrict external tool access to authorized tutors.

**Delegated decision.** Require authenticated tutor access, isolation by tutor/student, informed adult opt-in and tutor upload permission before learner-data use; no built-in recording. Collect aliases, adult confirmation and necessary learning evidence, not birth dates/contact details or unrelated sensitive data. Named processors must meet contracted purpose, retention and no-training terms before use. Raw uploads/transcripts and their embeddings expire after 30 days; structured records/plans after 12 months of inactivity. After source expiry, show it unavailable rather than reconstructing quotes. Deletion removes access immediately, active/derived records within seven days and backups within 30. Routine logs contain metadata only; Langfuse stores scores and minimum redacted excerpts only for permitted evaluation; excerpts expire after 30 days, and learner-linked records follow the same deletion rules. Only the owning tutor sees student records; exceptional support access needs that tutor's recorded authorization and a reason. Tutors can delete learners at any time; verified learner requests are handled through the tutor or support. Production-case reuse needs separate permission and reviewed anonymization; wholly synthetic golden cases need tutor review. These are product policies, not verified compliance.

Source: A, pp. 14, 19, 23, 26; I, “Later steps: Run API extras.”; D.

### PD-29. External assistant access is optional

**Documented decision.** Private MCP access from tutors' Claude/ChatGPT clients is conditional on a multi-client requirement; otherwise internal APIs suffice. I defers it.

**Delegated decision.** Use one authenticated tutor interface with copyable outputs. MCP access and calendar/email integrations are outside the pilot; revisit only after pilot feedback establishes a concrete multi-client need. No sending or sharing happens automatically.

Source: A, p. 19; I, “Later steps: Data and surfaces.”; D.

### PD-30. During-lesson tutoring is not an established core job

**Historical idea.** A live error → hint → retry → explanation dialogue was proposed outside the three preparation jobs; the pilot decision below excludes it.

**Delegated decision.** Exclude live student tutoring and hint/retry dialogues from the pilot. Keep preparation and tutor review as the product scope; a later live-teaching request needs its own interaction and evaluation design.

Source: A, p. 33; I, “Scope and assumptions.”; D.

## 6. Business success, quality and release scope

### PD-31. Judge product success by useful tutor outcomes

**Documented decision.** Measure preparation time, acceptance without substantive edits, edit volume, time-to-ready, second-lesson conversion, retention and tutor capacity. Revenue/retention are downstream outcomes, not retrieval metrics.

**Delegated decision.** Primary outcome: reduction in tutor-reported active minutes per homework task, including setup, clarification, revisions, retries and manual fallback. Compare each tutor's pilot median with three comparable manual tasks; report medians and tutor/task counts. Track confirmed student assignment within seven days / all eligible started requests, including failures/abandonment; unknown use is not success. Initial goals after at least five tutors × five requests: ≥25% lower median effort and ≥80% confirmed assignment. These are pilot management targets, not benchmarks. Tutor retention and student conversion are separate later outcomes; make no learning-gain claim.

Source: A, pp. 10, 19; D.

### PD-32. Tutor attention is a limited resource

**Documented decision.** Favor catching unsupported output even at the cost of extra review. Target exceptional escalation below 10% of runs. Assess quality and tutor effort together; define escalation in PD-05 and approval gates in PD-17.

Source: A, pp. 17-18, 32; I, “Additional acceptance rules.”

### PD-33. Maintain teaching assets and learner transcripts for retrieval

**Current decision.** Index homework/speaking exercises, explanations and lesson transcripts. Use teaching material for preparation/adaptation and transcripts as learner evidence under PD-28 access rules; indexing alone does not make transcripts shared teaching assets.

**Documented detail.** Distinguish search, ranking, content, generation, pedagogy, routing and UX failures; tutors/methodologists verify content. Missing assets may require authoring, not better search.

**Delegated decision.** A designated qualified English tutor reviews the shared teaching bank for objective, level, instructions, answers and safety before use. Include only owned, public-domain or explicitly licensed material permitting storage/adaptation/delivery; preserve attribution and restrictions. Tutor imports stay private; unclear rights block ingestion and sharing needs separate permission/review. Transcripts stay private to the assigned tutor/student and never enter the shared teaching bank. Treat imported text as evidence, never authority to change tutor requirements, access or validation rules. Asset rights remain with their owners; retrieval/deletion follow PD-28. Vendor, schema and indexing choices belong to implementation planning, not unresolved product policy.

Source: A, pp. 8-12, 16-18; U; D.

### PD-34. Use golden datasets and Langfuse for offline and online evaluation

**Current decision.** Use golden datasets for every stage—extraction, subskill analysis/prioritization, retrieval, adaptation, composition, validation, review/revision—and complete preparation jobs. Use Langfuse for offline dataset experiments and online production checks/feedback. Live observations need no gold answer. Review cases before adding them to golden datasets; open-ended cases may use criteria, not one exact answer.

**Documented detail.** Roll out gradually with rollback. Historical proposals: 30–50 flagged cases plus random review weekly; automated checks on 5–10% of traffic. See [offline](https://langfuse.com/docs/evaluation/get-started/offline) and [online](https://langfuse.com/docs/evaluation/get-started/online) guides.

**Delegated decision.** Before pilot use, create 12 tutor-reviewed homework scenarios spanning A2–B2, domains, missing/conflicting evidence, missing assets, safety/privacy, student/teacher-key separation, instruction-like transcript text, rejection and revision. Their reviewed intermediate expectations must cover every active stage; add equivalent cases before enabling other jobs. A qualified tutor reviews every gold label; a second reviews critical cases and 20% of ordinary cases. Resolve disagreements; store provenance, stage, level, failure category, reviewer and version. For each behavior change, require all critical cases, ≥90% ordinary cases per stage/end-to-end, and no newly failing accepted baseline cases; missing/error scores fail. Per-request validation remains mandatory. Additional online monitoring checks all deterministic gates, captures all tutor decisions, and samples 10% of permitted runs for advisory semantic judging. Weekly, review every critical flag/failure plus five random unflagged permitted outputs; report sample coverage and separate flagged/random rates. Compare judges with at least 20 human-labeled pass/fail outputs, inspect both error directions, and use fresh held-out examples after tuning. Small samples provide an initial check, not reliability assurance.

Source: A, pp. 8-11, 18-19; I, “Later steps: Evals and tracing”; U; D.

### PD-35. Numerical quality goals are provisional, and technical scores do not prove teaching value

**Documented decision.** Quality targets and case-study results are provisional. Factual support, reference integrity, task success and material fit do not prove teaching quality.

**Delegated decision.** Use pass/fail reasons for target subskill, level, clear instructions, linguistic/pedagogical correctness, answers or assessment criteria, workload, tutor constraints/preferences and supported learner claims. Safety/privacy/age are hard gates. Correct or remove failed parts before approval; never average away a serious defect. Report first-draft usability as drafts needing no substantive change / all returned drafts; target/task/answer/workload changes are substantive, typos/layout are not. Human approval and technical scores do not prove learning benefit.

Source: A, pp. 1, 8, 17-18, 27, 30-33; I, “Scope and assumptions” and “Later steps.”; D.

### PD-36. Model cost is an operating assumption, not a pricing decision

**Historical estimates, not current prices:**

| Item | Estimate |
| --- | --- |
| Typical run | $0.10–$0.20 |
| With retries/dialogue | Up to ~$0.40 |
| Active tutor volume | 100–200 runs/month |
| Model cost per tutor | $10–$40/month |

These exclude a complete serving-cost, price or margin calculation.

**Delegated decision.** Run an invitation-only free pilot with 20 completed preparations per tutor and no automatic paid conversion or overage. A completed preparation is an approved plan; failed runs and within-request revisions do not consume allowance. The tutor is the future payer; a monthly subscription is the chosen commercial model, without per-revision fees. Actual pricing and paid billing are outside this pilot and require a separate commercial launch based on measured costs and willingness to pay.

Source: A, pp. 30-33; I, “Time limits and failure handling” and “Later steps.”; D.

### PD-37. A working implementation stage is not yet a complete tutor pilot

**Historical scope.** I plans a runnable repository and review flow with simulated data/models/material. Real retrieval, evidence ingestion, mastery updates, authentication, alert delivery and some recovery remain deferred. No implementation is established here; current product choices remain agreed despite historical deferral.

**Delegated decision.** Pilot the complete homework journey: initial assessment/profile → tutor lesson notes or authorized transcript → draft and separate answer guide → validation → per-part tutor review/revision → manual student handoff. Require authentication, reviewed material, privacy controls, failure recovery and stage/end-to-end evaluation before real use. Start with five invited tutors; add lesson planning including first lessons next, then urgent replanning, only after equivalent checks. No application or integration is implemented by this document.

Source: I, “Scope and assumptions,” “Step 2,” “Testing” and “Later steps.”; D.

## Pilot review and deferred scope

Review these defaults after the first cohort of at least five tutors with five requests each, or sooner after a critical failure. Check saved tutor effort, actual use, repeated content gaps and reviewer disagreement before expanding scope. A critical safety, access or approval defect stops the affected feature until corrected.

The pilot is free homework preparation for adult A2–B2 English learners. Lesson planning and urgent replanning follow after equivalent checks. Live tutoring, MCP/calendar/email integrations, unrelated original exercise generation and paid billing are excluded. Technology selection and implementation remain separate work, not open product questions in this document.

## Sources

- **U:** Owner's 1 November 2026 priority update and confirmation to use both lesson and homework evidence.
- **D:** Defaults chosen under the owner's explicit instruction to resolve the open decisions. They supersede conflicting historical assumptions. Unrelated original-generation proposals remain outside the pilot.
- **A:** [Tutor Copilot — Merged Architecture Doc, 14 October 2026, 33 pages](</Users/HUAWEI/Yandex.Disk.localized/Coding-Ya/Legend/Tutor Copilot — Merged Architecture Doc.pdf>).
- **I:** [Tutor Copilot — Implementation Plan Repo + LangGraph HITL, dated 17 October, revised 18 October 2026](</Users/HUAWEI/Yandex.Disk.localized/Coding-Ya/Legend/Tutor Copilot — Implementation Plan Repo + LangGraph HITL.md>).

The [Langfuse guides](https://langfuse.com/docs/evaluation/get-started/offline) support the evaluation mechanisms; [EDPB guidance](https://www.edpb.europa.eu/sme/learn-the-basics/data-protection-basics_en) informs data minimization and retention principles. Specific pilot thresholds and retention periods are chosen policies, not prescribed standards. This document establishes no application implementation, current provider prices, compliance certification or measured outcomes.
