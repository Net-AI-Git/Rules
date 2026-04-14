---
description: "Sequences the **monitoring** subcommands in a recommended order and aggregates a single summary. **Does not** duplicate their steps\u2014see each command for details. **Does not** include `/monitoring-profile-code-bottlenecks` (Python profile..."
---

# Run All Monitoring

## Overview

Sequences the **monitoring** subcommands in a recommended order and aggregates a single summary. **Does not** duplicate their steps—see each command for details. **Does not** include `/monitoring-profile-code-bottlenecks` (Python profiler); run that separately when optimizing hot paths.

## Scope and boundaries

- **In scope:** Orchestration + consolidated report.
- **Out of scope:** Re-deriving metrics that belong to `/monitoring-analyze-langsmith-traces` or `/monitoring-performance-analysis`.

## Rules Applied

- `monitoring-and-observability`
- `agentic-logic-and-tools`
- `error-handling-and-resilience`
- `cost-and-budget-management`
- `model-routing-and-selection`
- `security-governance-and-observability`
- `human-in-the-loop-approval`
- `tests-and-validation`
- `llm-evaluation-and-metrics` *(reference; do not `@` manually)*
- `audit-protocol` *(reference; do not `@` manually)*

## Steps

1. Run `/monitoring-analyze-langsmith-traces` — if traces missing, note and continue.
2. Run `/monitoring-performance-analysis` — if metrics missing, note and continue.
3. Run `/monitoring-audit-prompt-registry-splunk` — if Splunk/registry unavailable, partial findings only.
4. Run `/monitoring-comprehensive-system-analysis` — synthesize using prior outputs where possible.
5. Produce **one** aggregated dashboard-style summary: health (Healthy/Degraded/Critical), top issues, alerting recommendations, cross-links to each sub-report.

## Data Sources

- Outputs of the four commands above; raw JSON traces/logs only when sub-reports are absent.

## Output

- Single executive summary plus pointers to each subcommand’s detailed findings
- No duplicate metric tables already produced by step 1–2

## Execution order

`analyze-langsmith-traces` → `performance-analysis` → `audit-prompt-registry-splunk` → `comprehensive-system-analysis` → aggregated summary
