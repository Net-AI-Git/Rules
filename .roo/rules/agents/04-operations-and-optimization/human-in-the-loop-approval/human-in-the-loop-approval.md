## Mandate

Every **human approval** interrupt ships a structured **Approval Context** — not free-form chat only — so risk, cost, and proposed changes are **measurable** and **auditable**.

**See:** `@examples_approval_context.py`.

## Required fields (adapt names to your codebase)

* `risk_level` — e.g. low | medium | high | critical  
* `estimated_cost` — USD (or org currency)  
* `proposed_diff` — structured change description (resource, action, before/after)  
* `action_description` — human-readable summary  
* `current_state_snapshot` — relevant pre-action state  
* Optional: deadline, alternatives, rollback, history  

## Process

Build context → interrupt → human approve/reject/change → resume graph; persist pending approval in state; handle **timeouts** (policy: reject, escalate, or auto-approve low-risk only if explicitly allowed).

## Integration

* **Graph:** `@langgraph-architecture-and-nodes` (interrupts/checkpoints).
* **Budget:** `@cost-and-budget-management` (estimated vs actual).
* **Audit:** `@audit-protocol` for approval events and decisions.
* **Security:** `@security-governance-and-observability` for sensitive actions.
