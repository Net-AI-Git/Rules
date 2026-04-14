# Roo Code slash commands (documentation)

This file documents the **slash commands** shipped in this repository for **Roo Code** (VS Code extension). Commands are Markdown files under [`.roo/commands/`](.) (project) or `~/.roo/commands/` (global). Typing `/` in chat lists commands; each **filename stem** is the command name (e.g. `testing-run-test-suite.md` → `/testing-run-test-suite`).

**Note:** This filename is intentionally not `README.md`, so it is **not** registered as a `/readme` slash command.

## Roo vs Cursor in this repo

- **Roo Code:** use `.roo/rules/`, `.roo/skills/`, `.roo/commands/` as documented on [docs.roocode.com](https://docs.roocode.com/).
- **Cursor:** the parallel tree under `.cursor/` remains available for Cursor users; conventions differ (e.g. Cursor commands used to use paths like `/testing/run-test-suite`).

## Command index (filename → invocation)

| File | Slash command |
|------|----------------|
| `testing-run-test-suite.md` | `/testing-run-test-suite` |
| `testing-write-targeted-tests.md` | `/testing-write-targeted-tests` |
| `testing-run-evaluation-suite.md` | `/testing-run-evaluation-suite` |
| `security-analyze-audit-logs.md` | `/security-analyze-audit-logs` |
| `security-security-audit.md` | `/security-security-audit` |
| `review-code-review-checklist.md` | `/review-code-review-checklist` |
| `review-final-compliance-check.md` | `/review-final-compliance-check` |
| `monitoring-analyze-langsmith-traces.md` | `/monitoring-analyze-langsmith-traces` |
| `monitoring-comprehensive-system-analysis.md` | `/monitoring-comprehensive-system-analysis` |
| `monitoring-performance-analysis.md` | `/monitoring-performance-analysis` |
| `monitoring-profile-code-bottlenecks.md` | `/monitoring-profile-code-bottlenecks` |
| `monitoring-audit-prompt-registry-splunk.md` | `/monitoring-audit-prompt-registry-splunk` |
| `monitoring-run-all-monitoring.md` | `/monitoring-run-all-monitoring` |
| `agents-setup-new-agent-system.md` | `/agents-setup-new-agent-system` |
| `agents-create-agent-node.md` | `/agents-create-agent-node` |
| `agents-implement-agent-tool.md` | `/agents-implement-agent-tool` |
| `agents-run-all-agents.md` | `/agents-run-all-agents` |

Each command file includes YAML **frontmatter** with at least `description:` (for the slash command menu).

## Skills

- **`evaluate-with-llm-judge`** — see [`.roo/skills/evaluate-with-llm-judge/SKILL.md`](../skills/evaluate-with-llm-judge/SKILL.md). Roo discovers skills by `name` / `description` in `SKILL.md`; there is no `@` trigger like in Cursor.
- **`splunk-instrumentation`** — see [`.roo/skills/splunk-instrumentation/SKILL.md`](../skills/splunk-instrumentation/SKILL.md).

## Command structure

Follow [`.roo/rules/commands-management/commands-management.md`](../rules/commands-management/commands-management.md) for required sections (Overview, Scope and boundaries, Rules Applied, Steps, Data Sources, Output) and the duplication policy.

## Related links

- [Repository README](../../README.md)
- [Rules documentation](../rules/README.md)
- [Roo Code — Slash Commands](https://docs.roocode.com/features/slash-commands)
- [Roo Code — Custom Instructions (rules)](https://docs.roocode.com/features/custom-instructions)
- [Roo Code — Skills](https://docs.roocode.com/features/skills)
