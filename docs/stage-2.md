# Stage 2 — reviewed teaching bank and retrieval

Implemented under the owner's 2 November 2026 request. Requirements remain in
[HG-0004](../specs/changes/HG-0004/spec.json); this record explains the local
implementation, commands, verification and remaining delivery limits.

## Completed blocks

1. Material versions and private import: validated rights, teaching metadata,
   content/instructions/key relationships, review provenance, immutable version
   selection, two-tutor ownership, revision conflicts, deletion and CSRF.
2. Controlled search and real embeddings: application-built descriptions,
   a pinned local model, authorized exact pgvector ranking, route/kind/task/level/
   confusion/support/prerequisite/duration filters, provenance and explicit gaps.
3. Audio material and shared publication: every audio modality requires a
   recording; retrieval enforces recording-version/criteria correspondence and
   availability/permission. An operator-only shared-bank command requires
   separate sharing permission and qualified-reviewer assertions.
4. Disposable query-vector caching: current database authorization on every
   search, 24-hour TTL, versioned keys, corrupt-value repair and bounded Redis
   bypass. Provider/database failures remain HTTP 503 failures.

These blocks complete the local Stage 2 slice. HG-0004 is not formally integrated:
its dependency HG-0003 still has the future approval/copy side of S5 to observe.
All current native checks pass. The [current native status](evidence/stage-2/HG-0004-status-v3.json)
records independent review GO and only `DependencyNotIntegrated` as the formal
delivery barrier.
This does not claim that either complete native specification, pilot readiness,
teaching quality or real-data activation has passed. Stage 3 still owns objective
selection, generation, checked adaptation and persistence with a preparation.

## Design and trade-offs

The implementation is ordinary functions and Pydantic models in
[materials.py](../src/tutor_copilot/materials.py),
[retrieval.py](../src/tutor_copilot/retrieval.py),
[embeddings.py](../src/tutor_copilot/embeddings.py) and
[bank.py](../src/tutor_copilot/bank.py). There is no additional retrieval framework,
vector service, model-directed search loop or chat-model query rewriting.
Metadata matching establishes suitability constraints; exact pgvector cosine
distance ranks only eligible rows. A preferred domain can fall back visibly via
`domain_match: false`; a required domain is never relaxed. `kinds` lets a caller
search for explanations separately from activities, input or frameworks.

Migration `0004` separates permanent material ownership from its versions, and
migration `0005` makes the version rows append-only for the restricted runtime
role. Tutors can create only private identities; shared publication uses the
existing local maintenance account. RLS checks ownership for every version. The
query selects the latest version before testing eligibility, so withdrawing
review or availability cannot resurrect an older eligible version. Material
deletion cascades through versions and their vectors. The separate sharing
permission is recorded at the material ownership identity; reviewer, source and
rights are versioned. The command does not provide a per-version
sharing-authorization audit. No learner ID/source pointer is accepted in a
material, and learner sources never enter this table automatically.
Importers must attest that content is teaching material; this does not detect a
deliberately mislabeled transcript or establish the truth of a rights assertion.

The local synthetic embedding baseline is FastEmbed **0.7.4**, model
`BAAI/bge-small-en-v1.5`, 384 dimensions, using the pinned ONNX repository revision
`aa8f8b060edb00e03bfdd08813a2949946c8ba55`. Public model files are downloaded
explicitly by `just embeddings-prepare` with `token=False`. Runtime uses only that
local directory and disables ONNX telemetry. The model source and actual file
hashes are in the [model manifest](evidence/stage-2/model-manifest-v1.json).
FastEmbed avoids a remote processor/API key and the larger PyTorch dependency of
Sentence Transformers. It adds local CPU/memory use and an explicit model setup
step. This is a reproducible development choice, not a measured quality winner
or selection of production processor terms. Current Context7 documentation was
read for FastEmbed, pgvector, SQLAlchemy, Hugging Face Hub and Redis before their
new features were used.

Database and Redis waits use asyncio. One application-lifetime executor thread
serializes local inference, with a three-second capacity wait and a thirty-second
caller timeout. ONNX uses two internal CPU threads. Cancellation does not release
capacity while inference is still running. A process pool would duplicate a small
model and add lifecycle/serialization work without measured benefit. Material
embedding happens before opening the write transaction; search embedding happens
before its short read transaction. The shared maintenance command also bounds
database connection and statement waits.

