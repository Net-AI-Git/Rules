# Cursor Rules & Commands Repository

A comprehensive collection of Cursor AI Rules and Commands for Python development, agentic systems, and production deployments. This repository provides standardized workflows, coding standards, and best practices that can be easily integrated into any project.

## Overview

This repository contains two main components:

- **Rules** (`.cursor/rules/`) - System-level instructions that guide the Cursor Agent with coding standards, best practices, and domain-specific knowledge
- **Commands** (`.cursor/commands/`) - Reusable workflows that can be triggered with a `/` prefix to automate common development tasks

Together, Rules and Commands provide a complete framework for maintaining code quality, security, and consistency across your projects.

## Quick Start

### Option 1: Copy Everything

Copy both `.cursor/rules` and `.cursor/commands` folders to your project root:

```bash
cp -r .cursor/ /path/to/your/project/
```

### Option 2: Copy by Need

**For all projects:**
- Copy `.cursor/rules/core/` and `.cursor/rules/security/`
- Copy `.cursor/commands/review/` and `.cursor/commands/security/`

**For agent projects:**
- Also copy `.cursor/rules/agents/` and `.cursor/rules/evaluation/`
- Also copy `.cursor/commands/agents/` and `.cursor/commands/testing/`

**For API projects:**
- Also copy `.cursor/rules/api/`
- Also copy relevant commands from `.cursor/commands/`

**For production projects:**
- Also copy `.cursor/rules/infrastructure/`
- Also copy `.cursor/commands/deployment/` and `.cursor/commands/monitoring/`

## Structure

```
.cursor/
├── rules/              # System-level instructions for Cursor Agent
│   ├── core/          # Always-applied core rules
│   ├── security/      # Security and governance
│   ├── agents/         # Agent-specific patterns
│   ├── infrastructure/# Deployment and operations
│   ├── development/   # Testing and code review
│   ├── api/           # API development
│   ├── data/          # Data management
│   ├── evaluation/    # LLM evaluation
│   └── configuration/# Configuration management
└── commands/          # Reusable workflows
    ├── testing/       # Testing and evaluation
    ├── security/      # Security audits
    ├── review/        # Code review
    ├── monitoring/    # Observability
    ├── deployment/    # Deployment workflows
    └── agents/         # Agent development
```

## Rules

Rules provide persistent, reusable context at the prompt level. They are automatically applied based on their configuration:

- **Always Apply** - Active in every chat session
- **Apply Intelligently** - Applied when Agent decides they're relevant
- **Apply to Specific Files** - Applied when working on matching file patterns
- **Apply Manually** - Applied when @-mentioned

See [`.cursor/rules/README.md`](.cursor/rules/README.md) for detailed documentation.

## Commands

Commands are reusable workflows triggered with a `/` prefix. They integrate with Rules to provide standardized processes:

- Individual commands for specific tasks
- Master commands that orchestrate multiple commands
- Integration with project Rules for consistent standards

See [`.cursor/commands/README.md`](.cursor/commands/README.md) for detailed documentation.

## Categories

### Core Rules & Commands
Essential for all projects:
- **Rules**: `core/`, `security/`
- **Commands**: `review/`, `security/`

### Agent Development
For multi-agent systems and LangGraph:
- **Rules**: `agents/`, `evaluation/`
- **Commands**: `agents/`, `testing/`

### Production Deployment
For production-ready applications:
- **Rules**: `infrastructure/`, `deployment/`
- **Commands**: `deployment/`, `monitoring/`

### API Development
For API projects:
- **Rules**: `api/`
- **Commands**: Relevant testing and review commands

## Usage Examples

### Using Rules

Rules are automatically applied based on their configuration. You can also manually apply them:

```
@core-python-standards help me write a function
@rules-management create a new rule for database patterns
```

### Using Commands

Commands are triggered with a `/` prefix:

```
/testing/run-test-suite
/security/security-audit
/review/code-review-checklist
/testing/run-all-testing
```

You can also provide additional context:

```
/testing/run-test-suite and fix any failures
/security/security-audit focusing on OWASP Top 10
```

## Creating and Updating

### Rules

To create or update a rule, the `rules-management` rule is automatically applied when working on `RULE.md` files. You can also tag it manually:

```
@rules-management create a new rule for database patterns
```

See [`.cursor/rules/rules-management/RULE.md`](.cursor/rules/rules-management/RULE.md) for the complete guide.

### Commands

To create or update a command, the `commands-management` rule is automatically applied when working on command files. You can also tag it manually:

```
@commands-management create a new command for database migrations
```

See [`.cursor/rules/commands-management/RULE.md`](.cursor/rules/commands-management/RULE.md) for the complete guide.

## Documentation

- **[Rules Documentation](.cursor/rules/README.md)** - Complete guide to Rules
- **[Commands Documentation](.cursor/commands/README.md)** - Complete guide to Commands
- **[Rules Management Guide](.cursor/rules/rules-management/RULE.md)** - How to create/update Rules
- **[Commands Management Guide](.cursor/rules/commands-management/RULE.md)** - How to create/update Commands

## Related Resources

- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Cursor Commands Documentation](https://cursor.com/docs/agent/chat/commands)

## Contributing

When adding new rules or commands:

1. Follow the structure and format defined in the management guides
2. Ensure proper categorization
3. Include relevant Rules Applied (for commands)
4. Test thoroughly before committing
5. Update relevant README files

## License

This repository contains configuration and documentation files for use with Cursor AI. Use and modify as needed for your projects.
