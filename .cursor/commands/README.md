# Cursor Commands Documentation

This directory contains custom commands for the Cursor AI agent. Commands are reusable workflows that can be triggered with a `/` prefix in the chat input box, providing standardized processes for development, testing, security, review, monitoring, and agent development.

## What are Cursor Commands?

Cursor Commands are plain Markdown files that describe workflows and tasks. They integrate with the project's Rules (`.cursor/rules`) to provide comprehensive, standardized processes. Commands help:

- **Standardize workflows** across your team
- **Automate repetitive tasks** with consistent processes
- **Ensure compliance** with project rules and standards
- **Provide reusable templates** for common development tasks

Commands are stored in three locations:
1. **Project commands**: Stored in `.cursor/commands` directory (version-controlled)
2. **Global commands**: Stored in `~/.cursor/commands` directory (user-specific)
3. **Team commands**: Created by team admins in the Cursor Dashboard (team-wide)

## Directory Structure

```
.cursor/commands/
├── testing/          # Testing and evaluation commands
│   ├── write-targeted-tests.md
│   ├── run-test-suite.md
│   └── run-evaluation-suite.md
├── security/         # Security audit commands
│   ├── security-audit.md
│   └── analyze-audit-logs.md
├── review/           # Code review and compliance check commands
│   ├── code-review-checklist.md
│   └── final-compliance-check.md
├── monitoring/       # Monitoring and observability commands
│   ├── analyze-langsmith-traces.md
│   ├── comprehensive-system-analysis.md
│   ├── performance-analysis.md
│   ├── audit-prompt-registry-splunk.md
│   ├── profile-code-bottlenecks.md
│   └── run-all-monitoring.md (Master Command)
├── agents/          # Agent development commands
│   ├── setup-new-agent-system.md
│   ├── create-agent-node.md
│   ├── implement-agent-tool.md
│   └── run-all-agents.md (Master Command)
└── README.md        # This file
```

### Command File Structure

Each command is a **markdown file** (`.md`) in the appropriate category directory:

```
.cursor/commands/
  category-name/
    command-name.md
```

**Important:**
- Commands are plain markdown files (`.md` extension)
- No frontmatter (unlike Rules)
- File name = command name (kebab-case)
- Command path = `/category-name/command-name`

## Command Categories

### 1. Testing Commands (`/testing/`)

Testing and evaluation workflows for ensuring code quality and functionality.

#### `/testing/write-targeted-tests`
Systematically identify new or modified code and automatically generate comprehensive, targeted test cases following project testing standards. Ensures every new feature, function, or code change has corresponding test coverage. Includes test generation, coverage analysis, and test execution validation.

**Rules Applied**: `tests-and-validation`, `core-python-standards`, `error-handling-and-resilience`, `monitoring-and-observability`

#### `/testing/run-test-suite`
Execute the full test suite and systematically analyze results, identify failures, and provide actionable recommendations. Includes test coverage analysis and performance metrics collection.

**Rules Applied**: `tests-and-validation`, `core-python-standards`, `error-handling-and-resilience`, `monitoring-and-observability`

#### `/testing/run-evaluation-suite`
Execute the complete LLM evaluation suite using specialized evaluation frameworks (Ragas, DeepEval, LangSmith). Includes evaluation framework validation, cost tracking, and comparison with previous evaluations.

**Rules Applied**: `llm-evaluation-and-metrics` (reference; commands/skills), `monitoring-and-observability`, `data-schemas-and-interfaces`, `error-handling-and-resilience`, `cost-and-budget-management`

#### `@evaluate-with-llm-judge` (Skill)
**Migrated to Skill** (`.cursor/skills/evaluate-with-llm-judge/SKILL.md`). Trigger with `@evaluate-with-llm-judge`. Comprehensive LLM-as-a-Judge evaluation with weighted rubric, chain-of-thought reasoning, and structured JSON verdict.

### 2. Security Commands (`/security/`)

Security review and audit-log analysis aligned with `.cursor/rules/security` (`security-governance-and-observability`, `prompt-injection-prevention`) and related cross-cutting Rules. For a **broad governance pass** against all active Rules (not only security), use `/review/final-compliance-check`.

#### `/security/analyze-audit-logs`
Analysis of audit logs for incidents, anomalies, and traceability, aligned with governance and observability expectations (structured fields, correlation). Not a substitute for legal/regulatory compliance attestation.

**Rules Applied**: `security-governance-and-observability`, `monitoring-and-observability`, `error-handling-and-resilience`, `human-in-the-loop-approval`, `audit-protocol` (reference; commands/skills)

#### `/security/security-audit`
Comprehensive security review: dependencies, OWASP Top 10 for LLM applications, infrastructure, and integration with `/security/analyze-audit-logs`. Maps findings to current security Rules and observability expectations.

**Rules Applied**: `security-governance-and-observability`, `prompt-injection-prevention`, `configuration-and-dependency-injection`, `data-schemas-and-interfaces`, `error-handling-and-resilience`, `monitoring-and-observability`, `api-interface-and-streaming`

