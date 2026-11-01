# Independent review: feedback privacy, tutor approval and repository plan

Verdict: **GO for the documentation/specification text only**. No blocking findings.

Reviewed under the active HighGrade independent-review method. Compared the Product Decisions opening/PD-25/28/34/37/38, feedback/durability/privacy architecture, implementation and repository plans, dataset contract, and HG-0006/0007/0008/0010 drafts. Read the original checks-v1.json, spec-validation-v1.json and executor-review-v1.md in this evidence directory. Recomputed all twelve declared input fingerprints; each matched the current document/native draft and the structural report.

## Findings

- **P3, wording only — specs/datasets.md:21:** The introduction now lists homework gold, feedback gold and judge calibration, while the item-contract paragraph still says “Both datasets use a versioned JSON schema.” “All datasets” would accurately describe the three named datasets. The common metadata includes both jobs and the native R2 names all three, so this is not a behavior ambiguity or a release blocker.

## Confirmed boundaries

1. **Selected transcript and frozen state:** PD-38, Architecture feedback path and HG-0010 require the selected authorized available transcript and frozen profile/confirmed observations. Saved history contextualizes current findings; notes do not silently replace missing/expired current transcript content, and expired quotes cannot be reconstructed. New confirmed/corrected evidence starts a new request; wording changes retain the old snapshot.
2. **Generated findings are not observed performance:** Candidate interpretations, student comments and private tutor notes stay distinct from canonical confirmed evidence. Feedback generation, approval, revision, copy and duplicate finalize cannot create observations, recount opportunities, update counts/trends/mastery or infer permanent preferences. HG-0010 S1/S5 and FB-08 expressly require before/after persisted-row observations, rather than relying on a model's assurance.
3. **Exact feedback approval and serialization:** Shared review accepts job-specific feedback sections without exercise IDs, keys or duration. It validates support and suitability, requires exact-version approval of each retained student section, invalidates affected approvals and rejects stale same-thread/draft actions. Private tutor notes are excluded by the student serializer, not merely hidden in the UI. HG-0006 S5, HG-0010 S4/S5 and FB-07 provide actual-copy canary scenarios. Part approval alone makes no model call; critical defects cannot be waived.
4. **Durable execution and failure:** PostgreSQL domain decisions remain authoritative; graph checkpoints are execution references. Shared learner/request locks, current leases, exact interrupts, idempotent receipts and separate checkpoint/domain reconciliation remain in the architecture. Abandoned active generation needs a manual new request; the new feedback branch does not enable arbitrary internal recovery. Invocation/process lifetimes and bounded async I/O remain explicit.
5. **Privacy/provider/checkpoint/cache boundary:** PD-28 remains the source for permission, minimization, thirty-day raw/excerpt expiry, twelve-month structured-record inactivity and seven-/thirty-day active/backup deletion. HG-0007 scope now expressly includes feedback artifacts, notes, transcript references and checkpoint/evaluation copies. Late publication/saver recreation, backups and providers remain within that boundary. Redis still contains only controlled generic query embeddings; private transcript text, feedback and generated plans/state do not become cache entries. No provider/model is authorized merely by a source link.
6. **Job-specific evaluation and accounting:** Feedback has eight separately reviewed families plus critical variants, active-stage/complete-job gates and feedback-specific criterion labels. Homework cases/averages cannot cover feedback failures; exercise adaptation/solving/timing are not forced into the feedback job. Cross-job related learner/source outputs remain in one calibration partition. Initial fixtures remain synthetic and rights-cleared; production reuse needs separate permission and reviewed anonymization, and historical reproducibility cannot override deletion. Homework allowance/cohort assignment targets remain homework-specific; feedback operating terms and real-data activation remain separately gated, with no invented quota or launch authority.
7. **Small repository and safe future commands:** One src package gives web/worker, evidence/metrics, job-specific composition, validation, review and graph operations explicit owners without extra agent services or generic adapter layers. The target tree is not a scaffold instruction; add modules only with working slices. Justfile recipes do not exist yet. Its default only lists recipes; routine check is source-preserving/local with no provider calls, migrations, service startup or remote trace writes. Integration requires explicit disposable local services/synthetic data. Evaluation explicitly selects the prepared job and is the named provider/Langfuse-write path, rather than a hidden routine check. Local caches/test artifacts are not claimed as application retention controls.
8. **Delivery and truth:** Security/logging start early and deletion handling accompanies every new learner-linked store. Real homework and feedback wait for their own complete checks and separate launch authority. Native application tasks remain unfinished with no runtime results. Structural validation reports ten changes and expressly disclaims semantic/runtime/acceptance certification; the executor report also preserves that distinction.

## Reviewed input fingerprints

- `Product Decisions.md`: `d0b6b484a49aa9469bbd0d6aa839b9e40a1b26a2b8b77d3a1afc15241c3674f0`.
- `Architecture.md`: `6ac846e2c1b5a709a915f27c07ea6b042dd8b8883c7a2480010b8d05ddb03b0d`.
- `Implementation Plan.md`: `138c957d435a3f1196649f7da5e08e783e82ab2c63a68909ae54ca6e711692c9`.
- `Repository Structure.md`: `b571d7937d1b38f6ae42ca1497bfa896afc1786d22b94dc4c6862c6a68f584f2`.
- `README.md`: `1fd2429aababe9085baf448d4df22d02369427ba5a4d2d384656f3dfa04abf4e`.
- `specs/README.md`: `2cf786c4037ef3d977e438d1e97fc68a5d98051ef9c941af97bebf835bde7981`.
- `specs/datasets.md`: `53c9f503bb4dc276750de34120ab71e356cb313b63f23add7d9e835cf63b2fed`.
- `specs/changes/HG-0006/spec.json`: `d029ea28d2c4601d44acacf80a0c0b2630abacfb84e31578dd63a022072f2252`.
- `specs/changes/HG-0007/spec.json`: `e56c7b48cc8a864c1cb0a8e414365a3afb00250ccb68b0227a961f244d83e0f4`.
- `specs/changes/HG-0008/spec.json`: `d2872fe74c3beff4d0de54d21babafb56994be7ef6e19e07e793b21fba8fc75e`.
- `specs/changes/HG-0009/spec.json`: `11668a82637ee3b8ba8b729350a70dba7286067da1059c7d7dd2f3089c8919ed`.
- `specs/changes/HG-0010/spec.json`: `350657ecf22eb2b71582baa1c7fd962212269cce35604fc177f8b4aff3c57fef`.

## Limits

This is a semantic review of intended document/specification content. No transcript, learner record, external service, credential, installed application, provider call, Just recipe, approval transaction, checkpoint/Redis/deletion behavior, gold label or judge calibration was executed or certified. The original structural report is evidence of text/format observations only. This review writes only this original evidence file; no delivered source or native requirement was modified. A human decision, implementation, commit, publication and launch retain separate authority.

## Final wording recheck

Final verdict: **GO**, with no outstanding findings. The P3 wording finding above is resolved: specs/datasets.md now says “All datasets use a versioned JSON schema.” Its final SHA-256 is `53c9f503bb4dc276750de34120ab71e356cb313b63f23add7d9e835cf63b2fed`, superseding only that file's fingerprint in the original reviewed snapshot above. Reversing this single wording replacement reproduces the exact original dataset hash; no dataset requirement changed. Recomputed all twelve fingerprints from the updated draft-inputs.json; the other eleven remain unchanged and match. Original checks-v1.json remains historical evidence of the preceding snapshot; the parent will retain final structural observations separately. All scope observations and runtime limits above continue to apply.
