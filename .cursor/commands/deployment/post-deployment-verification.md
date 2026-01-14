# Post-Deployment Verification

## Overview
Comprehensive post-deployment verification to ensure successful deployment and system stability. This command performs health checks, smoke tests, performance verification, and error monitoring after deployment to production.

## Rules Applied
- `deployment-and-infrastructure` - Deployment verification, health checks, rollback procedures
- `monitoring-and-observability` - Health check endpoints, metrics, alerting
- `error-handling-and-resilience` - Error monitoring and recovery

## Steps

1. **Health Checks**
   - **Liveness Probe**:
     - Verify `/health/live` or `/healthz` endpoint responds with 200 OK
     - Check service is running and responsive
     - Validate basic service availability
   - **Readiness Probe**:
     - Verify `/health/ready` or `/ready` endpoint responds with 200 OK
     - Check service is ready to accept traffic
     - Validate dependencies are available (database, external services)
   - **Startup Probe** (if applicable):
     - Verify `/health/startup` endpoint for long startup times
     - Check service initialization is complete

2. **Smoke Tests**
   - **Basic Functionality**:
     - Test core functionality endpoints
     - Verify basic operations work correctly
     - Check critical user flows
   - **API Endpoints**:
     - Test key API endpoints
     - Verify request/response formats
     - Check authentication and authorization
   - **Agent Operations**:
     - Test agent execution with sample inputs
     - Verify agent responses are correct
     - Check tool execution works properly

3. **Performance Verification**
   - **Latency Checks**:
     - Measure response times for key endpoints
     - Verify latency meets SLI/SLO requirements
     - Check P50, P95, P99 latency percentiles
   - **Throughput Verification**:
     - Verify request handling capacity
     - Check throughput meets requirements
     - Validate concurrent request handling
   - **Resource Usage**:
     - Monitor CPU and memory usage
     - Verify resource usage is within limits
     - Check for resource leaks

4. **Error Rate Monitoring**
   - **Error Rate Analysis**:
     - Monitor error rates in first hours after deployment
     - Check error rate is within acceptable thresholds
     - Identify any error rate spikes
   - **Error Type Analysis**:
     - Categorize errors by type
     - Identify new error types introduced by deployment
     - Check for error patterns
   - **Error Recovery**:
     - Verify error handling works correctly
     - Check retry mechanisms function properly
     - Validate graceful degradation

5. **Integration Verification**
   - **External Services**:
     - Verify integration with external services works
     - Check API connections are stable
     - Validate authentication with external services
   - **Database Connectivity**:
     - Verify database connections work
     - Check database queries execute correctly
     - Validate data integrity

6. **Monitoring and Observability**
   - **Metrics Collection**:
     - Verify metrics are being collected
     - Check metrics are available in monitoring systems
     - Validate metric accuracy
   - **Logging**:
     - Verify logs are being generated
     - Check log aggregation is working
     - Validate log structure and content
   - **Tracing**:
     - Verify distributed tracing is working
     - Check trace collection and correlation
     - Validate trace completeness

7. **Rollback Readiness**
   - **Rollback Plan Verification**:
     - Verify rollback procedure is documented
     - Check rollback tools are accessible
     - Validate rollback can be executed quickly
   - **Previous Version Availability**:
     - Verify previous version is available for rollback
     - Check rollback artifacts are accessible
     - Validate rollback can be performed if needed

8. **Generate Post-Deployment Report**
   - Create comprehensive post-deployment verification report
   - Include results from all verification steps
   - Provide overall deployment status
   - Highlight any issues or concerns
   - Include recommendations for monitoring
   - Provide rollback recommendation if needed

## Data Sources
- Health check endpoint responses
- Smoke test execution results
- Performance metrics from monitoring systems
- Error logs and metrics
- Integration test results
- Monitoring and observability data

## Output
A comprehensive post-deployment verification report including:
- **Health Check Status**: Liveness, readiness, startup probe results
- **Smoke Test Results**: Basic functionality, API endpoints, agent operations
- **Performance Verification**: Latency, throughput, resource usage
- **Error Rate Analysis**: Error rates, error types, error recovery
- **Integration Status**: External services, database connectivity
- **Monitoring Status**: Metrics, logging, tracing
- **Rollback Readiness**: Rollback plan, previous version availability
- **Overall Deployment Status**: Success/Needs Attention/Rollback Recommended
- **Issues and Concerns**: Identified issues with severity levels
- **Monitoring Recommendations**: Ongoing monitoring suggestions
