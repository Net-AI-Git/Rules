# Agents Rules – Phased Organization

Rules in this folder are organized by **development phase** so you know when to use each one while building agentic AI systems.

## Phase 1 – Foundation (`01-foundation/`)

**When:** Before you start building. Architecture decisions, graph design, state, and when to define contracts.

- **must/** – Required for every agentic system:
  - `langgraph-architecture-and-nodes` – Workflow design, READ→DO→WRITE→CONTROL, TypedDict state
  - `agentic-logic-and-tools` – LangChain basics, LCEL, tools, PydanticAI in nodes
  - `contract-scope-and-boundaries` – When to use explicit contracts vs implicit (replaceability test)
- **interfaces/** – Use when defining boundaries between Planner/Memory/Executor:
  - `agent-component-interfaces` – API contracts (ABCs) for Planner, Memory, Executor

## Phase 2 – Core Components (`02-core-components/`)

**When:** Implementing Planner, Executor, and Memory (including storage).

- **planning/** – `planner-strategic-planning` – Goals, risk assessment, action plans before decomposition
- **execution/** – `executor-action-translation` – Translate plans to concrete actions, coordinate execution
- **memory/** – `memory-feedback-node`, `memory-and-archival-management` – Feedback loop, learning, long-term storage (Vector DB / PostgreSQL)

## Phase 3 – Orchestration & Quality (`03-orchestration-and-quality/`)

**When:** Adding Orchestrator, Workers, Synthesizer, and quality gates.

- **multi-agent/** – `multi-agent-systems` – Orchestrator/Worker/Synthesizer, SECTIONS, FAN-OUT/FAN-IN
- **quality/** – `reflection-and-self-critique` – Reviewer Node before synthesis, self-evaluation loop

## Phase 4 – Operations & Optimization (`04-operations-and-optimization/`)

**When:** Preparing for production: cost, tokens, context size, HITL, model selection.

- `cost-and-budget-management` – BudgetState, token limits, guardrails
- `context-compression-and-optimization` – Context window management, summarization, trimming
- `model-routing-and-selection` – Dynamic routing by task complexity, multi-provider failover
- `human-in-the-loop-approval` – Approval Context schema for HITL (risk, cost, proposed_diff)

## Quick reference

| Phase | Use when |
|-------|----------|
| 01 Foundation | Designing workflow and contracts |
| 02 Core | Implementing Planner, Executor, Memory |
| 03 Orchestration | Adding multi-agent flow and Reviewer |
| 04 Operations | Production: cost, context, routing, HITL |
