# Independent LangGraph architecture boundary review

Verdict: **GO** for the requested Architecture.md revision. No blocking findings.

Reviewed on 1 November 2026 under the active HighGrade independent review method. Scope: the architecture recommendation only, with Product Decisions.md retained as product authority; no application or native-specification implementation is approved here.

## Inputs and freshness

Read the complete revised architecture, relevant unchanged product contracts, saved before-document and full diff, plus original checks-v1.json. Recomputed the following identities and matched the check report:

- Architecture.md: `10f1d80a6e3a95d8a9653c90ab18d1ac1a209fec5a7a8ca29f1026ed7be453dd`.
- Before-document: `dc6e2d035f4a89f6190d3f964122db40857340111c92b7c49812883de5a977eb`.
- Product Decisions.md: `dda62c0835e507fa48b59197090ae86888e48e05b11cccca2952ec18a7db9164`.
- Original checks-v1.json: `1ea7d614c1307c2058491cdeaa4b67bb49f593b1a858bfe9e505a6b417dbd116`.

The original report records successful whitespace, shell-syntax and existing-JSON checks, and expressly excludes runtime/SDK/database execution. Those checks are used only as documentation evidence.

## Findings and observations

1. **Execution versus domain authority, lines 7, 93–97, 128–131 and 178–180:** LangGraph owns permitted execution paths and durable human pauses; relational records own learner information, draft/validation versions, tutor decisions and export. The text acknowledges that graph checkpoints and application transactions are separate persistence boundaries even within PostgreSQL. Saved transition identities, idempotent publication/finalization and persisted-pause reconciliation address crash windows without claiming a cross-saver transaction.
2. **Exact human decisions, lines 153–154 and 184–190:** Tutor actions check authenticated ownership, current draft, exact interrupt/pause, expiry and validation under ordered locks. Partial approvals persist without model calls; actionable answers/regeneration/complete review queue continuation. The graph resumes the same thread from saved decision identities and rechecks application records. Stale/duplicate resumes cannot become new permission. Approval carryover requires unchanged content and relevant objective/timing/constraint context. Finalization transactionally verifies every retained part, creates the immutable approved manifest and counts completion once; replay cannot duplicate it. Student export remains separate from keys.
3. **Concurrency and replay, lines 160 and 178–186:** Start/resume invocations are serialized per graph thread, while domain publication is conditional on current lease/request version/active learner. Publication, tutor actions and deletion share learner-then-request lock order and locked eligibility checks. Wait nodes contain no expensive generation or non-idempotent pre-interrupt writes; repeated effects after resume also require duplicate protection. Graph-version compatibility is pinned or the request expires visibly. These are sufficient written invariants for this architecture study; they still need actual implementation mechanisms and race tests.
4. **Failure-policy alignment, lines 176–182 and 230–234:** A durable completed human-wait checkpoint may be reconciled after a crash without regenerating; abandoned/incomplete active generation without that checkpoint fails visibly and requires a manual new request under PD-27. A framework's ability to recover internal nodes does not activate that excluded feature. Segment/provider/repair budgets remain bounded, with no exactly-once external-call promise.
5. **Privacy across graph history, lines 194–202 and 220:** State/interrupt payloads contain bounded IDs/routing references rather than transcript text, prompts or teacher keys. All learner-linked historical checkpoints, pending writes, interrupt payloads and transition references join deletion/retention. Workers must stop or be fenced before final cleanup, and late saver writes must be removed before the active-data deadline. Accidental raw copies inherit thirty-day expiry. Backup restoration reapplies deletion; traces and contracted provider behavior remain covered without compliance certification.
6. **Scope and consistency, lines 85–97, 228–240 and 242–282:** The selection now consistently uses a small LangGraph with provider SDK/Pydantic model calls rather than requiring PydanticAI or a second durable orchestrator. Teaching routes, asset eligibility, learner evidence, per-part tutor control, manual student handoff and pilot exclusions remain. Alternatives retain explicit trade-offs. The final diagrams reflect the selected design. The report calls out actual restart, stale interrupt, split-persistence, replay and late-deletion tests before real use.

## Limits

No checkpoint saver, graph invocation, worker serialization, row locks, resume, generation, model-call count, export, expiry, deletion or SDK compatibility was executed. This review establishes consistency and sufficiency of the selected written boundaries, not reliable runtime behavior, legal compliance, human acceptance or pilot activation. The native initial-specification placeholders remain outside this change; this review did not edit them or Product Decisions.md.
