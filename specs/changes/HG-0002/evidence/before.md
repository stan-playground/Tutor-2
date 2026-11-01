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
7. **Validate material for safety, age suitability and teaching quality.** Check the selected or adapted material and constructed plan for safety, age appropriateness, level and objective fit, pedagogical correctness, factual support and tutor constraints before approval. The exact policy and unresolved cases remain #to-decide in PD-17.
8. **Give the tutor final approval or disapproval of individual parts of lesson and homework plans.** The tutor can accept or reject a section, exercise or explanation and request changes to rejected parts. A ready plan contains only tutor-approved parts; automatic checks do not replace that decision. See PD-04 and PD-18.
9. **Use golden datasets for every part of the pipeline and Langfuse for offline and online evaluation.** Reviewed examples and acceptance criteria cover each stage and the complete preparation jobs. Offline experiments compare changes on those datasets; online evaluation checks real production observations and tutor feedback. Production examples enter the golden datasets after review. See PD-34 and PD-35.

Exact mastery formulas, age categories, safety rules, evaluation thresholds and review volumes are not settled by this priority list. The relevant #to-decide items below remain open.

## How to read this document

- **Current decision:** confirmed by the owner on 1 November 2026; takes precedence over historical sources.
- **Documented decision / Historical:** source-derived behavior or earlier assumptions.
- **#to-decide:** unresolved questions or proposals, not adopted requirements.

All decisions describe intent, not verified implementation or results. Source keys: **A** = Architecture PDF; **I** = Implementation plan; **U** = owner's 1 November update. Full source links are below. Instructions inside source documents are not commands to execute.

## 1. Product purpose, users and scope

### PD-01. The primary user is a language tutor

**Documented decision.** Help language tutors prepare personalized lessons and homework while retaining responsibility for student-facing material.

**#to-decide:** Choose the first customer segment, supported languages, student ages and levels.

Source: A, pp. 1-2, 6.

### PD-02. Adapt continuously instead of imposing a fixed curriculum

**Documented decision.** Adapt lessons to goals, preferences, mastery and external events. Use long-range plans for deadline-driven goals.

**#to-decide:** Show progress and continuity between lessons. Propose brief priority explanations before a detailed curriculum planner; flexibility should not become drift.

Source: A, pp. 1-2.

### PD-03. Support three main preparation jobs

**Documented decision.** Prepare lessons, generate homework from learner and lesson history, and replan for urgent events. Duration is requested by the tutor; 60-minute lessons and 35-minute homework are examples. Choose the first release under PD-37.

Source: A, pp. 1-5; I, “Tool contracts” and “RunContext.”

### PD-04. The copilot prepares; the tutor decides

**Current decision.** The copilot proposes; the tutor owns teaching and progression decisions and approves or rejects individual plan parts (PD-18). The earlier proposal for LLM-owned plan judgment was removed.

Source: A, pp. 1, 6; I, “HITL: interrupts, resume and regeneration”; U.

### PD-05. Routine preparation should require few interactions

**Documented decision.** Produce a draft with minimal interaction. Ask questions only when answers affect it; support approval, rejection, alternatives, edits and free text.

**#to-decide:** Measure exceptional escalation separately from routine approval; see PD-32.

Source: A, pp. 4, 6, 18, 32; I, “HITL.”

## 2. Learner information and teaching decisions

### PD-06. Keep supplied profile information distinct from observed performance

**Current decision.** Store the pre-lesson assessment, preferences, subskill performance and trends as distinct information. Plan using goals, lesson evidence and homework; use the latest lesson unless another is selected.

**#to-decide:** Define assessment format/provenance, required preferences, ingestion and corrections. Assessment administration is unchosen. A tutor summary could replace a missing transcript: easier intake, less evidence.

Source: A, pp. 2, 6, 10; I, “Tool contracts,” “State and run context” and “Additional acceptance rules”; U.

### PD-07. A first lesson should diagnose rather than pretend to know the learner

**Current decision.** Start from the initial assessment and preferences; diagnose uncertain subskills without inventing lesson or homework history.

