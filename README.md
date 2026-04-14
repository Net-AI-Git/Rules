# Rules & commands repository (Cursor + Roo Code)

A comprehensive collection of **AI coding standards** (rules), **slash commands**, and **skills** for Python development, agent systems, and production deployments. This repository supports **two editor layouts**:

| Layout | Paths | Typical use |
|--------|--------|-------------|
| **Roo Code** | `.roo/rules/`, `.roo/commands/`, `.roo/skills/` | VS Code + Roo Code extension ([docs](https://docs.roocode.com/)) |
| **Cursor** | `.cursor/rules/`, `.cursor/commands/`, `.cursor/skills/` | Cursor IDE |

Content is aligned between them; **Roo** uses plain Markdown rules and slash commands named from **filenames** (e.g. `/testing-run-test-suite`). **Cursor** uses `.mdc` rules with frontmatter and nested command paths (e.g. `/testing/run-test-suite`).

## Quick start

### Roo Code

1. Copy or clone this repo and open it in VS Code with Roo Code installed.
2. Custom instructions load from [`.roo/rules/`](.roo/rules/). Slash commands load from [`.roo/commands/`](.roo/commands/). Skills load from [`.roo/skills/`](.roo/skills/).
3. Command index: [`.roo/commands/slash-commands-documentation.md`](.roo/commands/slash-commands-documentation.md).
4. Workspace agent summary: [`AGENTS.md`](AGENTS.md).

### Cursor

1. Copy the `.cursor/` folder to your project root.
2. Rules apply per `.mdc` configuration; commands use `/category/command-name`.

## Directory structure (simplified)

```
Rules/
├── .roo/                      # Roo Code (VS Code)
│   ├── rules/
│   ├── commands/
│   └── skills/
├── .cursor/                   # Cursor IDE
│   ├── rules/
│   ├── commands/
│   └── skills/
├── AGENTS.md                  # High-level agent instructions (Roo loads from root)
├── scripts/
│   └── migrate_to_roo.py      # Regenerate .roo/ from .cursor/ when needed
└── README.md
```

## Slash commands (Roo naming)

Invoke with `/` + **filename stem** of a file in `.roo/commands/`:

```
/testing-run-test-suite
/security-security-audit
/review-final-compliance-check
/monitoring-run-all-monitoring
```

See [`.roo/commands/slash-commands-documentation.md`](.roo/commands/slash-commands-documentation.md) for the full list.

## Categories (rule topics)

Examples of rule **folders** (same names under `.roo/rules/` and `.cursor/rules/`):

- **Core:** `core-python-standards`, `error-handling-and-resilience`
- **Security:** `security-governance-and-observability`; reference specs under `reference-for-commands-and-skills/`
- **Agents:** `multi-agent-systems`, `langgraph-architecture-and-nodes`, `agentic-logic-and-tools`
- **Infrastructure:** `monitoring-and-observability`, `redis-cache`, `oracle-database`
- **API / data / configuration:** see tree under `.roo/rules/`

## Documentation

- **[Roo rules README](.roo/rules/README.md)** — Rules tree (Roo + Cursor notes)
- **[Roo slash commands index](.roo/commands/slash-commands-documentation.md)**
- **[Cursor rules README](.cursor/rules/README.md)** — Cursor-oriented details
- **[Cursor commands README](.cursor/commands/README.md)** — Cursor path style `/category/name`
- **[Roo Code docs](https://docs.roocode.com/)** — Skills, rules, slash commands
- **[Cursor Rules docs](https://cursor.com/docs/context/rules)** / **[Commands](https://cursor.com/docs/agent/chat/commands)**

## Contributing

- **Roo layout:** follow [`.roo/rules/commands-management/commands-management.md`](.roo/rules/commands-management/commands-management.md) for commands; keep rule files as `{topic}.md` per folder.
- **Cursor layout:** follow [`.cursor/rules/commands-management/RULE.mdc`](.cursor/rules/commands-management/RULE.mdc) for commands under `.cursor/commands/`.
- After editing `.cursor/rules` or `.cursor/commands` or `.cursor/skills`, regenerate Roo files with:

```bash
python scripts/migrate_to_roo.py
```

Then re-apply any manual doc fixes in `.roo/commands/slash-commands-documentation.md` or `AGENTS.md` if the script overwrote them.

## License

This repository contains development standards and workflows. Use and adapt as needed for your projects.
