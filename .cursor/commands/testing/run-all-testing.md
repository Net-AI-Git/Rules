# Run All Testing

## Overview
Execute all testing commands in sequence: test suite, evaluation suite, and LLM Judge evaluation. This master command runs the complete testing workflow to ensure code quality, functionality, and agent performance.

## Rules Applied
- `tests-and-validation` - Testing framework standards
- `llm-evaluation-and-metrics` - LLM evaluation standards
- `llm-judge-protocol` - LLM Judge evaluation protocol
- `core-python-standards` - Code quality standards

## Steps

1. **Run Test Suite**
   - Execute `/testing/run-test-suite` command
   - Wait for completion and review results
   - **Error Handling**: 
     - If tests fail: Stop execution and report blocking issues
     - If tests pass with warnings: Continue with warning notification
     - If all tests pass: Proceed to next step
   - **Output**: Test execution report with pass/fail status

2. **Run Evaluation Suite**
   - Execute `/testing/run-evaluation-suite` command
   - Wait for completion and review results
   - **Error Handling**:
     - If evaluation fails: Stop execution and report blocking issues
     - If evaluation scores below threshold: Continue with warning, include in final report
     - If evaluation passes: Proceed to next step
   - **Output**: Evaluation report with metrics scores

3. **Evaluate with LLM Judge**
   - Execute `/testing/evaluate-with-llm-judge` command
   - Wait for completion and review results
   - **Error Handling**:
     - If LLM Judge evaluation fails: Report error but include partial results
     - If verdict is FAIL: Include in final report as critical issue
     - If verdict is WARNING: Include in final report as non-blocking issue
     - If verdict is PASS: Include in final report as success
   - **Output**: LLM Judge evaluation report with score and verdict

4. **Generate Comprehensive Testing Report**
   - Aggregate results from all three commands
   - Create summary with overall testing status
   - Highlight critical issues from all stages
   - Provide prioritized recommendations
   - Include links to detailed reports from each command

## Data Sources
- Results from `/testing/run-test-suite` command
- Results from `/testing/run-evaluation-suite` command
- Results from `/testing/evaluate-with-llm-judge` command

## Output
A comprehensive testing report including:
- **Overall Testing Status**: Pass/Fail/Needs Attention
- **Test Suite Summary**: Pass rate, failures, execution time
- **Evaluation Suite Summary**: Metrics scores, quality assessment
- **LLM Judge Summary**: Score, verdict, critical failures, efficiency rating
- **Critical Issues**: Blocking issues that must be addressed
- **Recommendations**: Prioritized suggestions for improvements
- **Next Steps**: Actionable items based on all testing results

## Execution Flow
```
run-test-suite → [Pass?] → run-evaluation-suite → [Pass?] → evaluate-with-llm-judge → Final Report
                    ↓ Fail                              ↓ Fail                              ↓
                 [Stop]                              [Stop]                          [Report & Continue]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Error handling ensures critical issues are not missed
- All reports are preserved for detailed analysis
