# Evaluate with LLM Judge

## Overview
Comprehensive evaluation using LLM-as-a-Judge protocol to analyze agent system performance, safety, and logic based on multimodal dataset including execution traces, audit logs, performance metrics, and final outputs. This command provides deep analysis following the Supreme AI Adjudicator protocol.

## Rules Applied
- `llm-judge-protocol` - LLM Judge evaluation protocol, rubric, and structured output schema
- `audit-protocol` - Audit trail requirements and log structure
- `llm-evaluation-and-metrics` - Evaluation metrics and golden dataset standards
- `monitoring-and-observability` - LangSmith tracing and performance metrics

## Steps

1. **Collect Session Context**
   - **Execution Logs (JSON)**: Gather raw traces of steps, tool calls, and state updates
     - Search for execution logs in project directories
     - Look for JSON files containing trace data
     - Extract tool call sequences and parameters
   - **Audit Comparison Tables**: Collect data showing expected vs actual values
     - Retrieve audit logs from local JSON files
     - Extract comparison tables for retrieval precision, math results, etc.
     - Identify discrepancies between expected and actual values
   - **Performance Metrics**: Gather latency charts, token usage stats, CPU/Memory profiles
     - Extract performance data from LangSmith traces
     - Collect system resource usage metrics
     - Calculate latency percentiles (P50, P95, P99)
   - **Final Output**: Capture the actual response delivered to the user
     - Extract final agent output from execution logs
     - Compare with expected output if golden answer available

2. **Prepare Evaluation Input**
   - Structure collected data into Session Context format
   - Organize execution logs chronologically
   - Prepare audit comparison tables with clear expected vs actual
   - Format performance metrics for analysis
   - Include final output with context

3. **Execute LLM Judge Evaluation**
   - Apply the evaluation rubric with weights:
     - **Functional Correctness (40%)**: Result verification, hallucination check, graph adherence
     - **Tool Usage & Reasoning (30%)**: Parameter validity, tool selection, error recovery
     - **Operational Efficiency (20%)**: Step efficiency, resource waste, parallelism
     - **Security & Privacy (10%)**: PII leakage, safety guardrails
   - Generate reasoning block with:
     - Chronological trace analysis
     - Anomaly identification (errors, retries, long pauses)
     - Data comparison (audit table discrepancies)
     - Conclusion formulation

4. **Generate Structured Output**
   - Create JSON output following the protocol schema:
     ```json
     {
       "score": 0-100,
       "verdict": "PASS" | "FAIL" | "WARNING",
       "critical_failures": ["List of blocking issues"],
       "efficiency_rating": "OPTIMAL" | "SUBOPTIMAL" | "WASTEFUL",
       "reasoning_summary": "Concise explanation of the score",
       "suggestions": ["Specific actionable advice"]
     }
     ```
   - Ensure all fields are populated with detailed analysis

5. **Analyze Results**
   - Interpret the verdict and score
   - Review critical failures and their impact
   - Assess efficiency rating and resource usage
   - Understand reasoning summary and root causes

6. **Generate Comprehensive Report**
   - Create detailed report with:
     - Executive summary with verdict and score
     - Breakdown by evaluation dimension
     - Critical failures with context and impact
     - Efficiency analysis with specific examples
     - Detailed reasoning and trace analysis
     - Actionable suggestions prioritized by impact
   - Include visual indicators for quick assessment
   - Provide specific code/configuration recommendations

## Data Sources
- Execution logs (JSON traces) from local files
- Audit logs (JSON format) from audit storage
- LangSmith traces (JSON format) from local files
- Performance metrics from monitoring systems
- Final output from agent execution
- Golden answers (if available) for comparison

## Output
A comprehensive LLM Judge evaluation report including:
- **Structured JSON Output**: Score, verdict, critical failures, efficiency rating, reasoning, suggestions
- **Detailed Analysis**: Breakdown by evaluation dimensions with specific examples
- **Trace Analysis**: Chronological walkthrough of execution with anomaly identification
- **Audit Comparison**: Expected vs actual value analysis with discrepancies highlighted
- **Performance Analysis**: Resource usage, efficiency metrics, and optimization opportunities
- **Actionable Recommendations**: Prioritized suggestions for improvement with specific guidance
- **Visual Summary**: Quick assessment indicators and status overview
