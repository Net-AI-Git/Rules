# Comprehensive System Analysis

## Overview

**Synthesis layer:** combine existing artifacts (traces, audit logs, tests, evaluations, metrics) to find **cross-cutting** patterns, correlations, and risk—after specialized commands have done their job. This command does **not** replace detailed LangSmith parsing, performance analysis, or security audit workflows.

## Scope and boundaries

- **In scope:** Time- and correlation-id–based joining of data sources; pattern and anomaly summaries; health-style assessment; recommendations that span more than one subsystem.
- **Out of scope — use instead:** Token/cost/latency per LLM call from LangSmith exports → `/monitoring/analyze-langsmith-traces`. Generic latency/throughput/resource analysis → `/monitoring/performance-analysis`. Audit field validation → `/security/analyze-audit-logs`. Prompt registry + Splunk governance → `/monitoring/audit-prompt-registry-splunk`.

## Rules Applied

- `monitoring-and-observability`
- `security-governance-and-observability`
- `error-handling-and-resilience`
- `cost-and-budget-management`
- `human-in-the-loop-approval`
- `tests-and-validation`
- `llm-evaluation-and-metrics` *(reference rule under `reference-for-commands-and-skills/evaluation/`; use via this command or evaluation workflows — do not `@` manually)*
- `audit-protocol` *(reference rule under `reference-for-commands-and-skills/security/`; use via this command or audit workflows — do not `@` manually)*

## Steps

1. **Gather artifacts (prefer existing reports)** — When available, use outputs from `/monitoring/analyze-langsmith-traces`, `/monitoring/performance-analysis`, `/security/analyze-audit-logs`, `/testing/run-test-suite`, `/testing/run-evaluation-suite`. Raw files only if reports are missing.

2. **Align timestamps and correlation IDs** — Join events across sources using `correlation_id` and time windows per `monitoring-and-observability`.

3. **Identify patterns and anomalies** — Cross-link errors, latency, cost spikes, eval regressions, and approval/HITL events; flag inconsistencies (e.g. high errors with no matching audit trail).

4. **Health and risk summary** — Short narrative: overall status (healthy / degraded / critical), top drivers, cross-system risks.

5. **Recommendations** — Prioritized actions that require **multiple** owners or systems; point to single-domain follow-ups with the relevant `/command` when deeper work is needed.

## Data Sources

- LangSmith traces (JSON), audit logs (JSON), test and evaluation outputs, performance/telemetry excerpts, prior command reports

## Output

- Executive summary and cross-system correlation findings
- Pattern/anomaly list with severity
- Health assessment and prioritized multi-domain recommendations
- Pointers to deeper analysis commands (not a repeat of their full metrics)
