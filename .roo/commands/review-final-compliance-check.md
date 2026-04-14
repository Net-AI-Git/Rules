---
description: "Governance pass before commit: map the current change set to **applicable Rules** under `.roo/rules/` (agents, API, data, configuration, infrastructure, security, tests). This command covers **cross-cutting** expectations. It **does not*..."
---

# Final Compliance Check

## Overview

Governance pass before commit: map the current change set to **applicable Rules** under `.roo/rules/` (agents, API, data, configuration, infrastructure, security, tests). This command covers **cross-cutting** expectations. It **does not** duplicate line-by-line code review—that is owned by `/review-code-review-checklist`.

## Scope and boundaries

- **In scope:** Identify which Rule domains apply to the work; verify architecture, configuration, prompts, tests, observability expectations, HITL, and security governance **when relevant to this repository**.
- **Out of scope — use instead:** Detailed style, formatting, and the PR checklist → `/review-code-review-checklist` (run first; cite its output here, do not repeat those checks). Vulnerability and dependency-focused review → `/security-security-audit`. Splunk/LangSmith deep dives → `/monitoring/*` commands.

## Rules Applied

- `core-python-standards`
- `error-handling-and-resilience`
- `tests-and-validation`
- `langgraph-architecture-and-nodes`
- `multi-agent-systems`
- `configuration-and-dependency-injection`
- `prompt-engineering-and-management`
- `data-schemas-and-interfaces`
- `api-interface-and-streaming`
- `api-documentation-standards`
- `monitoring-and-observability`
- `security-governance-and-observability`
- `prompt-injection-prevention`
- `agentic-logic-and-tools`
- `human-in-the-loop-approval`
- `cost-and-budget-management`
- `llm-evaluation-and-metrics` *(reference rule under `reference-for-commands-and-skills/evaluation/`; use via this command or evaluation workflows — do not `@` manually)*

## Steps

1. **Ingest code review** — Run `/review-code-review-checklist` if not already done. Capture pass/fail and **only** items that inform governance (e.g. missing tests affecting compliance); do not re-score purely stylistic findings already covered there.

2. **Map applicability** — From diffs and touched paths, list which Rule domains apply (e.g. graph nodes, multi-agent, HTTP API, HEC logging, prompts).

3. **Architecture & agents (if applicable)** — Check expectations per `langgraph-architecture-and-nodes`, `multi-agent-systems`, `agentic-logic-and-tools` (node structure, resilience patterns, state ownership).

4. **Configuration & prompts (if applicable)** — `configuration-and-dependency-injection`, `prompt-engineering-and-management` (settings, secrets hygiene, prompt lifecycle).

5. **Data & API (if applicable)** — `data-schemas-and-interfaces`, `api-interface-and-streaming`, `api-documentation-standards`.

6. **Observability & operations (if applicable)** — `monitoring-and-observability` (structured events, correlation, HEC-style fields where the codebase emits telemetry); `cost-and-budget-management` where budgets apply.

7. **Security** — `security-governance-and-observability`, `prompt-injection-prevention`.

8. **Tests & evaluation hooks (if applicable)** — `tests-and-validation`; evaluation metrics per reference `llm-evaluation-and-metrics` only if the product uses that workflow.

9. **HITL (if applicable)** — `human-in-the-loop-approval` for high-impact flows.

10. **Compliance matrix** — Build a compact table: Rule domain → status (met / gap / N/A) → evidence. **Verdict:** Pass / Needs attention / Block.

## Data Sources

- Report from `/review-code-review-checklist`
- Git diff, touched files, configs, tests, CI definitions when present

## Output

- Summary verdict and compliance matrix by Rule domain
- Gaps with severity (no duplication of the full code-review checklist)
- Prioritized follow-ups before merge
