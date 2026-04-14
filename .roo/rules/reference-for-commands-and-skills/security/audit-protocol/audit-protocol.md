## Mandate

Every significant operation MUST produce an audit event sent to **Splunk via HEC**. This rule defines **what** to audit and which extra fields to include. For **how** to send events (HEC structure, mandatory fields, naming), see `@monitoring-and-observability`.

## 1. Audit Fields (in addition to @monitoring-and-observability mandatory fields)

Every audit event MUST include these fields **on top of** `timestamp`, `correlation_id`, `operation_name`:

| Field | Type | Description |
|-------|------|-------------|
| `event_type` | string | `tool_call` · `state_change` · `api_request` · `db_access` · `auth` · `llm_call` · `error` |
| `actor_id` | string | User ID or agent ID that triggered the action |
| `actor_type` | enum | `user` · `agent` · `system` |
| `resource` | string | What was accessed/modified (table name, endpoint, tool name) |
| `action` | string | Specific action (`read`, `write`, `delete`, `execute`, `login`, `deny`) |
| `result` | enum | `success` · `failure` · `denied` |

Optional but recommended: `tenant_id`, `ip_address`, `session_id`.

## 2. Mandatory Audit Events

These operations MUST always produce audit events:

| Category | Events |
|----------|--------|
| **API** | Every request (endpoint, method, status code, duration) |
| **Auth** | Login, logout, token refresh, failed auth, authorization denied |
| **DB** | Queries, inserts, updates, deletes (table, operation, affected rows) |
| **Tool Calls** | Tool selection (which + why), execution (params sanitized), result (success/failure, duration) |
| **State Changes** | LangGraph node execution (node name, input→output state), errors, rollbacks, human-in-the-loop decisions |
| **LLM Operations** | Every LLM call: model, token usage (input/output), cost, duration. Prompts and responses with PII masked |
| **Errors** | Every caught exception: type, message, stack trace, correlation_id, which operation failed |

## 3. PII Masking

* **Before logging:** Mask PII fields (email, phone, SSN, credit card) in all audit events.
* **Prompts/responses:** Mask PII in LLM prompts and responses before sending to Splunk.
* **Never log:** Passwords, API keys, tokens, secrets — not even masked.

## 4. Log Integrity

* **Append-only:** Audit logs are immutable — no updates, no deletions.
* **Emit on failure:** Use context managers (`PerformanceTimer`) to ensure audit events are emitted even when operations fail.
