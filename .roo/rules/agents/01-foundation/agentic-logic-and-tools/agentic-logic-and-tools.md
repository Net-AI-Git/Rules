## LangChain fundamentals

* **LCEL:** Prefer LangChain Expression Language (LCEL) for composable pipelines.
* **Tools:** Define tools with the `@tool` decorator; document purpose, parameters, returns, and examples in the docstring.
* **Verbose / debug:** Use `verbose=True` (or equivalent) **only in local/dev** when debugging chains. **Do not** rely on verbose output for production observability.

## Observability (Splunk only)

* **No `print()` for logging.** Emit structured events to **Splunk via HEC** per `@monitoring-and-observability` (`timestamp`, `correlation_id`, `operation_name`, `duration_ms` for tool/LLM steps).
* **Tool and LLM spans:** Log tool invocations, model turns, and errors with `correlation_id` propagated from the request. Audit-sensitive tool use per `@audit-protocol`.
* **Streaming / traces:** Use `astream_events` (or LangGraph stream modes) to drive **metrics and log events**, not console `print_stream` for production. Local dev may print only for ad-hoc debugging sessions.

## Agent internals

* **Structured output (Pydantic v2):** Use `pydantic.BaseModel` with `Field(description=...)`; bind with `with_structured_output()` or `.bind_tools(...)`. See `@data-schemas-and-interfaces` and `@langgraph-architecture-and-nodes`.
* **Scratchpad:** Keep intermediate reasoning **out of the model context** when required; if persisted, store **outside** the prompt payload. **Trace scratchpad steps via Splunk** (same mandatory fields)—do not treat a local log file as the primary audit trail.
* **Tool binding:** Bind the allowed tool set explicitly; wrap tool results in `ToolMessage` with stable tool identifiers.
* **Security:** Follow `@prompt-injection-prevention` and `@security-governance-and-observability` for untrusted input and tool blast radius.

## Performance & caching

* **Module-level cache:** Use a module-level dict for heavy in-process data (e.g. DataFrames) to avoid re-tokenizing large blobs.
* **Data stores:** For Redis/Oracle in tools, follow `@redis-cache` / `@oracle-database`.

## Optional patterns

* **Summarization / routing maps:** Implement as ordinary tools or nodes; instrument each decision path to Splunk like any other `operation_name`.