All query text comes from controlled teaching values: route/outcome/skills,
optional exact confusion, level/task/modality/response/domain, kinds, prerequisites,
support and duration. Objective/evidence UUIDs are retained as references outside
that description. Free text, tutor scope, private summaries and unknown fields
are rejected before embedding. The vocabulary is deliberately small: unsupported
teaching distinctions require an explicit schema/vocabulary extension, rather
than being silently reinterpreted. Reviewed asset passages include their permitted
content/instructions locally; answer keys are not embedded.

Redis stores only a vector under
`qemb:{configuration_revision}:{sha256(exact_controlled_description)}`. No query
text, tutor/learner IDs, asset passages or candidate lists enter the cache. The
revision includes model commit, FastEmbed/settings and description format. Read
and write each have a 250 ms timeout, with zero client retries. Malformed JSON,
wrong dimensions, invalid UTF-8, nonfinite values and float32-unsafe norms are
misses. Cache errors bypass Redis; they cannot turn an embedding/database error
into a content gap. Current PostgreSQL ownership, latest versions, rights,
review and recording correspondence are checked even on a cache hit.

Audio recording references are reviewer assertions, not URLs fetched by the server.
The system verifies that an available permitted reference has the same recording
version as its reviewed criteria. It does not independently listen to media,
verify a third party's uptime, assess learner audio or infer listening ability
from a transcript/assignment. Teaching material supplied in tests is synthetic;
test reviewer assertions are not qualified pedagogical review or approved gold.

## HTTP and maintenance operations

| Operation | Input → output |
| --- | --- |
| `POST /teaching-assets` | Stable UUID, expected revision and reviewed/unreviewed material → private material UUID/version; reviewed available material is embedded before save. |
| `GET /teaching-assets/{id}` | Authorized identity → latest version, content, criteria, rights/source and reviewer reference. Shared items are readable, not tutor-editable. |
| `DELETE /teaching-assets/{id}` | Private owned identity → immediate deletion of identity, versions and vectors. |
| `POST /teaching-search` | Controlled `Objective` → `candidates`, explicit `gap`, or HTTP 503 `failed`; no learner/history writes. |
| `tutor-bank-publish FILE` | Explicit operator publication JSON → shared UUID/version; requires `reviewer_ref`, `reviewer_qualification: qualified_english_tutor` and separate `sharing_permission_ref`. |

All HTTP operations require the existing invited session. Unsafe methods require
CSRF. Invalid fields return sanitized 422, identity/revision conflicts 409,
unavailable/foreign writes 404 and embedding/search failure 503. Existing no-store
responses and sanitized unexpected 500 handling remain. Retrieval observations
contain only correlation ID, outcome, candidate count, cache state, calls avoided
and elapsed time, joined to the HTTP response's `X-Correlation-ID`.

## Methods and lifetimes

