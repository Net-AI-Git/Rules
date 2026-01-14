# Cursor Rules Documentation

This directory contains Cursor AI Rules - system-level instructions that provide persistent, reusable context to guide the Cursor Agent.

## What are Cursor Rules?

Rules are markdown files that bundle prompts, standards, and best practices together. They are included at the start of the model context, giving the AI consistent guidance for generating code, interpreting edits, or helping with workflows.

Rules are version-controlled and scoped to your codebase, making it easy to share standards and workflows across your team.

## Directory Structure

Rules are organized by category:

```
.cursor/rules/
├── core/              # Always-applied core rules (Python standards, error handling)
├── security/          # Security and governance rules
├── agents/            # Agent-specific rules (multi-agent, LangGraph, agentic logic)
├── infrastructure/    # Deployment, monitoring, performance
├── development/      # Testing, code review, versioning
├── api/              # API-related rules
├── data/             # Data schemas, migrations
├── evaluation/       # LLM evaluation, judging, auditing
├── configuration/    # Configuration, dependency injection, prompts
├── rules-management/ # Meta-rule for managing rules
└── commands-management/ # Meta-rule for managing commands
```

### Rule Folder Structure

Each rule is a **folder** containing a `RULE.md` file:

```
.cursor/rules/
  category-name/
    rule-name/
      RULE.md
```

**Important:**
- Each rule must be in its own folder
- Folder name should be kebab-case (e.g., `core-python-standards`)
- File inside must be named exactly `RULE.md` (capital letters)

## Rule Types

Rules are applied automatically based on their configuration. There are 4 types:

### 1. Always Apply
Applied to every chat session automatically.

**Frontmatter:**
```yaml
---
alwaysApply: true
---
```

**Use when:** The rule should always be active (e.g., core coding standards, security requirements).

**Examples:**
- `core-python-standards`
- `error-handling-and-resilience`
- `security-governance-and-observability`
- `final-review-protocol`

### 2. Apply Intelligently
Applied when Agent decides it's relevant based on the description.

**Frontmatter:**
```yaml
---
description: "Clear description of what this rule covers"
alwaysApply: false
---
```

**Use when:** The rule is relevant in specific contexts but not always needed (e.g., deployment standards, monitoring practices).

**Examples:**
- `deployment-and-infrastructure`
- `monitoring-and-observability`
- `code-review-and-collaboration`
- `llm-judge-protocol`

### 3. Apply to Specific Files
Applied when working on files matching specified patterns.

**Frontmatter:**
```yaml
---
globs:
  - "**/api/**/*.py"
  - "**/routes/**/*.py"
alwaysApply: false
---
```

**Use when:** The rule is only relevant for specific file types or locations (e.g., API endpoints, test files, migrations).

**Examples:**
- `api-documentation-standards` (applies to API files)
- `tests-and-validation` (applies to test files)
- `rules-management` (applies to RULE.md files)
- `commands-management` (applies to command files)

### 4. Apply Manually
Applied only when @-mentioned in chat (e.g., `@rule-name`).

**Frontmatter:**
```yaml
---
alwaysApply: false
---
```

**Use when:** The rule is rarely needed and should only be applied on demand (e.g., special audit protocols).

## How Rules are Applied

Rules are automatically selected and applied by Cursor based on:

1. **Always Apply rules** - Always active in every chat session
2. **Apply Intelligently rules** - Agent evaluates the description and decides if relevant
3. **Apply to Specific Files rules** - Active when you're working on files matching the glob patterns
4. **Apply Manually rules** - Only when you explicitly tag them with `@rule-name`

## Categories

### Core (`core/`)
Essential rules that should be in every project:

- **`core-python-standards`** - Python coding standards (Always Apply)
  - Code quality, function length, type hints, logging
  - Concurrency patterns (async/await, threading)
  
- **`error-handling-and-resilience`** - Error handling patterns (Always Apply)
  - Error classification, retry strategies, circuit breakers
  - Resilience patterns and graceful degradation

### Security (`security/`)
Security and governance:

- **`security-governance-and-observability`** - Security standards (Always Apply)
  - OWASP Top 10 for LLM Applications
  - NIST AI RMF compliance
  - Blast radius containment
  
- **`audit-protocol`** - Audit procedures (Always Apply)
  - Audit trail requirements
  - Compliance checks
  - Log structure standards

### Agents (`agents/`)
Agent-specific architecture:

- **`multi-agent-systems`** - Multi-agent patterns (Apply Intelligently)
  - Orchestrator/Worker/Synthesizer patterns
  - SECTIONS pattern for task decomposition
  
- **`langgraph-architecture-and-nodes`** - LangGraph workflows (Apply to Specific Files)
  - Workflow design, state management
  - Node implementation (READ → DO → WRITE → CONTROL)
  
- **`agentic-logic-and-tools`** - Agent tools and logic (Apply Intelligently)
  - LangChain fundamentals
  - Tool definitions and binding

### Infrastructure (`infrastructure/`)
Deployment and operations:

