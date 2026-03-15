# Amazon Q Developer Rules Documentation

This directory contains **project rules for Amazon Q Developer**: Markdown files that describe coding standards, architectural patterns, security requirements, and development workflows. Amazon Q loads these rules automatically when you chat in the project, so the assistant follows your team's conventions without repeating instructions.

## What are Amazon Q project rules?

Rules are stored under `.amazonq/rules` as **Markdown (`.md`)** files. Amazon Q Developer scans this folder and uses the rules as context for code generation, edits, and workflows. There is no YAML frontmatter; use the structure described in **rules-management/amazon-q-developer-rules-guide.md** (Purpose, Instructions, Priority, Error Handling). Code examples belong in separate files (e.g. `examples_*.py`) in the same folder as the rule; reference them in the rule text and add them to chat context when needed.

## Directory Structure

Rules are organized by category:

```
.amazonq/rules/
├── core/              # Core rules (Python standards, error handling)
├── security/          # Security and governance rules
├── agents/            # Agent-specific rules (multi-agent, LangGraph, agentic logic)
├── infrastructure/    # Deployment, monitoring, performance
├── development/      # Testing, code review, versioning
├── api/               # API-related rules
├── data/              # Data schemas, migrations
├── evaluation/        # LLM evaluation, judging, auditing
├── configuration/     # Configuration, dependency injection, prompts
├── rules-management/   # Meta-rule and amazon-q-developer-rules-guide.md
└── commands-management/
```

### Rule folder structure

Each rule lives in a **folder** with a `RULE.md` file and optional example files:

```
.amazonq/rules/
  category-name/
    rule-name/
      RULE.md
      examples_*.py    # optional
```

- Folder name: kebab-case (e.g. `core-python-standards`)
- Rule file: `RULE.md` (Markdown only; no frontmatter)
- For how to write and reference example files, see **rules-management/amazon-q-developer-rules-guide.md**

## Rule Categories

Amazon Q loads all `.md` rules from `.amazonq/rules`; you can turn individual rules on or off in the IDE chat. Below are the rule categories and main topics.

### Core Rules (`core/`)

- **`core-python-standards`** – Python coding standards, best practices, methodology, system planning, code generation, and review processes
- **`error-handling-and-resilience`** – Error handling patterns, resilience strategies, blast radius containment, failure recovery

### Security Rules (`security/`)

- **`security-governance-and-observability`** – Security standards, governance, OWASP LLM, NIST AI RMF
- **`audit-protocol`** – Audit procedures, compliance, tool call and state change auditing, LLM operation auditing
- **`prompt-injection-prevention`** – Prompt injection prevention and input sanitization

### Agent Rules (`agents/`)

- **`multi-agent-systems`** – Multi-agent architecture, Orchestrator/Worker/Synthesizer, micro-agents over monolith
- **`contract-scope-and-boundaries`** – When to define explicit API contracts vs implicit; boundary points, replaceability test
- **`agent-component-interfaces`**
  - API contracts between Planner, Memory, Executor
  - ABC interfaces and implementation swapping

- **`planner-strategic-planning`**  - Strategic goal setting and action planning
  - Risk assessment before task decomposition

- **`executor-action-translation`**  - Translates strategic plans to concrete actions
  - Action execution and coordination

- **`memory-feedback-node`**  - Memory Node for historical context and learning feedback
  - Applied to LangGraph/workflow/node files

- **`memory-and-archival-management`**  - Long-term memory and archival strategies

- **`langgraph-architecture-and-nodes`**  - LangGraph workflow architecture
  - Node structure (READ → DO → WRITE → CONTROL)
  - Applied to LangGraph node files

- **`agentic-logic-and-tools`**  - LangChain fundamentals and tool definitions
  - Agent internals and tool implementation

- **`cost-and-budget-management`**  - Token budget and cost guardrails

- **`context-compression-and-optimization`**  - Context window compression and optimization
  - Applied to LangGraph/workflow/agent files

- **`human-in-the-loop-approval`**  - Approval context schema for HITL interrupts

- **`model-routing-and-selection`**  - Dynamic model routing based on task complexity

- **`reflection-and-self-critique`**  - Self-critique and reflection patterns for quality assurance

### Infrastructure Rules (`infrastructure/`)

- **`uvicorn-asgi-server`** – Uvicorn as default ASGI server; `uvicorn[standard]`; `--reload` (dev), `--workers` (prod)
- **`deployment-and-infrastructure`** – CI/CD, Docker, Kubernetes; containerization defaults (non-root, image scanning, stdout/stderr logging, Docker Compose, BuildKit)
- **`monitoring-and-observability`** – Splunk and SPL for metrics, logging, tracing, alerting; HEC ingestion; PerformanceTimer
- **`rate-limiting-and-queue-management`** – Multi-agent rate limiting, queue management, API key protection, exponential backoff
- **`performance-optimization`** – Caching, query optimization, resource pooling
- **`multi-tenancy-and-isolation`** – Multi-tenant architecture, data isolation strategies

### Development Rules (`development/`)

- **`tests-and-validation`** – Testing framework standards, validation requirements
- **`code-review-and-collaboration`** – Code review standards, Git workflow
- **`versioning-and-release-management`** – Semantic versioning, changelog, release management
- **`gitflow-branching-model`** – GitFlow: master, develop, release, hotfix, feature workflow

