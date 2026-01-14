# Pre-Deployment Check

## Overview
Comprehensive pre-deployment verification to ensure code is ready for production deployment. This command runs all critical checks including tests, evaluations, security audits, compliance verification, and infrastructure validation before deployment.

## Rules Applied
- `deployment-and-infrastructure` - CI/CD, Docker, Kubernetes, deployment standards
- `final-review-protocol` - Final review compliance checklist
- `security-governance-and-observability` - Security governance requirements
- `tests-and-validation` - Testing requirements
- `llm-evaluation-and-metrics` - Evaluation requirements

## Steps

1. **Run Test Suite**
   - Execute `/testing/run-test-suite` command
   - Verify all tests pass (✅ status)
   - Review test execution report
   - Proceed only if tests pass or with explicit approval for warnings

2. **Run Evaluation Suite**
   - Execute `/testing/run-evaluation-suite` command
   - Verify evaluation metrics meet thresholds
   - Review evaluation report
   - Proceed only if evaluation scores meet requirements

3. **Security Audit**
   - Execute `/security/security-audit` command (includes compliance checks)
   - Review security audit report
   - Verify no critical vulnerabilities
   - Proceed only if security audit passes

4. **Compliance Verification**
   - Execute `/review/final-compliance-check` command (includes code review)
   - Review compliance report
   - Verify all governance requirements are met
   - Proceed only if compliance check passes

5. **Infrastructure Checks**
   - **Docker Validation**:
     - Verify Dockerfile is optimized (multi-stage builds, minimal size)
     - Check Docker image security (non-root user, no secrets)
     - Validate Docker image builds successfully
   - **Kubernetes Validation** (if applicable):
     - Verify Kubernetes manifests are correct
     - Check resource limits and requests
     - Validate health check configurations
     - Review rolling update strategy
   - **CI/CD Pipeline**:
     - Verify CI/CD pipeline is configured
     - Check pipeline stages are complete
     - Validate automated quality gates
   - **Configuration**:
     - Verify environment-specific configurations
     - Check secrets management
     - Validate configuration validation

7. **Performance Validation**
   - Verify performance meets SLI/SLO requirements
   - Check latency percentiles (P50, P95, P99)
   - Validate throughput requirements
   - Review resource usage limits

8. **Generate Pre-Deployment Report**
   - Create comprehensive pre-deployment report
   - Include results from all checks
   - Provide overall deployment readiness status
   - Highlight blocking issues
   - Include recommendations for non-blocking issues
   - Provide deployment approval/rejection recommendation

## Data Sources
- Results from `/testing/run-test-suite` command
- Results from `/testing/run-evaluation-suite` command
- Results from `/security/security-audit` command
- Results from `/review/final-compliance-check` command
- Infrastructure configuration files (Docker, Kubernetes, CI/CD)
- Performance metrics

## Output
A comprehensive pre-deployment report including:
- **Test Suite Results**: Summary from `/testing/run-test-suite` (pass/fail status, coverage, execution time)
- **Evaluation Suite Results**: Summary from `/testing/run-evaluation-suite` (metrics scores, quality assessment)
- **Security Audit Results**: Summary from `/security/security-audit` (vulnerabilities, compliance status)
- **Compliance Check Results**: Summary from `/review/final-compliance-check` (governance compliance status, code quality assessment)
- **Infrastructure Validation**: Docker, Kubernetes, CI/CD status
- **Performance Validation**: SLI/SLO compliance
- **Overall Deployment Readiness**: Pass/Fail/Needs Attention
- **Blocking Issues**: Critical issues that must be fixed before deployment
- **Recommendations**: Non-blocking improvements for future deployments