| Method | Purpose, inputs, output and caller | Separation, errors and lifetime |
| --- | --- | --- |
| `TeachingTarget.valid_route()` | Intake/search validation checks route/outcome, skill, exact remediation confusion and reading/listening modality; returns the validated target. | Shared contract for material and objective; rejects incompatible fields before I/O. Per input. |
| `Material.complete_material()` | Import validation requires a closed-answer key and a recording reference for every audio modality; returns material. | Content relationships are checked before storage/embedding. Does not certify answer quality; per import. |
| `describe_target(target)` | Import/search supplies controlled metadata; returns the shared teaching description. | One pure format shared by passage/query construction; no reference/private fields. Per operation. |
| `save_material(connection, tutor, data, vector, reviewer_ref, sharing_permission_ref)` | HTTP import or operator publication supplies a short transaction, identity/revision and optional vector; returns UUID/revision. | Serializes the identity with a PostgreSQL advisory lock, preserves ownership, rejects stale versions and supports replay. Database errors roll back; shared writes need separate permission/review. Transaction/data are operation-local. |
| `import_material(data, request, tutor)` | HTTP POST validates material, embeds an eligible passage, opens the tenant transaction and calls `save_material`. | Server session owns tutor identity. Provider failures return 503 and save nothing. Request-local data, application-lifetime resources. |
| `get_material(identity, tx)` / `delete_material(identity, tx)` | HTTP GET/DELETE reads latest authorized material or deletes a private owned identity. | Shared ownership/RLS is reused; absent/foreign writes are 404. One short transaction. |
| `validate_vector(value)` | Provider/cache supplies a value; returns 384 finite numeric floats. | Rejects wrong types/dimensions, zero/extreme norms and numeric overflow before PostgreSQL; per vector. |
| `LocalEmbeddings.__init__()` / `_encode(description, passage)` | Resource startup creates one bounded executor; first inference loads the pinned local model, then returns a validated query/passage vector. | No request download or remote model call. Missing files/model errors propagate to sanitized failures. Model/executor live for the application. |
| `LocalEmbeddings.embed()` / its `finished()` callback | HTTP/search/operator supplies description and query/passage mode; returns the executor result. | Bounds capacity and caller wait; callback releases capacity only after actual inference finishes, including cancelled callers. Future belongs to one operation. |
| `LocalEmbeddings.close()` | Resource shutdown/operator finally block waits for executor cleanup and releases model references. | Prevents leaked worker threads; application lifetime ends here. |
| `prepare()` | Explicit setup command downloads the pinned public file allowlist anonymously; prints only model/revision/dimensions/status. | Separate setup permits offline request handling. Download failure stops setup; short-lived CLI. |
| `build_search(objective)` | HTTP/future worker supplies a validated objective; returns controlled text without objective/evidence IDs. | Pure construction owns the privacy boundary; per search. |
| `query_vector(resources, description, use_cache)` | `retrieve()` requests a query vector; returns vector/cache status. | Enforces vector validation, TTL and disposable-cache behavior; provider failure propagates. Pools live for the application, key/vector for this search. |
| `retrieve(resources, tutor, objective)` | HTTP/future worker supplies authenticated scope and objective; returns eligible candidates/provenance, gap or failed outcome. | Owns current authorized exact database search. No metric calculation/history loading or writes; one invocation and short read transaction. |
| `search_materials(data, request, tutor)` | HTTP POST calls `retrieve`, records fixed metadata and returns JSON/200 or 503. | HTTP encoding/status/logging are separate from worker-callable retrieval. Request lifetime. |
| `SharedPublication.reviewed_material()` | Operator file validation requires reviewed material in addition to qualification/sharing fields; returns validated publication. | Qualified review/permission are explicit operator assertions, not web-controlled scope. Per publication. |
| `publish(data, settings)` / `bank.main()` | Explicit CLI reads one supplied publication file, embeds locally and saves using the fixed local maintenance account; prints UUID/revision. | Maintenance authority is unavailable from HTTP. Failures exit with a fixed message; imported text/exception details are not printed. One command, one short transaction, explicit resource cleanup. |

## Commands and verification

Commands used while implementing the coherent blocks:

```bash
UV_CACHE_DIR=.uv-cache uv add 'fastembed>=0.7,<0.8'
UV_CACHE_DIR=.uv-cache uv run --locked tutor-embeddings-prepare
UV_CACHE_DIR=.uv-cache uv run --locked ruff format src migrations tests
UV_CACHE_DIR=.uv-cache uv run --locked ruff check src migrations tests
UV_CACHE_DIR=.uv-cache uv run --locked mypy
UV_CACHE_DIR=.uv-cache uv run --locked pytest tests/unit -q
UV_CACHE_DIR=.uv-cache uv run --locked pytest tests/integration/test_materials.py tests/integration/test_foundation.py -q --tb=short
UV_CACHE_DIR=.uv-cache uv run --locked pytest tests/integration/test_retrieval.py tests/integration/test_materials.py -q --tb=short
just check
just integration
just migrate
```

See the current [check report](evidence/stage-2/check-v3.txt),
[integration report](evidence/stage-2/integration-v3.xml) and
[integration console report](evidence/stage-2/integration-v3.txt), plus the
current [independent review](evidence/stage-2/review-repair-v1.md). The earlier
[security review](evidence/stage-2/review-security-v1.md) and
[coverage review](evidence/stage-2/review-coverage-v1.md) describe the original
slice; they are not the independent verdict for this repair. The tests use
isolated random databases and exact temporary Redis keys; they do not delete the
application database or flush Redis. Public weights are recoverable through the
pinned setup command and remain ignored rather than being committed.

Checks cover all six HG-0004 scenarios, every enabled non-error route, exact
confusion/kind/task/level/domain constraints, two-tutor/shared RLS, append-only
version privileges, review/rights/availability, audio recording defects on
listening and non-listening routes, private canaries, latest-version withdrawal,
cache corruption/outage/revocation, actual provider inference and real database
failure. The final full suite passed 72 unit and 45 integration tests, with no
skips. Ruff formatting/lint and strict mypy passed. Current native check inputs
were compared after execution. Future generation, student export,
teaching-quality evaluation, production hosting/processors and real-learner
activation remain outside these observations.
