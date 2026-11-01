# Independent dataset-specification privacy review

Verdict: **GO for specification text only**. No blocking findings or required privacy/data-boundary corrections.

Reviewed under the active HighGrade independent-review method. This review covers specs/datasets.md and HG-0008's proposed requirements/scenarios, using Product Decisions PD-28/33/34 and Architecture privacy, graph-history and Redis rules as the governing sources. It does not approve runtime behavior, dataset admission, a pilot or live-data use.

## Input identity

All five hashes in draft-inputs.json were independently recomputed and matched the current files:

- `specs/datasets.md`: `90805e46e135dbdea0b254222b4e7cc4d10daa184e997c9ba4da62eb4c76cf6d`.
- `specs/README.md`: `5ff8e70d7c29178d7bd81962839502792f8ab774b47066b8f78f14453ae25203`.
- `specs/changes/HG-0008/spec.json`: `70f2ecb5746062a368a2dcd666ee27da7808f13ae24b38ba187e9aa13686f4f9`.
- `Product Decisions.md`: `dda62c0835e507fa48b59197090ae86888e48e05b11cccca2952ec18a7db9164`.
- `Architecture.md`: `ca54755bb6367f8132d222a9351b4d69dc6f83161e161e8c5e9220367c215e80`.

The input snapshot itself was read as a fingerprint report; it does not demonstrate execution of any proposed scenario.

## Priority findings

None. In particular, the specification does not authorize production traces as fixtures merely because a model or tutor approved an output, does not use archiving as a substitute for deletion, and does not expose gold verdicts as model inputs.

## Confirmed contract boundaries

- **Synthetic versus production data:** datasets.md:24–30 and :53–78 require initially synthetic learner/evidence identities and responses, fixtures that resolve without live production dependencies, rights-permitted teaching material and no fixture credentials. Native HG-0008-R2/R3/R4 and S4/S11 reflect those limits. The harness establishes synthetic authorization; source text cannot create a real identity or grant access.
- **Permission and anonymization:** datasets.md:74–78, :101 and HG-0008-R4/S11 distinguish ordinary processing permission from separately permitted production-case reuse, require reviewed anonymization and reject alias substitution as sufficient. Raw private transcripts, real learner keys and identifying/contact information are excluded from shared fixtures; synthetic privacy/key canaries remain usable. A live trace or homework approval never supplies gold-admission authority.
- **Withheld labels, keys and human verdicts:** datasets.md:24–30 and :97–99 separate task input, expected output and reviewer metadata. The task receives input only; the independent solver does not receive the proposed key; the semantic judge receives legitimate context/rubric but not the human verdict or measurement rationale. Native R2/S5 explicitly require observation at each provider boundary, including nested metadata. A reviewed source key can support adaptation without becoming the proposed-key input to independent solving.
- **Review eligibility:** datasets.md:74, HG-0008-R4 and S10 approve exact item revisions, not entire families by implication. Every label needs a qualified tutor review, all critical items need second review and the ordinary second-review count rounds up. Unresolved disagreements and unreviewed stage/variant labels cannot enter an approved release suite. Model labels remain drafts. Reviewer identities/qualifications belong in controlled review records, outside task payloads.
- **Reproducibility versus erasure:** datasets.md:78–91 and HG-0008-R4/S12 explicitly make privacy override freezing, archiving and historical replay. Required removal includes historical dataset versions, exports, local copies and trace links; affected manifests retire rather than silently reconstructing deleted data. Admission of production-derived items is barred if the selected deployment cannot enforce removal. The thirty-day source/excerpt, seven-day active/derived deletion and thirty-day backup policies remain tied to PD-28 rather than being replaced by indefinite experiment retention.
- **Safe fixtures and actual boundaries:** HW-07/08/09/10 exercise eligibility, authorization, key separation and instruction-like transcripts with synthetic canaries. Own evidence is allowed only in its legitimate context; foreign/private content cannot leak through prompts, logs, checkpoints, Redis or shared material. datasets.md:70 and native S5/S12 require real provider/storage/cache/deletion observations before behavioral claims; an LLM verdict or document check cannot prove isolation or erasure.
- **Scope and honest status:** The document says no items, gold approvals, experiments or measured results have been produced. HG-0008 tasks remain unfinished and its checks list is empty. Verification strings describe future observations, not executed PASS evidence. The current change prepares construction/acceptance contracts without granting live-service or deployment authority.

## Limits

No actual fixtures, qualified-review records, permission evidence, provider payloads, Langfuse deployment, historic-item deletion, local export, checkpoint, Redis entry, backup or replay execution was inspected. No secrets or live services were accessed. This review confirms that the written requirements preserve the selected privacy and data boundaries; actual anonymization, rights, review qualifications, filtering and removal must be verified when datasets are constructed. Evaluation arithmetic/pedagogical labeling beyond these boundaries belongs to the separate specialist review. No runtime GO, human acceptance or native mutation is recorded.
