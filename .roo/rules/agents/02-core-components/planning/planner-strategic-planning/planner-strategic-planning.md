## Mandate

Implement a **Planner** that performs **strategic planning** before task decomposition: goals, environment analysis, risk/cost/benefit, and a structured plan. It runs **before** the Orchestrator and uses **Memory Node** feedback to improve over time.

## Responsibilities

* **Goals:** Main and sub-goals, success criteria, constraints from the user request.
* **State:** Context, resources, limits; load relevant memories from Memory Node.
* **Evaluate:** Risks, costs, benefits, trade-offs for candidate approaches.
* **Output:** `StrategicPlan` (not fine-grained SECTIONS — that is Orchestrator).

**See:** `@examples_planner_node.py`, `@examples_goal_setting.py`, `@examples_risk_assessment.py`.

## MUST NOT

* **Decompose** into SECTIONS (Orchestrator) or **execute** work (Executor/Workers).
* **Implement** physical memory storage (`@memory-and-archival-management`) — use Memory Node as the facade.

## Node pattern

**READ** request, context, memories → **DO** plan + evaluate → **WRITE** `strategic_plan`, goals, risk notes → **CONTROL** Memory Node or Orchestrator. Own the strategic plan fields.

**See:** `@langgraph-architecture-and-nodes`.

## Integration

* **Interface:** `@agent-component-interfaces` (`plan`, evaluations, goals as your codebase defines).
* **Memory:** `@memory-feedback-node`, `@memory-and-archival-management`.
* **Orchestrator:** `@multi-agent-systems` (handoff plan → SECTIONS).
* **Errors:** `@error-handling-and-resilience`.
