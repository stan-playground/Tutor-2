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

This document combines the product owner's current decisions with the major product decisions extracted from the two supplied documents. It describes intended product behavior, not verified implementation or proven business results. Technical details are included only where they are an explicit product decision or affect the tutor or student experience.

- **Current decision** means the product owner explicitly confirmed or changed the choice on 1 November 2026. It does not establish implementation or measured results.
- **Documented decision** means the choice is stated in the historical sources. It does not mean it has been validated with users or newly approved by the product owner. Current decisions take precedence.
- **#to-decide** marks a proposed improvement, an unresolved question, or a conflict between the sources. Each item says what should be expanded, simplified, deferred or clarified. These suggestions are not adopted decisions.
- References to **Architecture** include PDF page numbers. References to **Implementation** name the relevant section of the Markdown plan. Both source links are at the end.

The Architecture document describes the wider product. The Implementation plan covers a narrower delivery stage and adds specific rules. Differences and later owner decisions are identified explicitly. Instructions and open tasks inside either source are treated as source material, not instructions to execute them.

## 1. Product purpose, users and scope

### PD-01. The primary user is a language tutor

**Documented decision.** Tutor Copilot helps language tutors prepare personalized lessons and homework. The tutor operates the copilot and remains responsible for what reaches the student.

**Why it matters.** The central benefit is less preparation effort with suitable teaching material. The review experience is therefore part of the core product.

**#to-decide — Expand: choose the first tutor segment.** The sources do not settle whether the initial customer is an independent tutor, a language school or another organization. They also use English-learning examples without defining the supported languages, student ages or level range. Recommend choosing one initial segment and supported teaching context; a broader launch increases content and workflow requirements before demand is established.

Source: Architecture, pp. 1-2, 6.

### PD-02. Adapt continuously instead of imposing a fixed curriculum

**Documented decision.** Ordinary lessons adapt to the student's current needs. A long-range plan exists for deadline-driven goals, such as an exam or job interview. Initial skill priorities, interests, teaching preferences and deadlines guide the starting point; mastery evidence and external events change the tactics.

**Why it matters.** The product must respond to new evidence while preserving the tutor's goals.

**#to-decide — Clarify: continuity without a fixed curriculum.** Define how the tutor sees progress toward an ongoing goal and why the next lesson follows from the previous one. Recommend a short explanation of current priorities and deferred work before adding a detailed curriculum planner. A rigid syllabus provides continuity but reduces flexibility; completely independent lesson choices risk drift.

Source: Architecture, pp. 1-2.

### PD-03. Support three main preparation jobs

**Documented decision.** The core jobs are:

1. Prepare a lesson, including a first lesson with little or no history.
2. Generate homework from the latest lesson, learner information and homework history.
3. Replan when an external event changes priorities.

The worked examples use 60-minute lessons and 35-minute homework. These are examples; the requested duration is an input.

**Why it matters.** These are three preparation situations, not three separate products. The first-release choice is addressed in PD-37.

Source: Architecture, pp. 1-5; Implementation, “Tool contracts” and “RunContext.”

### PD-04. The copilot prepares; the tutor decides

**Documented decision.** The tutor is the final decision-maker on material that reaches the student or affects progression. The copilot proposes a draft rather than replacing the tutor's professional judgment. The earlier claim that an LLM should judge plan feedback better than a human was explicitly removed.

**Current decision.** Final approval or disapproval applies to individual parts of the constructed lesson and homework plans, not only to the whole draft. PD-18 describes that review boundary.

**Why it matters.** Approval is an essential product action. Low effort review should come from good drafts and clear explanations.

Source: Architecture, pp. 1, 6; Implementation, “HITL: interrupts, resume and regeneration”; product-owner update, 1 November 2026.

### PD-05. Routine preparation should require few interactions

**Documented decision.** A normal request produces a draft for review. It becomes a planning dialogue when clarification could materially change the result. Tutor input should use the lightest suitable interaction: approve or reject, choose among valid alternatives, make an edit, or enter free text.

**#to-decide — Clarify: routine review versus escalation.** Every output requires tutor review, while the Architecture target is fewer than 10% of runs escalating to the tutor. Define escalation as additional clarification or exceptional review effort, separate from normal approval, and measure both. Otherwise the target conflicts with the intended workflow and hides tutor effort.

Source: Architecture, pp. 4, 6, 18, 32; Implementation, “HITL.”

