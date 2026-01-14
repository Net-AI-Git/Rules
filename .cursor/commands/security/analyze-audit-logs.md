# Analyze Audit Logs

## Overview
Comprehensive analysis of audit logs to identify security incidents, compliance issues, anomalies, and operational patterns. This command examines audit trails from local JSON files to ensure accountability, traceability, and regulatory compliance.

## Rules Applied
- `audit-protocol` - Audit trail requirements, log structure, compliance checks
- `monitoring-and-observability` - Log aggregation, correlation IDs, distributed tracing
- `security-governance-and-observability` - Security event monitoring and incident detection

## Steps

1. **Read Audit Logs**
   - Locate audit log files in project directories
     - Search for JSON files containing audit data
     - Look for files in common audit log locations
     - Identify log file formats and structures
   - Parse audit log entries
     - Extract structured log data (JSON format)
     - Validate log structure against audit protocol requirements
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
     - Check human-in-the-loop intervention points
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
   - **Error Patterns**:
     - Identify recurring error types
     - Analyze error recovery patterns
     - Detect cascading failures
   - **Resource Usage Anomalies**:
     - Identify unusual resource consumption
     - Detect potential DoS attempts
     - Flag excessive tool usage

5. **Compliance Verification**
   - **GDPR Compliance**:
     - Verify data access logging for data subject rights
     - Check consent management tracking
     - Validate data processing records
     - Review data deletion audit trails
   - **HIPAA Compliance** (if applicable):
     - Verify PHI access logging
     - Check access control enforcement
     - Validate audit trail completeness
   - **SOC 2 Compliance**:
     - Verify access control change logging
     - Check system configuration change tracking
     - Review incident response logging

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
     - Reconstruct incident timelines
     - Track user activities across sessions
     - Identify root causes

7. **Generate Audit Report**
   - Create comprehensive audit log analysis report
   - Include event statistics and patterns
   - Highlight anomalies and security incidents
   - Provide compliance status assessment
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
- **Compliance Status**: GDPR, HIPAA, SOC 2 compliance verification results
- **Security Incidents**: Detected incidents with timeline reconstruction and impact analysis
- **Patterns and Trends**: Operational patterns, usage trends, and behavioral analysis
- **Recommendations**: Actionable suggestions for improving audit logging and security
