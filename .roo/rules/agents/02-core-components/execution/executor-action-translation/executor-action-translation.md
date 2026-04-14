## Mandate

Implement an **Executor** between Planner/Orchestrator and **Workers**: translate strategic plans into **concrete actions**, coordinate execution, react to runtime changes, and report results. It does **not** own strategy or task decomposition.

## Responsibilities

* **Translate:** `StrategicPlan` → ordered `ConcreteAction` list (API, tools, files, DB, commands); validate feasibility and dependencies.
* **Coordinate:** Dispatch to Workers/tools; sequential/parallel/conditional execution; collect and validate outcomes.
* **Monitor:** Track status/errors; format experiences for `@memory-feedback-node`.

**See:** `@examples_executor_node.py`, `@examples_action_translation.py`, `@examples_execution_coordination.py`.

## MUST NOT

* **Plan** strategically (Planner) or **decompose** into SECTIONS (Orchestrator).
* **Specialize** in a domain task (Workers) — Executor coordinates only.

## Node pattern

**READ** `strategic_plan`, sections/context → **DO** translate + dispatch + monitor → **WRITE** `concrete_actions`, `execution_status`, results → **CONTROL** route to Workers/Memory/next. Single-writer fields for execution outputs.

**See:** `@langgraph-architecture-and-nodes`.

## Integration

* **Interface:** `@agent-component-interfaces` (`translate_plan`, `execute_action`, `monitor_execution` as appropriate).
* **Multi-agent:** `@multi-agent-systems` (SECTIONS, FAN-OUT/FAN-IN).
* **Tools:** `@agentic-logic-and-tools`.
* **Errors:** `@error-handling-and-resilience`.