## 2. Learner information and teaching decisions

### PD-06. Keep supplied profile information distinct from observed performance

**Current decision.** The system stores the student's initial language assessment from before the first lesson, preferences, and subsequently observed subskill performance and trends. Planning uses that information together with goals, recent lesson evidence and homework history. Keep the initial assessment, supplied preferences and later observations distinguishable. Without an explicit lesson selection, the latest lesson is used where applicable.

**Why it matters.** The first lesson has an assessment starting point, and later preparation can respond to observed progress. A preference should not silently become a performance claim.

**#to-decide — Expand: define the minimum useful input.** Specify the assessment format and provenance, required preference fields, how lesson and homework records enter the product, and how the tutor corrects information. The decision to retain an initial assessment does not yet choose how that assessment is administered. Recommend allowing a concise tutor summary where a transcript is unavailable; summaries are easier to provide, while transcripts offer richer evidence with more collection and review work.

Source: Architecture, pp. 2, 6, 10; Implementation, “Tool contracts,” “State and run context” and “Additional acceptance rules”; product-owner update, 1 November 2026.

### PD-07. A first lesson should diagnose rather than pretend to know the learner

**Current decision.** Before the first lesson, the initial language assessment and preferences provide the starting point. The copilot can include targeted diagnostic checkpoints to confirm uncertain subskills rather than treating the absence of lesson history as absence of all assessment evidence. It does not invent previous lesson observations or homework results.

**Historical source detail.** The earlier worked case began from a profile and estimated level with a baseline diagnostic objective. The current decision adds a saved assessment obtained before the first lesson; it does not establish a validated placement-test feature.

**#to-decide — Expand: distinguish missing evidence from a new student.** A returning student can have a missing transcript, incomplete homework or stale records. Define how those cases affect confidence and planning. Recommend showing which evidence is available and allowing the tutor to confirm assumptions; a single “history available” choice is too coarse to explain these differences.

Source: Architecture, pp. 4, 6; Implementation, “Signals” and scenario C1; product-owner update, 1 November 2026.

### PD-08. Track performance at the subskill level

**Current decision.** Track each subskill through accuracy, use when appropriate, correct non-use when inappropriate, and an improving, stable or regressing trend. The observations need enough task context to show whether the subskill was called for. Absence of a form in an unrelated answer is not evidence of correct avoidance.

**Historical source detail.** The Architecture used correct uses divided by opportunities and described recognition, controlled production, free production and automaticity as possible mastery stages. An opportunity was a meaningful linguistic choice, not simply an exercise attempted. One ratio does not yet cover all the newly agreed evidence types.

**Why it matters.** “Knows present perfect” is less useful than evidence about the exact distinction the learner can or cannot make.

**#to-decide — Clarify: what qualifies as mastery evidence.** Define the opportunities and formulas for accuracy, appropriate use, missed use and inappropriate use, including how correct avoidance is observed. Decide which observations are comparable and how confidence and recency affect interpretation. A controlled drill should not automatically establish fluent spontaneous use. Recommend starting with dated observations and qualified trends; keep the four mastery stages descriptive until their relationship to observations is defined.

Source: Architecture, p. 2; Implementation, “Tool contracts” and “Signals”; product-owner update, 1 November 2026.

### PD-09. Use lesson and homework evidence to change priorities

**Current decision.** Use both lesson and homework evidence to change priorities, together with saved subskill performance and trends. Recent regression raises the relevant objective's priority; sustained mastery reduces repeated drills and moves the skill toward maintenance. Improvement, low homework completion and repeated errors are also meaningful signals. If one source is missing or conflicts with the other, show that limit rather than fabricating agreement.

The historical Implementation defaults to the last four homework records and proposes these initial rules; these remain provisional rather than newly confirmed thresholds:

| Signal | Initial rule in the source | Intended response |
| --- | --- | --- |
| Regression | Lesson accuracy at least 0.15 below the long-term ratio with at least five opportunities, or homework accuracy falling three times in succession | Raise priority, target the exact confusion, notify the tutor |
| Mastery | Ratio at least 0.85 across at least three homeworks | Move toward maintenance and avoid repeat drills |
| Improvement | Improving trend across at least three points | Positive notification |
| Low homework volume | Completion below 0.5 | Notify the tutor |

