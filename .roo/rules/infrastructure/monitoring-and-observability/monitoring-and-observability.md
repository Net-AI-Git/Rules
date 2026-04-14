## Mandate

All services MUST send metrics, logs, and traces to **Splunk** via **HEC** (HTTP Event Collector) as structured JSON. No `print()` for logging. This rule defines mandatory fields, event structure, metrics, and naming conventions.

## 1. HEC Event Structure

Every event sent to Splunk MUST be a JSON object with these **mandatory fields**:

| Field | Format | Description |
|-------|--------|-------------|
| `timestamp` | ISO 8601, UTC | `datetime.now(timezone.utc).isoformat()` |
| `correlation_id` | UUID | Propagated across service boundaries (HTTP headers, queues, async). Generate UUID when no trace context exists. |
| `operation_name` | string | What operation this event represents |

**For timed operations** (API calls, DB queries, LLM calls, tool executions, agent steps), also include:

| Field | Format | Description |
|-------|--------|-------------|
| `start_time` | ISO 8601, UTC | Operation start |
| `end_time` | ISO 8601, UTC | Operation end |
| `duration_ms` | float | Use `time.perf_counter()` — **not** `time.time()` |
| `operation_type` | string | e.g., `api_call`, `db_query`, `llm_call`, `tool_call` |

**For multi-stage operations**, add: `stage_name`, `stage_latency_ms`, `total_latency_ms`.

Use context managers (e.g., `PerformanceTimer`) to ensure events are emitted even on failure. **See:** `@examples_splunk_hec` for HEC client, `@examples_performance_timing` for PerformanceTimer pattern.

## 2. Mandatory Metrics

Track as structured Splunk events; analyze with **SPL**:

* **Request Rate:** `timechart count` or `stats count` per time unit
* **Error Rate:** Filter by `level=ERROR`; alert if > threshold
* **Latency:** `duration_ms` per event → SPL `perc50`, `perc95`, `perc99`
* **Throughput:** Successful operations per time unit
* **Resource Usage:** CPU, memory, disk, network as metric events
* **Business Metrics:** LLM token usage, agent step count, tool call success rate (domain-specific)

**Reference:** [Splunk Search Reference](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/9.2/introduction/welcome-to-the-search-reference). **See:** `@examples_spl_queries` for SPL examples.

## 3. Naming Conventions

* **Source type:** `{service}:{component}` (e.g., `agent:planner`, `api:auth`)
* **Fields:** `snake_case`, consistent across all events
* **Trace reconstruction:** SPL `transaction correlation_id` or `stats values(operation_name) by correlation_id`

## 4. Health Check Endpoints

* `/health/live` — liveness probe (200 OK)
* `/health/ready` — readiness probe (checks DB, external services; 200 or 503)
* `/health/startup` — for services with long initialization

Implement with FastAPI dependency injection; cache results briefly (5s).

## 5. Alerting & SLO

* **SPL Alerts:** Saved searches with thresholds (e.g., error rate > 5%, P99 > 1s). Require sustained violation (e.g., 5 min) before alerting.
* **Severity:** critical, warning, info. Use suppression windows to prevent alert fatigue.
* **SLI/SLO:** Track availability, latency (P95/P99), error rate in SPL dashboards. Error budget = 100% − SLO; alert when approaching limits.
* **Alert Targets:** PagerDuty, Opsgenie, Slack, email as needed.

**See:** `@audit-protocol` for audit-specific fields and mandatory audit events; `@security-governance-and-observability` for agent security policy (references only, no duplicated field specs).
