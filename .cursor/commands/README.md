# Cursor Commands Documentation

This directory contains custom commands for the Cursor AI agent. Commands are reusable workflows that can be triggered with a `/` prefix in the chat input box, providing standardized processes for development, testing, security, deployment, and agent development.

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
│   ├── run-test-suite.md
│   ├── run-evaluation-suite.md
│   ├── evaluate-with-llm-judge.md
│   └── run-all-testing.md (Master Command)
├── security/         # Security audit and compliance commands
│   ├── security-audit.md
│   ├── analyze-audit-logs.md
│   ├── compliance-check.md
│   └── run-all-security.md (Master Command)
├── review/           # Code review and compliance check commands
│   ├── code-review-checklist.md
│   ├── final-compliance-check.md
│   └── run-all-review.md (Master Command)
├── monitoring/       # Monitoring and observability commands
│   ├── analyze-langsmith-traces.md
│   ├── comprehensive-system-analysis.md
│   ├── performance-analysis.md
│   └── run-all-monitoring.md (Master Command)
├── deployment/       # Deployment and infrastructure commands
│   ├── pre-deployment-check.md
│   ├── post-deployment-verification.md
│   └── run-all-deployment.md (Master Command)
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

#### `/testing/run-test-suite`
Execute the full test suite and systematically analyze results, identify failures, and provide actionable recommendations.

**Rules Applied**: `tests-and-validation`, `core-python-standards`, `error-handling-and-resilience`

#### `/testing/run-evaluation-suite`
Execute the complete LLM evaluation suite using specialized evaluation frameworks (Ragas, DeepEval, LangSmith).

**Rules Applied**: `llm-evaluation-and-metrics`, `llm-judge-protocol`

#### `/testing/evaluate-with-llm-judge`
Comprehensive evaluation using LLM-as-a-Judge protocol to analyze agent system performance, safety, and logic.

**Rules Applied**: `llm-judge-protocol`, `audit-protocol`, `llm-evaluation-and-metrics`

#### `/testing/run-all-testing` (Master Command)
Runs all testing commands in sequence: test suite → evaluation suite → LLM Judge evaluation.

### 2. Security Commands (`/security/`)

Security audit and compliance verification workflows.

#### `/security/compliance-check`
Comprehensive compliance verification to ensure the system meets regulatory requirements (GDPR, HIPAA, SOC 2).

**Rules Applied**: `audit-protocol`, `security-governance-and-observability`

#### `/security/analyze-audit-logs`
Comprehensive analysis of audit logs to identify security incidents, compliance issues, anomalies, and operational patterns.

**Rules Applied**: `audit-protocol`, `monitoring-and-observability`

#### `/security/security-audit`
Comprehensive security review to identify and fix vulnerabilities in the codebase, infrastructure, and dependencies. Uses results from compliance check and audit log analysis.

**Rules Applied**: `security-governance-and-observability`, `audit-protocol`

#### `/security/run-all-security` (Master Command)
Runs all security commands in sequence: compliance check → audit log analysis → security audit.

### 3. Review Commands (`/review/`)

Code review and compliance check workflows.

#### `/review/code-review-checklist`
Comprehensive code review using a structured checklist to ensure code quality, functionality, testing, documentation, security, and maintainability.

**Rules Applied**: `code-review-and-collaboration`, `core-python-standards`, `final-review-protocol`

#### `/review/final-compliance-check`
Comprehensive final review before commit to verify solution complies with all active governance files and project standards. Uses results from code review checklist.

**Rules Applied**: `final-review-protocol`, all relevant rules

#### `/review/run-all-review` (Master Command)
Runs all review commands in sequence: code review checklist → final compliance check.

### 4. Monitoring Commands (`/monitoring/`)

Monitoring and observability analysis workflows.

#### `/monitoring/analyze-langsmith-traces`
Comprehensive analysis of LangSmith traces to understand LLM operations, tool usage, agent behavior, and performance.

**Rules Applied**: `monitoring-and-observability`, `agentic-logic-and-tools`

#### `/monitoring/performance-analysis`
Comprehensive performance analysis to identify bottlenecks, optimize resource usage, and improve system efficiency.

**Rules Applied**: `performance-optimization`, `monitoring-and-observability`

#### `/monitoring/comprehensive-system-analysis`
Complete cross-system analysis combining all available data sources to provide holistic insights. Uses results from trace and performance analysis.

