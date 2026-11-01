# Initial specifications

Draft specs for homework first and post-lesson feedback next, before lesson planning and urgent replanning, based on [Product Decisions](<../Product Decisions.md>) and [Architecture](../Architecture.md). Most remain concise; HG-0008 has a concrete per-job dataset contract. Detailed application design and real checks come before implementation.

1. [HG-0003 — Learner intake and subskill evidence](changes/HG-0003/spec.json): tutor-owned assessment, preferences, lesson/homework evidence and qualified subskill measures.
2. [HG-0004 — Reviewed assets and retrieval](changes/HG-0004/spec.json): find suitable, permissioned material with provenance; expose missing content.
3. [HG-0005 — Homework generation and validation](changes/HG-0005/spec.json): select evidence-linked objectives, adapt reviewed material and produce checked student/tutor outputs.
4. [HG-0006 — Durable tutor review and export](changes/HG-0006/spec.json): shared LangGraph pauses, exact part decisions, revisions and approved student copy with job-specific homework/feedback validation.
5. [HG-0007 — Data lifecycle and safe observability](changes/HG-0007/spec.json): permission, retention and deletion across both jobs, private notes, sources, checkpoints and telemetry.
6. [HG-0008 — Evaluation and free homework pilot](changes/HG-0008/spec.json): twelve homework and eight feedback families, per-job stage/golden gates, review and judge calibration; original homework cohort/allowance. See [dataset fields and matrices](datasets.md).
7. [HG-0010 — Post-lesson feedback](changes/HG-0010/spec.json): selected transcript plus frozen learner state/learning curve, supported feedback sections, private tutor notes, exact tutor approval and no canonical performance writes.

Lesson planning, urgent replanning, unrestricted original authoring, live tutoring, external delivery integrations and paid billing have no initial implementation specs here. Model/provider selection and detailed API, schema and graph contracts remain implementation preparation.

These application drafts are not implemented, tested behavior or human acceptance. HG-0001/0002 are earlier documentation changes; [HG-0009](changes/HG-0009/spec.json) records the product-document feedback update. The [implementation plan](<../Implementation Plan.md>) owns delivery order and [repository plan](<../Repository Structure.md>) owns proposed modules/tools.

[HG-0011](changes/HG-0011/spec.json) records the documentation change for PD-39/40: cumulative learning history/on-request review and teaching beyond visible errors. HG-0003–0008 and HG-0010 are refined in place as unimplemented drafts; history/route scenarios and the dataset contract define future checks, not passed application behavior.
