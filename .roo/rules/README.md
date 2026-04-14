# Rules documentation (Roo Code & Cursor)

This tree is the **Roo Code** workspace copy of the rules (`.roo/rules/`). The same topics also exist under `.cursor/rules/` for **Cursor** (`.mdc` rules with frontmatter). Rules define coding standards, architectural patterns, security requirements, and development workflows.

## What are these rules?

For **Roo Code**, custom instructions are plain Markdown/text under `.roo/rules/` (recursive load, merged into the system prompt). For **Cursor**, rules use `.mdc` files with YAML frontmatter (`description`, `alwaysApply`, `globs`, etc.). This repository keeps both layouts in sync for tooling used in different editors.

Rules are included at the start of the model context, giving the AI consistent guidance for generating code, interpreting edits, or helping with workflows.

## Directory Structure

Rules in this repository are organized by category:

```
.roo/rules/
├── core/              # Always-applied core rules (Python standards, error handling)
├── security/          # Security and governance rules (manual @ when relevant)
├── agents/            # Agent-specific rules (multi-agent, LangGraph, agentic logic)
├── infrastructure/    # Deployment, monitoring, performance
├── development/       # Testing, code review, versioning
├── api/               # API-related rules
├── data/              # Data schemas, migrations
├── configuration/     # Configuration, dependency injection, prompts
├── reference-for-commands-and-skills/  # Specs for Commands/Skills only — do not @ manually
│   ├── evaluation/    # e.g. llm-evaluation-and-metrics
│   └── security/      # e.g. audit-protocol
├── rules-management/ # Meta-rule for managing rules
└── commands-management/ # Meta-rule for managing commands
```

### Rule Folder Structure

Each rule is a **folder** containing a `RULE.mdc` file:

```
.roo/rules/
  category-name/
    rule-name/
      RULE.mdc
```

**Important:**
- Each rule must be in its own folder
- The folder name should be kebab-case (e.g., `core-python-standards`)
- The file inside must be named exactly `RULE.mdc` (capital letters, `.mdc` extension)

## Rule Types

Rules are applied automatically based on their type, defined in the YAML frontmatter at the start of each `RULE.mdc` file:

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
- `core-python-standards` - Python coding standards
- `error-handling-and-resilience` - Error handling patterns
- `security-governance-and-observability` - Agent policy + pointers (no duplicate specs)

### 2. Apply Intelligently

Applied when the Agent decides it's relevant based on the description.

**Frontmatter:**
```yaml
---
description: "Clear description of what this rule covers"
alwaysApply: false
---
```

**Use when:** The rule is contextually relevant but not always needed (e.g., API documentation when working on APIs, multi-agent patterns when building agents).

**Examples:**
- `code-review-and-collaboration` - Code review standards
- `multi-agent-systems` - Multi-agent architecture patterns
- `contract-scope-and-boundaries` - When to define explicit API contracts
- `redis-cache` - Redis data structures and usage patterns
- `oracle-database` - Oracle DB bind variables and bulk operations

### 3. Apply to Specific Files

Applied when working on files that match the specified glob patterns.

**Frontmatter:**
```yaml
---
globs: **/api/**/*.py, **/routes/**/*.py
alwaysApply: false
---
```

**Use when:** The rule is only relevant for specific file types or locations.

**Examples:**
- `api-documentation-standards` - Applied when working on API files
- `api-interface-and-streaming` - Applied when working on API routes
- `tests-and-validation` - Applied when working on test files
- `langgraph-architecture-and-nodes` - Applied when working on LangGraph nodes

### 4. Apply Manually

Applied only when explicitly mentioned in chat (e.g., `@rule-name`).

**Frontmatter:**
```yaml
---
alwaysApply: false
---
```

**Use when:** The rule is rarely needed and should only be applied on demand (e.g., special audit protocols, meta-rules).

**Note:** Currently, no rules use this type. Meta-rules (`rules-management`, `commands-management`) use "Apply to Specific Files" instead.

## How Rules Are Applied

1. **Always Apply rules** are automatically included in every chat session
2. **Apply Intelligently rules** are considered by the Agent based on the conversation context and the rule's description
3. **Apply to Specific Files rules** are automatically included when you're working on files matching the glob patterns
4. **Apply Manually rules** are only included when you explicitly mention them (e.g., `@rule-name`)

The Agent combines relevant rules to provide comprehensive guidance for your specific task.

