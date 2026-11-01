# Independent architecture review: minimal Redis cache

Verdict: **GO** for this Architecture.md update. No blocking findings.

Reviewed on 1 November 2026 under the active HighGrade independent review method. Scope is the requested initial architecture recommendation, not implementation, runtime certification or a new comprehensive cache specification.

## Reviewed inputs

Read the complete current architecture, relevant unchanged product privacy/access/approval contracts, preserved before-document, full diff and original checks-v1.json. Recomputed fingerprints match that report:

- Current Architecture.md: `ca54755bb6367f8132d222a9351b4d69dc6f83161e161e8c5e9220367c215e80`.
- Before-document: `10f1d80a6e3a95d8a9653c90ab18d1ac1a209fec5a7a8ca29f1026ed7be453dd`.
- Product Decisions.md: `dda62c0835e507fa48b59197090ae86888e48e05b11cccca2952ec18a7db9164`.
- Original checks-v1.json: `580a485952bcf36bc1ba429ba39d133f04c094be42644d312fd185c3c312dbde`.

## Findings and observations

- **Minimality and benefit:** The change selects one disposable cache: exact query vectors for repeated generic teaching searches. It explains the process-local alternative and Redis operational cost, and explicitly treats saved embedding calls as a plausible benefit to measure. It makes no demonstrated performance or correctness necessity claim.
- **Privacy eligibility before keys:** Inputs must be assembled from controlled non-sensitive vocabulary. Free-text tutor input, private assets, learner source text and free-form summaries bypass caching. Eligibility precedes hashing; the text does not portray SHA-256 as anonymizing private content. No raw query, tutor/learner identity or query hash is logged. Sentinel verification and immediate purge/fix after accidental caching are explicit future safeguards.
- **Correctness and invalidation:** The key uses exact embedding input plus a configuration revision identifying provider/model version, settings and query format. Changes use a new revision, while old values expire. Malformed vectors/wrong dimensions are misses. The cache contains no retrieved lists, so current authorization, review, license and content checks remain PostgreSQL reads on every request. Asset embeddings remain in pgvector.
- **Failure behavior:** Reads/writes are best effort with short timeouts and no request-path Redis retries; loss does not remove application state. Misses/outages compute normally through the provider, while provider failure remains an explicit preparation failure. Duplicate concurrent embedding calls are accepted rather than adding locks or a second coordination system.
- **Lifecycle and operations:** The client/pool is bounded and process-lived with explicit shutdown. Twenty-four-hour expiry is a selected initial policy, not a product retention rule. Cache-only deployment has a memory bound, allkeys-lru and no snapshot/AOF/backups. Redis does not become queue, session, checkpoint or approval storage.
- **Integration consistency:** The opening, storage table, retrieval-stage contract, privacy section, future check list, selected diagram and final summary agree on the same single cache. LangGraph execution and PostgreSQL authority for facts, decisions and exact approved export remain intact. Product scope and native specifications were not expanded by this recommendation.

## Evidence and limits

The original report records successful whitespace and launcher syntax checks, local structure/link/JSON observations and unchanged product fingerprint. These establish documentation properties only. No Redis deployment, connection timeout, TTL, eviction, async-pool behavior, embedding compatibility, cache hit, authorization, sentinel exclusion or outage fallback was exercised. Official-source/API checking belongs to the parent study's source work; this independent review assesses the concrete design and its consistency. No application implementation, measured savings, compliance certification, human acceptance, commit or activation is claimed.