**Historical:** The first-lesson example used an estimated level. Neither version establishes a validated placement test.

**#to-decide:** Distinguish new students from returning students with missing, incomplete or stale evidence; show uncertainty and let tutors confirm assumptions.

Source: A, pp. 4, 6; I, “Signals” and scenario C1; U.

### PD-08. Track performance at the subskill level

**Current decision.** Track accuracy, appropriate use, correct avoidance and an improving/stable/regressing trend per subskill. Non-use needs a meaningful linguistic choice; unrelated silence proves nothing.

**Historical:** Correct uses/opportunities was the ratio; recognition → controlled production → free production → automaticity described stages.

**#to-decide:** Define opportunities, formulas, evidence comparability, confidence and recency. Keep stages descriptive; controlled-drill success does not establish spontaneous fluency.

Source: A, p. 2; I, “Tool contracts” and “Signals”; U.

### PD-09. Use lesson and homework evidence to change priorities

**Current decision.** Combine lesson and homework evidence with saved performance and trends. Raise regressing skills, maintain mastered ones, consider repeated errors, and expose missing or conflicting evidence.

**Historical defaults:** Analyze the last four homeworks; these rules remain provisional:

| Signal | Initial rule | Response |
| --- | --- | --- |
| Regression | Lesson ratio drops ≥0.15 against long-term ratio with ≥5 opportunities, or homework accuracy falls three times consecutively | Prioritize exact confusion; alert |
| Mastery | Ratio ≥0.85 across ≥3 homeworks | Maintenance; avoid repeat drills |
| Improvement | Improving across ≥3 points | Positive alert |
| Low completion | Completion <0.5 | Alert |

**#to-decide:** Validate thresholds with tutors. Low completion may indicate workload or circumstances, not low ability.

Source: A, pp. 2, 5; I, “Signals, routing policy and stop conditions”; U (lesson/homework clarification).

### PD-10. Explain why objectives were selected

**Documented decision.** Show each objective's skill/confusion, priority, reason, share and action: promote, retain, postpone, maintain or recheck. Respect required skills and tutor allocations; shares cannot exceed 100%.

**#to-decide:** Define share units, mandatory priorities and conflicts among preferences, weaknesses, goals and deadlines. Propose time allocations with short trade-off explanations.

Source: A, pp. 2, 5; I, “Tool contracts,” review payload and “Additional acceptance rules.”

### PD-11. Urgent goals cause a temporary priority shift

**Documented decision.** Temporarily promote event-related objectives and postpone others; clarify missing event details. The initial urgency window is 14 days. Record a post-event action and recompute normal priorities afterward.

**#to-decide:** Handle confirmation, cancellation and postponement; validate the urgency window. Propose returning to normal at the next tutor-confirmed request; reminders/background replanning are undefined.

Source: A, pp. 2, 5-6; I, “Signals” and scenario C4.

## 3. Teaching material and output quality

### PD-12. Produce a usable, timed teaching artifact

**Documented decision.** Produce sections with exercises, skill targets and durations fitting the requested total. Homework can mix targeted practice, speaking, rechecks and maintenance; avoid near-duplicates while retaining relevance. Lesson sections prioritize the best-fitting activity.

**#to-decide:** Define notes, instructions, keys, editing/export, student handoff and timing tolerance. Propose copyable text first; richer editing/integrations need demand.

Source: A, pp. 3-5, 17; I, “Tool contracts” and validation rules.

### PD-13. Match the actual learning problem, not just a topic label

**Documented decision.** Match the exact confusion and level; preserve pedagogical requirements when broadening context.

**Current decision.** Select/adapt exercises and explanations to domain preferences without changing the learning objective.

**#to-decide:** Let tutors mark essential context. Confirm when the source's ±1 level allowance is acceptable.

Source: A, pp. 4-5, 8, 15; I, “Routing”; U.

### PD-14. Reuse suitable exercises and adapt their context when necessary

**Current decision.** Adapt exercises and explanations to preferred domains while preserving the target subskill, level, learning mechanism and source reference.

