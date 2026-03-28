# Run All Testing

## Overview
Execute all testing commands in sequence: write targeted tests for new code, test suite, evaluation suite, and prompt test suite. This master command runs the complete testing workflow to ensure code quality, functionality, prompt quality, and agent performance. **LLM-as-a-Judge** evaluation is available separately via the **`@evaluate-with-llm-judge`** skill.

## Rules Applied
- `tests-and-validation` - Testing framework standards and validation requirements
- `llm-evaluation-and-metrics` - LLM evaluation standards and mandatory metrics
- `core-python-standards` - Code quality standards and best practices
- `error-handling-and-resilience` - Error handling patterns, error classification, retry strategies
- `monitoring-and-observability` - Test execution metrics, logging, LangSmith tracing
- `performance-optimization` - Test performance analysis, efficiency metrics
- `data-schemas-and-interfaces` - Evaluation data structures and Pydantic schemas
- `audit-protocol` - Audit trail requirements and log structure
- `security-governance-and-observability` - Security and privacy checks, PII leakage detection

## Steps

1. **Write Targeted Tests**
   - Execute `/testing/write-targeted-tests` command
   - Wait for completion and review results
   - **Comprehensive Error Handling**:
     - **No New Code**: If no new/modified code detected, skip this step and proceed
     - **Test Generation Failures**: If test generation fails, continue with warning, include in final report
     - **Test Failures**: If generated tests fail, fix issues and re-run, or continue with warning
     - **Success**: If tests are generated and pass, proceed to next step
   - **Output**: Test generation report with new test files, test cases, coverage metrics

2. **Run Test Suite**
   - Execute `/testing/run-test-suite` command
   - Wait for completion and review results
   - **Comprehensive Error Handling**: 
     - **Critical Failures**: If tests fail with blocking issues, stop execution and report
     - **Non-Critical Failures**: If tests fail with non-blocking issues, continue with warning
     - **Warnings**: If tests pass with warnings, continue with warning notification
     - **Success**: If all tests pass, proceed to next step
     - **Dependency Check**: Verify test suite completion before proceeding to evaluation
   - **Output**: Test execution report with pass/fail status, coverage metrics, performance data

3. **Run Evaluation Suite**
   - Execute `/testing/run-evaluation-suite` command
   - Wait for completion and review results
   - **Comprehensive Error Handling**:
     - **Critical Failures**: If evaluation fails completely, stop execution and report blocking issues
     - **Threshold Failures**: If evaluation scores below threshold, continue with warning, include in final report
     - **Partial Failures**: If some metrics fail but others pass, continue with warning
     - **Success**: If evaluation passes all thresholds, proceed to next step
     - **Dependency Check**: Verify evaluation suite completion before proceeding to LLM Judge
   - **Output**: Evaluation report with metrics scores, cost analysis, trend comparison

4. **Run Prompt Test Suite**
   - Execute `/testing/run-prompt-test-suite` command
   - Wait for completion and review results
   - **Comprehensive Error Handling**:
     - **Critical Failures**: If prompt tests fail on safety or output contract violations, stop execution and report blocking issues
     - **Regression Findings**: If prompt regressions are detected, continue with warning and include in final report
     - **Partial Data**: If some scenarios cannot run, continue with warning and include partial coverage status
     - **Success**: If prompt test suite passes, proceed to next step
   - **Output**: Prompt testing report with validation status, regressions, and release recommendation

5. **Generate Comprehensive Testing Report**
   - **Aggregated Reporting**:
     - Aggregate results from all four commands (write targeted tests, test suite, evaluation suite, prompt test suite)
     - Combine metrics, scores, and findings into unified report
     - Cross-reference findings across different evaluation methods
   - **Dependency Management**:
     - Document command execution order and dependencies
     - Track which commands completed successfully
     - Identify dependencies between test results and evaluation results
   - Create summary with overall testing status (Pass/Fail/Needs Attention)
   - Highlight critical issues from all stages with severity classification
   - Provide prioritized recommendations across all testing dimensions
   - Include links to detailed reports from each command
   - **Trend Analysis**: Compare current results with previous runs if available
   - **Execution Flow**: 
     - `write-targeted-tests → [New code?] → run-test-suite → [Pass?] → run-evaluation-suite → [Pass?] → run-prompt-test-suite → Final Report`
     - If no new code detected, skip write-targeted-tests step
     - If test suite fails, stop execution and report blocking issues
     - If evaluation suite fails, stop execution and report blocking issues
     - For LLM-as-a-Judge evaluation, use `@evaluate-with-llm-judge` skill separately

## Data Sources
- Results from `/testing/write-targeted-tests` command
- Results from `/testing/run-test-suite` command
- Results from `/testing/run-evaluation-suite` command
- Results from `/testing/run-prompt-test-suite` command

## Output
A comprehensive testing report including:
- **Overall Testing Status**: Pass/Fail/Needs Attention with justification
- **Targeted Tests Summary**: New test files created, test cases generated, coverage for new code
- **Test Suite Summary**: Pass rate, failures, execution time, coverage metrics, performance data
- **Evaluation Suite Summary**: Metrics scores, quality assessment, cost analysis, trend comparison
- **Prompt Test Suite Summary**: Prompt validation status, regressions, quality/cost/latency checks
- **Aggregated Metrics**: Combined metrics across all testing methods
- **Cross-Reference Analysis**: Correlations between test results, evaluation results, and LLM Judge findings
- **Critical Issues**: Blocking issues that must be addressed, classified by severity
- **Recommendations**: Prioritized suggestions for improvements across all testing dimensions
- **Dependency Status**: Command execution status and dependency fulfillment
- **Next Steps**: Actionable items based on all testing results with priority levels
