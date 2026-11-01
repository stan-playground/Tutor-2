# Stage 1 independent contract review — revision 2

Reviewer: independent `final_contract_review` subagent. Reviewed on 2 November
2026 against base `a004bdd9e96ac9bde85b989ca1ed9c73bcef0583` and the current
uncommitted Stage 1 result. This report supersedes the readiness verdict in
[revision 1](review-contract-v1.md), which remains unchanged as review history.

## Verdict: GO for the implemented Stage 1 scope

The two implementation findings from revision 1 are resolved, and the refreshed
evidence matches the current executable inputs. No blocking contract or
maintainability finding remains within this delivery slice. This is not human
acceptance, commit authority, real-learner activation, or full integration of the
HG-0003/HG-0007 contracts.

## Targeted re-review and evidence

1. `intake.py` now declares `Depends(transaction, scope="function")`, and
   pyproject.toml requires FastAPI >=0.121. The installed framework and current
   official documentation establish that this closes the transaction dependency
   before sending the response. `test_commit_failure_never_returns_http_success`
   installs a real PostgreSQL deferred constraint trigger, causes COMMIT to fail,
   and asserts a sanitized HTTP 500, unchanged learner/profile row counts,
   `Cache-Control: no-store`, and no private exception text. Its executed passed
   case is present in the final JUnit report. This checks the actual storage and
   response boundary, rather than mocking commit failure.
2. `Activity.complete_reference` now requires an existing observation reference or
   a qualitative checked result with a criterion reference. The allowed qualitative
   outcomes include explicit `unknown`; other fact kinds cannot claim results.
   `test_qualitative_checked_outcomes_need_criteria_and_never_create_rates` rejects
   an unsupported check, persists fluency/project criterion results through the
   actual API/database, freezes them through purpose selection, preserves the
   unknown qualification, and obtains no recent performance groups. The existing
   numeric observation-reference path remains supported.
3. The current result also applies no-store responses, permits the owning tutor
   to delete an inactive learner without restoring read/write access, and checks
   every learner-linked table through the actual restricted database role. The
   final integration cases cover those additions.

I independently inspected the original machine evidence:

- [check-v2.txt](check-v2.txt): Ruff formatting/lint and strict mypy pass, with
  26 executed unit cases passed.
- [integration-v2.txt](integration-v2.txt) and
  [integration-v2.xml](integration-v2.xml): 28 executed real integration cases,
  zero failures, errors or skips. The commit-time and qualitative-outcome cases
  appear individually, along with permissions, all-table RLS, inactive deletion,
  actual OIDC login, corrections, expiry and deletion-race cases.
- [input-snapshot-v2.json](input-snapshot-v2.json): all 34 declared executable,
  test, dependency, migration, configuration and non-secret fixture hashes match
  the current files. No generated credential file was opened.
- [native-import-v2.json](native-import-v2.json): twelve successful native check
  imports refer to that actual JUnit report. Each imported before/after causal
  file hash matches both its counterpart and the current file. These imports
  record execution evidence; they do not replace this semantic review.

The full barriers were not repeated by this reviewer: their current original
reports and exact input hashes were inspected directly. I changed no application
code, tests, specification, dependency, credential or owner-authored plan content.

## Stage 1 completion assessment

| Required outcome | Assessment |
| --- | --- |
| Login and two-tutor isolation | Actual Keycloak OIDC and PostgreSQL session evidence, authenticated endpoint denials, transaction-local restricted-role RLS checks. |
| Assessment/preferences/adult permission | Distinct validated profile fields and revisions; false permission flags and unrelated birth-date collection are rejected without a new learner row. |
| Lesson/homework intake and confirmation | Source versions and independent observation revisions; replay, duplicate identity, pending confirmation, corrections and audit reads are checked. |
| Recent measures and trends | Latest four lesson/four homework source selection precedes grouping; exact arithmetic, minimum samples, unknowns, separate task/assistance/completion and mixed trends have focused unit plus persisted integration checks. |
| Independent actual-use facts | Assignment, encounter, attempt and checked outcome are independently recorded. Encounter requires no answer or amount. Qualitative outcomes do not create performance rates. |
| Qualified cumulative/frozen context | Historical facts stay separate from recent denominators; selected revisions, purpose/subskill filtering, coverage, source-version availability and unchanged old contexts are checked. No inferred mastery, forgetting score or schedule is introduced. |
| Lifecycle for introduced stores | Expiry guards, physical current/history raw-body cleanup, calendar-month inactivity, immediate deletion and a real waiting-write deletion race are checked against PostgreSQL. |
| Architecture and implementation size | Existing FastAPI/Pydantic/SQLAlchemy/Authlib and bounded async I/O; direct operations with no speculative repository, memory, NLP or scheduling layer. |

## Scope and operational limits

- HG-0003-C9 explicitly remains an unexecuted future approval/copy observation.
  Those artifact actions do not exist in Stage 1. The current intake/context
  checks cannot prove their future absence of evidence writes. Full HG-0003
  integration must therefore remain open.
- HG-0007's future graph/checkpoint, model-exporter, evaluation and backup
  obligations remain open. Current local-storage checks do not prove those
  later boundaries or external processor terms.
- The exact fixed-application-database `just cleanup` purge was rejected by
  automatic approval review and was not executed or bypassed. Its shared cleanup
  operation is verified against real disposable databases; do not describe the
  fixed-database operator invocation as runtime-verified. No daemon is installed;
  documented operator cleanup remains required while synthetic services are used.
- The interface is currently an authenticated JSON API with local synthetic OIDC,
  not learner-management browser forms or a production deployment. Real provider
  terms, browser-engine QA and real-learner activation are outside this evidence.

Stage 1 contract re-review is complete. The parent may finish task/evidence and
delivery records within these limits, while preserving the separate authority for
any commit and the explicit future specification gaps.