## Rule Categories

### Core Rules (`core/`)

Essential rules for all projects:

- **`core-python-standards`** (Always Apply)
  - Python coding standards, best practices, and methodology
  - System planning, code generation, and review processes

- **`error-handling-and-resilience`** (Always Apply)
  - Error handling patterns and resilience strategies
  - Blast radius containment and failure recovery

### Security Rules (`security/`)

Security and governance:

- **`security-governance-and-observability`** (Always Apply)
  - Agent security **policy** + routing table to other rules (no duplicated Splunk/sanitization/eval specs)
  - Details: `@prompt-injection-prevention`, `@cost-and-budget-management`, `@api-interface-and-streaming`, `@human-in-the-loop-approval`, `@monitoring-and-observability`, `@audit-protocol`, `@llm-evaluation-and-metrics`

- **`prompt-injection-prevention`** (Apply to Specific Files — `**/api/**/*.py`, `**/routes/**/*.py`, `**/main.py`, `**/agents/**/*.py`)
  - Sanitize and validate user input before prompts; detect and log injection attempts

### Agent Rules (`agents/`)

Agent-specific architecture:

- **`multi-agent-systems`** (Apply to Specific Files — `**/agents/**/*.py`, `**/langgraph/**/*.py`, `**/workflows/**/*.py`)
  - Multi-agent system architecture patterns
  - Orchestrator/Worker/Synthesizer patterns
  - Micro-agents over monolith principle

- **`contract-scope-and-boundaries`** (Apply to Specific Files — `**/agents/**/*.py`, `**/interfaces/**/*.py`, `**/schemas/**/*.py`, `**/contracts/**/*.py`)
  - When to define explicit API contracts vs implicit contracts
  - Boundary points, replaceability test, avoiding over-engineering

- **`agent-component-interfaces`** (Apply to Specific Files — `**/agents/**/*.py`, `**/interfaces/**/*.py`, `**/contracts/**/*.py`, `**/schemas/**/*.py`)
  - ABCs / Protocol for Planner, Memory Node, Executor; Pydantic v2 at boundaries
  - Splunk HEC for cross-component spans (`correlation_id`, `operation_name`); no `print()` logging
  - Summary table + pointers; full patterns in `@examples_*.py`

- **`planner-strategic-planning`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/nodes/**/*.py`)
  - Strategic goal setting and action planning
  - Risk assessment before task decomposition

- **`executor-action-translation`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/nodes/**/*.py`)
  - Translates strategic plans to concrete actions
  - Action execution and coordination

- **`memory-feedback-node`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/nodes/**/*.py`)
  - Memory Node for historical context and learning feedback
  - Applied to LangGraph/workflow/node files

- **`memory-and-archival-management`** (Apply to Specific Files — `**/memory/**/*.py`, `**/agents/**/*.py`, `**/repositories/**/*.py`)
  - Long-term memory and archival strategies

- **`langgraph-architecture-and-nodes`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/nodes/**/*.py`)
  - LangGraph workflow architecture; node structure (READ → DO → WRITE → CONTROL)
  - Pydantic v2 + LangChain (`with_structured_output` / `bind_tools`) in the DO phase
  - Applied to LangGraph node files

- **`agentic-logic-and-tools`** (Apply to Specific Files — `**/agents/**/*.py`, `**/tools/**/*.py`, `**/chains/**/*.py`)
  - LCEL, `@tool`, Pydantic v2 bindings; Splunk HEC for traces (no `print()` logging)

- **`cost-and-budget-management`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/agents/**/*.py`)
  - Token budget and cost guardrails

- **`context-compression-and-optimization`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/agents/**/*.py`)
  - Context window compression and optimization
  - Applied to LangGraph/workflow/agent files

