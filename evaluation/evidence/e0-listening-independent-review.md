# Independent review: listening retrieval drafts

4 November 2026. Independent reviewer: `boundary_check` subagent. Verdict: **GO**
for the two retrieval-only draft fixtures and their parametrized local HTTP test;
this is not qualified-tutor approval, complete-job coverage or E0 completion.

The reviewer compared the required unavailable and recording/criteria-version
mismatch variants in `specs/datasets.md` with both draft JSON files,
`test_listening_gap_fixture_against_http_boundary`, the original sandbox-denied
setup report, the passing integration report and the `just check` report. The
review found no blocking code issue. Each test imports both assets, checks the
specific defect, returns the synthetic metadata-eligible alternative, revises it
through HTTP and observes an empty gap response. The sandbox failure preceded
execution; the repeated test passed both cases. The
[hashed input list](e0-listening-input-sha256-v1.txt) identifies selected
inputs; it is not a complete experiment snapshot.

Limits: no recording was supplied or heard, no content/key semantic match or
actual rights were checked, and the material review flags are synthetic test
setup. The prohibited inference of listening ability is not independently
exercised at this retrieval boundary. Qualified review and full-stage/job cases
remain outstanding.

A separate read-only independent Batch 4 workbook check returned **GO** for the
handoff snapshot. In both workbooks the reviewer checked the separate reviewer
identity, case IDs, revisions, local hashes, full original JSON and keyless
exercises, including prior-label-exposure and no-audio warnings. The reviewer
did not read decision/comment columns or inspect every flattened field. This
does not establish current sharing, completed tutor review, actual audio or
content/rights review.