### 3. Review Commands (`/review/`)

Code review and compliance check workflows.

#### `/review/code-review-checklist`
Comprehensive code review using a structured checklist to ensure code quality, functionality, testing, documentation, security, and maintainability. Includes comprehensive checklist with all standards, automated checks, and review approval workflow.

**Rules Applied**: `core-python-standards`, `error-handling-and-resilience`, `tests-and-validation`, `security-governance-and-observability`, `prompt-injection-prevention`, `data-schemas-and-interfaces`, `monitoring-and-observability`

#### `/review/final-compliance-check`
Governance pass before commit: map changes to applicable Rules; uses `/review/code-review-checklist` output without duplicating it. Produces a compliance matrix by domain.

**Rules Applied**: `core-python-standards`, `error-handling-and-resilience`, `tests-and-validation`, `langgraph-architecture-and-nodes`, `multi-agent-systems`, `configuration-and-dependency-injection`, `prompt-engineering-and-management`, `data-schemas-and-interfaces`, `api-interface-and-streaming`, `api-documentation-standards`, `monitoring-and-observability`, `security-governance-and-observability`, `prompt-injection-prevention`, `agentic-logic-and-tools`, `human-in-the-loop-approval`, `cost-and-budget-management`, `llm-evaluation-and-metrics` (reference; commands/skills)

### 4. Monitoring Commands (`/monitoring/`)

Monitoring and observability analysis workflows.

#### `/monitoring/analyze-langsmith-traces`
Comprehensive analysis of LangSmith traces to understand LLM operations, tool usage, agent behavior, and performance. Includes cost optimization recommendations, model selection analysis, and token usage optimization.

**Rules Applied**: `monitoring-and-observability`, `agentic-logic-and-tools`, `error-handling-and-resilience`, `cost-and-budget-management`, `model-routing-and-selection`

#### `/monitoring/performance-analysis`
Comprehensive performance analysis to identify bottlenecks, optimize resource usage, and improve system efficiency. Includes SLI/SLO compliance checks, capacity planning recommendations, and performance regression detection.

**Rules Applied**: `monitoring-and-observability`, `core-python-standards`, `error-handling-and-resilience`, `api-interface-and-streaming`, `redis-cache`

#### `/monitoring/profile-code-bottlenecks`
Run a code profiler (e.g., `cProfile`) on target code to identify real performance bottlenecks through measurement rather than guessing. Follows the principle that every optimization must start with measurement: profile first, identify 1–2 bottleneck functions, understand their Big-O complexity, then perform targeted refactoring.

**Rules Applied**: `core-python-standards`, `monitoring-and-observability`

#### `/monitoring/comprehensive-system-analysis`
Synthesis across traces, logs, tests, and evaluations—correlates artifacts; does not replace specialized monitoring commands.

**Rules Applied**: `monitoring-and-observability`, `security-governance-and-observability`, `error-handling-and-resilience`, `cost-and-budget-management`, `human-in-the-loop-approval`, `tests-and-validation`, `llm-evaluation-and-metrics` (reference; commands/skills), `audit-protocol` (reference; commands/skills)

#### `/monitoring/audit-prompt-registry-splunk`
Audit prompt registry lifecycle events and Splunk observability signals to validate traceability, governance compliance, and prompt telemetry completeness.

**Rules Applied**: `prompt-engineering-and-management`, `monitoring-and-observability`, `security-governance-and-observability`, `audit-protocol` (reference; commands/skills)

#### `/monitoring/run-all-monitoring` (Master Command)
Runs monitoring subcommands in order (LangSmith → performance → prompt registry/Splunk → comprehensive synthesis). Does not include `profile-code-bottlenecks`.

### 5. Agent Development Commands (`/agents/`)

Agent development and setup workflows.

#### `/agents/setup-new-agent-system`
Systematic setup of a new multi-agent system from initial planning through implementation structure. Includes comprehensive setup checklist, architecture validation, and setup verification steps.

**Rules Applied**: `multi-agent-systems`, `langgraph-architecture-and-nodes`, `agentic-logic-and-tools`, `core-python-standards`, `configuration-and-dependency-injection`, `data-schemas-and-interfaces`, `prompt-engineering-and-management`, `error-handling-and-resilience`, `human-in-the-loop-approval`, `cost-and-budget-management`, `api-interface-and-streaming`

#### `/agents/create-agent-node`
Create a new LangGraph node following the four-part structure (READ → DO → WRITE → CONTROL). Includes node validation checklist, performance considerations, and node testing requirements.

**Rules Applied**: `langgraph-architecture-and-nodes`, `core-python-standards`, `error-handling-and-resilience`, `multi-agent-systems`, `tests-and-validation`, `monitoring-and-observability`, `reflection-and-self-critique`

#### `/agents/implement-agent-tool`
Implement a new tool for agent use following LangChain tool definition standards. Includes tool security validation, tool performance considerations, and tool access control setup.

**Rules Applied**: `agentic-logic-and-tools`, `data-schemas-and-interfaces`, `core-python-standards`, `error-handling-and-resilience`, `security-governance-and-observability`, `tests-and-validation`, `monitoring-and-observability`, `prompt-injection-prevention`

