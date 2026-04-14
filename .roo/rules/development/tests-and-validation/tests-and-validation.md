## 1. Structure & Environment
* **Directory Mandate:** You must create a dedicated `tests/` directory in the root if it does not exist.
* **Framework:** Use `pytest` as the sole testing framework.
* **File Organization:**
    * **Do not** create one giant test file.
    * Create many small, atomic test files named `test_<component_name>.py` (e.g., `test_data_loader.py`, `test_agent_routing.py`).
    * Mirror the main source code structure within the `tests/` directory.

## 2. Granular Testing Strategy
* **Atomic Tests:** Each test function must test exactly one concept or edge case.
* **Isolation:** Tests must be independent. One test failure should not cascade to others.
* **Regression:** Every time code is modified, run `pytest` to ensure existing tests pass before approval.
* **New Features:** No new feature is considered "complete" without a corresponding new test file or function in `tests/`.

## 3. Visual Feedback & Reporting
* **Execution:** Run tests using `pytest -v` (verbose) to show a detailed list.
* **Explicit Status:** When summarizing or logging test results, you must clearly indicate status using visual symbols:
    * ✅ **PASS:** The logic works as expected.
    * ❌ **FAIL:** Critical logic error; strictly blocking.
    * ⚠️ **WARNING:** Non-critical issue or "XFAIL" (expected failure).
* **Traceability:** On failure, the output must show exactly *why* it failed (expected vs. actual value).

## 4. Implementation Rules (Arrange-Act-Assert)
* **Arrange:** Set up the necessary data or state.
* **Act:** Execute the specific function or method being tested.
* **Assert:** Verify the result strictly. Use clear assertion messages.
    * *Bad:* `assert result == 5`
    * *Good:* `assert result == 5, f"Expected 5 but got {result}"`
* **LLM-First Testing:** For LLM behavior validation, tests must call real LLM endpoints (no mocks/fakes for LLM responses).
* **Stability Guardrails:** To reduce flaky outcomes when using real LLMs, pin model/version where possible, keep prompts fixed, and assert on clear acceptance criteria (structure, required facts, policy constraints) rather than exact wording.
* **Mocking Scope:** Mocking is allowed only for non-LLM infrastructure dependencies when needed (e.g., unavailable third-party systems), and must not replace real LLM validation.
