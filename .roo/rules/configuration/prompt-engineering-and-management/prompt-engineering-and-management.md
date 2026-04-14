## 1. Prompt as Code

* **Separation:** Prompts must NOT be hardcoded strings inside Python logic functions.

* **Storage:** Store prompts in dedicated files (e.g., `prompts.py`, YAML, or text templates) or a dedicated directory.

* **Templating:** Use **Jinja2** (or LangChain's PromptTemplates) for dynamic insertion of variables. String concatenation (`+`) for prompts is forbidden.



## 2. Structure & Clarity

* **XML Tagging:** Use XML-style tags (e.g., `<context>...</context>`, `<instructions>...</instructions>`) to clearly delimit sections for the LLM. This significantly improves adherence in modern models (Claude/GPT-4).

* **System Prompts:** Every agent must have a distinct System Prompt defining its `Persona`, `Constraints`, and `Output Format`.



## 3. Versioning

* **Tracking:** Prompts are experimental. Version them (e.g., `prompts/agent_v1.py`, `prompts/agent_v2.py`) to allow A/B testing and rollback.

* **Version Control:**
  * **Semantic Versioning:** Use semantic versioning for prompts (e.g., `v1.0.0`, `v1.1.0`, `v2.0.0`)
  * **Version Tags:** Tag versions with meaningful names (e.g., `production`, `experimental`, `deprecated`)
  * **Version History:** Maintain changelog for prompt versions documenting changes and rationale

* **A/B Testing:**
  * **Parallel Versions:** Run multiple prompt versions in parallel for comparison
  * **Traffic Splitting:** Split traffic between versions (e.g., 50/50, 90/10)
  * **Metrics Collection:** Collect performance metrics for each version
  * **Winner Selection:** Select winning version based on metrics (quality, cost, latency)

* **Rollback Strategy:**
  * **Quick Rollback:** Maintain ability to quickly rollback to previous version
  * **Version Registry:** Keep registry of all prompt versions with metadata
  * **Rollback Triggers:** Define conditions for automatic rollback (e.g., quality drop, errors)

**See:** `@examples_prompt_versioning.py` for version control patterns and A/B testing implementation.

## 4. Prompt Registry and Splunk Observability

* **Mandate:** Use a **Prompt Registry** as the single source of truth for prompt identity, ownership, lifecycle, and version history.
* **Auditability:** Prompt retrieval, version selection, promotion, rollback, and deprecation events must be logged.
* **Observability:** Prompt performance metrics (quality, latency, cost, success/error rates) must be emitted with correlation IDs for analysis.
* **Splunk Requirement:** Registry and performance events must be sent to Splunk (HEC) for audit trails and monitoring.

**Execution Workflow:** Use `/monitoring-audit-prompt-registry-splunk` for operational audits.

## 5. YAML Management

* **Structured Storage:** Store prompts in YAML files for structured, readable format.

* **YAML Structure:**
  * **Metadata:** Version, author, description, tags
  * **Prompt Content:** Actual prompt text with variables
  * **Variables:** Define variables and their types/descriptions
  * **Examples:** Include example inputs/outputs
  * **Tests:** Embed test cases in YAML

* **YAML Schema:**
  ```yaml
  version: "1.0.0"
  name: "agent_system_prompt"
  description: "System prompt for main agent"
  variables:
    - name: "user_context"
      type: "string"
      description: "User context information"
  prompt: |
    You are an expert AI assistant...
    <context>{{ user_context }}</context>
  examples:
    - input: { user_context: "..." }
      expected_output: "..."
  ```

* **YAML Tools:**
  * **Validation:** Validate YAML schema before use
  * **Parsing:** Parse YAML to extract prompts and variables
  * **Templating:** Use YAML with Jinja2 for dynamic prompts

**See:** `@examples_prompt_versioning.py` for YAML management patterns.

## 6. Prompt Registry

* **Centralized Management:** Maintain one registry for all prompts in the system.
* **Required Metadata:** Each prompt must include prompt ID, version, ownership, lifecycle status, and tags.
* **Runtime Lookup:** Prompt selection must resolve from registry state (or a validated cache), not hardcoded versions.
* **Deprecation Policy:** Deprecated prompts must include migration targets and removal timelines.

