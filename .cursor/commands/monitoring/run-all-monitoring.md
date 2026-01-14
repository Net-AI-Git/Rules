# Run All Monitoring

## Overview
Execute all monitoring commands in sequence: LangSmith trace analysis, performance analysis, and comprehensive system analysis. This master command runs the complete monitoring workflow to analyze system performance, identify bottlenecks, and provide holistic insights.

## Rules Applied
- `monitoring-and-observability` - Metrics, tracing, log aggregation
- `performance-optimization` - Performance optimization strategies
- `agentic-logic-and-tools` - Tool usage patterns

## Steps

1. **Analyze LangSmith Traces**
   - Execute `/monitoring/analyze-langsmith-traces` command
   - Wait for completion and review results
   - **Error Handling**:
     - If trace analysis fails: Continue with warning, report data availability issues
     - If traces unavailable: Skip this step, continue with available data
     - If analysis completes: Proceed to next step
   - **Output**: LangSmith trace analysis report with LLM calls, tool usage, agent steps

2. **Performance Analysis**
   - Execute `/monitoring/performance-analysis` command
   - Wait for completion and review results
   - **Error Handling**:
     - If performance analysis fails: Continue with warning, report data availability issues
     - If metrics unavailable: Skip this step, continue with available data
     - If analysis completes: Proceed to next step
   - **Output**: Performance analysis report with latency, throughput, resource usage

3. **Comprehensive System Analysis**
   - Execute `/monitoring/comprehensive-system-analysis` command (uses results from steps 1 and 2)
   - Wait for completion and review results
   - **Error Handling**:
     - If comprehensive analysis fails: Report error but include partial results
     - If analysis completes: Generate final report
   - **Output**: Comprehensive system analysis report with cross-system correlations

4. **Generate Comprehensive Monitoring Report**
   - Aggregate results from all three commands
   - Create summary with overall system health status
   - Highlight performance bottlenecks and anomalies
   - Provide prioritized optimization recommendations
   - Include links to detailed reports from each command

## Data Sources
- Results from `/monitoring/analyze-langsmith-traces` command
- Results from `/monitoring/performance-analysis` command
- Results from `/monitoring/comprehensive-system-analysis` command
- LangSmith traces (JSON format)
- Performance metrics
- Audit logs (JSON format)

## Output
A comprehensive monitoring report including:
- **Overall System Health**: Healthy/Degraded/Critical
- **LangSmith Analysis Summary**: LLM calls, tool usage, agent steps, bottlenecks
- **Performance Analysis Summary**: Latency, throughput, resource usage, optimization opportunities
- **Comprehensive Analysis Summary**: Cross-system correlations, patterns, anomalies
- **Critical Issues**: Performance bottlenecks and system issues
- **Prioritized Recommendations**: Optimization suggestions with impact assessment
- **Next Steps**: Actionable performance improvements

## Execution Flow
```
analyze-langsmith-traces → performance-analysis → comprehensive-system-analysis → Final Report
           ↓                        ↓                           ↓
      [Continue]              [Continue]                  [Aggregate Results]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Comprehensive system analysis uses results from trace and performance analysis
- All reports are preserved for detailed analysis