**#to-decide — Reconsider: provisional rules versus pedagogical judgments.** These values are explicitly initial settings, not validated educational standards. Recommend checking them with tutors before making them strong recommendations. Low completion should prompt a workload or circumstances question rather than imply low ability. Restrict mastery claims to the evidence actually observed.

Source: Architecture, pp. 2, 5; Implementation, “Signals, routing policy and stop conditions”; product-owner update and lesson/homework clarification, 1 November 2026.

### PD-10. Explain why objectives were selected

**Documented decision.** Objectives identify the skill or confusion, priority, reason, intended share of the output and an action such as promotion, maintenance, postponement or recheck. The tutor sees why each objective won. Required skills and tutor-specified shares must be respected; cumulative shares cannot exceed the whole allocation.

**#to-decide — Clarify: what a share means and how conflicts are resolved.** Specify whether shares allocate minutes, activity count or another measure, and which priorities are mandatory. The sources do not fully define how tutor preferences, measured weaknesses, learner goals and deadlines compete. Recommend using time where practical and asking only when a conflict changes the lesson materially. Include the trade-off in the explanation rather than exposing a complex weighting system.

Source: Architecture, pp. 2, 5; Implementation, “Tool contracts,” review payload and “Additional acceptance rules.”

### PD-11. Urgent goals cause a temporary priority shift

**Documented decision.** An upcoming interview or similar event can promote relevant speaking and preparation objectives and postpone lower-priority work. Missing essential event details trigger clarification. The Implementation initially treats deadlines within 14 days as urgent. Normal priorities are recomputed after the event, and the plan records a post-event action.

**#to-decide — Expand: define how the temporary change ends.** Specify who confirms the event happened, how postponement or cancellation is handled, and when deferred learning returns. Recommend returning to ordinary priorities on the next preparation request after tutor confirmation. Automatic reminders or background replanning add a separate experience that is not defined in the sources. Also confirm whether a single 14-day window makes sense across different event types.

Source: Architecture, pp. 2, 5-6; Implementation, “Signals” and scenario C4.

## 3. Teaching material and output quality

### PD-12. Produce a usable, timed teaching artifact

**Documented decision.** The output is a lesson plan or homework organized into sections, with exercises, skill targets and durations that fit the requested total. Homework can combine targeted practice, speaking, diagnostic rechecks and maintenance. It should avoid near-duplicate exercises while retaining relevance; lesson sections prioritize the best-fitting activity.

**#to-decide — Expand: define the actual deliverable.** The sources do not fully specify teacher notes, student instructions, answer keys, editable formatting, export or the handoff to the student. Recommend defining the smallest artifact a pilot tutor can use in their existing workflow. Copyable text is inexpensive to deliver; a richer editor or integrations may save more effort but need evidence of demand. Clarify how lesson time and homework completion time are estimated, and how much timing variation is acceptable.

Source: Architecture, pp. 3-5, 17; Implementation, “Tool contracts” and validation rules.

### PD-13. Match the actual learning problem, not just a topic label

**Documented decision.** Material selection considers the exact confusion, learner level and context. An exercise about a broad grammar topic is insufficient if it does not test the intended distinction. Pedagogical requirements are preserved when search is broadened; contextual requirements are normally more flexible. Speaking practice is selected alongside other exercises.

**Current decision.** Use the student's domain preferences when selecting and adapting exercises and explanations. Domain adaptation must preserve the intended subskill, level and learning mechanism; it cannot substitute a more entertaining but irrelevant activity.

**#to-decide — Clarify: which requirements may be relaxed.** Let the tutor identify a context or exercise feature that is essential for a particular request. Workplace context may be optional for grammar practice but essential for an imminent interview. The Architecture also mentions level matching within one step; confirm when that is an acceptable teaching choice rather than an automatic allowance.

Source: Architecture, pp. 4-5, 8, 15; Implementation, “Routing”; product-owner update, 1 November 2026.

### PD-14. Reuse suitable exercises and adapt their context when necessary

**Current decision.** Adapt suitable exercises to the student's preferred domain, such as a professional field or personal interest, while preserving the target subskill and learning mechanism. Explanations can also be adapted where needed. Keep the source reference so the tutor can distinguish the original material from the adaptation.

**Why it matters.** Adaptation makes an existing exercise bank useful for more learner goals without treating invented material as retrieved content.

