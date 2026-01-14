# Run Test Suite

## Overview
Execute the full test suite and systematically analyze results, identify failures, and provide actionable recommendations for fixes. This command ensures code quality and functionality before proceeding with development or deployment.

## Rules Applied
- `tests-and-validation` - Testing framework standards and validation requirements
- `core-python-standards` - Code quality standards and best practices
- `error-handling-and-resilience` - Error handling patterns for test failures

## Steps

1. **Execute Test Suite**
   - Run `pytest -v` to execute all tests with verbose output
   - Capture full test output including stdout, stderr, and exit codes
   - Identify test files and test functions executed
   - Record execution time for each test

2. **Analyze Test Results**
   - Categorize results: ✅ PASS, ❌ FAIL, ⚠️ WARNING, ⏭️ SKIP
   - Extract failure messages and stack traces for failed tests
   - Identify skipped tests and reasons for skipping
   - Count total tests, passed, failed, skipped, and warnings

3. **Identify Failure Patterns**
   - Group failures by type (assertion errors, import errors, timeout errors, etc.)
   - Identify common failure patterns across multiple tests
   - Check if failures are related to recent code changes
   - Determine if failures are flaky or deterministic

4. **Generate Statistics**
   - Total number of tests executed
   - Pass rate percentage
   - Execution time (total and per-test average)
   - Test coverage metrics (if available)
   - Breakdown by test file and test category

5. **Provide Recommendations**
   - Suggest fixes for each failed test with specific error context
   - Identify tests that may need updates due to code changes
   - Recommend adding tests for uncovered functionality
   - Suggest test organization improvements if needed

6. **Create Test Report**
   - Generate structured report with all findings
   - Include failure details with expected vs actual values
   - Provide actionable next steps
   - Highlight critical failures that block development

## Data Sources
- Test files in `tests/` directory and `test_*.py` files
- Test execution output from pytest
- Test coverage reports (if available)
- Recent code changes (git diff)

## Output
A comprehensive test report including:
- Summary statistics (total tests, pass rate, execution time)
- Detailed failure analysis with stack traces
- Grouped failures by type and pattern
- Specific recommendations for each failure
- Overall assessment and next steps
- Visual indicators (✅/❌/⚠️) for quick status identification
