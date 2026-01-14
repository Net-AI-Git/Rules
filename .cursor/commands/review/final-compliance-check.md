# Final Compliance Check

## Overview
Comprehensive final review before commit to verify solution complies with all active governance files and project standards. This command performs a complete compliance check covering all critical aspects of the codebase.

## Rules Applied
- `final-review-protocol` - Final review compliance checklist
- `core-python-standards` - Core Python standards and best practices
- `error-handling-and-resilience` - Error handling and resilience patterns
- `agents/langgraph-architecture-and-nodes` - LangGraph architecture standards
- `agents/multi-agent-systems` - Multi-agent system patterns
- `configuration/configuration-and-dependency-injection` - Configuration management
- `configuration/prompt-engineering-and-management` - Prompt engineering standards
- `data/data-schemas-and-interfaces` - Data schema standards
- `api/api-interface-and-streaming` - API standards
- `infrastructure/performance-optimization` - Performance optimization
- `security/security-governance-and-observability` - Security governance

## Steps

1. **Code Review**
   - Execute `/review/code-review-checklist` command
   - Review code review report
   - Verify code quality standards are met
   - Use code review findings in compliance assessment

2. **Architecture & Agents Checks**
   - **Nodes**:
     - Verify nodes follow READ → DO → WRITE → CONTROL structure
     - Check node size and single-purpose design
     - Validate state field ownership
   - **Resilience**:
     - Verify external calls are wrapped in `@retry` (Tenacity)
     - Check error classification (transient vs permanent)
     - Validate circuit breaker patterns where applicable
   - **Config**:
     - Verify no secrets are hardcoded
     - Check `pydantic-settings` is used for configuration
     - Validate environment variable usage
   - **Prompts**:
     - Verify prompts are separated from code (Templates)
     - Check prompt versioning and management
     - Validate XML tagging for prompt structure

3. **RAG & Data Checks** (If Applicable)
   - **Hybrid Search**:
     - Verify both keyword and vector search are enabled
     - Check search implementation quality
   - **Reranking**:
     - Verify reranker step is included
     - Check reranking implementation
   - **Streaming**:
     - Verify API supports SSE/Streaming response
     - Check streaming implementation

4. **Testing & Validation Checks**
   - **Evals**:
     - Verify Ragas/DeepEval metrics are defined for agents
     - Check evaluation suite completeness
   - **Unit Tests**:
     - Verify `pytest` tests pass with ✅ visuals
     - Check test coverage is adequate
   - **Coverage**:
     - Verify edge cases are covered
     - Check test quality and independence

5. **Error Handling & Resilience Checks**
   - **Error Classification**:
     - Verify errors are properly classified (transient vs permanent)
     - Check error handling patterns
   - **Retry Logic**:
     - Verify retries are implemented with exponential backoff
     - Check retry configuration is appropriate
   - **Circuit Breaker**:
     - Verify circuit breakers are used for external services
     - Check circuit breaker configuration
   - **Graceful Degradation**:
     - Verify system degrades gracefully on failures
     - Check fallback mechanisms
   - **Error Logging**:
     - Verify errors are logged with full context
     - Check structured error log format

6. **Performance & Optimization Checks**
   - **Caching**:
     - Verify appropriate caching strategies are implemented
     - Check cache invalidation mechanisms
   - **Query Optimization**:
     - Verify database queries are optimized (indexes, no N+1 queries)
     - Check query performance
   - **Resource Pooling**:
     - Verify connections/resources are pooled
     - Check connection pooling configuration

7. **Documentation & API Checks**
   - **API Docs**:
     - Verify OpenAPI/Swagger documentation is complete
     - Check API documentation quality
   - **Versioning**:
     - Verify API versioning strategy is defined
     - Check version implementation
   - **Examples**:
     - Verify request/response examples are provided
     - Check example quality
   - **Error Responses**:
     - Verify error response schemas are documented
     - Check error handling documentation

8. **Deployment & Infrastructure Checks**
   - **CI/CD**:
     - Verify CI/CD pipeline is configured
     - Check pipeline stages and quality gates
   - **Containerization**:
     - Verify Docker images are optimized (multi-stage builds, minimal size)
     - Check Dockerfile quality
   - **Health Checks**:
     - Verify health check endpoints are implemented
     - Check health check configuration
   - **Rollback Plan**:
     - Verify rollback procedure is documented and tested
     - Check rollback readiness

9. **Security Checks**
   - **Security Governance**:
     - Verify security governance requirements are met
     - Check OWASP Top 10 compliance
   - **Environment Isolation**:
     - Verify environment isolation is properly configured
     - Check security boundaries

10. **Generate Compliance Report**
    - Create comprehensive compliance report
    - Include all checklist items with status
    - Provide specific feedback for non-compliant items
    - Prioritize issues by severity
    - Include recommendations for achieving compliance
    - Provide overall compliance status

## Data Sources
- Results from `/review/code-review-checklist` command
- Source code files (all Python files)
- Test files (`tests/` directory)
- Configuration files (`.env`, config files)
- Documentation files (README, API docs)
- Infrastructure files (Docker, CI/CD configs)
- Evaluation results (if available)

## Output
A comprehensive final compliance report including:
- **Compliance Summary**: Overall status with visual indicators
- **Code Review Results**: Summary from `/review/code-review-checklist` (function length, parallelism, typing, logging, code quality)
- **Architecture Compliance**: Nodes, resilience, config, prompts
- **RAG/Data Compliance**: Hybrid search, reranking, streaming (if applicable)
- **Testing Compliance**: Evals, unit tests, coverage
- **Error Handling Compliance**: Classification, retries, circuit breakers, degradation
- **Performance Compliance**: Caching, query optimization, resource pooling
- **Documentation Compliance**: API docs, versioning, examples
- **Deployment Compliance**: CI/CD, containerization, health checks, rollback
- **Security Compliance**: Governance, environment isolation
- **Non-Compliance Issues**: Prioritized list with remediation steps
- **Overall Verdict**: Pass/Fail/Needs Attention with justification