**#to-decide — Resolve: the checks required for adapted material.** The Architecture calls for independent solution and ambiguity checks, while the historical Implementation defers them. Domain adaptation is now an agreed product capability; its first-release scope and checking method remain open. Decide which automatic checks and explicit tutor checks are required before use. Automatic checks improve coverage but add cost and still need validation. Agreement with the source alone does not establish that an exercise or answer key is correct; safety and age suitability also apply under PD-17.

Source: Architecture, pp. 4, 17-18; Implementation, “Tool contracts” and “Later steps: RAG”; product-owner update, 1 November 2026.

### PD-15. Broaden or ask when suitable material is missing

**Documented decision.** When material is insufficient, the copilot can broaden the search, adapt an exercise or ask the tutor which trade-off to make. It should not continue indefinitely. If the gap remains after clarification, the affected section is marked unfilled with a reason.

**Why it matters.** A visible gap is useful only if the tutor understands what remains unfinished. The completion and approval policy is addressed in PD-17.

Source: Architecture, pp. 3-4, 17; Implementation, “Routing,” “Stop conditions and caps” and “Tool contracts.”

### PD-16. Never present unsupported learner facts or nonexistent exercise references as valid

**Documented decision.** Referenced exercises must come from the material available to the run, including adaptations with provenance. Factual claims about the learner must be supported by learner evidence. If no exercise fits, the copilot should leave a visible gap instead of inventing a reference or learner fact.

**Why it matters.** A confident explanation based on nonexistent evidence undermines the tutor's decisions and trust.

Source: Architecture, pp. 9-10, 12, 17; Implementation, “Tool contracts” and “Additional acceptance rules.”

### PD-17. Validate safety, suitability and constraints before approval

**Current decision.** Validate retrieved and adapted material, individual plan parts and the constructed plan for safety, age appropriateness, learner-level and objective fit, pedagogical correctness, factual support and tutor constraints. Validation findings must be available to the tutor before approving the affected parts. These checks complement the tutor's final decision.

**Historical source detail.** The Implementation blocks approval for failed reference integrity or hard tutor constraints, including duration, pinned exercises, removals and required allocations, while allowing editing and rejection. It treats low factual-support scores, initially below approximately 0.8, as advisory. Factual checks concern learner claims and exercise descriptions rather than planning choices such as minutes per objective. That historical rule does not yet define the new safety and age-suitability policy.

**#to-decide — Resolve: safety rules, warnings and incomplete output.** Define the safety categories, supported age groups, handling of missing age information, and which findings block approval or require explicit tutor acknowledgment. The historical sources also leave gaps in the policy for factual warnings and unfilled plans. Unknown references remain blocking. For a gap, decide whether the tutor supplies material, accepts a reduced plan or saves a draft. Any retained part still needs tutor approval; choosing the validation policy does not authorize automatic approval.

Source: Architecture, pp. 7, 17-18; Implementation, “validate_output,” “Stop conditions and caps” and “Additional acceptance rules”; product-owner update, 1 November 2026.

## 4. Tutor review, clarification and revision

### PD-18. Show the tutor the draft and the reasons for it

**Current decision.** The tutor gives final approval or disapproval to individual parts of a constructed lesson or homework plan, including sections, exercises and explanations. The tutor can approve suitable parts and reject or request changes to others. A plan is ready only when its retained parts have tutor approval; a rejected part cannot silently remain in the approved plan.

**Retained source detail.** Review includes the draft, objectives and rationale, validation findings, unfilled sections, relevant learner alerts and valid alternatives. Whole-draft rejection, editing and choosing an alternative remain available. Those actions supplement review of individual parts.

**Why it matters.** The tutor needs enough evidence to make a decision without reconstructing the preparation process. Warnings need to explain the issue and its consequence, not just display a confidence score.

Source: Architecture, p. 6; Implementation, “Interrupt payloads” and “Review outcomes”; product-owner update, 1 November 2026.

### PD-19. Ask a question only when the answer changes the plan

**Documented decision.** Clarification is warranted by a significant conflict in evidence or goals, missing essential event details, an ambiguous material trade-off, or unsuccessful material search. Answers can use suggested options or free text. The Implementation gives a two-CEFR-step evidence disagreement as an initial trigger.

**#to-decide — Reconsider: forced questions when the tutor has no useful information.** The Implementation forces clarification after two unsuccessful retrieval retries and caps clarifications at two per run. Recommend asking when the tutor can resolve an ambiguity; otherwise show the content gap and a useful next action. A limit protects attention, but should not force a meaningless question or conceal an essential unanswered one.

