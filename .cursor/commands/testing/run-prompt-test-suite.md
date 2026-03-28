# Run Prompt Test Suite

## Overview
Execute a structured prompt testing workflow to validate prompt behavior, detect regressions, and ensure prompt changes are safe before rollout.

## Rules Applied
- `prompt-engineering-and-management` - Prompt testing standards, versioning expectations, and context constraints
- `llm-evaluation-and-metrics` - Evaluation metrics and quality assessment framework
- `tests-and-validation` - Test structure and validation discipline
- `monitoring-and-observability` - Telemetry, tracing, and runtime visibility
- `commands-management` - Command format and workflow conventions

## Steps

1. **Define Prompt Under Test**
   - Identify prompt ID, target version, and deployment context.
   - Freeze the exact prompt template and variable schema for reproducible runs.
   - Enumerate expected output contracts (format, fields, safety constraints).

2. **Build Test Dataset**
   - Prepare representative test cases across normal, edge, and adversarial inputs.
   - Include at least: happy path, ambiguity, malformed input, and long-context case.
   - Store expected outcomes or acceptance criteria for each case.

3. **Run Deterministic Validation**
   - Execute fast checks with mocked/stubbed LLM responses when possible.
   - Validate output shape, required fields, and constraint adherence.
   - Fail the run on schema violations, missing fields, or forbidden content.

4. **Run Real Model Evaluation**
   - Execute the same suite against the real model/runtime configuration.
   - Measure quality, latency, token usage, and error rates per case.
   - Compare with baseline prompt version and classify regressions by severity.

5. **Analyze Results and Decide**
   - Summarize pass/fail by test category and risk level.
   - Mark blocked rollout if critical regressions or safety failures appear.
   - Recommend one of: promote, iterate, or rollback.

## Data Sources
- Prompt definitions from `prompts/` (YAML, template, or registry-backed sources)
- Prompt test cases and expected outcomes from local test datasets
- Runtime execution logs and evaluation artifacts
- Metrics and traces from observability systems (if configured)

## Output
A prompt testing report including:
- **Coverage Summary**: Tested prompt versions and scenario categories
- **Validation Results**: Schema/format/constraint pass-fail outcomes
- **Performance Metrics**: Quality, latency, token usage, and failure rates
- **Regression Analysis**: Comparison to baseline with severity classification
- **Release Decision**: Promote, iterate, or rollback with rationale