### API Rules (`api/`)

- **`api-interface-and-streaming`** – FastAPI, Uvicorn, Pydantic, OpenAPI, SSE/WebSocket; rate limiting (slowapi/fastapi-limiter)
- **`api-documentation-standards`** – OpenAPI/Swagger, API documentation requirements
- **`mcp-protocol-implementation`** – Model Context Protocol (MCP) servers and clients, dynamic tool management

### Data Rules (`data/`)

- **`data-schemas-and-interfaces`** – Pydantic schemas, data models, structured interfaces and validation
- **`data-migration-and-compatibility`** – Data migration patterns, compatibility and versioning

### Evaluation Rules (`evaluation/`)

- **`llm-evaluation-and-metrics`** – LLM evaluation frameworks, metrics and scoring

- **`llm-judge-protocol`**  - LLM-as-a-Judge evaluation protocol
  - Performance, safety, and logic analysis

- **`graph-traversal-testing`**  - Graph traversal tests for agent workflow paths
  - Node sequence validation

- **`simulation-and-property-testing`**  - Property-based and chaos testing
  - Edge case simulation

- **`bias-detection-and-ethics`**  - Bias detection and ethical AI practices

- **`final-review-protocol`** (Always Apply)
  - Final review process before commit
  - Compliance verification

### Configuration Rules (`configuration/`)

Configuration and setup:

- **`configuration-and-dependency-injection`**  - Configuration management using pydantic-settings
  - Dependency injection patterns

- **`prompt-engineering-and-management`**  - Prompt engineering standards
  - Prompt management and versioning
  - Applied to prompt files (`**/prompts/**/*.py`, `**/prompts/**/*.yaml`, `**/prompts/**/*.txt`)

### Meta-Rules

Rules for managing rules and commands:

- **`rules-management`**  - Format and structure for creating/updating Rules
  - Applied when working on `RULE.mdc` files
  - References: `helper-files-guide`, `frontmatter-reference`

- **`commands-management`**  - Format and structure for creating/updating Commands
  - Applied when working on command files (`.cursor/commands/**/*.md`)

## Usage

### Copying Rules to Your Project

#### Option 1: Copy Everything
Copy the entire `.cursor/rules` folder to your project root. Cursor will automatically:
- Apply "Always Apply" rules to every session
- Apply "Apply to Specific Files" rules when working on matching files
- Consider "Apply Intelligently" rules based on context

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
- `api-interface-and-streaming` - Active (matches `**/api/**/*.py`)
- `api-documentation-standards` - Active (matches `**/api/**/*.py`)

**Example 2: Working on test files**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `tests-and-validation` - Active (matches test files)

**Example 3: Building a multi-agent system**
- `core-python-standards` (Always Apply) - Active
- `error-handling-and-resilience` (Always Apply) - Active
- `multi-agent-systems` - Considered (relevant to conversation)
- `langgraph-architecture-and-nodes` - Active (if working on node files)

## Creating and Updating Rules

When creating or updating Rules, follow the format defined in `.cursor/rules/rules-management/RULE.mdc`:

1. **Choose the appropriate category** folder
2. **Create the folder structure**: `category-name/rule-name/RULE.mdc`
3. **Write the frontmatter** based on the rule type:
   - Always Apply: `alwaysApply: true`
   - Apply Intelligently: `description: "..."` and `alwaysApply: false`
   - Apply to Specific Files: `globs: "pattern1, pattern2"` and `alwaysApply: false`
   - Apply Manually: `alwaysApply: false` (no description or globs)
4. **Write the rule content** following the structure and format guidelines
5. **Use helper files** for code examples (see `helper-files-guide`)

See `.cursor/rules/rules-management/RULE.mdc` for detailed format specifications and examples.

## Rule File Format

Every `RULE.mdc` file must follow this structure:

1. **Frontmatter** (YAML between `---` markers)
   - Defines rule type and application behavior
   - Must be at the very start of the file

2. **Rule Content** (Markdown)
   - Mandate/Overview section
   - Detailed guidelines and standards
   - Examples via `@examples_*.py` helper files (keep rules under 400 lines)

See `.cursor/rules/rules-management/RULE.mdc` for complete format specifications.

## Integration with Commands

Rules work together with Commands (`.cursor/commands/`) to provide comprehensive workflows:

- **Rules** define standards and patterns that guide the AI's behavior
- **Commands** define workflows that use these standards
- Commands reference Rules in their "Rules Applied" section
- The Agent automatically applies relevant Rules when executing Commands

For example, the `/testing/run-test-suite` command references `tests-and-validation` and `core-python-standards` rules. When you run the command, the Agent automatically applies these rules (if they match the rule type criteria).

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
- **[Commands Documentation](../commands/README.md)** - Complete guide to Cursor Commands
- **[Rules Management Rule](rules-management/RULE.mdc)** - Format specifications for creating/updating rules
- **[Helper Files Guide](rules-management/helper-files-guide/RULE.mdc)** - Using helper files for code examples
- **[Frontmatter Reference](rules-management/frontmatter-reference/RULE.mdc)** - Frontmatter templates for all rule types
- **[Commands Management Rule](commands-management/RULE.mdc)** - Format specifications for creating/updating commands
- **[Cursor Rules Documentation](https://cursor.com/docs/context/rules)** - Official Cursor documentation
