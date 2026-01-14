# Run All Deployment

## Overview
Execute all deployment commands in sequence: pre-deployment check and post-deployment verification. This master command runs the complete deployment workflow to ensure successful and verified deployment.

## Rules Applied
- `deployment-and-infrastructure` - Deployment standards and procedures
- `final-review-protocol` - Final review compliance
- `security-governance-and-observability` - Security governance
- `monitoring-and-observability` - Health checks and monitoring

## Steps

1. **Pre-Deployment Check**
   - Execute `/deployment/pre-deployment-check` command
   - Wait for completion and review results
   - **Error Handling**:
     - If pre-deployment check fails: Stop execution, do not proceed with deployment
     - If blocking issues found: Stop execution, require fixes before deployment
     - If non-blocking issues found: Continue with warning, include in final report
     - If check passes: Proceed to deployment (manual or automated)
   - **Output**: Pre-deployment report with deployment readiness status

2. **Post-Deployment Verification**
   - Execute `/deployment/post-deployment-verification` command
   - Wait for completion and review results
   - **Error Handling**:
     - If post-deployment verification fails: Report critical issues, consider rollback
     - If health checks fail: Report service issues, consider rollback
     - If verification passes: Generate final report
   - **Output**: Post-deployment verification report with system status

3. **Generate Comprehensive Deployment Report**
   - Aggregate results from both commands
   - Create summary with overall deployment status
   - Highlight pre-deployment issues and post-deployment status
   - Provide recommendations for improvements
   - Include links to detailed reports from each command

## Data Sources
- Results from `/deployment/pre-deployment-check` command
- Results from `/deployment/post-deployment-verification` command
- Health check endpoints
- Performance metrics
- Error logs

## Output
A comprehensive deployment report including:
- **Overall Deployment Status**: Success/Failed/Needs Attention
- **Pre-Deployment Summary**: Test results, evaluation results, security audit, compliance, infrastructure validation
- **Post-Deployment Summary**: Health checks, smoke tests, performance verification, error monitoring
- **Critical Issues**: Blocking issues that require immediate attention or rollback
- **Recommendations**: Improvements for future deployments
- **Next Steps**: Actionable items for deployment optimization

## Execution Flow
```
pre-deployment-check → [Deploy] → post-deployment-verification → Final Report
         ↓ Fail                              ↓ Fail
      [Stop]                          [Report & Consider Rollback]
```

## Notes
- Pre-deployment check must pass before deployment
- Post-deployment verification should be run immediately after deployment
- Each command can be run independently if needed
- Master command provides workflow orchestration
- All reports are preserved for detailed analysis