**#to-decide:** Set first-release scope and automatic/tutor checks. A proposes independent solution and ambiguity checks; I defers them. Source fidelity alone cannot establish correct answers or pedagogy. Apply PD-17 safety checks.

Source: A, pp. 4, 17-18; I, “Tool contracts” and “Later steps: RAG”; U.

### PD-15. Broaden or ask when suitable material is missing

**Documented decision.** When material is insufficient, broaden, adapt or ask the tutor, with bounded retries. Mark remaining gaps unfilled and explain why. PD-17 governs completing or approving gaps.

Source: A, pp. 3-4, 17; I, “Routing,” “Stop conditions and caps” and “Tool contracts.”

### PD-16. Never present unsupported learner facts or nonexistent exercise references as valid

**Documented decision.** Reference only available exercises, including adaptations with provenance. Support learner claims with evidence. Leave visible gaps instead of inventing exercises, references or learner facts.

Source: A, pp. 9-10, 12, 17; I, “Tool contracts” and “Additional acceptance rules.”

### PD-17. Validate safety, suitability and constraints before approval

**Current decision.** Before approval, show checks for safety, age, level/objective fit, pedagogy, factual support and tutor constraints for material, parts and the plan.

**Historical:** Integrity, duration, pins/removals and required allocations block approval on failure; edit/reject remain available. Factual-support scores below ~0.8 warn; planning choices are excluded from factual checks.

**#to-decide:** Define safety categories, ages/missing-age handling, blockers and acknowledgment rules. Unknown references remain blocking. For gaps, choose tutor-supplied material, reduced plans or drafts. Resolve factual warnings; retained parts always need tutor approval.

Source: A, pp. 7, 17-18; I, “validate_output,” “Stop conditions and caps” and “Additional acceptance rules”; U.

## 4. Tutor review, clarification and revision

### PD-18. Show the tutor the draft and the reasons for it

**Current decision.** Tutors approve/reject sections, exercises and explanations or request changes. Only approved retained parts form a ready plan.

**Documented detail.** Show objectives/reasons, actionable warnings, gaps, learner alerts and alternatives. Whole-draft rejection, editing and choosing a variant remain available.

Source: A, p. 6; I, “Interrupt payloads” and “Review outcomes”; U.

### PD-19. Ask a question only when the answer changes the plan

**Documented decision.** Clarify evidence/goal conflicts, missing event details, material trade-offs or failed search using options or free text. Initial I rules: evidence differs by ≥2 CEFR steps; force clarification after two retrieval retries; maximum two clarifications per run.

**#to-decide:** Ask only useful questions; otherwise expose the gap. Limits must not conceal essential unknowns.

Source: A, pp. 4, 6; I, “Signals,” “Routing” and “Stop conditions and caps.”

### PD-20. Offer alternatives when several teaching directions are valid

**Documented decision.** Offer alternatives only for genuinely different valid teaching directions. Validate each separately and retain the chosen alternative's report.

Source: A, p. 6; I, “Review outcomes” and “Additional acceptance rules.”

### PD-21. Tutor edits become requirements for the next draft

**Documented decision.** Support pin/remove, share/duration changes and free-text instructions. Requirements persist within the request; latest structured changes win. Preserve draft/edit history and refuse invalid shares.

**#to-decide:** Define undo, instruction removal, free-text conflicts and whether any instruction becomes a lasting preference.

Source: I, “Edit → full regeneration” and “Additional acceptance rules.”

### PD-22. Substantive edits regenerate and recheck the whole output

**Documented decision.** Substantive edits create a new version, recompute from objective selection onward and revalidate using unchanged learner evidence. Selective regeneration was dropped.

**Current boundary.** Changed parts need renewed tutor review; individual-part approval does not select selective regeneration.

**#to-decide:** Handle unchanged approvals, minor corrections and new evidence requiring a fresh request. Selective regeneration could preserve work but adds complexity.

Source: A, pp. 1, 7; I, “Concept” and “Edit → full regeneration”; U.

### PD-23. A tutor can leave and return to a pending decision

**Documented decision.** Preserve paused drafts and answers across restarts and hours/days of waiting. Reject stale decisions and prevent duplicate effects.

