## Workflow design

* **State:** `TypedDict` for graph state; flat, clear field names; agree Graph shape with the team before large refactors.
* **Graph:** Edges and conditional routing for loops/branches/HITL — avoid tangled inline control flow in one node.
* **Visualization:** Save `get_graph().draw_png()` (e.g. under `images/`).
* **Separation:** Split validation, integration, and business logic across nodes; handle external failures with fallbacks.
* **Quality:** Test nodes in isolation; grow graphs incrementally; keep nodes single-purpose and state fields owned by one writer.

## Node pattern (mandatory)

**READ** → **DO** → **WRITE** → **CONTROL**: one logical task per node; no comment-only nodes.

## DO phase: Pydantic v2 + LangChain

* LangGraph owns structure, state, edges, interrupts, checkpoints — not a separate “orchestration framework” inside nodes.
* LLM outputs: `pydantic.BaseModel` + `Field(description=...)`; `with_structured_output()` or `.bind_tools(...)`. Parse failures at the boundary — never treat raw strings as final state. See `@data-schemas-and-interfaces`, `@agentic-logic-and-tools`.
* Inject DB/HTTP/settings via closures, graph config, or explicit parameters (ordinary Python DI).
* Non-LLM nodes: deterministic logic; optional Pydantic for I/O validation.

## Errors & resilience

* `try/except` around core logic; append errors to a dedicated state field; route repeated failures to error/HITL paths; reset error counters on success; add supervisor summaries to `messages` where useful.

**See:** `@error-handling-and-resilience` for retries, circuit breakers, degradation.

## Checkpoints & interrupts

Persist checkpoints; use interrupts for HITL per `@human-in-the-loop-approval`.

## Multi-agent

**See:** `@multi-agent-systems` for Orchestrator/Worker/Synthesizer, SECTIONS, FAN-OUT/FAN-IN.
