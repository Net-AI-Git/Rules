# Security & Governance



## Blast Radius Containment

* **Limit Scope:** Limit blast radius by design. Apply least privilege—agents access only data/tools strictly needed.

* **No Implicit Access:** Do not allow "free" tool access. Use explicit tool whitelisting via a registry.

* **Sandboxing:** Sandbox high-risk tools and code execution. Isolate side effects.



## Environment Management

* **Tool Registry:** Select tools explicitly by environment (Dev vs. Prod).

    * **Dev:** Load sandboxed or mock tools.

    * **Prod:** Load real tools with guardrails.

* **Consistency:** Never "disable" tools ad-hoc for production. Switch tool sets via env configuration to ensure auditable behavior.

* **Sandboxing Logic:** Use a Tool sandbox where necessary to separate PRODUCTION from DEVELOPMENT.



## Governance & Control

* **Human-in-the-Loop:** Require approval for critical or irreversible actions.

* **Rate Limits:** Enforce budgets and rate limits to prevent runaway loops. See `api-interface-and-streaming.md` for implementation details.

* **Auditing:** Enable full auditing and tracing to attribute every action to a specific agent and context. See `monitoring-and-observability.md` for comprehensive auditing and tracing strategies.

## AI Risk Management Framework (NIST AI RMF)

* **Compliance:** Adhere to NIST AI RMF + Generative AI Profile for risk management, pre-deployment testing, and governance.

* **Key Areas:**
  * **Govern:** Establish policies and procedures for AI system governance.
  * **Map:** Identify and document AI system risks and context.
  * **Measure:** Assess AI system performance and risks.
  * **Manage:** Implement risk mitigation strategies.

* **Resources:** Reference NIST AI RMF publications and Generative AI Profile for detailed guidance.

## OWASP Top 10 for LLM Applications

* **Security Risks:** Address the OWASP Top 10 for LLM Applications:
  1. **Prompt Injection:** Validate and sanitize all prompts to prevent injection attacks.
  2. **Insecure Output Handling:** Validate and sanitize LLM outputs before use.
  3. **Training Data Poisoning:** Use trusted, validated training data sources.
  4. **Model Denial of Service:** Implement rate limiting and resource quotas.
  5. **Supply Chain Vulnerabilities:** Audit and secure all dependencies.
  6. **Sensitive Information Disclosure:** Implement data masking and PII protection.
  7. **Insecure Plugin Design:** Secure tool/plugin interfaces with proper authentication.
  8. **Excessive Agency:** Implement guardrails and human-in-the-loop for critical actions.
  9. **Overreliance:** Implement validation and fallback mechanisms.
  10. **Model Theft:** Protect model weights and intellectual property.

* **Implementation:** Apply OWASP guidelines throughout the development lifecycle.

* **Resources:** Reference OWASP Foundation publications for detailed security guidance.

## Red Teaming Protocols

* **Purpose:** Identify vulnerabilities and failure modes before deployment.

* **Process:**
  * **External Red Teaming:** Conduct external red teaming exercises to test system robustness.
  * **Adversarial Testing:** Test system behavior under adversarial inputs.
  * **Failure Mode Analysis:** Identify and document potential failure modes.
  * **Remediation:** Address identified vulnerabilities before production deployment.

* **Frequency:** Conduct red teaming exercises regularly, especially before major releases.

* **Resources:** Reference OpenAI External Red Teaming paper for methodology and best practices.

## Evaluation Best Practices

* **Continuous Evaluation:** Implement continuous evaluation of LLM outputs and agent behavior.

* **Production Monitoring:** Monitor LLM quality and compliance in production using evaluation frameworks.

* **Metrics:** Track evaluation metrics alongside operational metrics.

* **See:** `llm-evaluation-and-metrics.md` for comprehensive evaluation strategies.

* **Resources:** Reference OpenAI Evaluation best practices for detailed guidance on building evals to monitor quality and compliance in production.



## Authentication & Authorization

* **OAuth2 Patterns:**
    * **Authorization Code Flow:** Use authorization code flow for web applications (most secure).
    * **Client Credentials Flow:** Use client credentials flow for server-to-server communication.
    * **Token Storage:** Store tokens securely (encrypted, not in localStorage for web apps).
    * **Token Refresh:** Implement automatic token refresh before expiration.

