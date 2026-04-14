# Agent instructions (Roo Code)

This repository is a **standards pack** (rules, skills, slash commands), not an application. When working here:

- **Custom instructions (rules):** [`.roo/rules/`](.roo/rules/) — Markdown loaded recursively into the Roo Code system prompt (see [Roo docs — Custom Instructions](https://docs.roocode.com/features/custom-instructions)).
- **Skills:** [`.roo/skills/*/SKILL.md`](.roo/skills/) — on-demand workflows with required `name` / `description` frontmatter ([Skills](https://docs.roocode.com/features/skills)).
- **Slash commands:** [`.roo/commands/*.md`](.roo/commands/) — command name = **filename without `.md`** ([Slash Commands](https://docs.roocode.com/features/slash-commands)). Index: [`.roo/commands/slash-commands-documentation.md`](.roo/commands/slash-commands-documentation.md).

**Cursor users** use the parallel [`.cursor/`](.cursor/) tree (`.mdc` rules, nested command paths). Prefer editing the Roo layout when your team standardizes on Roo Code.

## Verification

After cloning or changing files:

1. Reload the VS Code window if new slash commands do not appear.
2. Open Slash Commands in Roo settings and confirm files under `.roo/commands/` list as expected.
3. Open a rule file under `.roo/rules/` and confirm content is plain Markdown (no stray YAML frontmatter unless intentional).