Source: Architecture, pp. 4, 6; Implementation, “Signals,” “Routing” and “Stop conditions and caps.”

### PD-20. Offer alternatives when several teaching directions are valid

**Documented decision.** The tutor may choose among multiple valid drafts when the planner identifies genuinely different directions. Alternatives are not mandatory for every request. Each retained alternative has its own validation result, and choosing it keeps that result with the chosen output.

**Why it matters.** Alternatives give the tutor control over a meaningful teaching trade-off. The documented conditional use avoids requiring several drafts for every routine request.

Source: Architecture, p. 6; Implementation, “Review outcomes” and “Additional acceptance rules.”

### PD-21. Tutor edits become requirements for the next draft

**Documented decision.** Supported edits include keeping or removing an exercise, changing a skill share, changing the total duration and adding free-text instructions. Requirements survive later revisions. The latest structured instruction for the same item takes precedence, earlier drafts and edits remain in history, and invalid cumulative shares are refused rather than silently ignored.

**#to-decide — Expand: define how a tutor withdraws an instruction.** “Latest change wins” covers replacing a value, but not all undo or free-text conflicts. Recommend letting the tutor inspect and remove active requirements before regenerating. Decide when an instruction applies only to this preparation request and when, if ever, it becomes a persistent preference. The sources only establish persistence within the current request.

Source: Implementation, “Edit → full regeneration” and “Additional acceptance rules.”

### PD-22. Substantive edits regenerate and recheck the whole output

**Documented decision.** A meaningful tutor edit creates a new version, recomputes the plan from objective selection onward, and repeats validation. The learner evidence stays fixed during that revision. Selective regeneration was explicitly dropped.

**Current review boundary.** Approval or disapproval of individual parts does not itself choose selective regeneration. Any regenerated or materially changed part returns to tutor review; earlier approval cannot automatically approve changed content.

**Why it matters.** Changing an objective or duration can affect the rest of the plan. The tutor needs to review the affected parts in the context of the complete revised plan.

**#to-decide — Clarify: revisions and existing approvals.** Full regeneration can change material the tutor already liked. Decide whether unchanged approved parts retain approval or require confirmation again, and whether wording and formatting corrections can be saved directly while substantive changes regenerate the draft. Also specify when changed learner evidence requires a fresh preparation request. More selective regeneration could preserve work but adds complexity; the historical decision dropped it, and approval of individual parts does not silently reverse that choice.

Source: Architecture, pp. 1, 7; Implementation, “Concept” and “Edit → full regeneration”; product-owner update, 1 November 2026.

### PD-23. A tutor can leave and return to a pending decision

**Documented decision.** A paused clarification or review survives a service restart and can resume hours or days later with its draft and answers intact. A response to an outdated question or draft must not act on the current one, and repeated clicks must not apply the same decision twice.

**#to-decide — Clarify: expiration and revision limits.** The Implementation expires a pending decision after seven days and allows at most five tutor revisions per run, after which a new run is required. Recommend validating these limits with the preparation workflow and specifying what the tutor can still read or reuse after expiration. Fixed limits bound effort and cost, but restarting should not mean re-entering the whole brief.

Source: Architecture, pp. 19-20; Implementation, “Time limits and failure handling,” “HITL” and “Stop conditions and caps.”

### PD-24. Notifications inform; questions block preparation

**Documented decision.** Regression, low homework completion, notable improvement and repeated weak material search can notify the tutor without stopping the request. Clarification requires an answer. Repeating or revising the same request should not create duplicate notifications.

**Delivery scope.** Relevant alerts are included in the review payload. The Implementation records alerts for later delivery but defers the delivery mechanism. External notifications are therefore not an established initial feature; the pilot boundary is addressed in PD-37.

Source: Architecture, pp. 4, 6; Implementation, graph notes, “alert_tutor” and “Later steps.”

### PD-25. Consequential judgments remain with the tutor

**Documented decision.** The Architecture identifies level promotion, grading, placement, exam readiness, suspected academic-integrity issues and the amount of feedback given to a student as situations requiring tutor judgment. For example, a tutor may address three of fifteen detected errors to avoid overloading the student.

**Scope.** These are examples of where tutor judgment matters. The Implementation does not define complete assessment, feedback-selection or academic-integrity features. In particular, a sudden change in homework quality is described as a concern, not evidence of a reliable cheating-detection capability.

