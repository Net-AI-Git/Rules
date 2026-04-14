## Purpose

Commands in `.roo/commands/**/<name>.md` are workflows for the Agent, invoked as `/category/name`. This rule defines **required sections** and **anti-duplication** expectations so commands stay maintainable and match `.roo/rules/`.

**Roo Code:** The same repository ships a Roo layout under `.roo/commands/` (slash command = filename stem, e.g. `/testing-run-test-suite`). Authoritative meta-rule for Roo: [`.roo/rules/commands-management/commands-management.md`](../../../.roo/rules/commands-management/commands-management.md). Index: [`.roo/commands/slash-commands-documentation.md`](../../../.roo/commands/slash-commands-documentation.md).

## Required sections (in order)

1. `# Title` — Short, action-oriented (e.g. "Run Test Suite").
2. `## Overview` — What the command does, in a few sentences.
3. `## Scope and boundaries` — **In scope** vs **out of scope**; point to another `/command` or Rule for work that belongs elsewhere.
4. `## Rules Applied` — Bullet list of **rule folder names** that exist under `.roo/rules/` (see repository layout). Do not invent rule names.
   - Specs that live only under `reference-for-commands-and-skills/` MUST be labeled: *(reference; use via this command or documented skill — do not `@` manually)*.
5. `## Steps` — Ordered workflow. For sub-workflows already defined in another command, write **Execute `/other/command`** and summarize gaps, do not copy the full checklist.
6. `## Data Sources`
7. `## Output`

Optional: `## Related commands` — paths only, no duplicated steps.

## Duplication policy (mandatory)

| Situation | Policy |
|-----------|--------|
| Code style, local quality, PR checklist | `/review-code-review-checklist` owns the detailed checklist. Other commands **reference** its output. |
| Audit log parsing & field validation | `/security-analyze-audit-logs` owns deep log analysis. `/security-security-audit` invokes it once. |
| LangSmith token/latency/tool analysis | `/monitoring-analyze-langsmith-traces` owns trace metrics. |
| Service latency / throughput / resources | `/monitoring-performance-analysis` owns generic performance analysis. |
| Cross-artifact synthesis | `/monitoring-comprehensive-system-analysis` **correlates** artifacts; it does not replace the specialized commands above. |
| Orchestration | `run-all-*` commands only sequence subcommands and aggregate; they do not duplicate step lists. |

## Rules Applied — naming

- Use kebab-case names matching the **folder** of `RULE.mdc` (e.g. `monitoring-and-observability`, `core-python-standards`).
- If a topic has no dedicated rule folder in this repo (e.g. generic CI/CD runbooks), state it under **Scope** as project-specific verification, not as a fake Rule name.