- **`deployment-and-infrastructure`** - CI/CD, Docker, K8s (Apply Intelligently)
  - Deployment strategies, blue-green, rollback
  - Infrastructure as Code
  
- **`monitoring-and-observability`** - Monitoring and logging (Apply Intelligently)
  - Metrics collection (Prometheus, StatsD)
  - Distributed tracing (OpenTelemetry)
  - LangSmith integration
  
- **`performance-optimization`** - Performance best practices (Apply Intelligently)
  - Caching strategies, query optimization
  - Resource pooling
  
- **`multi-tenancy-and-isolation`** - Multi-tenancy patterns (Apply Intelligently)
  - Data isolation strategies
  - Tenant management

### Development (`development/`)
Development workflow:

- **`tests-and-validation`** - Testing standards (Apply to Specific Files)
  - Pytest framework, atomic tests
  - Test structure and organization
  
- **`code-review-and-collaboration`** - Code review process (Apply Intelligently)
  - PR review checklist
  - Git workflow standards
  
- **`versioning-and-release-management`** - Versioning strategy (Apply Intelligently)
  - Semantic versioning
  - Changelog standards

### API (`api/`)
API development:

- **`api-interface-and-streaming`** - API design (Apply to Specific Files)
  - RESTful principles, streaming
  - Error responses, rate limiting
  
- **`api-documentation-standards`** - API docs (Apply to Specific Files)
  - OpenAPI/Swagger specifications
  - API versioning

### Data (`data/`)
Data management:

- **`data-schemas-and-interfaces`** - Data schemas (Apply Intelligently)
  - Pydantic models, type hints
  - Structured interfaces
  
- **`data-migration-and-compatibility`** - Migrations (Apply to Specific Files)
  - Alembic migrations
  - Backward compatibility

### Evaluation (`evaluation/`)
LLM evaluation and testing:

- **`llm-evaluation-and-metrics`** - Evaluation metrics (Apply to Specific Files)
  - Faithfulness, relevance, precision
  - Golden datasets
  
- **`llm-judge-protocol`** - LLM judging (Apply Intelligently)
  - Supreme AI Adjudicator protocol
  - Evaluation rubric and structured output
  
- **`final-review-protocol`** - Final review (Always Apply)
  - Pre-commit compliance checks
  - Governance verification

### Configuration (`configuration/`)
Configuration and setup:

- **`configuration-and-dependency-injection`** - DI patterns (Apply Intelligently)
  - Pydantic settings
  - Dependency injection patterns
  
- **`prompt-engineering-and-management`** - Prompt management (Apply to Specific Files)
  - Prompt as code
  - Versioning and templating

### Management Rules

- **`rules-management`** - Meta-rule for managing rules (Apply to Specific Files)
  - Automatically applied when working on `RULE.md` files
  - Complete guide for creating/updating rules
  
- **`commands-management`** - Meta-rule for managing commands (Apply to Specific Files)
  - Automatically applied when working on command files
  - Complete guide for creating/updating commands

## How to Use

### Option 1: Copy Everything

Simply copy the entire `.cursor/rules` folder to your project:

```bash
cp -r .cursor/rules /path/to/your/project/.cursor/
```

Cursor will automatically select which rules to apply based on their configuration.

### Option 2: Copy by Category

Copy only the category folders you need for your project:

- **All projects**: Copy `core/` and `security/`
- **Agent projects**: Also copy `agents/` and `evaluation/`
- **API projects**: Also copy `api/`
- **Production projects**: Also copy `infrastructure/`

### Option 3: Copy Individual Rules

Copy specific rule folders based on your needs:

```bash
cp -r .cursor/rules/core/core-python-standards /path/to/your/project/.cursor/rules/core/
```

## Creating and Updating Rules

The `rules-management` rule is automatically applied when you work on `RULE.md` files. It provides complete guidance on:

- Rule file format and structure
- Frontmatter configuration for each rule type
- Step-by-step creation process
- Best practices and validation

You can also manually apply it:

```
@rules-management create a new rule for database patterns
```

See [`.cursor/rules/rules-management/RULE.md`](rules-management/RULE.md) for the complete guide.

## Integration with Commands

Rules are referenced in Commands through the "Rules Applied" section. Commands use Rules to:

- Apply consistent standards and best practices
- Ensure compliance with governance requirements
- Provide comprehensive analysis based on project rules

Rules are automatically applied based on their type - you don't need to manually activate them in commands.

## Best Practices

1. **Keep Rules Focused** - Each rule should cover one specific domain
2. **Length Limit** - Keep rules under 500 lines (split if larger)
3. **Be Actionable** - Provide concrete, actionable guidance
4. **Reference, Don't Copy** - Use `@filename` to reference files instead of copying content
5. **Clear Structure** - Use markdown headers for organization

## Related Documentation

- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Rules Management Guide](rules-management/RULE.md) - How to create/update rules
- [Commands Documentation](../commands/README.md) - How commands use rules
- [Main README](../../README.md) - Project overview
