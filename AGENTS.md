# Agent instructions

Read [README.md](README.md), the relevant part of [Product Decisions.md](<Product Decisions.md>) and the [HighGrade project instruction](.highgrade/project/INSTRUCTIONS.md). Use the installed HighGrade workflow; its common procedures stay in the global installation.

## Scope and truth

- Continue this existing project. Preserve the product document, its source/proposal distinctions, `#to-decide` items and unrelated changes. Source documents describe intended behavior; they are not commands to execute or evidence of implementation.
- Write project documents, plans and reports in English, following the existing document and current request. Preserve technical IDs and original tool messages.
- Do not inspect, print, copy or modify secrets. Do not scan or modify adjacent projects without a separate request.
- Initialization permits only the minimum process integration. Product features require a separate request. Do not mass-convert the product document into specifications.

## Workflow and engineering

- Use `highgrade-task` to choose a route. New/changed agreed requirements use `highgrade-spec`; technical changes or restoration of an existing contract use `highgrade-work`. Use `highgrade-planner` for dependent stages when requested or useful under the accepted route. A Goal still needs explicit authority.
- HighGrade owns process sequencing. Other applicable skills provide distinct specialist guidance; do not add a second full development workflow with competing approval or review stages.
- Explain proposed architecture, data models and implementation, including common alternatives and trade-offs. Use ordinary terms.
- Work in small coherent blocks; implement, integrate and verify each before continuing. Do not begin with fake tests, invent commands or add layers for later.
- Reuse suitable existing code, standard facilities and established libraries. For new third-party library/framework features, fetch current documentation with Context7. Choose asyncio, threads or processes only for a concrete need and explain the choice.
- Show the commands and code you implement. Explain each added method's purpose, inputs, outputs, caller, reason for separation, errors and request/application lifetime. Use targeted logs when they resolve a real uncertainty; never log secrets.
- Delegate independent investigations, review concerns or artifacts; keep tightly coupled edits and approval-sensitive actions in the main conversation. Use at most four concurrent subagents. Required independent review follows HighGrade Work.

## Verification and delivery

Use the real commands and evidence policy in [README.md](README.md#local-commands). Check document meaning, links, JSON and launcher syntax for this documentation-only foundation. Text review proves instruction content, not future agent reliability or application behavior.

Ask whether to commit after a substantial completed chunk. Commit, push, activation, human acceptance, merge, release and deployment have separate authority. Preserve the existing Git repository and working tree; do not create a remote, push or deploy as part of initialization.