**Rules Applied**: All relevant rules

#### `/monitoring/run-all-monitoring` (Master Command)
Runs all monitoring commands in sequence: LangSmith trace analysis → performance analysis → comprehensive system analysis.

### 5. Deployment Commands (`/deployment/`)

Deployment and infrastructure verification workflows.

#### `/deployment/pre-deployment-check`
Comprehensive pre-deployment verification to ensure code is ready for production deployment. Calls testing, security, and review commands.

**Rules Applied**: `deployment-and-infrastructure`, `final-review-protocol`, `security-governance-and-observability`

#### `/deployment/post-deployment-verification`
Comprehensive post-deployment verification to ensure successful deployment and system stability.

**Rules Applied**: `deployment-and-infrastructure`, `monitoring-and-observability`

#### `/deployment/run-all-deployment` (Master Command)
Runs all deployment commands in sequence: pre-deployment check → [deploy] → post-deployment verification.

### 6. Agent Development Commands (`/agents/`)

Agent development and setup workflows.

#### `/agents/setup-new-agent-system`
Systematic setup of a new multi-agent system from initial planning through implementation structure.

**Rules Applied**: `multi-agent-systems`, `langgraph-architecture-and-nodes`, `agentic-logic-and-tools`

#### `/agents/create-agent-node`
Create a new LangGraph node following the four-part structure (READ → DO → WRITE → CONTROL).

**Rules Applied**: `langgraph-architecture-and-nodes`, `core-python-standards`

#### `/agents/implement-agent-tool`
Implement a new tool for agent use following LangChain tool definition standards.

**Rules Applied**: `agentic-logic-and-tools`, `data-schemas-and-interfaces`

#### `/agents/run-all-agents` (Master Command)
Runs all agent development commands in sequence: setup new agent system → create agent node → implement agent tool.

## Usage

### Basic Usage

To use a command, type `/` followed by the command path in the Cursor chat input box:

```
/testing/run-test-suite
/security/security-audit
/testing/evaluate-with-llm-judge
/testing/run-all-testing
```

### With Additional Context

You can provide additional context after the command name:

```
/testing/run-test-suite and fix any failures
/security/security-audit focusing on OWASP Top 10
/deployment/pre-deployment-check before merging to main
```

### Master Commands

Master commands execute all commands in a category in the proper sequence:

```
/testing/run-all-testing
/security/run-all-security
/review/run-all-review
/monitoring/run-all-monitoring
/deployment/run-all-deployment
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

1. **Overview** (H1): Brief description of what the command does
2. **Rules Applied**: List of Rules that are integrated into the command
3. **Steps**: Detailed workflow steps the command follows
4. **Data Sources**: Sources of data the command analyzes
5. **Output**: Description of the expected output

See `.cursor/rules/commands-management/RULE.md` for detailed format specifications.

## Command Dependencies and Overlap Prevention

Commands are designed to avoid duplication:

- **`pre-deployment-check`** calls `/testing/run-test-suite`, `/testing/run-evaluation-suite`, `/security/security-audit`, and `/review/final-compliance-check` instead of duplicating their checks
- **`security-audit`** calls `/security/compliance-check` and `/security/analyze-audit-logs` instead of duplicating their analysis
- **`final-compliance-check`** calls `/review/code-review-checklist` instead of duplicating code review checks

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

1. **Use Master Commands for Complete Workflows**: Use master commands (e.g., `/testing/run-all-testing`) when you need to run all commands in a category
2. **Use Individual Commands for Specific Tasks**: Use individual commands when you need to run a specific check or analysis
3. **Review Output**: Always review command output and recommendations before taking action
4. **Update Commands**: Keep commands updated as Rules and requirements evolve
5. **Avoid Duplication**: When creating new commands, check if existing commands can be reused instead of duplicating functionality

## Command Development

When creating or updating commands, follow the format defined in `.cursor/rules/commands-management/RULE.md`:

1. Follow the standard command structure (Overview, Rules Applied, Steps, Data Sources, Output)
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
- **[Commands Management Rule](../rules/commands-management/RULE.md)** - Format specifications for creating/updating commands
- **[Cursor Commands Documentation](https://cursor.com/docs/agent/chat/commands)** - Official Cursor documentation
- **[Cursor Rules Documentation](https://cursor.com/docs/context/rules)** - Official Cursor documentation
