# Analyze Audit Logs

## Overview

Parse and assess **audit trail** JSON (or equivalent) for traceability, anomalies, and governance alignment with structured telemetry expectations. Field-level audit semantics for products using the reference spec: `audit-protocol` *(reference under `reference-for-commands-and-skills/security/` — do not `@` manually)*.

## Scope and boundaries

- **In scope:** Log shape, correlation, security-relevant sequences, HITL-related events, masking gaps.
- **Out of scope — use instead:** LangSmith trace analytics → `/monitoring/analyze-langsmith-traces`. Full codebase security scan → `/security/security-audit`.

## Rules Applied

- `security-governance-and-observability`
- `monitoring-and-observability`
- `error-handling-and-resilience`
- `human-in-the-loop-approval`
- `audit-protocol` *(reference; use via this command — do not `@` manually)*

## Steps

1. **Read Audit Logs**
   - Locate audit log files in project directories
     - Search for JSON files containing audit data
     - Look for files in common audit log locations
     - Identify log file formats and structures
   - Parse audit log entries
     - Extract structured log data (JSON format)
     - Validate log structure against governance and observability expectations (required fields, correlation, actor/resource/action/result where applicable)
     - Handle different log formats if present

2. **Validate Log Structure**
   - Verify required fields are present:
     - `timestamp` (ISO 8601 format with timezone)
     - `event_type` (categorized event type)
     - `actor_id` (user ID or agent ID)
     - `actor_type` ("user" | "agent" | "system")
     - `resource` (resource being accessed or modified)
     - `action` (specific action performed)
     - `result` ("success" | "failure" | "denied")
     - `correlation_id` (request/transaction ID)
     - `tenant_id` (if multi-tenant)
     - `metadata` (additional context)
   - Check for log integrity
     - Verify timestamps are sequential and valid
     - Validate correlation IDs are properly propagated
     - Check for missing or malformed entries

3. **Analyze Events by Category**
   - **Tool Calls**:
     - Analyze tool invocation patterns
     - Identify tool selection decisions and reasoning
     - Review tool execution results and failures
     - Check tool access control compliance
   - **State Changes**:
     - Review LangGraph state transitions
     - Analyze node executions and state modifications
     - Identify error states and recovery actions
     - **Human Intervention Tracking**: Check human-in-the-loop intervention points and approval workflows
     - Analyze human intervention patterns and effectiveness
   - **API Requests**:
     - Analyze incoming API request patterns
     - Review authentication and authorization events
     - Check rate limiting compliance
     - Identify unusual request patterns
   - **Data Access**:
     - Review database query patterns
     - Analyze data access operations
     - Check for unauthorized data access attempts
     - Verify data retention policy compliance

4. **Identify Anomalies**
   - **Unusual Access Patterns**:
     - Detect access at unusual times
     - Identify access from unexpected locations
     - Flag rapid successive access attempts
   - **Failed Authorization Attempts**:
     - Count and analyze failed authorization checks
     - Identify repeated denial patterns
     - Check for potential brute force attempts
   - **Error Pattern Analysis**:
     - Identify recurring error types
     - **Error Classification**: Classify errors as transient vs permanent
     - Analyze error recovery patterns
     - Detect cascading failures
     - Track error frequency and trends
   - **Performance Anomaly Detection**:
     - Identify unusual resource consumption patterns
     - Detect latency spikes and performance degradation
     - Flag excessive tool usage or resource waste
     - Analyze performance trends over time
   - **Resource Usage Anomalies**:
     - Identify unusual resource consumption
     - Detect potential DoS attempts
     - Flag excessive tool usage

5. **Governance & observability alignment**
   - Verify entries support end-to-end traceability (correlation IDs, request/session linkage)
   - Check for required semantic fields for audit-style events (actor, resource, action, result) consistent with project observability rules
   - Flag PII or secrets in log payloads (should follow masking/redaction rules)
   - Note gaps that would block incident response or dashboard use — not a GDPR/HIPAA/SOC 2 attestation

6. **Security Incident Detection**
   - **Automated Detection**:
     - Identify potential security incidents from log patterns
     - Flag suspicious activities (unusual access, multiple failures)
     - Detect potential data breaches
   - **Incident Analysis**:
     - Correlate events to identify incident timelines
     - Analyze incident scope and impact
     - Identify affected resources and users
   - **Forensic Analysis**:
     - **Timeline Reconstruction**: Reconstruct detailed incident timelines with event sequencing
     - **Activity Tracking**: Track user activities across sessions with correlation IDs
     - **Root Cause Analysis**: Identify root causes with evidence chain
     - **Incident Correlation**: Correlate related incidents across time periods

7. **Generate Audit Report**
   - Create comprehensive audit log analysis report
   - Include event statistics and patterns
   - Highlight anomalies and security incidents
   - Summarize governance/observability alignment gaps (field coverage, masking, correlation)
   - Include recommendations for improvements

## Data Sources
- Audit log files (JSON format) from local storage
- Audit log directories and file patterns
- Correlation IDs for cross-log analysis
- Configuration files for audit log structure

## Output
A comprehensive audit log analysis report including:
- **Log Statistics**: Total events, event types breakdown, time range coverage
- **Event Analysis**: Detailed analysis by category (tool calls, state changes, API requests, data access)
- **Anomaly Detection**: Identified anomalies with severity levels and context
  - Error patterns with classification (transient vs permanent)
  - Performance anomalies with resource usage analysis
  - Human intervention patterns and approval workflow analysis
- **Governance & observability alignment**: Gaps vs expected structured audit/telemetry fields and traceability (not regulatory certification)
- **Security Incidents**: Detected incidents with detailed timeline reconstruction, impact analysis, and root cause identification
- **Forensic Analysis**: Timeline reconstruction, activity tracking, incident correlation
- **Patterns and Trends**: Operational patterns, usage trends, behavioral analysis, performance trends
- **Recommendations**: Actionable suggestions for improving audit logging and security
