# Independent coverage review

Reviewer: `/root/final_coverage`, 2 November 2026. Original verdict follows.

**GO — Stage 2’s implemented local slice is complete.** This verdict covers the application code, tests and current evidence. Formal HG-0004 integration remains pending its HG-0003 dependency; this review does not clear that separate requirement.

I independently checked the HG-0004 scenarios against the actual implementation and assertions:

- S1/S3: exact confusion, level/task/modality/response/material kind and hard versus preferred domain; source/version provenance; controlled descriptions and invalid-field rejection before embedding.
- S2/S3: private and shared ownership, no-context RLS, forbidden shared writes, review/rights/availability restrictions, latest-version withdrawal and separate operator publication permission/review.
- S4: provider faults and invalid vectors, actual database-table unavailability, and successful empty-bank gaps remain distinguishable.
- S5: all seven goal-led routes execute without an invented confusion, with prerequisite/support/duration constraints.
- S6: unavailable, unpermitted, missing and version-mismatched listening references are excluded.
- Cache behavior: actual query-vector hits preserve current authorization and version checks; TTL, bypass, Redis refusal and malformed JSON/dimensions/nonfinite/zero/huge/tiny/invalid-UTF-8 values are covered. The additional nested-JSON `RecursionError` finding is fixed and included in the corruption regression.

Current original evidence:

- `docs/evidence/stage-2/check-v2.txt`: Ruff formatting/lint and strict mypy passed; **71 unit tests passed**.
- `docs/evidence/stage-2/integration-v2.xml` and `.txt`: **45 integration tests passed in 23.49 seconds**, with **zero failures, errors or skips**. These include 14 retrieval cases and three material cases.
- I independently reran `tests/unit/test_retrieval.py`: **45 passed**.
- I recomputed every hash in `input-snapshot-v2.json` and all five model-file hashes in `model-manifest-v1.json`; **no declared input or model-file changes** were found.

No blocking implementation or coverage findings remain. Before recording the review, update `docs/stage-2.md` to link its final check/integration/input evidence to **v2**; its current v1 links identify the earlier revision.

The tests establish synthetic HTTP/PostgreSQL/pgvector/Redis and local-inference boundaries. They do not establish qualified pedagogical review, approved gold quality, production suitability or real-learner activation. The operator’s qualification/permission fields are explicit assertions, and listening availability/version correspondence is metadata checked by the application rather than independent media assessment.