**#to-decide:** Validate I's seven-day expiry and requirement for a new run after five revisions. Define what remains readable/reusable after expiry and preserve the brief when restarting.

Source: A, pp. 19-20; I, “Time limits and failure handling,” “HITL” and “Stop conditions and caps.”

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

**#to-decide:** Define working/input-needed states, return-to-result behavior and whether timing includes clarification, revisions and tutor review. Start simply; richer streaming can wait.

Source: A, p. 31; I, “Run API” and “Later steps.”

### PD-27. Failed preparation must be visible and recoverable

**Documented decision.** I allows five active minutes per segment. Failure records error/state but requires a new run; failed-run retries and mid-generation recovery are deferred. Paused decisions survive (PD-23).

**#to-decide:** Preserve the brief on restart, define carried-over requirements and decide whether failures/retries consume a usage allowance. Exact-step recovery can remain deferred.

Source: I, “Time limits and failure handling,” “Persistence, Redis and the run API” and “Later steps.”

### PD-28. Student information needs an explicit privacy and access boundary

**Documented decision.** Protect identifiable transcripts through suitable processor terms or self-hosting. Exclude personal data from exercise queries/logs; restrict external tool access to authorized tutors.

**#to-decide:** Define access, recording/upload permission, retention, deletion, quality-review reuse and age-specific handling. I defers authentication; internal experiments and tutor pilots need distinct access criteria. Compliance is unverified.

Source: A, pp. 14, 19, 23, 26; I, “Later steps: Run API extras.”

### PD-29. External assistant access is optional

**Documented decision.** Private MCP access from tutors' Claude/ChatGPT clients is conditional on a multi-client requirement; otherwise internal APIs suffice. I defers it.

**#to-decide:** Propose one primary interface first. External clients add support/access/data-sharing work; calendar/email references do not authorize integrations or sending messages.

Source: A, p. 19; I, “Later steps: Data and surfaces.”

### PD-30. During-lesson tutoring is not an established core job

**Documented status.** Live error → hint → retry → explanation tutoring is an open idea outside the three preparation jobs and I's scope.

**#to-decide:** Propose deferring it unless pilot evidence justifies its different timing and student-facing responsibilities.

Source: A, p. 33; I, “Scope and assumptions.”

## 6. Business success, quality and release scope

### PD-31. Judge product success by useful tutor outcomes

**Documented decision.** Measure preparation time, acceptance without substantive edits, edit volume, time-to-ready, second-lesson conversion, retention and tutor capacity. Revenue/retention are downstream outcomes, not retrieval metrics.

**#to-decide:** Choose a baseline and primary pilot measure; clarify whose conversion/retention counts. Propose total tutor effort plus actual use. Learning-benefit claims need evidence.

Source: A, pp. 10, 19.

### PD-32. Tutor attention is a limited resource

**Documented decision.** Favor catching unsupported output even at the cost of extra review. Target exceptional escalation below 10% of runs. Assess quality and tutor effort together; define escalation in PD-05 and approval gates in PD-17.

Source: A, pp. 17-18, 32; I, “Additional acceptance rules.”

### PD-33. Maintain teaching assets and learner transcripts for retrieval

**Current decision.** Index homework/speaking exercises, explanations and lesson transcripts. Use teaching material for preparation/adaptation and transcripts as learner evidence under PD-28 access rules; indexing alone does not make transcripts shared teaching assets.

**Documented detail.** Distinguish search, ranking, content, generation, pedagogy, routing and UX failures; tutors/methodologists verify content. Missing assets may require authoring, not better search.

**#to-decide:** Assign ownership, review, licensing, coverage, tutor imports and transcript access/retention. A shared bank offers consistency; tutor material offers fit with variable quality. Vendor, schema and indexing method remain unchosen.

Source: A, pp. 8-12, 16-18; U.

### PD-34. Use golden datasets and Langfuse for offline and online evaluation

**Current decision.** Use golden datasets for every stage—extraction, subskill analysis/prioritization, retrieval, adaptation, composition, validation, review/revision—and complete preparation jobs. Use Langfuse for offline dataset experiments and online production checks/feedback. Live observations need no gold answer. Review cases before adding them to golden datasets; open-ended cases may use criteria, not one exact answer.

