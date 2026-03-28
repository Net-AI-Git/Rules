---
name: splunk-instrumentation
description: Scan code and add Splunk HEC instrumentation (logging, tracing, metrics) following monitoring-and-observability standards. Optionally consult on Splunk dashboards.
disable-model-invocation: true
---

# Splunk Instrumentation

## Overview

On-demand code instrumentation for Splunk observability. Scan the codebase, identify missing instrumentation, and add HEC events following the `@monitoring-and-observability` rule standards.

Trigger with **`@splunk-instrumentation`**.

## Workflow

### Step 1: Understand Requirements

Ask the user:
1. **Scope:** Which files/modules to instrument? (e.g., "all API endpoints", "agent nodes", specific files)
2. **What to add:** Logs, traces (spans), metrics, or all?
3. **Custom fields:** Any business-specific fields beyond the mandatory ones?

### Step 2: Read Standards

Read `@monitoring-and-observability` for the current mandatory fields and event structure:
- **Mandatory:** `timestamp`, `correlation_id`, `operation_name`
- **Timed operations:** also `start_time`, `end_time`, `duration_ms`, `operation_type`
- **Multi-stage:** also `stage_name`, `stage_latency_ms`, `total_latency_ms`

### Step 3: Scan Code

Scan the target files and identify gaps:

| Gap | What to look for |
|-----|-----------------|
| Missing timing | Functions/endpoints without `PerformanceTimer` or manual `start_time`/`end_time`/`duration_ms` |
| Missing correlation | No `correlation_id` propagation across service calls |
| `print()` statements | Any `print()` used for logging — must be HEC events |
| Missing request metrics | API endpoints without request/error rate tracking |
| Missing LLM metrics | LLM calls without token usage, model name, or cost tracking |
| Missing tool spans | Tool executions without span events |
| Missing error events | Exceptions caught but not sent to Splunk |

### Step 4: Add Instrumentation

For each gap:

1. **HEC Client:** Import the project's Splunk HEC client. If none exists, create one based on `@examples_splunk_hec` (uses `httpx`, direct HTTP POST).
2. **PerformanceTimer:** Wrap timed operations with the `PerformanceTimer` context manager (see `@examples_performance_timing`). It automatically sends `start_time`, `end_time`, `duration_ms` to HEC.
3. **Mandatory fields:** Every event MUST include `timestamp`, `correlation_id`, `operation_name`.
4. **Business metrics:** Add domain-specific fields where relevant (token usage, tool call success, agent step count).
5. **Replace `print()`:** Convert to structured HEC events with proper fields.
6. **Naming:** Use `snake_case` fields and source type format `{service}:{component}`.

### Step 5: Verify

- [ ] All instrumented functions have mandatory fields (`timestamp`, `correlation_id`, `operation_name`)
- [ ] `correlation_id` is propagated across service boundaries (HTTP headers, queue messages)
- [ ] No `print()` remains for logging purposes
- [ ] `time.perf_counter()` is used for duration (not `time.time()`)
- [ ] Source type follows `{service}:{component}` convention

### Step 6 (Optional): Dashboard Consultation

If the user asks about dashboards:

1. Review the instrumented fields and metrics in the codebase
2. Suggest relevant Splunk dashboards based on the project's domain, for example:
   - **API Performance:** latency percentiles, error rate, throughput over time
   - **Agent Execution:** step count, tool usage distribution, LLM calls per request
   - **Cost Monitoring:** token usage trends, API call costs by model
   - **Error Analysis:** error types, trends, grouped by `correlation_id`
3. Provide ready-to-use **SPL queries** for each dashboard panel
4. Dashboards are managed in Splunk directly — this skill provides the queries, not the dashboard JSON

## Reference

- **Rule:** `@monitoring-and-observability` — mandatory fields, metrics, naming conventions
- **HEC Client:** `@examples_splunk_hec` — Splunk HEC client implementation
- **Timing:** `@examples_performance_timing` — PerformanceTimer context manager
- **SPL Queries:** `@examples_spl_queries` — example SPL queries for analysis