- **`human-in-the-loop-approval`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/agents/**/*.py`)
  - Approval context schema for HITL interrupts

- **`model-routing-and-selection`** (Apply to Specific Files — `**/agents/**/*.py`, `**/langgraph/**/*.py`, `**/services/**/*.py`)
  - Dynamic model routing based on task complexity

- **`reflection-and-self-critique`** (Apply to Specific Files — `**/langgraph/**/*.py`, `**/workflows/**/*.py`, `**/nodes/**/*.py`)
  - Self-critique and reflection patterns for quality assurance

### Infrastructure Rules (`infrastructure/`)

Deployment and operations:

- **`deployment-and-infrastructure`** (Apply Intelligently)
  - CI/CD, Docker, Kubernetes standards
  - Infrastructure deployment patterns
  - Docker is the **default** for containerization; defaults include full Python base image (pinned), non-root, image scanning in CI, layer cache order, API-only (no model weights when using external APIs), logging to stdout/stderr, Docker Compose for local multi-service dev, BuildKit, and versioned registry

- **`monitoring-and-observability`** (Apply Intelligently)
  - **Splunk HEC** as the single destination for all metrics, logs, and traces (direct HTTP POST, no stdout pipeline)
  - Mandatory event fields: `timestamp`, `correlation_id`, `operation_name`; timed operations add `duration_ms`
  - Use `@splunk-instrumentation` skill to add HEC instrumentation to existing code on demand

- **`redis-cache`** (Apply Intelligently)
  - Redis data structures: when to use strings, hashes, sorted sets, lists, sets
  - TTL, serialization with orjson

- **`oracle-database`** (Apply Intelligently)
  - Bind variables (`:param` syntax) for cached execution plans and SQL injection prevention
  - Bulk operations with `executemany()` instead of looped `execute()`

- **`multi-tenancy-and-isolation`** (Apply Intelligently)
  - Multi-tenant architecture patterns
  - Data isolation strategies

### Development Rules (`development/`)

Development workflow:

- **`tests-and-validation`** (Apply to Specific Files)
  - Testing framework standards
  - Validation requirements
  - Applied to test files

- **`code-review-and-collaboration`** (Apply Intelligently)
  - Code review standards
  - Git workflow and collaboration practices

- **`versioning-and-release-management`** (Apply Intelligently)
  - Semantic versioning standards
  - Changelog and release management

- **`gitflow-branching-model`** (Apply Intelligently)
  - GitFlow branching model: master, develop, release, hotfix, feature workflow
  - When to push or merge to each branch

### API Rules (`api/`)

API development:

- **`api-interface-and-streaming`** (Apply to Specific Files)
  - FastAPI as default framework; Uvicorn with `uvicorn[standard]` (uvloop, httptools, watchfiles)
  - Pydantic, OpenAPI, SSE/WebSocket streaming, rate limiting (slowapi/fastapi-limiter)
  - Applied to API route files and `main.py`

- **`api-documentation-standards`** (Apply to Specific Files)
  - OpenAPI/Swagger specifications
  - API documentation requirements
  - Applied to API files

- **`mcp-protocol-implementation`** (Apply Intelligently)
  - Model Context Protocol (MCP) servers and clients
  - Dynamic tool management

### Data Rules (`data/`)

Data management:

- **`data-schemas-and-interfaces`** (Apply Intelligently)
  - Pydantic schemas and data models
  - Structured interfaces and validation
  - References `contract-scope-and-boundaries` for when to define schemas

- **`data-migration-and-compatibility`** (Apply to Specific Files)
  - Data migration patterns
  - Compatibility and versioning strategies
  - Applied to migration files

### Reference rules (`reference-for-commands-and-skills/`)

Authoritative rules for **Commands** and **Skills** only — **do not** `@` manually in chat; invoke the workflow that applies them.

- **`audit-protocol`** (`security/audit-protocol/`) — Mandatory audit events, audit-specific fields, PII masking. Applied via **`@splunk-instrumentation`** and security/monitoring commands; complements `@monitoring-and-observability`.

- **`llm-evaluation-and-metrics`** (`evaluation/llm-evaluation-and-metrics/`) — Eval metrics, Splunk reporting. Applied via **`@evaluate-with-llm-judge`** and evaluation commands; globs: `**/evals/**/*.py`, `**/evaluation/**/*.py`.

- **LLM-as-a-Judge** — **not** a separate rule file; canonical workflow is the Skill **`@evaluate-with-llm-judge`** (`.roo/skills/evaluate-with-llm-judge/SKILL.md`).

### Configuration Rules (`configuration/`)

Configuration and setup:

- **`configuration-and-dependency-injection`** (Apply Intelligently)
  - Configuration management using pydantic-settings
  - Dependency injection patterns

- **`prompt-engineering-and-management`** (Apply to Specific Files)
  - Prompt engineering standards
  - Prompt management and versioning
  - Applied to prompt files (`**/prompts/**/*.py`, `**/prompts/**/*.yaml`, `**/prompts/**/*.txt`)

### Meta-Rules

Rules for managing rules and commands:

- **`rules-management`** (Apply to Specific Files)
  - Format and structure for creating/updating Rules
  - Applied when working on `RULE.mdc` files
  - References: `helper-files-guide`, `frontmatter-reference`

- **`commands-management`** (Apply to Specific Files)
  - Format and structure for creating/updating Commands
  - Applied when working on command files (`.roo/commands/**/*.md`)

## Usage

### Copying Rules to Your Project

#### Option 1: Copy Everything
Copy the entire `.roo` folder (or at least `.roo/rules`) into your project root. **Roo Code** loads `.roo/rules/**/*.md` as custom instructions (see [Custom Instructions](https://docs.roocode.com/features/custom-instructions)). Rule **types** (always / globs / intelligent) are a **Cursor** concept for `.mdc` files; in Roo, split content by mode using `.roo/rules-{mode}/` if needed.

#### Option 2: Copy by Category
Copy only the category folders you need:

**For all projects:**
- `core/` - Essential coding standards
- `security/` - Security and governance

**For agent projects:**
- `agents/` - Multi-agent patterns
- `evaluation/` - LLM evaluation

**For API projects:**
- `api/` - API design and documentation

**For production projects:**
- `infrastructure/` - Deployment and monitoring

### Rule Application Examples

**Example 1: Working on API code**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `api-interface-and-streaming` (Apply to Specific Files) - Active (matches `**/api/**/*.py`)
- `api-documentation-standards` (Apply to Specific Files) - Active (matches `**/api/**/*.py`)

**Example 2: Working on test files**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `tests-and-validation` (Apply to Specific Files) - Active (matches test files)

**Example 3: Building a multi-agent system**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `multi-agent-systems` (Apply Intelligently) - Considered (relevant to conversation)
- `langgraph-architecture-and-nodes` (Apply to Specific Files) - Active (if working on node files)

## Creating and updating rules

- **In this repo (Roo layout):** each topic folder contains one Markdown file named `{topic}.md` (for example `infrastructure/redis-cache/redis-cache.md`). Do **not** put YAML frontmatter in Roo rule files unless you intend it to appear as plain text in the prompt.
- **Cursor layout:** authoritative authoring for `.mdc` metadata (`alwaysApply`, `globs`, etc.) still lives under [`.roo/rules/`](../../.roo/rules/). To refresh `.roo/rules/` from `.roo/rules/`, run `python scripts/migrate_to_roo.py` from the repository root.

## Rule file format (Roo)

1. **Body** — Markdown sections (mandate, tables, examples).
2. **Helper examples** — optional `examples_*.py` (or other) files alongside the rule; Roo does not execute them, but the model can read them when referenced.

## Integration with Commands

Rules work together with Commands (`.roo/commands/`) to provide comprehensive workflows:

- **Rules** define standards and patterns that guide the AI's behavior
- **Commands** define workflows that use these standards
- Commands reference Rules in their "Rules Applied" section
- The Agent automatically applies relevant Rules when executing Commands

For example, the `/testing-run-test-suite` command references `tests-and-validation` and `core-python-standards` rules. When you run the command, the Agent automatically applies these rules (if they match the rule type criteria).

## Best Practices

1. **Use Appropriate Rule Types**: Choose the right type based on when the rule should be active
2. **Keep Rules Focused**: Each rule should cover a specific domain or concern
3. **Use Clear Descriptions**: For "Apply Intelligently" rules, write clear, specific descriptions
4. **Use Specific Glob Patterns**: For "Apply to Specific Files" rules, use precise glob patterns
5. **Update Rules Regularly**: Keep rules updated as standards and requirements evolve
6. **Test Rule Application**: Verify that rules are applied correctly in different contexts

## Related Documentation

- **[Root README](../README.md)** - Overview of the entire repository
- **[README_HE.md](README_HE.md)** - Hebrew documentation: what each rule says, when to use it, which libraries it defines (quick reference + full sections)
- **[Slash commands documentation](../commands/slash-commands-documentation.md)** - Roo Code commands index
- **[Commands management (Roo)](commands-management/commands-management.md)** — Slash command structure and duplication policy
- **[Commands management (Cursor)](../../.roo/rules/commands-management/RULE.mdc)** — Same policy for `.roo/commands` path style
- **[Cursor Rules Documentation](https://cursor.com/docs/context/rules)** - Official Cursor documentation
