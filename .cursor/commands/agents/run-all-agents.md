# Run All Agents

## Overview
Execute all agent development commands in sequence: setup new agent system, create agent node, and implement agent tool. This master command provides a complete workflow for developing new agent systems from scratch.

## Rules Applied
- `multi-agent-systems` - Multi-agent architecture patterns
- `langgraph-architecture-and-nodes` - LangGraph workflow design
- `agentic-logic-and-tools` - LangChain fundamentals and tool definitions
- `core-python-standards` - Code quality standards

## Steps

1. **Setup New Agent System**
   - Execute `/agents/setup-new-agent-system` command
   - Wait for completion and review results
   - **Error Handling**:
     - If setup fails: Stop execution, report blocking issues
     - If setup completes with warnings: Continue with warning notification
     - If setup completes successfully: Proceed to next step
   - **Output**: Agent system setup report with project structure and workflow definition

2. **Create Agent Node**
   - Execute `/agents/create-agent-node` command
   - Wait for completion and review results
   - **Error Handling**:
     - If node creation fails: Stop execution, report blocking issues
     - If node creation completes with issues: Continue with warning, include in final report
     - If node creation completes successfully: Proceed to next step
   - **Output**: Agent node creation report with node implementation and tests

3. **Implement Agent Tool**
   - Execute `/agents/implement-agent-tool` command
   - Wait for completion and review results
   - **Error Handling**:
     - If tool implementation fails: Report error but include partial results
     - If tool implementation completes with issues: Include in final report
     - If tool implementation completes successfully: Generate final report
   - **Output**: Agent tool implementation report with tool definition and tests

4. **Generate Comprehensive Agent Development Report**
   - Aggregate results from all three commands
   - Create summary with overall agent development status
   - Highlight setup, node creation, and tool implementation status
   - Provide recommendations for next steps
   - Include links to detailed reports from each command

## Data Sources
- Results from `/agents/setup-new-agent-system` command
- Results from `/agents/create-agent-node` command
- Results from `/agents/implement-agent-tool` command

## Output
A comprehensive agent development report including:
- **Overall Development Status**: Complete/In Progress/Needs Attention
- **System Setup Summary**: Project structure, workflow definition, visualization
- **Node Creation Summary**: Node implementation, state integration, tests
- **Tool Implementation Summary**: Tool definition, LLM integration, tests
- **Issues and Recommendations**: Development issues and improvement suggestions
- **Next Steps**: Actionable items for completing agent development

## Execution Flow
```
setup-new-agent-system → create-agent-node → implement-agent-tool → Final Report
         ↓ Fail                  ↓ Fail                  ↓ Fail
      [Stop]                  [Stop]              [Report & Continue]
```

## Notes
- This is a sequential workflow - each step depends on the previous
- Each command can be run independently if needed
- Master command provides workflow orchestration for new agent development
- All reports are preserved for detailed analysis
