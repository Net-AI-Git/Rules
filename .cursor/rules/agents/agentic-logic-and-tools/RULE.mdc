---
description: "LangChain fundamentals, tool definitions, and agent internals"
alwaysApply: false
---

## LangChain Fundamentals
* **LCEL:** Always use LangChain Expression Language (LCEL).
* **Verbose Mode:** Set `verbose=True` when initializing LangChain components for better debugging and observability.
* **Tool Definition:** Define tools using the `@tool` decorator.
* **Documentation:** Provide deep explanations for every tool: what it does, parameters, return values, input/output examples, and docstrings.

## Agent Internals
* **Scratchpad:** Maintain an internal scratchpad for each agent, saved to a long LOG file for debugging, but **excluded** from the context window passed to the model.
* **Tool Binding:** Bind tools to the model.
* **Tool Usage Display:** Print the sequence of messages and tools used using `stream_mode` with `print_stream` for a clean, readable presentation.
* **Output Wrapping:** Wrap results in `ToolMessage` and include the `TOOL ID`.

## Performance & Caching
* **Module-Level Caching:** Use a module-level dictionary to cache loaded data (e.g., DataFrames) outside of functions.
    * **Benefits:** Reduces token usage (refer by reference), improves performance (RAM vs Disk), and maintains availability between calls.
    * **Clean Interface:** Avoids passing cache objects as parameters to every tool.

* **See:** `performance-optimization.md` for comprehensive performance optimization strategies including caching, connection pooling, and database query optimization.

## Special Tools
* **Summarization Tool:** Apply logic to determine where summarization is needed and implement it.
* **Dynamic Mapping:** Use mapping dictionaries for dynamic calls.
