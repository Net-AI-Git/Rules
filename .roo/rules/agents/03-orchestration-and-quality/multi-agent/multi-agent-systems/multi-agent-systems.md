## Mandate

Design **multi-agent** flows: **micro-agents / Workers** over monoliths; clear roles; **SECTIONS** as the unit of work; deterministic limits and failure isolation.

## Core roles

* **Planner** — strategy before decomposition (`@planner-strategic-planning`).
* **Orchestrator** — user request → **SECTIONS** list; **must not** execute work or emit final user-facing synthesis.
* **Workers** — one SECTION in, one primary write target out; **must not** mutate others’ SECTIONS or the SECTIONS list.
* **Executor** — plan → concrete actions (`@executor-action-translation`).
* **Memory Node** — feedback/context (`@memory-feedback-node`).
* **Synthesizer** — merge worker outputs to **FINAL_OUTPUT**; **must not** spawn new SECTIONS/workers.
* **Contracts:** `@contract-scope-and-boundaries`, `@agent-component-interfaces`.

**See:** `@examples_orchestration.py`, `@examples_sections.py`, `@examples_state_management.py`.

## SECTIONS

Each SECTION: ids, scope, inputs, constraints, **expected output shape**. Workers treat the SECTION as the contract; shared context is read-mostly except designated keys.

## FAN-OUT / FAN-IN

* **OUT:** map SECTIONS → workers (parallel when independent).
* **IN:** collect results into agreed structures; **read many, write one** — append-only shared collections; no two writers on the same scalar key.

## State

**Shared** context for all agents; **worker_state.section** for per-worker payload; **single owner** per state field (`@langgraph-architecture-and-nodes`).

## Reliability

`max_iterations` everywhere it loops; partial results on worker failure; fallback agent optional; deterministic graph routing.

**See:** `@error-handling-and-resilience`.
