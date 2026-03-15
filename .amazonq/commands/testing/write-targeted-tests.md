# Write Targeted Tests

## Overview
Systematically identify new or modified code and automatically generate comprehensive, targeted test cases following project testing standards. This command ensures every new feature, function, or code change has corresponding test coverage before approval.

## Rules Applied
- `tests-and-validation` - Testing framework standards, atomic tests, Arrange-Act-Assert pattern
- `core-python-standards` - Code quality standards, function structure
- `error-handling-and-resilience` - Error handling test cases, edge cases
- `monitoring-and-observability` - Test execution metrics and logging
- `code-review-and-collaboration` - Test quality standards

## Steps

1. **Identify New/Modified Code**
   - Scan recent git changes (unstaged, staged, and recent commits)
   - Identify new files, modified files, and deleted files
   - Extract new functions, classes, and methods
   - Identify modified functions and their changes
   - Categorize code by type:
     - New features
     - Bug fixes
     - Refactoring
     - Configuration changes
     - Documentation changes

2. **Analyze Code Structure**
   - For each new/modified function:
     - Parse function signature (parameters, return type, type hints)
     - Identify dependencies (imports, external services)
     - Extract business logic and edge cases
     - Identify error handling patterns
     - Note async/await usage
     - Identify I/O operations (database, API calls, file operations)
   - For each new/modified class:
     - Extract class methods
     - Identify initialization requirements
     - Note inheritance relationships
     - Identify state management

3. **Check Existing Test Coverage**
   - Check if tests already exist for new/modified code
   - Verify test file structure matches source code structure
   - Identify gaps in test coverage
   - Check if existing tests need updates for modified code
   - Verify test quality (atomic, isolated, comprehensive)

4. **Generate Test Cases**
   - For each new/modified function, generate test cases:
     - **Happy Path Tests**: Test normal operation with valid inputs
     - **Edge Case Tests**: Test boundary conditions, empty inputs, None values
     - **Error Handling Tests**: Test error conditions, invalid inputs, exception handling
     - **Type Validation Tests**: Test type hints are respected
     - **Async Tests**: If async, test with proper async test patterns
     - **Mocking Requirements**: Identify what needs to be mocked (external APIs, databases, file I/O)
   - Follow Arrange-Act-Assert pattern:
     - **Arrange**: Set up test data, mocks, and fixtures
     - **Act**: Execute the function/method being tested
     - **Assert**: Verify results with clear assertion messages
   - Ensure tests are atomic (one concept per test)
   - Ensure tests are isolated (no dependencies between tests)
   - **Test Generation Patterns**:
     - **Function Tests**: Happy path, edge cases (empty strings, None, zero, negative, boundaries), error cases, async patterns
     - **Class Tests**: Initialization with various parameters, methods independently, state management, inheritance
     - **Integration Tests**: API endpoints (HTTP requests/responses), database operations (CRUD with test database), external services (with mocks)
     - **Mocking Strategy**: External APIs (mock HTTP requests), database (test database or mocks), file I/O (mocks or temp files), LLM calls (mocks for deterministic tests), time-dependent (mock datetime)

5. **Create/Update Test Files**
   - Create test file structure matching source code structure
   - Use naming convention: `test_<component_name>.py`
   - Create test file in appropriate location in `tests/` directory
   - Mirror source code directory structure
   - For each test function:
     - Use descriptive test names: `test_<function_name>_<scenario>`
     - Add docstrings explaining what is being tested
     - Include type hints for test functions
     - Use pytest fixtures where appropriate
     - Add proper mocking for external dependencies
     - Include clear assertion messages

6. **Write Test Implementation**
   - Generate complete test code following standards:
     - Use `pytest` framework
     - Use `pytest.fixture` for reusable test data
     - Use `pytest.mark.parametrize` for multiple test cases
     - Use `unittest.mock` or `pytest-mock` for mocking
     - Use `pytest-asyncio` for async tests
     - Include proper imports and setup
   - Ensure tests follow visual feedback standards:
     - Tests should produce clear ✅ PASS or ❌ FAIL status
     - Include descriptive error messages
     - Show expected vs actual values on failure
   - Add test documentation:
     - Explain test purpose
     - Document test scenarios
     - Note any special setup requirements

7. **Validate Test Quality**
   - Verify tests follow Arrange-Act-Assert pattern
   - Check tests are atomic and isolated
   - Verify proper mocking of external dependencies
   - Check test names are descriptive
   - Verify assertion messages are clear
   - Check tests handle edge cases
   - Verify error handling is tested
   - Check async tests use proper async patterns

8. **Run Generated Tests**
   - Execute `pytest -v` on newly created/updated tests
   - Verify all tests pass (✅ status)
   - Fix any test failures or issues
   - Verify test execution time is reasonable
   - Check test output is clear and informative

9. **Generate Test Coverage Report**
   - Run coverage analysis on new/modified code
   - Verify coverage meets standards (target: 80%+ for new code)
   - Identify any uncovered code paths
   - Generate additional tests for uncovered paths if needed
   - Document coverage metrics

10. **Create Test Summary Report**
    - **New Test Files Created**: List of new test files with locations
    - **Test Functions Generated**: Count and list of test functions
    - **Test Coverage**: Coverage metrics for new/modified code
    - **Test Categories**: Breakdown by happy path, edge cases, error handling
    - **Mocking Strategy**: What was mocked and why
    - **Test Execution Results**: Pass/fail status with execution time
    - **Coverage Gaps**: Any uncovered code paths
    - **Recommendations**: Additional tests needed or improvements

## Data Sources
- Git changes (unstaged, staged, recent commits)
- Source code files (Python files)
- Existing test files (`tests/` directory)
- Test execution output from pytest
- Test coverage reports

## Output
A comprehensive test generation report including:

- **Code Analysis Summary**: 
  - New files identified
  - Modified files identified
  - Functions/classes requiring tests
- **Test Files Created/Updated**: 
  - List of test files with full paths
  - Test file structure
  - Number of test functions per file
- **Test Cases Generated**:
  - Happy path tests
  - Edge case tests
  - Error handling tests
  - Type validation tests
  - Async tests (if applicable)
- **Test Implementation Details**:
  - Test code with Arrange-Act-Assert structure
  - Mocking strategy and implementation
  - Fixtures created
  - Test parameters used
- **Test Execution Results**:
  - Pass/fail status for each test
  - Execution time
  - Any test failures with fixes
- **Test Coverage Report**:
  - Coverage percentage for new/modified code
  - Uncovered code paths
  - Recommendations for additional tests
- **Quality Validation**:
  - Atomic test verification
  - Isolation verification
  - Assertion message quality
  - Mocking completeness
- **Next Steps**:
  - Additional tests recommended
  - Test improvements suggested
  - Coverage improvements needed
