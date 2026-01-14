# Cursor Commands Documentation

This directory contains custom commands for the Cursor AI agent. These commands provide reusable workflows that can be triggered with a `/` prefix in the chat input box.

## Overview

Commands are defined as plain Markdown files that describe workflows and tasks. They integrate with the project's Rules (`.cursor/rules`) to provide comprehensive, standardized processes for development, testing, security, deployment, and agent development.

Commands are organized into categories with dedicated directories. Each category includes individual commands and a master command that runs all commands in that category in sequence.

## Directory Structure

```
.cursor/commands/
├── testing/
│   ├── run-test-suite.md
│   ├── run-evaluation-suite.md
│   ├── evaluate-with-llm-judge.md
│   └── run-all-testing.md (Master Command)
├── security/
│   ├── security-audit.md
│   ├── analyze-audit-logs.md
│   ├── compliance-check.md
│   └── run-all-security.md (Master Command)
├── review/
│   ├── code-review-checklist.md
│   ├── final-compliance-check.md
│   └── run-all-review.md (Master Command)
├── monitoring/
│   ├── analyze-langsmith-traces.md
│   ├── comprehensive-system-analysis.md
│   ├── performance-analysis.md
│   └── run-all-monitoring.md (Master Command)
├── deployment/
│   ├── pre-deployment-check.md
│   ├── post-deployment-verification.md
│   └── run-all-deployment.md (Master Command)
├── agents/
│   ├── setup-new-agent-system.md
│   ├── create-agent-node.md
│   ├── implement-agent-tool.md
│   └── run-all-agents.md (Master Command)
└── README.md
```

## Command Categories

### 1. Testing Commands (`/testing/`)

#### `/testing/run-test-suite`
Execute the full test suite and systematically analyze results, identify failures, and provide actionable recommendations.

**Rules Applied**: `tests-and-validation`, `core-python-standards`

#### `/testing/run-evaluation-suite`
Execute the complete LLM evaluation suite using specialized evaluation frameworks (Ragas, DeepEval, LangSmith).

**Rules Applied**: `llm-evaluation-and-metrics`, `llm-judge-protocol`

#### `/testing/evaluate-with-llm-judge`
Comprehensive evaluation using LLM-as-a-Judge protocol to analyze agent system performance, safety, and logic.

**Rules Applied**: `llm-judge-protocol`, `audit-protocol`, `llm-evaluation-and-metrics`

#### `/testing/run-all-testing` (Master Command)
Runs all testing commands in sequence: test suite → evaluation suite → LLM Judge evaluation.

### 2. Security Commands (`/security/`)

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

#### `/review/code-review-checklist`
Comprehensive code review using a structured checklist to ensure code quality, functionality, testing, documentation, security, and maintainability.

**Rules Applied**: `code-review-and-collaboration`, `core-python-standards`, `final-review-protocol`

#### `/review/final-compliance-check`
Comprehensive final review before commit to verify solution complies with all active governance files and project standards. Uses results from code review checklist.

**Rules Applied**: `final-review-protocol`, all relevant rules

#### `/review/run-all-review` (Master Command)
Runs all review commands in sequence: code review checklist → final compliance check.

### 4. Monitoring Commands (`/monitoring/`)

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

#### `/deployment/pre-deployment-check`
Comprehensive pre-deployment verification to ensure code is ready for production deployment. Calls testing, security, and review commands.

**Rules Applied**: `deployment-and-infrastructure`, `final-review-protocol`, `security-governance-and-observability`

#### `/deployment/post-deployment-verification`
Comprehensive post-deployment verification to ensure successful deployment and system stability.

**Rules Applied**: `deployment-and-infrastructure`, `monitoring-and-observability`

#### `/deployment/run-all-deployment` (Master Command)
Runs all deployment commands in sequence: pre-deployment check → [deploy] → post-deployment verification.

### 6. Agent Development Commands (`/agents/`)

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

## Master Commands

Each category includes a master command (e.g., `run-all-testing.md`) that executes all commands in that category in the proper sequence. Master commands:

- Run commands in the correct order with proper dependencies
- Handle errors appropriately (stop on critical failures, continue with warnings)
- Aggregate results from all commands
- Provide comprehensive summary reports
- Can be run independently or as part of a larger workflow

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

## Usage

To use a command, type `/` followed by the command path in the Cursor chat input box. For example:

```
/testing/run-test-suite
/security/security-audit
/testing/evaluate-with-llm-judge
/testing/run-all-testing
```

You can also provide additional context after the command name:

```
/testing/run-test-suite and fix any failures
/security/security-audit focusing on OWASP Top 10
```

## Command Structure

Each command follows a consistent structure:

1. **Overview**: Brief description of what the command does
2. **Rules Applied**: List of Rules that are integrated into the command
3. **Steps**: Detailed workflow steps the command follows
4. **Data Sources**: Sources of data the command analyzes
5. **Output**: Description of the expected output

## Integration with Rules

Commands integrate with the project's Rules (`.cursor/rules`) to:

- Apply consistent standards and best practices
- Ensure compliance with governance requirements
- Provide comprehensive analysis based on project rules
- Standardize workflows across the team

## Best Practices

1. **Use Master Commands for Complete Workflows**: Use master commands (e.g., `/testing/run-all-testing`) when you need to run all commands in a category
2. **Use Individual Commands for Specific Tasks**: Use individual commands when you need to run a specific check or analysis
3. **Review Output**: Always review command output and recommendations before taking action
4. **Update Commands**: Keep commands updated as Rules and requirements evolve
5. **Avoid Duplication**: When creating new commands, check if existing commands can be reused instead of duplicating functionality

## Command Development

When creating new commands:

1. Follow the standard command structure
2. Integrate relevant Rules
3. Specify data sources clearly
4. Provide detailed steps
5. Document expected output
6. Test commands thoroughly
7. Check for overlaps with existing commands and reuse them when possible

## Related Documentation

- [Cursor Commands Documentation](https://cursor.com/docs/agent/chat/commands)
- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- Project Rules in `.cursor/rules/`
