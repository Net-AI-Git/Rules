# Cursor Rules & Commands Repository

A comprehensive collection of Cursor AI Rules and Commands for Python development, agent systems, and production deployments. This repository provides standardized workflows, coding standards, and best practices that can be easily integrated into any project.

## Overview

This repository contains two main components:

### 📋 Rules (`.cursor/rules/`)
System-level instructions for the Cursor AI Agent. Rules define coding standards, architectural patterns, security requirements, and development workflows. They are automatically applied based on their configuration (always, intelligently, or for specific files).

### ⚡ Commands (`.cursor/commands/`)
Reusable workflows that can be triggered with a `/` prefix in the chat. Commands provide standardized processes for testing, security audits, code reviews, deployment, and agent development.

## Quick Start

### Option 1: Copy Everything
Simply copy the entire `.cursor` folder to your project root. Cursor will automatically:
- Apply rules based on their configuration
- Make commands available via `/` prefix

### Option 2: Copy by Category
Copy only what you need:

**For all projects:**
- `.cursor/rules/core/` - Essential coding standards
- `.cursor/rules/security/` - Security and governance

**For agent projects:**
- `.cursor/rules/agents/` - Multi-agent patterns
- `.cursor/rules/evaluation/` - LLM evaluation

**For API projects:**
- `.cursor/rules/api/` - API design and documentation

**For production projects:**
- `.cursor/rules/infrastructure/` - Deployment and monitoring

## Directory Structure

```
Rules/
├── .cursor/
│   ├── rules/          # Cursor Rules (see .cursor/rules/README.md)
│   │   ├── core/       # Always-applied core rules
│   │   ├── security/   # Security and governance
│   │   ├── agents/     # Agent-specific rules
│   │   ├── infrastructure/  # Deployment, monitoring, performance
│   │   ├── development/     # Testing, code review, versioning
│   │   ├── api/        # API-related rules
│   │   ├── data/       # Data schemas, migrations
│   │   ├── evaluation/ # LLM evaluation, judging
│   │   └── configuration/  # Configuration, DI, prompts
│   └── commands/       # Cursor Commands (see .cursor/commands/README.md)
│       ├── testing/    # Testing and evaluation
│       ├── security/   # Security audit and compliance
│       ├── review/     # Code review and compliance
│       ├── monitoring/ # Monitoring and observability
│       ├── deployment/ # Deployment workflows
│       └── agents/    # Agent development
└── README.md          # This file
```

## How Rules Work

Rules are applied automatically based on their type:

- **Always Apply** (`alwaysApply: true`) - Active in every chat session
- **Apply Intelligently** (`description` field) - Applied when Agent deems relevant
- **Apply to Specific Files** (`globs` patterns) - Applied when working on matching files
- **Apply Manually** - Applied only when explicitly mentioned (e.g., `@rule-name`)

See [`.cursor/rules/README.md`](.cursor/rules/README.md) for detailed documentation.

## How Commands Work

Commands are triggered with a `/` prefix in the chat input:

```
/testing/run-test-suite
/security/security-audit
/deployment/pre-deployment-check
```

Each command follows a standardized workflow and integrates with relevant Rules. See [`.cursor/commands/README.md`](.cursor/commands/README.md) for detailed documentation.

## Categories

### Core Rules
Essential rules for all projects:
- `core-python-standards` - Python coding standards (always applied)
- `error-handling-and-resilience` - Error handling patterns (always applied)

### Security Rules
Security and governance:
- `security-governance-and-observability` - Security standards (always applied)
- `audit-protocol` - Audit procedures (always applied)

### Agent Rules
Agent-specific architecture:
- `multi-agent-systems` - Multi-agent patterns
- `langgraph-architecture-and-nodes` - LangGraph workflows
- `agentic-logic-and-tools` - Agent tools and logic

### Infrastructure Rules
Deployment and operations:
- `deployment-and-infrastructure` - CI/CD, Docker, K8s
- `monitoring-and-observability` - Monitoring and logging
- `performance-optimization` - Performance best practices
- `multi-tenancy-and-isolation` - Multi-tenancy patterns

### Development Rules
Development workflow:
- `tests-and-validation` - Testing standards
- `code-review-and-collaboration` - Code review process
- `versioning-and-release-management` - Versioning strategy

### API Rules
API development:
- `api-interface-and-streaming` - API design
- `api-documentation-standards` - API docs

### Data Rules
Data management:
- `data-schemas-and-interfaces` - Data schemas
- `data-migration-and-compatibility` - Migrations

### Evaluation Rules
LLM evaluation and testing:
- `llm-evaluation-and-metrics` - Evaluation metrics
- `llm-judge-protocol` - LLM judging
- `final-review-protocol` - Final review (always applied)

### Configuration Rules
Configuration and setup:
- `configuration-and-dependency-injection` - DI patterns
- `prompt-engineering-and-management` - Prompt management

## Documentation

- **[Rules Documentation](.cursor/rules/README.md)** - Complete guide to Cursor Rules
- **[Commands Documentation](.cursor/commands/README.md)** - Complete guide to Cursor Commands
- **[Cursor Rules Docs](https://cursor.com/docs/context/rules)** - Official Cursor documentation
- **[Cursor Commands Docs](https://cursor.com/docs/agent/chat/commands)** - Official Cursor documentation

## Contributing

When creating or updating Rules:
- Follow the format defined in `.cursor/rules/rules-management/RULE.md`
- Use appropriate rule types (Always Apply, Apply Intelligently, etc.)

When creating or updating Commands:
- Follow the format defined in `.cursor/rules/commands-management/RULE.md`
- Integrate with relevant Rules
- Avoid duplication by reusing existing commands

## License

This repository contains development standards and workflows. Use and adapt as needed for your projects.
