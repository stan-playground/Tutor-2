# Initial specifications

Draft specs for the clear homework-pilot cases, based on [Product Decisions](<../Product Decisions.md>) and the revised [Architecture](../Architecture.md). Most remain concise; HG-0008 has a concrete dataset construction contract. Detailed application design and executable checks come before implementation.

1. [HG-0003 — Learner intake and subskill evidence](changes/HG-0003/spec.json): tutor-owned assessment, preferences, lesson/homework evidence and qualified subskill measures.
2. [HG-0004 — Reviewed assets and retrieval](changes/HG-0004/spec.json): find suitable, permissioned material with provenance; expose missing content.
3. [HG-0005 — Homework generation and validation](changes/HG-0005/spec.json): select evidence-linked objectives, adapt reviewed material and produce checked student/tutor outputs.
4. [HG-0006 — Durable tutor review and export](changes/HG-0006/spec.json): LangGraph pauses, exact part decisions, revisions, manual failure recovery and approved student copy.
5. [HG-0007 — Data lifecycle and safe observability](changes/HG-0007/spec.json): permission, retention, deletion and privacy across sources, derived records, checkpoints and telemetry.
6. [HG-0008 — Evaluation and free pilot](changes/HG-0008/spec.json): typed dataset items, twelve homework families, stage coverage, tutor review, frozen release gates and judge calibration; tutor outcomes and once-only allowance accounting. See the [dataset fields and case matrix](datasets.md).

Lesson planning, urgent replanning, unrestricted original authoring, live tutoring, external delivery integrations and paid billing have no initial implementation specs here. Model/provider selection and detailed API, schema and graph contracts remain implementation preparation.

These drafts are not implemented, tested product behavior or human acceptance. Earlier HG-0001/0002 records concern documentation changes, not application features.
