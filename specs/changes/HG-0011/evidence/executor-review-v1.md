# HG-0011 executor review

1 November 2026. This is a semantic review of documentation against the owner's request, supported by structural checks. It is not application execution, a learning study, gold-label approval or human acceptance.

## Scope and baseline

The owner adopted two changes: cumulative exposure/practice/later-check context with important-now/worth-revisiting selection on tutor requests; and teaching routes beyond visible errors. The four major files are Product Decisions.md, Architecture.md, Implementation Plan.md and Repository Structure.md. Supporting drafts HG-0003–0008/HG-0010, datasets.md and navigation are aligned. No application, scheduler, student interface, original-authoring mode or automated audio assessment was implemented.

[before.json](before.json) records the clean source baseline at Git revision `5c6df6f` and exact file hashes before document changes. All earlier product IDs and original A/I source links remain; PD-39/40 are appended. Integrated historical specifications were not rewritten. Application drafts retain unimplemented tasks and unintegrated state.

## Scenario observations

| Documentation scenario | Observed current content |
| --- | --- |
| HG-0001-S1 | Opening priorities retain the four-job order, separate subskill measures, both evidence streams, assessment/preferences, reviewed material, domain adaptation, safety, part review and per-stage Langfuse evaluation. PD-39/40 add history and broader routes. |
| HG-0001-S2 | Prior decision IDs/provenance and intent-versus-implementation distinctions remain; numerical defaults are not recast as measured results. The architecture remains a design proposal. |
| HG-0002-S1 | Concrete existing pilot/default decisions remain, with no newly unresolved product questions or invented learning-gain/compliance claim. Existing privacy and recent-rate policy paragraphs are retained verbatim. |
| HG-0009-S1 | Feedback remains second, transcript-grounded and independent of a homework request. It changes no canonical activity/performance facts and retains its own gates and homework-accounting separation. |
| HG-0011-S1 | PD-02/07/09/10/39, architecture source loading and plan stage 1 separate recent comparable performance from cumulative retained facts. Current/revisit choices use goals/history without fixed quotas, automatic forgetting or exposure-based mastery. |
| HG-0011-S2 | PD-39, architecture records/intake and HG-0003/0006/0007/0010 define independent dated source-qualified facts, correction/deduplication, frozen references, separate tutor actual-use intake and existing expiry/deletion. Derived views are not independent model memory. |
| HG-0011-S3 | PD-40 and the architecture table/search schema permit accessible reading/listening, vocabulary exposure, fluency, discourse, strategies and meaningful tasks/projects without invented errors. Reviewed sources, available recording-specific criteria, accessibility/support, appropriate outcomes and gaps remain explicit. |
| HG-0011-S4 | The four files, seven application drafts and dataset contract use the same concepts. Existing modules/graph own the work; plan stages 1/2/3/4/6/8a and early evaluation reflect dependencies. No application task is marked done. |

## Decision table checked in the text

| Input/condition | Required interpretation or next action |
| --- | --- |
| Relevant confirmed work older than 90 days | Qualified cumulative context/revisit reason; never silently widen recent count/rate selection. |
| Approved/copied artifact or assignment-only report | Preparation/assignment only; actual encounter, attempt and checked outcome remain unknown without separate evidence. |
| Confirmed input encounter without a response | Exposure context without invented attempt/opportunities/mastery; facts need not follow a compulsory progression. |
| Duplicate/corrected source/activity/attempt | Link/supersede without double-counting; existing requests keep frozen revisions. |
| Supported current goal with no visible error | Select a suitable PD-40 route with purpose, demands/support and criteria; exact confusion is conditional. |
| Uncertain prerequisite | Proportionate support, lighter reviewed task or recheck if useful; no automatic readiness claim or compulsory diagnostic. |
| Known unavailable/ineligible recording or mismatched key/criteria | Checked eligible alternative or explicit material gap; no ready invalid listening material. |
| Provider/database outage | Preparation failure, distinct from a genuine material gap. |
| New history arrives during a request | New request; no silent refresh through wording revision or review. |
| Feedback generation/approval/export | Feedback/decision records only; no confirmed activity/performance writes. |
| Expired raw source or learner deletion | Existing retention/deletion applies to facts/views/checkpoints/evaluation; no reconstructed quotes or indefinite archive. |

## Checks and commands

[checks-v1.json](checks-v1.json) preserves the actual commands, exit codes and full CLI reports: `global-status --profile /Users/HUAWEI`, `doctor --root .`, `inspect --root . --registry .highgrade/project/documents.json`, `survey-check --root .`, `spec-validate --root .`, `git diff --check`, and `sh -n "HighGrade UI.sh"`. Commands use the active HighGrade v0-4-1 executable.

Specification validation passed for all 11 changes. Doctor initially overlapped a catalog read and received StoreBusy; the identical command passed sequentially without lock recovery. Registry inspection has no structural errors, but returns BudgetNotAgreed unknowns. The initialization survey is structurally valid and historically completed, but its source snapshot is stale (including earlier instruction/registry changes); this product task does not renew setup acceptance or rewrite that history.

[document-checks-v2.json](document-checks-v2.json) records the latest actual inline Python command, 27 successful JSON/link/preservation/scope checks, 58 local links/anchors and exact current design/draft input hashes. Version 1 remains development history before the final unknown-date/source-kind clarifications. Original external provenance contents were not inspected. Link checks cover local standard Markdown links/headings, not remote availability.

## Limits and review handoff

The executor finds the requested documentation behavior present. Independent semantic GO is still required. JSON validation and text assertions do not prove future intake, retrieval, graph execution, listening playback, privacy enforcement or learning benefit. Draft application verification descriptions and dataset variants remain future work. No live learner records, secrets, adjacent-project contents or external service were accessed; no commit, publication or activation occurred.
