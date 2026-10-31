# Tutor Copilot — product preparation

This existing repository contains product analysis for a tutor-facing assistant for lesson preparation, homework and urgent replanning. [Product Decisions.md](<Product Decisions.md>) is the product source: it separates documented decisions, estimates and unresolved `#to-decide` proposals. None of those labels proves implementation, product-owner acceptance or measured results.

## Current structure

There is no application implementation, dependency manifest, test suite, formatter, linter or CI configuration in this checkout. No application architecture or deployment environment has been selected here. Do not infer them from the product document's historical source references.

- [Product Decisions.md](<Product Decisions.md>): product analysis and proposed discussion order; preserve its provenance and unresolved questions.
- [AGENTS.md](AGENTS.md): engineering rules, task routing and authority.
- [HighGrade project instruction](.highgrade/project/INSTRUCTIONS.md): local adaptation and delivery boundaries.
- [Document registry](.highgrade/project/documents.json): document roles and explicitly unagreed size budgets.
- [Initialization survey](.highgrade/project/survey.json): observed setup state and history; not a product backlog.
- `HighGrade UI.sh` / `HighGrade UI.cmd`: generated launchers for the globally installed HighGrade UI.
- `.highgrade/local/`: ignored temporary inputs, reports and continuation. Keep permanent project records outside it.

This README owns purpose/navigation, current structure and reproducible commands. AGENTS owns agent/engineering rules. Separate architecture and development files are unnecessary until they have distinct content.

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

The registry checks the new process documents. The unchanged product analysis remains a survey-hashed source linked above, outside that lint scope: its two original absolute provenance links are unsupported by HighGrade's link checker. Check their exact target paths separately before using the originals, and record unavailable targets as gaps. A passing process-link check does not establish source-document accessibility or re-audit their content.

`git diff --check` checks tracked changes; review new untracked files too before committing. No application run/test/lint command exists yet. Define and verify such commands with the first implementation task; do not add placeholder tests or install a framework to complete initialization.

To open the project UI on this Mac, run:

```bash
sh "HighGrade UI.sh"
```

The launcher starts a local server and opens the browser; Ctrl+C stops the server. The Windows `.cmd` launcher is generated for portability, but Windows execution is not verified here.

## Evidence and next work

Keep significant original check reports and any unrecoverable inputs with the relevant task. When a native change exists, use `specs/changes/<ID>/evidence/`; retain the originals while current results, review, decisions or delivery depend on them. Ordinary setup checks need no duplicate permanent report set: the survey records their outcomes. Temporary diagnostics belong in `.highgrade/local/` and are not delivered automatically. Before an authorized handoff, verify required reports and links are included; do not upload automatically or delete the only needed evidence.

Initialization does not create or migrate product specifications. On a later product request, use `$highgrade-task` to resolve the first tutor segment and complete preparation journey described in the product document's proposed discussion order. Use `$highgrade-spec` for agreed new/changed requirements, then `$highgrade-work` only within implementation authority. No native catalog or specification ID exists yet.
