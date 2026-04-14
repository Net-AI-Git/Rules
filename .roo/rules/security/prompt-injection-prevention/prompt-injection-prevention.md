## Mandate

User-controlled text **MUST** be sanitized and validated before it is embedded in prompts or influences tool calls. Injection can hijack instructions, exfiltrate secrets, or trigger unauthorized tools. **Fail closed:** reject or strip unsafe input rather than passing it through silently.

## 1. Where to Apply

| Stage | Action |
|-------|--------|
| **API / entry** | First sanitization and length limits (middleware or dependency). |
| **Before prompt build** | Second pass: delimiters, instruction-like patterns, encoding tricks. |
| **Before LLM / tool** | Final check; validate structured tool args; never trust raw user strings in system prompts. |

## 2. Techniques (combine layers)

* **Normalize and bound:** UTF-8, strip control chars where unsafe, enforce `max_length` on every string field.
* **Escape / fence:** When embedding user text inside prompts, use clear delimiters (e.g. XML/markdown fences) and escape or neutralize characters that break structure (angle brackets, backticks, triple quotes).
* **Filter:** Block or remove known override phrases and fake system roles (see §3). Maintain a small allowlist for domains that need exceptions.
* **Schema:** Use **Pydantic** (or equivalent) for request bodies and tool arguments — types, enums, `Field(max_length=...)`. See `@data-schemas-and-interfaces`.

**Code patterns:** `@examples_input_sanitization.py`, `@examples_injection_detection.py`, `@examples_validation_patterns.py`.

## 3. Detection

* **String patterns:** e.g. “ignore previous instructions”, “you are now”, “system:”, “### instructions”, delimiter breaks, pasted code blocks pretending to be system messages.
* **Obfuscation:** Base64/URL-encoded instructions, unusual Unicode homoglyphs — consider lightweight checks or a classifier for high-risk surfaces.
* **Response:** Log attempts (Splunk HEC, `@monitoring-and-observability` fields); optionally block, sanitize, or route for review; tune false positives with allowlists.

## 4. Outputs and Tools

* **LLM output:** Validate tool calls and structured outputs before execution (no run of shell/SQL/API from unchecked model text). Blast radius and tool policy: `@security-governance-and-observability`.
* **Tools:** Reject tool calls with unexpected argument shapes or disallowed values.

## 5. References

* **Observability / audit:** `@monitoring-and-observability` (HEC events); `@audit-protocol` (security-relevant audit fields for denied / suspicious input).
* **API / agents:** `@api-interface-and-streaming`, `@agentic-logic-and-tools`.