**Documented detail.** Roll out gradually with rollback. Historical proposals: 30–50 flagged cases plus random review weekly; automated checks on 5–10% of traffic. See [offline](https://langfuse.com/docs/evaluation/get-started/offline) and [online](https://langfuse.com/docs/evaluation/get-started/online) guides.

**#to-decide:** Define cases, labels/criteria, reviewers, calibration, sampling and release thresholds. Tool choice and stage coverage are settled.

Source: A, pp. 8-11, 18-19; I, “Later steps: Evals and tracing”; U.

### PD-35. Numerical quality goals are provisional, and technical scores do not prove teaching value

**Documented decision.** Quality targets and case-study results are provisional. Factual support, reference integrity, task success and material fit do not prove teaching quality.

**#to-decide:** Agree on a tutor rubric covering target, difficulty, instructions, answers, timing and supported learner claims. Use technical metrics diagnostically; do not present hypothetical gains as measured.

Source: A, pp. 1, 8, 17-18, 27, 30-33; I, “Scope and assumptions” and “Later steps.”

### PD-36. Model cost is an operating assumption, not a pricing decision

**Historical estimates, not current prices:**

| Item | Estimate |
| --- | --- |
| Typical run | $0.10–$0.20 |
| With retries/dialogue | Up to ~$0.40 |
| Active tutor volume | 100–200 runs/month |
| Model cost per tutor | $10–$40/month |

These exclude a complete serving-cost, price or margin calculation.

**#to-decide:** Define payer, charging unit, limits and treatment of revisions/failures after measuring usage and support/content costs. Subscription offers predictability; per-use pricing follows consumption but may discourage revision.

Source: A, pp. 30-33; I, “Time limits and failure handling” and “Later steps.”

### PD-37. A working implementation stage is not yet a complete tutor pilot

**Historical scope.** I plans a runnable repository and review flow with simulated data/models/material. Real retrieval, evidence ingestion, mastery updates, authentication, alert delivery and some recovery remain deferred. No implementation is established here; current product choices remain agreed despite historical deferral.

**#to-decide:** Select one complete pilot journey from actual tutor needs: homework if lesson evidence exists, lesson planning if homework records are scarce. Define real inputs, reviewed content, usable output/review, access, privacy and failure reporting. Manual integrations are acceptable; the tutor must finish the job.

Source: I, “Scope and assumptions,” “Step 2,” “Testing” and “Later steps.”

## Recommended order for unresolved decisions

Proposed discussion order, not an implementation plan:

1. Initial tutor segment and pilot job (PD-01, PD-03, PD-37).
2. Minimum inputs and usable output (PD-06, PD-07, PD-12).
3. Adaptation checks, safety, warnings and gaps (PD-14–PD-17).
4. Evidence formulas and priority thresholds (PD-08–PD-11).
5. Review effort, revisions and recovery (PD-05, PD-18–PD-24, PD-26–PD-27).
6. Asset ownership, access and data handling (PD-28, PD-33).
7. Golden cases, evaluation thresholds, pilot success, costs and pricing (PD-29–PD-32, PD-34–PD-37).

## Sources

- **U:** Owner's 1 November 2026 request and confirmation to use both lesson and homework evidence. Earlier generation suggestions remain proposals unless separately adopted.
- **A:** [Tutor Copilot — Merged Architecture Doc, 14 October 2026, 33 pages](</Users/HUAWEI/Yandex.Disk.localized/Coding-Ya/Legend/Tutor Copilot — Merged Architecture Doc.pdf>).
- **I:** [Tutor Copilot — Implementation Plan Repo + LangGraph HITL, dated 17 October, revised 18 October 2026](</Users/HUAWEI/Yandex.Disk.localized/Coding-Ya/Legend/Tutor Copilot — Implementation Plan Repo + LangGraph HITL.md>).

Langfuse links explain evaluation terminology. This document establishes no application implementation, current provider prices, compliance or measured product outcomes.
