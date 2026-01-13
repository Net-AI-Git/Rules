# Prompt Engineering & Management



## 1. Prompt as Code

* **Separation:** Prompts must NOT be hardcoded strings inside Python logic functions.

* **Storage:** Store prompts in dedicated files (e.g., `prompts.py`, YAML, or text templates) or a dedicated directory.

* **Templating:** Use **Jinja2** (or LangChain's PromptTemplates) for dynamic insertion of variables. String concatenation (`+`) for prompts is forbidden.



## 2. Structure & Clarity

* **XML Tagging:** Use XML-style tags (e.g., `<context>...</context>`, `<instructions>...</instructions>`) to clearly delimit sections for the LLM. This significantly improves adherence in modern models (Claude/GPT-4).

* **System Prompts:** Every agent must have a distinct System Prompt defining its `Persona`, `Constraints`, and `Output Format`.



## 3. Versioning

* **Tracking:** Prompts are experimental. Version them (e.g., `prompts/agent_v1.py`, `prompts/agent_v2.py`) to allow A/B testing and rollback.



## 4. Context Management

* **Token Counting:** You must estimate token usage before sending a prompt.

* **Truncation:** Implement logic to truncate "History" or "Context" if it exceeds model limits (FIFO - First In First Out, or Summary-based).
