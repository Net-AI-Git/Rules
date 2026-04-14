---
description: "Verify **prompt registry** coverage and **Splunk** (or HEC-aligned) telemetry for prompt lifecycle and version signals\u2014per `prompt-engineering-and-management` and `monitoring-and-observability`."
---

# Audit Prompt Registry Splunk

## Overview

Verify **prompt registry** coverage and **Splunk** (or HEC-aligned) telemetry for prompt lifecycle and version signals—per `prompt-engineering-and-management` and `monitoring-and-observability`.

## Scope and boundaries

- **In scope:** Registry vs runtime, event schema, masking, version/regression signals in logs.
- **Out of scope — use instead:** General audit JSON files on disk → `/security-analyze-audit-logs`. LangSmith traces → `/monitoring-analyze-langsmith-traces`.

## Rules Applied

- `prompt-engineering-and-management`
- `monitoring-and-observability`
- `security-governance-and-observability`
- `audit-protocol` *(reference under `reference-for-commands-and-skills/security/` — do not `@` manually)*

## Steps

1. **Verify Registry Coverage**
   - Enumerate active prompt IDs and expected versions from the registry.
   - Confirm each active prompt has ownership, metadata, and lifecycle status.
   - Identify unregistered prompts referenced by runtime systems.

2. **Validate Splunk Event Flow**
   - Confirm prompt load/retrieval/version-change events are emitted.
   - Validate required event fields (prompt_id, version, correlation_id, timestamp, environment).
   - Check for ingestion gaps, malformed events, or delayed indexing.

3. **Analyze Prompt Performance Signals**
   - Aggregate quality, latency, cost, and error metrics by prompt version.
   - Detect outliers and regressions compared to recent baseline.
   - Correlate behavior with deployment windows and version changes.

4. **Review Governance and Security**
   - Verify sensitive fields are masked in prompt-related logs.
   - Confirm auditability for version promotions, rollbacks, and deprecations.
   - Identify policy violations (missing metadata, missing audit events, unsafe logging).

5. **Produce Remediation Plan**
   - Prioritize findings by severity and blast radius.
   - Define fixes for instrumentation, schema compliance, and governance gaps.
   - Assign ownership and due dates for critical issues.

## Data Sources
- Prompt registry data (prompt IDs, versions, metadata, lifecycle states)
- Splunk indexes containing prompt lifecycle and performance events
- Runtime logs and trace correlation identifiers
- Deployment change records for version transitions

## Output
An audit report for prompt registry observability including:
- **Coverage Status**: Registered vs unregistered prompt usage
- **Telemetry Health**: Event completeness, schema validity, and ingestion latency
- **Performance Insights**: Version-level quality, latency, cost, and error trends
- **Governance Findings**: Audit and security compliance issues
- **Remediation Plan**: Prioritized actions with ownership guidance