#### `/agents/run-all-agents` (Master Command)
Runs all agent development commands in sequence: setup new agent system → create agent node → implement agent tool. Includes agent system validation, workflow verification, and comprehensive setup report.

## Usage

### Basic Usage

To use a command, type `/` followed by the command path in the Cursor chat input box:

```
/testing/run-test-suite
/security/security-audit
/testing/write-targeted-tests
```

### With Additional Context

You can provide additional context after the command name:

```
/testing/run-test-suite and fix any failures
/security/security-audit focusing on OWASP Top 10
/review/final-compliance-check before merging to main
```

### Master Commands

Master commands execute all commands in a category in the proper sequence:

```
/monitoring/run-all-monitoring
/agents/run-all-agents
```

Master commands:
- Run commands in the correct order with proper dependencies
- Handle errors appropriately (stop on critical failures, continue with warnings)
- Aggregate results from all commands
- Provide comprehensive summary reports
- Can be run independently or as part of a larger workflow

## Command Structure

Each command follows a consistent structure:

1. **`#` Title** — Short heading.
2. **`## Overview`** — What the command does.
3. **`## Scope and boundaries`** — In scope vs out of scope (other `/commands` or Rules).
4. **`## Rules Applied`** — Existing rule folder names under `.cursor/rules/`; reference-only specs labeled per `commands-management`.
5. **`## Steps`** — Workflow; orchestrators defer to subcommands instead of duplicating steps.
6. **`## Data Sources`**
7. **`## Output`**

See `.cursor/rules/commands-management/RULE.mdc` for the full specification and duplication policy.

## Command Dependencies and Overlap Prevention

Commands are designed to avoid duplication:

- **`security-audit`** calls `/security/analyze-audit-logs` instead of duplicating audit log analysis
- **`final-compliance-check`** ingests `/review/code-review-checklist` results and adds cross-cutting governance; it does not repeat the PR checklist

This ensures:
- No redundant checks are performed
- Each command has a clear, focused responsibility
- Results are consistent across commands
- Maintenance is easier (fix once, used everywhere)

## Data Sources

Commands analyze data from various sources:

- **LangSmith Traces**: JSON files containing LLM operation traces
- **Audit Logs**: JSON files containing audit trail events
- **Test Results**: Test execution outputs and coverage reports
- **Evaluation Results**: LLM evaluation metrics and scores
- **Performance Metrics**: System resource usage and performance data
- **Source Code**: Python files, configuration files, documentation

## Integration with Rules

Commands integrate with the project's Rules (`.cursor/rules`) to:

- Apply consistent standards and best practices
- Ensure compliance with governance requirements
- Provide comprehensive analysis based on project rules
- Standardize workflows across the team

**Note:** Commands reference Rules in their "Rules Applied" section, but Rules are applied automatically by the Agent based on their type (Always Apply, Apply Intelligently, Apply to Specific Files). Commands don't directly "call" Rules - the Agent applies relevant Rules when executing commands.

## Best Practices

1. **Use Master Commands for Complete Workflows**: Use master commands (e.g., `/monitoring/run-all-monitoring`) when you need to run all commands in a category. Master commands orchestrate sub-commands in the correct order and aggregate results.
2. **Use Individual Commands for Specific Tasks**: Use individual commands when you need to run a specific check or analysis. Each command can be run independently for focused analysis.
3. **Review Output**: Always review command output and recommendations before taking action. Commands provide detailed reports with prioritized recommendations.
4. **Understand Command Dependencies**: Some commands call other commands (e.g., `security-audit` calls `analyze-audit-logs`). Understanding dependencies helps avoid redundant executions.
5. **Update Commands**: Keep commands updated as Rules and requirements evolve. Commands should reference all relevant rules for comprehensive coverage.
6. **Avoid Duplication**: When creating new commands, check if existing commands can be reused instead of duplicating functionality. Commands are designed to be composable.

## Command Development

When creating or updating commands, follow the format defined in `.cursor/rules/commands-management/RULE.mdc`:

1. Follow the standard command structure (Overview, Scope and boundaries, Rules Applied, Steps, Data Sources, Output)
2. Integrate relevant Rules in the "Rules Applied" section
3. Specify data sources clearly
4. Provide detailed, actionable steps
5. Document expected output
6. Test commands thoroughly
7. Check for overlaps with existing commands and reuse them when possible
8. Use kebab-case for file names
9. Place commands in the appropriate category directory

## Related Documentation

- **[Root README](../README.md)** - Overview of the entire repository
- **[Rules Documentation](../rules/README.md)** - Complete guide to Cursor Rules
- **[Commands Management Rule](../rules/commands-management/RULE.mdc)** - Format specifications for creating/updating commands
- **[Cursor Commands Documentation](https://cursor.com/docs/agent/chat/commands)** - Official Cursor documentation
- **[Cursor Rules Documentation](https://cursor.com/docs/context/rules)** - Official Cursor documentation
