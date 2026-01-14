# Analyze LangSmith Traces

## Overview
Comprehensive analysis of LangSmith traces to understand LLM operations, tool usage, agent behavior, and performance. This command examines traces from local JSON files to identify bottlenecks, errors, and optimization opportunities.

## Rules Applied
- `monitoring-and-observability` - LangSmith integration, tracing, performance metrics
- `agentic-logic-and-tools` - Tool usage patterns, agent internals, performance
- `error-handling-and-resilience` - Error patterns and retry strategies

## Steps

1. **Read LangSmith Traces**
   - Locate LangSmith trace files in project directories
     - Search for JSON files containing LangSmith trace data
     - Look for files in common trace storage locations
     - Identify trace file formats and structures
   - Parse trace data
     - Extract structured trace data (JSON format)
     - Validate trace structure
     - Handle different trace formats if present

2. **Analyze LLM Calls**
   - **Token Usage**:
     - Extract input token counts for each LLM call
     - Extract output token counts for each LLM call
     - Calculate total token usage and costs
     - Identify high token usage patterns
   - **Latency**:
     - Measure latency for each LLM call
     - Calculate P50, P95, P99 latency percentiles
     - Identify slow LLM calls
     - Analyze latency patterns
   - **Costs**:
     - Calculate costs based on token usage and model pricing
     - Identify expensive operations
     - Analyze cost trends
   - **Model Information**:
     - Extract model name and version used
     - Check model configuration
     - Analyze model selection patterns

3. **Analyze Tool Calls**
   - **Tool Selection**:
     - Analyze which tools were selected and why
     - Check tool selection decisions
     - Identify tool selection patterns
   - **Tool Execution**:
     - Analyze tool execution results (success/failure)
     - Measure tool execution duration
     - Identify slow or failing tools
   - **Tool Parameters**:
     - Review tool parameter validity
     - Check for parameter errors
     - Analyze parameter patterns
   - **Tool Usage Patterns**:
     - Identify frequently used tools
     - Detect unused or rarely used tools
     - Analyze tool usage efficiency

4. **Analyze Agent Steps**
   - **Flow Analysis**:
     - Reconstruct agent execution flow
     - Identify step sequences and patterns
     - Check for unnecessary steps or loops
   - **Decision Points**:
     - Analyze agent decision-making
     - Review routing decisions
     - Check decision quality
   - **State Transitions**:
     - Analyze state changes between steps
     - Identify state modification patterns
     - Check for state inconsistencies

5. **Identify Bottlenecks**
   - **Slow Operations**:
     - Identify operations with high latency
     - Analyze causes of slowness
     - Check for sequential operations that could be parallelized
   - **Inefficient Patterns**:
     - Detect repetitive operations
     - Identify unnecessary tool calls
     - Find redundant LLM calls
   - **Resource Waste**:
     - Identify excessive token usage
     - Detect unnecessary retries
     - Find inefficient caching patterns

6. **Identify Errors and Retries**
   - **Error Analysis**:
     - Extract error types and messages
     - Identify error patterns
     - Analyze error frequency
   - **Retry Patterns**:
     - Identify retry attempts
     - Analyze retry success rates
     - Check retry configuration effectiveness
   - **Error Recovery**:
     - Review error recovery strategies
     - Check if errors are handled gracefully
     - Identify unrecoverable errors

7. **Performance Metrics**
   - **Overall Performance**:
     - Calculate total execution time
     - Measure average step duration
     - Calculate throughput metrics
   - **Resource Usage**:
     - Analyze token consumption patterns
     - Calculate cost per operation
     - Identify resource-intensive operations
   - **Efficiency Metrics**:
     - Calculate steps per task
     - Measure tool call efficiency
     - Analyze LLM call efficiency

8. **Generate Performance Report**
   - Create comprehensive trace analysis report
   - Include LLM call analysis with metrics
   - Provide tool usage analysis
   - Highlight bottlenecks and inefficiencies
   - Include error analysis and recommendations
   - Provide optimization recommendations

## Data Sources
- LangSmith trace files (JSON format) from local storage
- Trace directories and file patterns
- Model configuration files
- Tool registry and definitions

## Output
A comprehensive LangSmith trace analysis report including:
- **LLM Call Analysis**: Token usage, latency, costs, model information
- **Tool Call Analysis**: Selection, execution, parameters, usage patterns
- **Agent Step Analysis**: Flow, decisions, state transitions
- **Bottleneck Identification**: Slow operations, inefficient patterns, resource waste
- **Error Analysis**: Error types, retry patterns, recovery strategies
- **Performance Metrics**: Overall performance, resource usage, efficiency metrics
- **Optimization Recommendations**: Prioritized suggestions for improving performance
- **Cost Analysis**: Token costs, operation costs, cost optimization opportunities
