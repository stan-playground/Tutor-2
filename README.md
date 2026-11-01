# Tutor Copilot — product preparation

This existing repository contains product analysis for a tutor-facing assistant for lesson preparation, homework and urgent replanning. [Product Decisions.md](<Product Decisions.md>) is the product source: it distinguishes owner-confirmed priorities, delegated pilot defaults, historical source decisions and estimates. Product decisions describe intent, not implementation or measured results.

## Current structure

There is no application implementation, dependency manifest, test suite, formatter, linter or CI configuration in this checkout. Architecture.md records the selected design proposal; dependency compatibility and the deployment environment remain unverified. Do not infer implementation from design choices or historical source references.

- [Product Decisions.md](<Product Decisions.md>): product priorities, delegated pilot defaults and deferred scope; preserve their provenance and evidence limits.
- [Architecture.md](Architecture.md): proposed framework, storage, human-review and caching choices with trade-offs.
- [Implementation Plan.md](<Implementation Plan.md>): high-level delivery order, dependencies and completion barriers.
- [Initial specifications](specs/README.md): draft homework-pilot contracts, including the [dataset specification](specs/datasets.md).
- [AGENTS.md](AGENTS.md): engineering rules, task routing and authority.
- [HighGrade project instruction](.highgrade/project/INSTRUCTIONS.md): local adaptation and delivery boundaries.
- [Document registry](.highgrade/project/documents.json): document roles and explicitly unagreed size budgets.
- [Initialization survey](.highgrade/project/survey.json): observed setup state and history; not a product backlog.
- [Native specification catalog](specs/catalog.json): scoped changes tracked through HighGrade; the product descriptions remain in Product Decisions.md.
- `HighGrade UI.sh` / `HighGrade UI.cmd`: generated launchers for the globally installed HighGrade UI.
- `.highgrade/local/`: ignored temporary inputs, reports and continuation. Keep permanent project records outside it.

This README owns purpose/navigation, current structure and reproducible commands. AGENTS owns agent/engineering rules; Architecture.md owns design recommendations; the implementation plan coordinates delivery order; native specifications own their requirements and evidence.

## Local commands

Run from the repository root. Git, Python 3 and a working global HighGrade installation are required for these checks. They do not require Node, Cargo, OpenSpec, an application server or an external service.

Resolve the active CLI instead of pinning a release path:

```bash
hgExe="$(python3 -c 'import json,pathlib; p=pathlib.Path.home()/".highgrade/global"; print(p/"releases"/json.loads((p/"active.json").read_text())["release"]/"highgrade")')"
```

Then check installation, local compatibility, registered documents and the saved survey:

```bash
"$hgExe" global-status --profile "$HOME"
"$hgExe" doctor --root "$PWD"
"$hgExe" inspect --root "$PWD" --registry .highgrade/project/documents.json
"$hgExe" survey-check --root "$PWD"
git diff --check
sh -n "HighGrade UI.sh"
python3 -m json.tool .highgrade/project/documents.json > /dev/null
python3 -m json.tool .highgrade/project/survey.json > /dev/null
```

Read the report as well as the exit code: `1` is failed and `2` is unknown. Document/route budgets remain unagreed, so registry inspection reports `BudgetNotAgreed`; this is not a successful budget check. Doctor may report missing Cargo/OpenSpec from its legacy probe before connection. Neither is required for this repository's documentation work or native HighGrade route. Investigate other findings rather than treating every unknown as harmless.

The registry checks the process documents. The product analysis remains outside that lint scope: its two original absolute provenance links are unsupported by HighGrade's link checker. The initialization survey preserves its historical hash; current task evidence records later edits. Check the exact source paths separately before using the originals, and record unavailable targets as gaps. A passing process-link check does not establish source-document accessibility or re-audit their content.

`git diff --check` checks tracked changes; review new untracked files too before committing. No application run/test/lint command exists yet. Define and verify such commands with the first implementation task; do not add placeholder tests or install a framework to complete initialization.

To open the project UI on this Mac, run:

```bash
sh "HighGrade UI.sh"
```

The launcher starts a local server and opens the browser; Ctrl+C stops the server. The Windows `.cmd` launcher is generated for portability, but Windows execution is not verified here.

## Evidence and next work

Keep significant original check reports and any unrecoverable inputs with the relevant task. When a native change exists, use `specs/changes/<ID>/evidence/`; retain the originals while current results, review, decisions or delivery depend on them. Ordinary setup checks need no duplicate permanent report set: the survey records their outcomes. Temporary diagnostics belong in `.highgrade/local/` and are not delivered automatically. Before an authorized handoff, verify required reports and links are included; do not upload automatically or delete the only needed evidence.

Initialization did not create or migrate product specifications. [HG-0001](specs/changes/HG-0001/spec.json) records the priority update; [HG-0002](specs/changes/HG-0002/spec.json) records the delegated resolution of open product choices. Neither implements product features or mass-converts the analysis into specifications. For later requests, use `$highgrade-task`, `$highgrade-spec` for agreed new/changed requirements, and `$highgrade-work` within the request's authority. The selected pilot serves independent tutors preparing homework for adult A2–B2 English learners; implementation remains separate work.