Source: Architecture, p. 6; Implementation, “Scope and assumptions” and “Later steps.”

## 5. Waiting, failures, access and privacy

### PD-26. Preparation may take time, and the tutor should see progress

**Documented decision.** The Architecture treats preparation as an asynchronous task rather than a rapid chat reply. Its targets are a first progress update within three seconds, typical completion around 20-40 seconds, and 95% of runs completing in roughly 60-90 seconds. These are targets, not measured performance. The Implementation defers live progress events.

**#to-decide — Resolve: the initial waiting experience.** Recommend at least a visible working state, a clear indication when tutor input is needed, and a recoverable result when the tutor returns. Rich progress streaming can wait if a simpler status experience is sufficient. Specify whether the timing target includes clarification, revision and the tutor's own review time.

Source: Architecture, p. 31; Implementation, “Run API” and “Later steps.”

### PD-27. Failed preparation must be visible and recoverable

**Documented decision.** The Implementation bounds active preparation to five minutes per uninterrupted segment. A failed request records its error and preserves its saved state, but the current plan requires the tutor to start a new run. Recovery of work interrupted while actively generating and retrying failed runs are deferred. Recovery of an already paused tutor decision is supported.

**#to-decide — Improve: define a retry experience that preserves the brief.** Recommend allowing the tutor to restart with the same inputs and clearly stating whether earlier requirements are carried over. Full continuation from the precise failure point can remain deferred; a usable restart is still a product requirement. Decide whether failed attempts or retries count toward any future usage allowance.

Source: Implementation, “Time limits and failure handling,” “Persistence, Redis and the run API” and “Later steps.”

### PD-28. Student information needs an explicit privacy and access boundary

**Documented decision.** Lesson transcripts may identify students. Components handling them need suitable data-processing terms or self-hosting options. Personal information should be kept out of exercise-search queries and their logs. The intended external tool access is restricted to authorized tutors.

**#to-decide — Expand: define the minimum policy before real student use.** Decide who can view each student's records, what lesson recording or upload permission is required, how long transcripts and drafts are kept, how deletion works, and whether real cases may be reused for quality review. Age-specific requirements depend on the chosen student segment. Authentication is deferred in the Implementation, so an authorized internal experiment and a tutor-facing pilot need distinct release criteria. These are unresolved product requirements; the documents do not establish compliance.

Source: Architecture, pp. 14, 19, 23, 26; Implementation, “Later steps: Run API extras.”

### PD-29. External assistant access is optional

**Documented decision.** A private MCP connection could let authorized tutors access the copilot from their own Claude or ChatGPT client. The Architecture says this is justified only if access from multiple clients is a product requirement; internal APIs are otherwise sufficient. The Implementation defers this surface.

**#to-decide — Defer unless validated: external-client access.** Recommend choosing one primary tutor interface first. External-client access can fit tutors' existing habits, but it adds access, support and data-sharing questions. The mention of calendar and email context is not a commitment to build integrations or send messages.

Source: Architecture, p. 19; Implementation, “Later steps: Data and surfaces.”

### PD-30. During-lesson tutoring is not an established core job

**Documented status.** The Architecture leaves an error → hint → retry → explanation dialogue as an open item. It is not among the three established preparation jobs, and the Implementation does not plan it.

**#to-decide — Defer: treat live teaching assistance as a separate scope decision.** Recommend keeping it outside the initial release unless pilot evidence changes the priority. Live interaction has different timing, student-facing behavior and teaching responsibilities from preparation.

Source: Architecture, p. 33; Implementation, “Scope and assumptions.”

## 6. Business success, quality and release scope

### PD-31. Judge product success by useful tutor outcomes

**Documented decision.** Product measures include preparation time, acceptance without substantive edits, manual edit volume, time until a lesson is ready, second-lesson conversion, retention and tutor capacity. Retention and revenue are downstream business signals, not measures of exercise-search quality.

**#to-decide — Focus: choose a primary pilot success measure.** Recommend measuring total tutor time from request to usable material, including clarification and review, alongside whether the tutor actually uses the output. Acceptance alone can reward superficial approval, while fast generation can hide extensive editing. Define the baseline workflow and clarify whose second lesson and retention are being counted. Student learning benefit also needs evidence before it becomes a marketing claim.

Source: Architecture, pp. 10, 19.

### PD-32. Tutor attention is a limited resource

