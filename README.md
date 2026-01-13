# Rules

Repository for Cursor AI rules and configurations. Rules are grouped by category for easier management.

## Structure

```
.cursor/rules/
├── core/              # Always-applied core rules (Python standards, error handling)
├── security/          # Security and governance rules
├── agents/            # Agent-specific rules (multi-agent, LangGraph, agentic logic)
├── infrastructure/    # Deployment, monitoring, performance
├── development/       # Testing, code review, versioning
├── api/               # API-related rules
├── data/              # Data schemas, migrations
├── evaluation/        # LLM evaluation, judging, auditing
└── configuration/     # Configuration, dependency injection, prompts
```

## How to Use

### Option 1: Copy Everything
Simply copy the entire `.cursor/rules` folder to your project. Cursor will automatically select which rules to apply based on:
- `alwaysApply: true` - Always active
- `globs` - Active when working on matching files
- `alwaysApply: false` - Applied when Agent decides it's relevant

### Option 2: Copy by Category
Copy only the category folders you need for your project:
- **All projects**: Copy `core/` and `security/`
- **Agent projects**: Also copy `agents/` and `evaluation/`
- **API projects**: Also copy `api/`
- **Production projects**: Also copy `infrastructure/`

## Categories

### Core (`core/`)
Essential rules that should be in every project:
- `core-python-standards` - Python coding standards (always applied)
- `error-handling-and-resilience` - Error handling patterns (always applied)

### Security (`security/`)
Security and governance:
- `security-governance-and-observability` - Security standards (always applied)
- `audit-protocol` - Audit procedures (always applied)

### Agents (`agents/`)
Agent-specific architecture:
- `multi-agent-systems` - Multi-agent patterns
- `langgraph-architecture-and-nodes` - LangGraph workflows
- `agentic-logic-and-tools` - Agent tools and logic

### Infrastructure (`infrastructure/`)
Deployment and operations:
- `deployment-and-infrastructure` - CI/CD, Docker, K8s
- `monitoring-and-observability` - Monitoring and logging
- `performance-optimization` - Performance best practices
- `multi-tenancy-and-isolation` - Multi-tenancy patterns

### Development (`development/`)
Development workflow:
- `tests-and-validation` - Testing standards
- `code-review-and-collaboration` - Code review process
- `versioning-and-release-management` - Versioning strategy

### API (`api/`)
API development:
- `api-interface-and-streaming` - API design
- `api-documentation-standards` - API docs

### Data (`data/`)
Data management:
- `data-schemas-and-interfaces` - Data schemas
- `data-migration-and-compatibility` - Migrations

### Evaluation (`evaluation/`)
LLM evaluation and testing:
- `llm-evaluation-and-metrics` - Evaluation metrics
- `llm-judge-protocol` - LLM judging
- `final-review-protocol` - Final review (always applied)

### Configuration (`configuration/`)
Configuration and setup:
- `configuration-and-dependency-injection` - DI patterns
- `prompt-engineering-and-management` - Prompt management
