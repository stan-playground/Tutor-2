# E0 local checks

## Private learner-source access and feedback trend, 4 November 2026

`HW-LEARNER-ACCESS-01` is a critical draft with two synthetic tutors and learners.
The local authenticated intake test checks own source access, foreign learner
and foreign-source denials, and cross-source observation/activity write denial.
It verifies the evidence stays unchanged after denials, then writes the same
payloads with each owner's source as positive controls. The test requires 12
new captured request records during denied operations and checks actual
`metadata_line` values and captured standard streams for the synthetic canaries.
It does not establish external identity-provider login, production process
logging, provider/model/checkpoint privacy, feedback authorization or a full job.

`FB-03.trend-boundaries` is an ordinary draft checked only against the shared
fixed-clock metrics function: three comparable observations yield +0.15
attempted accuracy, -0.15 required use and a mixed group. Its transcript and
confirmed counts are synthetic input; transcript selection/authorization,
extraction, feedback generation and prohibited prose/writes are not exercised.

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Ruff format/lint, strict mypy and 90 unit tests passed; all current 33 draft cases passed schema validation. | [output](evidence/e0-private-trend-just-check-v3.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_intake.py::test_private_learner_fixture_denies_foreign_source_access` | One paired two-tutor local HTTP/PostgreSQL scenario passed, including denied cross-source writes, successful owned-source controls and captured denial-path metadata. | [output](evidence/e0-learner-access-boundary-v3.log) |

The [v1 test](evidence/e0-learner-access-boundary-v1.log) falsely treated a
misspelled activity endpoint's route-level 404 as authorization denial. An
independent review requested positive controls and denial-specific logging; the
[v2 run](evidence/e0-learner-access-boundary-v2.log) exposed the endpoint typo.
The corrected v3 uses `/activities`. [Selected input hashes](evidence/e0-private-trend-input-sha256-v3.txt)
are not a full experiment manifest; service configuration, migrations and
helpers also affect results. See the [independent review](evidence/e0-private-trend-independent-review.md)
for the scoped verdict. Neither draft has tutor approval.

## Domain fallback and zero-opportunity feedback drafts, 4 November 2026

The ordinary `HW-DOMAIN-01` is one paired isolated search case, not two
certified items. Two independently supplied requests use the same corpus: a
required `project_updates` domain produces a gap, while an optional domain
returns the suitable general-domain item. This does not exercise the required
healthcare-domain HW-06 situation, clarification or tutor consent to relax a
constraint. Synthetic material review and rights flags are test setup.

The ordinary `FB-02.zero-opportunities` is a synthetic extraction draft with a
speaker-attributed transcript, an optional prompt and learner silence. Its
proposed zero opportunities and unknown rates are **unexecuted labels**: the
feedback extraction runtime does not exist. No tutor approval is claimed.

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Ruff format/lint, strict mypy and 89 unit tests passed; all current 31 draft fixtures passed schema validation. | [output](evidence/e0-domain-feedback-just-check-v1.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_retrieval.py::test_domain_fixture_distinguishes_required_from_optional` | One paired local HTTP/PostgreSQL/pgvector search scenario passed with the two independent inputs and expected outcomes. | [output](evidence/e0-domain-boundary-v1.log) |

[Selected input hashes](evidence/e0-domain-feedback-input-sha256-v1.txt) identify
case files, test files, schema, selected implementation modules and lockfile;
other service configuration, migrations, helpers and model files also affect
the result. This is not a frozen experiment manifest. The
[independent technical review](evidence/e0-domain-feedback-independent-review.md)
gave GO for these scoped drafts and the search test, not for tutor review or E0
completion.

## Assignment and encounter variants, 4 November 2026

Two new ordinary draft cases isolate tutor-confirmed assignment and reading
encounter. Their synthetic source and activity records are supplied directly;
approval/copy and confirmation timestamps are authored facts, not observed
workflow actions. No generation, review, export, model claims or complete job
is exercised. The activity record is not bound to an exact source revision;
the provenance repair remains separate Stage 2R work.

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Ruff format/lint, strict mypy and 89 unit tests passed; all current 29 draft case files passed schema validation. | [output](evidence/e0-activity-just-check-v3.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_intake.py::test_activity_fixture_preserves_recent_performance` | Both cases passed through authenticated local HTTP/PostgreSQL intake and context. One existing observation remains unchanged while exactly one assignment or encounter appears in history; a fixed-clock call confirms the original 4/5 rate. | [output](evidence/e0-activity-boundaries-v3.log) |

The context endpoint uses its database clock, so the test compares its observed
recent source IDs and groups before and after each write. It separately uses
the fixture clock for the direct calculation; the endpoint clock is not frozen.
Neither the expected unknown exposure classification nor prohibited prose claims
are computed by the tested endpoint. [Input hashes](evidence/e0-activity-input-sha256-v3.txt)
identify selected case files, tests, schema, implementation and dependency lock;
configuration, migrations and helpers also affect the integration result. This
is not a frozen experiment manifest. The [first passing run](evidence/e0-activity-boundaries-v1.log)
preceded addition of authored confirmation timestamps. An independent review
of the [v2 run](evidence/e0-activity-boundaries-v2.log) found that the assignment
source's `actual_use` kind was misleading when exposure was unknown. The fixture
was corrected to tutor lesson notes and the current v3 checks were rerun. The
[final independent review](evidence/e0-activity-independent-review.md) gave GO
for the corrected drafts and scoped test, not for tutor review or E0 completion.

## Listening variants, 4 November 2026

Two new unreviewed critical retrieval-stage drafts exercise the mandatory
`HW-02.listening-unavailable` and `HW-02.listening-key-mismatch` variants.
Their recording references are synthetic identifiers: no recording or answer
key audio was supplied or inspected. The tests exercise declared availability
and criteria-version metadata, not the semantic correctness of a recording,
the full homework job, or qualified review. The materials' `reviewed` flags
are test setup, not evidence of human review. The prohibited inference of
listening ability is a draft expectation, not independently observed by this
retrieval-only test. The alternate's eligibility is based on declared metadata,
not an inspection of a real recording or its rights.

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Ruff format/lint, strict mypy and 89 unit tests passed; the current 27 fixture files passed schema validation. | [output](evidence/e0-listening-just-check-v1.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_retrieval.py::test_listening_gap_fixture_against_http_boundary` | Two parameterized cases passed through authenticated local HTTP import and search using PostgreSQL/pgvector and a local embedding model. Each excludes its ineligible asset while returning a matching alternative; after a new revision marks the alternative's recording unavailable, search returns an explicit gap. | [output](evidence/e0-listening-boundaries-v2.log) |

The [first attempt](evidence/e0-listening-boundaries-v1.log) executed neither
case: the sandbox denied loopback access to the test PostgreSQL service. The
successful repeat used local loopback access. [Input hashes](evidence/e0-listening-input-sha256-v1.txt)
identify selected changed cases, tests, schema, implementation and lockfile;
other service configuration, migrations, helpers and model files also affect
these observations. This is not a frozen experiment manifest. The
[independent technical review](evidence/e0-listening-independent-review.md)
gave GO for this scoped draft and test, not for qualified review or E0 completion.

## Additional privacy drafts, 4 November 2026

Two unreviewed cases extend the earlier 23-case set: a real two-tutor private
teaching-asset search and a static feedback permission stop. They are in
separate `Batch 3` tabs in the reviewer workbooks. Against the working tree based on HEAD
`8a29aa98384321f37bf6bdf70a56c7903367b07a`:

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Ruff format/lint, strict mypy and 89 unit tests passed. The 25 draft case files were schema checked; the permission-stop consistency test is not feedback-runtime evidence. | [output](evidence/e0-just-check-v10.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_intake.py::test_correction_fixture_at_persistence_and_fixed_clock_boundaries tests/integration/test_retrieval.py::test_retrieval_fixture_against_http_boundary tests/integration/test_retrieval.py::test_outage_fixture_is_failure_not_content_gap tests/integration/test_retrieval.py::test_private_search_fixture_is_scoped_by_authenticated_tutor tests/integration/test_retrieval.py::test_contrast_fixture_reports_unsupported_positive_form_target` | Five isolated HTTP/PostgreSQL and local embedding checks passed, including authenticated private-asset isolation, forged-scope rejection before query embedding, and the earlier correction, outage and search cases. | [output](evidence/e0-boundaries-v10.log) |

[Input hashes](evidence/e0-input-sha256-v10.txt) identify the case files, schema,
changed tests, shared metrics and dependency lock for these observations. Other
application code, service configuration, migrations, helpers and model files
also contribute. The private-search case verifies teaching-asset isolation,
query text and captured in-process INFO metadata during import and search only; it does not verify production console emission or an external identity-provider login. An [initial log-coverage check](evidence/e0-private-log-initial-fail.log) failed because no INFO metadata was captured. The final test enables INFO, asserts request and retrieval metadata exist, and examines their actual metadata fields. An [intermediate format check](evidence/e0-just-check-v9.log) failed before the affected files were formatted. The [earlier v7 run](evidence/e0-boundaries-v7.log) preceded the stronger assertion. The two material passages contain
synthetic canaries during import; it does not observe learner-evidence, model,
checkpoint or complete-job boundaries. The feedback permission case is an
unreviewed static draft and does not establish an authorization/resume runtime.


## Second draft batch, 4 November 2026

The second batch adds four unreviewed cases to the first 19-case snapshot. It
is in separate `Batch 2` tabs in the reviewer workbooks. Against the working
tree based on HEAD `8a29aa98384321f37bf6bdf70a56c7903367b07a`:

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Ruff format/lint, strict mypy and 88 unit tests passed; all 23 case JSON items were schema checked. Two checks verify internal consistency of the missing/expired feedback-source drafts, not a feedback runtime. | [output](evidence/e0-just-check-v6.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_intake.py::test_correction_fixture_at_persistence_and_fixed_clock_boundaries tests/integration/test_retrieval.py::test_outage_fixture_is_failure_not_content_gap` | Two synthetic HTTP/PostgreSQL checks passed. The correction check observes replay, duplicate rejection and revision history, then calculates rates from returned current evidence at the fixture clock. The outage check observes a healthy candidate and a query-embedding failure returning HTTP 503, not a content gap. | [output](evidence/e0-correction-outage-v1.log) |

[Input hashes](evidence/e0-input-sha256-v6.txt) cover the fixture set, schema,
changed tests, shared metric calculation and lockfile. Other application and
service inputs are also causal to the HTTP checks. The correction fixture's
confirmation timestamps are authored facts and are not sent to or persisted by
the current API; the fixed-clock arithmetic is a direct function call after the
HTTP evidence read, not an observation of the `/context` database clock. The
feedback cases remain static drafts, and neither test proves a complete job or
qualified review. The first batch's v5 hashes remain its historical snapshot.


## Expanded draft cases, 3–4 November 2026

Against the working tree based on HEAD `8a29aa98384321f37bf6bdf70a56c7903367b07a`:

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Ruff format/lint and strict mypy passed; 86 unit tests passed, including schema validation of 19 draft items and 13 numeric/window/feedback calculation cases. | [output](evidence/e0-just-check-v5.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_retrieval.py::test_retrieval_fixture_against_http_boundary tests/integration/test_retrieval.py::test_contrast_fixture_reports_unsupported_positive_form_target` | Both local HTTP retrieval checks passed before the contrast fixture wording was clarified. | [output](evidence/e0-retrieval-fixtures-v3.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_retrieval.py::test_contrast_fixture_reports_unsupported_positive_form_target` | The corrected contrast case passed. The truthful positive-form-only target was rejected at import before search; its exclusion from an eligible corpus remains unobserved. | [output](evidence/e0-retrieval-contrast-v4.log) |

[Earlier input hashes](evidence/e0-input-sha256-v5.txt) identify the schema, fixture
bytes, changed tests, metrics and lockfile at this run. The existing application
source, test helpers, migrations, service configuration and model files also
contribute to integration outcomes; this list is not a frozen experiment
manifest. The earlier [v4 unit run](evidence/e0-just-check-v4.log) preceded a test change that permits future reviewed cases. The earlier [contrast test failure](evidence/e0-contrast-initial-fail.log)
resulted from expecting detailed HTTP validation text where the API returns a
generic message; the corrected test checks the public response and the model's
validation separately. Neither draft labels nor simulated review flags are human
approval. The feedback extraction case has no executable feedback boundary;
the FB-03 check exercises only shared numeric calculation.

## Earlier initial increment

Run on 3 November 2026 against the working tree based on Git HEAD
`8a29aa98384321f37bf6bdf70a56c7903367b07a`, with uncommitted E0 files; HEAD
alone does not identify the checked result. Python 3.12.5, locked uv dependencies,
pytest 9.2.0 and local synthetic services were used. No live model provider or
production learner data was used. These checks are not tutor approval.

| Command | Observation | Original report |
| --- | --- | --- |
| `just check` | Earlier Ruff format/lint, strict mypy and 73 unit tests passed, including structural validation of all four items and the recent-performance sample. | [final output](evidence/e0-just-check-v2.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_intake.py tests/integration/test_retrieval.py` | 25 existing scenarios passed with loopback access to isolated synthetic databases and Redis. This run preceded addition of the new retrieval test; its existing tests and application inputs were unchanged. | [output](evidence/e0-integration.log) |
| `UV_CACHE_DIR=.uv-cache uv run --locked pytest -q --tb=short tests/integration/test_retrieval.py::test_retrieval_fixture_against_http_boundary` | One new case passed using HTTP, PostgreSQL/pgvector, Redis and the locally installed embedding model. | [output](evidence/e0-retrieval-fixture-v2.log) |

The first integration attempt in the restricted sandbox ran no scenarios:
25 setups failed because the local PostgreSQL connection was denied with
`Operation not permitted`. Its [original output](evidence/e0-integration-attempt.log)
is retained. The successful run used local loopback access. An earlier
[unit-check run](evidence/e0-just-check.log) and the earlier [fixture run](evidence/e0-retrieval-fixture.log) preceded independent-review corrections. The [intermediate unit run](evidence/e0-just-check-final.log) also predates those corrections.

For the numeric sample, the test passes only the input's observation, sources
and clock to `summarize_recent`, and compares the returned source and
observation IDs, all three counts/rates, group trend and maintenance flags with
its draft expectation. It does not check prose claims, authorization, tutor
confirmation, persistence or extraction. This function assumes already
validated, authorized current observations.

For the retrieval sample, the test imports only the two synthetic assets in
the input into the test tutor's private bank, then sends the input objective to
`POST /teaching-search`. It asserts the expected candidate and exclusion of the
distractor. The fixture's `reviewed` and rights fields are test setup, not
proof of an independent pedagogical or rights review. The acting tutor and private ownership are declared in the input; the test
checks the authenticated tutor and the returned reviewer identity. The test is not a full
homework preparation, and it does not establish the other required retrieval
items, search-provider payloads in future model stages or release coverage.

Historical input hashes for the initial increment (the test files have since changed):

```text
620e366fa6446ebba4c2d9746c8b58f917bb4973cb093421e8e4c881df76ba6d  evaluation/item.schema.json
03a41050f1fe92abf703ced7ba4c282c6ef56db9830193b2f830b140136ba548  evaluation/homework/HW-RECENT-01.json
333650584c79e3549da408482b0ddee1dc8cbd5298eb2bd56a2f091c61a9941b  evaluation/homework/HW-RETRIEVAL-01.json
b4f155c73d0b869d743442fc896a7102e4c0943613b0e79553f82e114cd88924  tests/unit/test_fixtures.py
c0b320ec711cd69414c37668ee782f7b4829bfb8993ca99e851e1e8c4f21b87c  tests/integration/test_retrieval.py
3c769cac70a4784f6c02128cf75133dd07b89eba384701d707002fb7b925c825  src/tutor_copilot/metrics.py
5be9dac46eb64d811cbf147d0a51e2aa74d48eed1d71bfc5e21df62114029865  uv.lock
```

The source tree, migrations, test helpers, schema, model files, service image
digests and configuration are also causal to the integration tests; the list
above is not a complete frozen experiment manifest. The test report is a local
observation, not a release decision or acceptance.