**Documented decision.** The quality policy favors catching unsupported outputs even if that creates extra review. The Architecture simultaneously targets exceptional escalation on fewer than 10% of runs, because too much intervention erodes the time-saving benefit.

**Why it matters.** Quality requirements and tutor workload must be assessed together. The definition of escalation is addressed in PD-05, and the distinction between blocking defects and warnings in PD-17.

Source: Architecture, pp. 17-18, 32; Implementation, “Additional acceptance rules.”

### PD-33. Maintain teaching assets and learner transcripts for retrieval

**Current decision.** Assets in the vector database include homework exercises, speaking exercises, explanations and lesson transcripts. Retrieve exercises and explanations for preparation and adaptation, and use relevant transcripts as learner evidence. A transcript records observed learning context; it is not automatically a reusable exercise or explanation. Student access and privacy rules in PD-28 apply to transcript retrieval.

**Retained source detail.** Quality review distinguishes retrieval failure, ranking failure, missing content, unsupported generation, pedagogical errors, routing errors and UX problems. A missing exercise or explanation may require content work. Tutors and methodologists supply or verify pedagogical judgments.

**#to-decide — Expand: assign ownership and scope of the assets.** Define who supplies, reviews, updates and licenses exercises and explanations, what coverage the first tutor segment needs, and whether tutors can bring their own material. Define which student transcripts a tutor may retrieve and their retention rules under PD-28. A shared reviewed teaching bank offers consistency; tutor-provided material may fit existing practice but varies in quality and permissions. The vector-database decision does not yet select a vendor, schema or indexing method.

Source: Architecture, pp. 8-12, 16-18; product-owner update, 1 November 2026.

### PD-34. Use golden datasets and Langfuse for offline and online evaluation

**Current decision.** Maintain golden datasets covering every pipeline stage and the complete lesson-planning, homework and urgent-replanning jobs. Coverage includes learner-evidence extraction, subskill analysis and prioritization, retrieval, adaptation, composition, validation, and tutor-review and revision behavior. Use Langfuse for offline evaluation against these datasets and online evaluation of real production observations, including tutor feedback and appropriate automated checks. Review production examples before adding them to golden datasets.