* **JWT Handling:**
    * **Token Validation:** Always validate JWT signature, expiration, and issuer.
    * **Secret Management:** Store JWT secrets securely (use environment variables or secret management).
    * **Token Claims:** Include minimal necessary claims (user ID, tenant ID, roles).
    * **Token Expiration:** Set appropriate token expiration times (short for access tokens, longer for refresh tokens).

* **API Key Management:**
    * **Key Generation:** Generate cryptographically secure API keys.
    * **Key Storage:** Store API keys hashed in database (never store plaintext).
    * **Key Rotation:** Implement key rotation mechanism for compromised keys.
    * **Key Scoping:** Associate API keys with specific permissions/scopes.

* **Role-Based Access Control (RBAC):**
    * **Role Definition:** Define clear roles with specific permissions.
    * **Permission Checking:** Check permissions at endpoint level (use decorators or dependencies).
    * **Least Privilege:** Grant minimum permissions necessary for each role.
    * **Role Hierarchy:** Support role hierarchies if needed (e.g., admin > user > guest).



## Input Validation & Sanitization

* **SQL Injection Prevention:**
    * **Parameterized Queries:** Always use parameterized queries (never string concatenation).
    * **ORM Usage:** Prefer ORM over raw SQL to reduce injection risk.
    * **Input Validation:** Validate and sanitize all user inputs before database operations.

* **XSS Prevention:**
    * **Output Encoding:** Encode user input when rendering in HTML/JavaScript.
    * **Content Security Policy:** Implement Content Security Policy (CSP) headers.
    * **Input Sanitization:** Sanitize user input to remove potentially dangerous content.

* **CSRF Protection:**
    * **CSRF Tokens:** Use CSRF tokens for state-changing operations.
    * **SameSite Cookies:** Set SameSite cookie attribute to prevent CSRF.
    * **Origin Validation:** Validate request origin for sensitive operations.

* **Input Validation:**
    * **Pydantic Models:** Use Pydantic models for request validation (see `data-schemas-and-interfaces.md`).
    * **Type Validation:** Validate data types, ranges, and formats.
    * **Length Limits:** Enforce length limits on input fields.
    * **Pattern Validation:** Use regex patterns to validate input format (e.g., email, phone number).



## Security Headers

* **CORS Configuration:**
    * **Origin Whitelist:** Whitelist specific origins instead of allowing all origins.
    * **Credentials:** Configure CORS credentials handling appropriately.
    * **Methods:** Allow only necessary HTTP methods.
    * **Headers:** Allow only necessary request headers.

* **Security Headers:**
    * **HSTS (HTTP Strict Transport Security):** Enable HSTS to force HTTPS connections.
    * **CSP (Content Security Policy):** Implement CSP to prevent XSS attacks.
    * **X-Frame-Options:** Prevent clickjacking by setting X-Frame-Options.
    * **X-Content-Type-Options:** Set to "nosniff" to prevent MIME type sniffing.
    * **X-XSS-Protection:** Enable browser XSS protection (legacy, but still useful).

* **FastAPI Implementation:**
    * **Middleware:** Use FastAPI middleware to add security headers to all responses.
    * **CORS Middleware:** Use FastAPI's CORSMiddleware for CORS configuration.



## Secret Rotation

* **Rotation Strategies:**
    * **Scheduled Rotation:** Rotate secrets on a regular schedule (e.g., every 90 days).
    * **Event-Based Rotation:** Rotate secrets immediately after security incidents.
    * **Gradual Rotation:** Support gradual rotation with overlap period for zero-downtime.

* **Key Management Systems:**
    * **AWS KMS / Azure Key Vault / GCP Secret Manager:** Use cloud key management services.
    * **HashiCorp Vault:** Use Vault for on-premises or multi-cloud deployments.
    * **Benefits:** Centralized management, audit logging, automatic rotation support.

* **Rotation Process:**
    * **Generate New Secret:** Generate new secret using secure random generation.
    * **Update Configuration:** Update configuration with new secret (via environment variables or secret manager).
    * **Verify:** Verify new secret works before removing old secret.
    * **Remove Old Secret:** Remove old secret after verification period.

* **Secret Types:**
    * **API Keys:** Rotate API keys for external services.
    * **Database Credentials:** Rotate database passwords regularly.
    * **JWT Secrets:** Rotate JWT signing secrets (requires token re-issuance).
    * **Encryption Keys:** Rotate encryption keys used for data encryption.
