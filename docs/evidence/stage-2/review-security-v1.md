# Stage 2 independent security and architecture review

**Verdict: GO for the implemented local Stage 2 slice. Review complete.**

Reviewed on 2 November 2026 against HG-0004 S1–S6, Product Decisions PD-13/14/15/16/28/33/40, Architecture section 6 and its Redis policy. This verdict covers teaching-bank persistence/publication, controlled search, local embeddings, authorization, eligibility, failure handling and query-vector caching. It does not certify formal HG-0004 integration or later preparation/export behavior.

Examined the complete relevant implementation and changes in `materials.py`, `retrieval.py`, `embeddings.py`, `bank.py`, migration `0004`, `runtime.py`, `web.py`, dependency/configuration changes and the corresponding tests. The implementation preserves the required boundaries:

- Authenticated server context owns tutor identity; tutor imports remain private and tutors cannot publish or modify shared material.
- Database RLS applies before candidate ranking. The latest version is selected before eligibility, preventing withdrawal from reviving an older eligible version.
- Rights, review, availability, purpose/outcome, kind, skill/confusion, level, task, modality, support, prerequisites, duration and required-domain constraints precede ranking.
- Listening eligibility requires an available permitted recording reference and matching recording/criteria version.
- Controlled query descriptions exclude private source text and objective/evidence references. Redis contains only versioned generic query vectors; current database authorization is rechecked on cache hits.
- Provider/database failures remain failures rather than content gaps. Runtime inference is offline, bounded and serialized; cancellation retains capacity until inference actually finishes.

Previously identified cache edge cases are resolved: integer overflow, float32-unsafe norms, malformed UTF-8 and recursive JSON are rejected or treated as cache misses. The material-kind filter, request/retrieval correlation ID and maintenance database timeouts are also present. No blocking security or architecture finding remains.

Inspected original reports:

- `docs/evidence/stage-2/check-v2.txt`: Ruff formatting/lint and strict mypy passed; **71 unit tests passed**.
- `docs/evidence/stage-2/integration-v2.txt` and `.xml`: **45 integration tests passed**, with **zero failures, errors or skips**.
- `docs/evidence/stage-2/input-snapshot-v2.json` and `model-manifest-v1.json`: independently recomputed all declared implementation/test/configuration and model-file hashes; **no changed inputs**.

The integration observations exercise actual local FastEmbed inference, HTTP, PostgreSQL/pgvector, Redis, ownership revocation, latest-version withdrawal, corrupted cache values and real database failure. Inspection of the assertions supports the claimed synthetic boundaries; this is not an inference from exit codes alone.

Limits: qualified-reviewer, recording availability and rights are explicit operator/reviewer assertions, not independently established teaching-quality or legal conclusions. Sharing permission is retained at material-identity level; this implementation does not provide a per-version sharing-authorization audit. Production identity/processor terms, real-learner activation, pedagogical quality, generation and student export remain outside this review. HG-0004’s formal integration remains pending the declared HG-0003 dependency; this GO does not close that future approval/copy scenario or record human acceptance.