For open-ended plans, a golden case may provide reviewed examples and acceptance criteria rather than a single exact answer. Online evaluation does not assume that every production observation has a gold reference. The official Langfuse guides distinguish [offline dataset experiments](https://langfuse.com/docs/evaluation/get-started/offline) from [online production evaluation](https://langfuse.com/docs/evaluation/get-started/online).

**Retained source detail.** Changes roll out gradually and can be withdrawn. Reviewed failures improve future quality checks. The current decision selects golden datasets and Langfuse as product requirements; it does not claim that datasets, evaluators or the integration already exist in this repository.

**Proposed operating assumptions.** The Architecture suggests reviewing roughly 30-50 flagged cases plus a random sample each week and automatically checking 5-10% of traffic. These are proposed review volumes, not evidence that an operating review program exists. Permission to reuse student material is addressed in PD-28.

**#to-decide — Define the evaluation cases and release rules.** Agree on representative examples, labels or acceptance criteria for each stage, who reviews them, evaluator calibration, and the online sampling and release thresholds. Tool selection and the decision to evaluate every stage are settled; these operating details are not.

Source: Architecture, pp. 8-11, 18-19; Implementation, “Later steps: Evals and tracing”; product-owner update, 1 November 2026. Official Langfuse links explain the selected evaluation terms, not product implementation.

### PD-35. Numerical quality goals are provisional, and technical scores do not prove teaching value

**Documented decision.** The Architecture proposes release targets for supported factual claims, correct exercise references, task success and useful material selection. It explicitly labels its numbers as targets, estimates or illustrative results and says suggested case-study narratives must be replaced by real evidence. A high score for factual support does not establish pedagogical correctness.

**Why it matters.** The product can have correct references and still produce an unsuitable lesson. Tutor judgment and actual use remain necessary.

**#to-decide — Clarify: the smallest credible product quality bar.** Recommend agreeing on a short tutor rubric: correct learning target, appropriate difficulty, usable instructions, correct answers, feasible timing and no unsupported learner facts. Use technical metrics to diagnose failures, and avoid presenting the document's hypothetical improvements or targets as measured achievements.

Source: Architecture, pp. 1, 8, 17-18, 27, 30-33; Implementation, “Scope and assumptions” and “Later steps.”

### PD-36. Model cost is an operating assumption, not a pricing decision

**Documented assumptions from the Architecture, not current verified prices:**

| Item | Source estimate |
| --- | --- |
| Typical lesson-plan or homework run | $0.10-$0.20 |
| Run with retries or tutor dialogue | Up to approximately $0.40 |
| Active tutor volume | Approximately 100-200 runs per month |
| Model cost per active tutor | Approximately $10-$40 per month |

These figures do not establish the total cost of serving a tutor, a selling price, a margin or willingness to pay. The sources do not settle whether a regenerated draft consumes another billable allowance.

**#to-decide — Expand: define the business model after measuring usage.** Decide who pays, the charging unit, and how revisions and failures are treated. A subscription makes tutor spending predictable; per-use pricing follows consumption but can discourage experimentation and necessary revision. Recommend measuring actual total usage and support/content costs before choosing limits or making margin claims.

Source: Architecture, pp. 30-33; Implementation, “Time limits and failure handling” and “Later steps.”

### PD-37. A working implementation stage is not yet a complete tutor pilot

**Historical delivery scope.** The Implementation's first two stages plan a runnable project and the planning/review flow, while deferring real retrieval, ingestion of lesson and homework evidence, learner-progress updates, authentication, notification delivery and several recovery features. Its core scenarios use prepared learner information and simulated model/material responses. These are descriptions of the historical plan, not evidence that those stages have been implemented here.

The newly confirmed asset, learner-evidence, validation, individual-part approval and evaluation principles belong to the product direction. Their delivery order remains to be planned; historical deferral does not make them undecided product choices again.

**#to-decide — Simplify and complete: define the first real-user release.** Recommend validating one complete preparation-and-review journey before adding the others. Homework may be relatively bounded when lesson evidence exists; lesson planning may be the better start if homework records are scarce. Choose using pilot tutors' actual work. Then define the necessary inputs, reviewed material, usable output, review flow, access, data handling and way to report failures. Some integrations can remain manual, but the tutor must be able to finish the job. Passing the implementation stages alone does not establish product readiness.

Source: Implementation, “Scope and assumptions,” “Step 2,” “Testing” and “Later steps.”

## Recommended order for unresolved decisions

This is a proposed discussion order, not an implementation plan or a change to the documented decisions.

1. **Choose the initial tutor segment and preparation job** (PD-01, PD-03). This determines which content and workflow are necessary.
2. **Define minimum input and the usable output** (PD-06, PD-07, PD-12). This makes a complete pilot possible without unnecessary integrations.
3. **Set the policy for incomplete drafts, warnings and adapted exercises** (PD-14 through PD-17). This establishes what approval means.
4. **Define the remaining learner-evidence formulas and priority rules** (PD-08 through PD-11). Subskill tracking and the use of both lesson and homework evidence are agreed; the formulas and thresholds remain open.
5. **Define review effort, revisions and recovery** (PD-05, PD-18 through PD-24, PD-26 through PD-27). This determines whether the product saves preparation time.
6. **Set asset ownership, access and data handling before using real student records** (PD-28, PD-33). The asset types are agreed; their content coverage and access details remain open.
7. **Define golden cases, evaluation thresholds and pilot success criteria; measure costs before pricing and expansion** (PD-29 through PD-32, PD-34 through PD-37). Langfuse and offline/online evaluation are agreed choices.

## Sources

- **Current product decisions:** the product owner's request on 1 November 2026 and the explicit clarification that both lesson and homework evidence change priorities. These decisions take precedence over conflicting historical extracts. The earlier generation suggestions remain proposals unless separately adopted.
- [Architecture: Tutor Copilot — Merged Architecture Doc, 14 October 2026, 33 pages](</Users/HUAWEI/Yandex.Disk.localized/Coding-Ya/Legend/Tutor Copilot — Merged Architecture Doc.pdf>).
- [Implementation: Tutor Copilot — Implementation Plan Repo + LangGraph HITL, dated 17 October and revised 18 October 2026](</Users/HUAWEI/Yandex.Disk.localized/Coding-Ya/Legend/Tutor Copilot — Implementation Plan Repo + LangGraph HITL.md>). References use the supplied file's section headings, including its additional acceptance rules.

Historical extracts are grounded in the two supplied documents; current decisions are grounded in the dated product-owner request and clarification. The linked Langfuse documentation supports the distinction between offline and online evaluation. No application implementation, market claim, provider price or measured project outcome is established by this document.
