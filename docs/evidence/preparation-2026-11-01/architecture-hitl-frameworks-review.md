# LangGraph architecture revision — independent framework review

Date: 1 November 2026. Verdict: **GO** for the assigned documentation scope.

Reviewed Architecture.md SHA-256: `10f1d80a6e3a95d8a9653c90ab18d1ac1a209fec5a7a8ca29f1026ed7be453dd`.

Before-document SHA-256: `dc6e2d035f4a89f6190d3f964122db40857340111c92b7c49812883de5a977eb`.

Unchanged Product Decisions.md SHA-256: `dda62c0835e507fa48b59197090ae86888e48e05b11cccca2952ec18a7db9164`.

## Inputs and method

Read the active HighGrade independent-review method, the complete current architecture, the unchanged product decisions relevant to scope/approval/recovery/privacy/evaluation, and the before document and diff-v1.patch. Read the original checks-v1.json and independently compared all three recorded hashes with actual file bytes; all match. Earlier advice favoring a custom workflow was not treated as the current decision or evidence against the owner's authorized selection.

Review scope: framework fairness, consistency of the selected orchestration/model boundary, stage and final diagrams, replay and graph/domain ownership, generation scope and implementation claims. Documentation review confirms the stated design, not runtime behavior.

## Findings

No actionable blocking findings in the assigned scope.

- **Selected framework and fair alternatives — lines 7, 67–99:** The opening, alternatives and framework selection consistently choose a small LangGraph for execution and durable human pauses, with one provider SDK and Pydantic schemas inside nodes. PydanticAI remains an accurately described optional model-integration alternative; it is no longer a required initial dependency. Custom persisted control flow remains a credible alternative rather than a second selected orchestrator. CrewAI Flows retain credit for actual routing/persistence/human-feedback capabilities.
- **Responsibility boundaries — lines 93–95, 109–110 and 128–131:** PostgreSQL domain records remain authoritative for learner facts, constraints, validation, exact tutor decisions and approved export. Graph checkpoints contain execution position and bounded references, not approval authority or another editable learner profile. The queue dispatches starts/resumes and does not duplicate graph routing. Durable checkpoints are explicitly required; memory-only persistence is not portrayed as restart-safe.
- **Stages and diagrams — lines 141–160 and 242–282:** The stage table separates artifact publication from wait nodes, identifies actionable saved decisions, and preserves typed-output validation and the bounded format-repair rule. Both final diagrams agree with the revised selection. The teaching path returns through objective selection for substantive revision and gates finalization on retained-part approval and validity. The finalization transaction remains authoritative even though the component diagram groups execution responsibilities.
- **Resume and replay — lines 178–190:** Invocations for a thread are serialized. Domain/checkpointer writes are explicitly separate transactions; persisted transition identities and idempotent publication/finalization reconcile repeated execution. Same-thread continuation uses the expected interrupt identity and a saved decision/transition reference; client-supplied graph input is not authorization. Individual part approvals cause no model call. Small wait nodes avoid generation or unsafe writes before interrupt; effects after the pause also require duplicate protection. Graph-version compatibility for paused requests is addressed.
- **Recovery policy preserved — lines 22, 180–186 and 234:** Durable human pauses do not silently enable arbitrary active-generation recovery. A persisted human-wait checkpoint can be reconciled without regenerating; an abandoned active generation follows PD-27's visible failure/manual-new-request policy and five-minute active-segment limit. Selecting a capable framework is not claimed to supersede that product policy.
- **Approval and completion policy preserved — lines 188–190:** Exact part content and relevant context govern approval carry-forward. New requests/retries retain no approvals, substantive edits regenerate fully, and typo/layout edits require validation and renewed part approval. Finalization verifies domain approvals and validation before creating the student manifest, with once-only completion accounting despite graph replay.
- **Checkpoint privacy — lines 95 and 198–202:** The revised design brings historical checkpoints, pending writes, interrupt payloads and transition references into the learner-linked deletion boundary now. It requires worker fencing/stopping before final cleanup and prevents late saver writes from silently escaping cleanup. IDs/bounded routing state are the intended checkpoint contents; raw copies inherit raw-source expiry. This adds required design responsibilities rather than claiming a checkpointer automatically implements privacy.
- **Generation and evidence limits — lines 31–65, 99 and 218–224:** The homework pilot still uses reviewed reuse/adaptation/composition and exposes gaps. Original authoring and deferred preparation jobs are not enabled by graph routing. Typed schemas, solver agreement and framework selection do not certify teaching correctness. Langfuse remains the evaluation system; mandatory per-request validation is still separate from additional sampled monitoring. No runtime, model-quality or implementation-success claims were added.

## Source check

Reopened the current official [LangGraph interrupt documentation](https://docs.langchain.com/oss/python/langgraph/interrupts) and [persistence documentation](https://docs.langchain.com/oss/python/langgraph/persistence). They support persistent checkpoints, same-thread resumption, Command-based continuation and node restart semantics. The study's StateGraph/AsyncPostgresSaver selection is a proposed compatible architecture, not a dependency-lock or execution claim. Earlier current official PydanticAI/CrewAI research remains relevant to the unchanged capability descriptions.

## Limits

The original checks establish whitespace, launcher syntax and JSON parsing, not pause/resume reliability or transaction correctness. Real process-restart, stale/duplicate resume, domain/checkpoint crash-window, late saver/deletion and approved-export checks remain implementation work, as the architecture explicitly states. Exact package compatibility is untested.

No application, model, database, graph, checkpoint, telemetry exporter or deletion operation ran during this review. No product document, native specification placeholder/catalog or application file was changed. This GO is a documentation verdict, not user acceptance, authority to commit/push or permission to launch a pilot.
