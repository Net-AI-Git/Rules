# Run All Security

## Overview
Execute all security commands in sequence: compliance check, audit log analysis, and comprehensive security audit. This master command runs the complete security workflow to ensure system security, compliance, and audit trail integrity.

## Rules Applied
- `security-governance-and-observability` - Security governance requirements
- `audit-protocol` - Audit trail requirements and compliance
- `data-schemas-and-interfaces` - Data handling and PII protection

## Steps

1. **Compliance Check**
   - Execute `/security/compliance-check` command
   - Wait for completion and review results
   - **Error Handling**:
     - If compliance check fails: Continue with warning, include in final report
     - If compliance issues found: Mark as non-blocking but include in report
     - If compliance passes: Proceed to next step
   - **Output**: Compliance report with GDPR, HIPAA, SOC 2 status

2. **Analyze Audit Logs**
   - Execute `/security/analyze-audit-logs` command
   - Wait for completion and review results
   - **Error Handling**:
     - If audit log analysis fails: Continue with warning, report data availability issues
     - If security incidents detected: Mark as critical, include in final report
     - If analysis completes: Proceed to next step
   - **Output**: Audit log analysis report with anomalies and incidents

3. **Security Audit**
   - Execute `/security/security-audit` command (uses results from steps 1 and 2)
   - Wait for completion and review results
   - **Error Handling**:
     - If security audit fails: Report error but include partial results
     - If critical vulnerabilities found: Mark as blocking issues
     - If high/medium vulnerabilities found: Include in final report
     - If audit completes: Generate final report
   - **Output**: Comprehensive security audit report

4. **Generate Comprehensive Security Report**
   - Aggregate results from all three commands
   - Create summary with overall security status
   - Highlight critical vulnerabilities and compliance gaps
   - Provide prioritized remediation recommendations
   - Include links to detailed reports from each command

## Data Sources
- Results from `/security/compliance-check` command
- Results from `/security/analyze-audit-logs` command
- Results from `/security/security-audit` command

## Output
A comprehensive security report including:
- **Overall Security Status**: Pass/Fail/Needs Attention
- **Compliance Summary**: GDPR, HIPAA, SOC 2 compliance status
- **Audit Log Summary**: Anomalies, incidents, patterns
- **Security Audit Summary**: Vulnerabilities, OWASP Top 10 compliance, infrastructure security
- **Critical Issues**: Blocking security issues that must be addressed
- **Prioritized Recommendations**: Remediation steps with severity levels
- **Next Steps**: Actionable security improvements

## Execution Flow
```
compliance-check → analyze-audit-logs → security-audit → Final Report
      ↓                    ↓                    ↓
  [Continue]          [Continue]          [Aggregate Results]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Security audit uses results from compliance check and audit log analysis
- All reports are preserved for detailed analysis
