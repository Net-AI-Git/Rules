## Mandate

Define explicit contracts (Interface, ABC, Schema, structured output) **only** at meaningful **integration boundaries**. Do not formalize helpers, single-module logic, or non-swappable internals — that adds cost without replaceability benefit.

## Replaceability test

* **Explicit contract:** The implementation may be swapped (provider, team, test double) without breaking callers.
* **Implicit is enough:** No realistic replacement — rely on types, names, and docstrings.

## When contracts are required

Boundaries where components may **evolve separately**, be **replaced**, or are **swappable** (A/B, providers, tests):

* **Planner↔Executor**, **Agent↔Tool**, **Agent↔Agent**, **LLM↔Code** (structured output).

At boundaries: typed I/O, documented behavior (not implementation), enforce with ABC / Pydantic / JSON Schema.

**See:** `@agent-component-interfaces`, `@data-schemas-and-interfaces`.

## When not to formalize

Internal helpers, single-owner logic, private implementation detail, or single-use code — use implicit contracts (type hints, clear naming).

## Integration

* `@agent-component-interfaces` — Planner / Memory / Executor surfaces.
* `@data-schemas-and-interfaces` — tools and LLM outputs.
* `@multi-agent-systems` — SECTIONS and Agent↔Agent boundaries.

## Decision

1. Replaceable/evolvable boundary? → Explicit contract.  
2. Internal or single-owner? → Implicit.  
3. Unsure? → *“Could we swap this without breaking the system?”* — yes → contract.
