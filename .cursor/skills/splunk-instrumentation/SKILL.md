---
name: splunk-instrumentation
description: Scan recent code changes (or specified files) and add comprehensive Splunk HEC instrumentation — observability + audit trail + PII masking. Ensures end-to-end monitoring.
disable-model-invocation: true
---

# Splunk Instrumentation

End-to-end instrumentation for Splunk. Scans code, identifies missing logging/tracing/audit events, and adds them following `@monitoring-and-observability` (HEC structure) and `@audit-protocol` (what to audit).

Trigger with **`@splunk-instrumentation`**.

## Workflow

### Step 1: Determine Scope

Check what to instrument:

1. **If user specifies files/modules** — use those.
2. **If user says "recent changes"** — run `git diff --name-only HEAD~5` (or the range the user specifies) to find changed files.
3. **If user says "everything"** — scan all Python files in `src/` or the project root.

Ask only if unclear:
- **Scope:** Which files? Recent changes? All?
- **Custom fields:** Any business-specific fields beyond the mandatory ones?

### Step 2: Read Standards

Read both rules to get the current standards:

**From `@monitoring-and-observability`** (HEC structure):
- Mandatory fields: `timestamp`, `correlation_id`, `operation_name`
- Timed operations: also `start_time`, `end_time`, `duration_ms`, `operation_type`
- Multi-stage: also `stage_name`, `stage_latency_ms`, `total_latency_ms`
- Naming: `snake_case` fields, source type `{service}:{component}`

**From `@audit-protocol`** (what to audit):
- Audit fields: `event_type`, `actor_id`, `actor_type`, `resource`, `action`, `result`
- Mandatory events: API requests, auth, DB access, tool calls, state changes, LLM operations, errors
- PII masking requirements

### Step 3: Scan and Identify Gaps

For each file in scope, check for:

| Gap | What to look for |
|-----|-----------------|
| **Missing timing** | Functions/endpoints without `PerformanceTimer` or manual `duration_ms` |
| **Missing correlation** | No `correlation_id` propagation across service calls |
| **`print()` statements** | Any `print()` used for logging — must be HEC events |
| **Missing API audit** | Endpoints without request logging (method, status, actor_id) |
| **Missing auth audit** | Login/logout/token operations without audit events |
| **Missing DB audit** | Database operations without audit events (table, operation, affected rows) |
| **Missing tool audit** | Tool executions without audit events (tool name, params, result) |
| **Missing state audit** | LangGraph node executions without state change logging |
| **Missing LLM audit** | LLM calls without token usage, model name, cost, duration |
| **Missing error audit** | Exceptions caught without error events to Splunk |
| **PII exposure** | Email, phone, SSN, credit card logged without masking |
| **Secrets in logs** | Passwords, API keys, tokens appearing in log events |

### Step 4: Add Instrumentation

For each gap found:

1. **HEC Client:** Import the project's Splunk HEC client. If none exists, create one based on `@examples_splunk_hec`.
2. **PerformanceTimer:** Wrap timed operations with `PerformanceTimer` context manager (see `@examples_performance_timing`). Emits events even on failure.
3. **Observability fields:** Every event MUST include `timestamp`, `correlation_id`, `operation_name`.
4. **Audit fields:** Add `event_type`, `actor_id`, `actor_type`, `resource`, `action`, `result` for audit events.
5. **Error events:** Every `except` block must emit an error event with: exception type, message, `correlation_id`, which operation failed.
6. **PII masking:** Mask PII before logging. Never log secrets.
7. **Business metrics:** Add domain-specific fields (token usage, tool call success, agent step count).
8. **Naming:** `snake_case` fields, source type `{service}:{component}`.

### Step 5: Verify

- [ ] Every API endpoint emits request audit event (method, status, actor_id, duration)
- [ ] Every auth operation emits auth audit event
- [ ] Every DB operation emits db_access audit event (table, operation, rows)
- [ ] Every tool call emits tool_call audit event (tool, params sanitized, result)
- [ ] Every LangGraph node emits state_change audit event
- [ ] Every LLM call emits llm_call audit event (model, tokens, cost, duration)
- [ ] Every exception emits error audit event
- [ ] `correlation_id` propagated across all service boundaries
- [ ] No `print()` remains for logging
- [ ] `time.perf_counter()` used for duration (not `time.time()`)
- [ ] No PII in logs without masking
- [ ] No secrets in logs at all

### Step 6 (Optional): Dashboard Consultation

If the user asks about dashboards:

1. Review the instrumented fields and metrics
2. Suggest Splunk dashboards:
   - **API Performance:** latency percentiles, error rate, throughput
   - **Agent Execution:** step count, tool usage, LLM calls per request
   - **Audit Trail:** actor activity, authorization decisions, tool access patterns
   - **Cost Monitoring:** token usage trends, API call costs by model
   - **Error Analysis:** error types, trends, grouped by `correlation_id`
   - **Security:** failed auth attempts, denied actions, anomalous access patterns
3. Provide ready-to-use **SPL queries** for each panel

## Reference

- **HEC Structure:** `@monitoring-and-observability` — mandatory fields, metrics, naming
- **Audit Events:** `@audit-protocol` — what to audit, audit fields, PII masking
- **HEC Client:** `@examples_splunk_hec` — Splunk HEC client implementation
- **Timing:** `@examples_performance_timing` — PerformanceTimer context manager
- **SPL Queries:** `@examples_spl_queries` — example SPL queries
