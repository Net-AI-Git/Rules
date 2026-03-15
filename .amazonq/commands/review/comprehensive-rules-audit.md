# Comprehensive Rules Audit

## Overview
Systematic audit that goes through **every single RULE.mdc file** in the `.cursor/rules` directory, checks if each rule is relevant to the current codebase, identifies missing implementations, and provides fixes for compliance gaps. This command ensures no rule is overlooked and all applicable standards are met.

## Rules Applied
- **ALL RULES** - This command systematically checks every rule in the repository
- `rules-management` - Rule structure and format validation
- `final-review-protocol` - Final review compliance checklist
- `code-review-and-collaboration` - Code review standards

## Steps

1. **Discover All Rules**
   - Scan `.cursor/rules` directory recursively
   - Find all `RULE.mdc` files
   - Build complete inventory of all rules (currently 39 rules)
   - Categorize rules by type:
     - Always Apply rules
     - Apply Intelligently rules
     - Apply to Specific Files rules
     - Apply Manually rules
   - **Rule Categories Checked**:
     - **Core Rules**: `core-python-standards`, `error-handling-and-resilience`
     - **Security Rules**: `security-governance-and-observability`, `audit-protocol`, `prompt-injection-prevention`
     - **Agent Rules**: `langgraph-architecture-and-nodes`, `multi-agent-systems`, `agentic-logic-and-tools`, `context-compression-and-optimization`, `memory-and-archival-management`, `model-routing-and-selection`, `cost-and-budget-management`, `human-in-the-loop-approval`, `reflection-and-self-critique`
     - **Infrastructure Rules**: `monitoring-and-observability`, `performance-optimization`, `rate-limiting-and-queue-management`, `deployment-and-infrastructure`, `multi-tenancy-and-isolation`
     - **Development Rules**: `tests-and-validation`, `code-review-and-collaboration`, `versioning-and-release-management`
     - **API Rules**: `api-interface-and-streaming`, `api-documentation-standards`, `mcp-protocol-implementation`
     - **Data Rules**: `data-schemas-and-interfaces`, `data-migration-and-compatibility`
     - **Configuration Rules**: `configuration-and-dependency-injection`, `prompt-engineering-and-management`
     - **Evaluation Rules**: `llm-evaluation-and-metrics`, `llm-judge-protocol`, `graph-traversal-testing`, `simulation-and-property-testing`, `bias-detection-and-ethics`, `final-review-protocol`

2. **Read and Parse Each Rule**
   - Read frontmatter from each `RULE.mdc` file
   - Extract rule type, description, globs (if applicable)
   - Parse rule content to understand requirements
   - Identify key compliance points from each rule
   - Build rule compliance checklist for each rule

3. **Analyze Codebase Against Each Rule**
   - For each rule, determine if it's relevant to current codebase:
     - Check if rule's glob patterns match any files
     - Check if rule's description matches current context
     - Check if rule's category is relevant (agents, API, security, etc.)
   - For relevant rules, check compliance:
     - Scan source code files for rule violations
     - Check if required patterns are implemented
     - Verify standards are followed
     - Identify missing implementations

4. **Identify Compliance Gaps**
   - For each relevant rule, create gap analysis:
     - List all requirements from the rule
     - Check which requirements are met (✅)
     - Identify which requirements are missing (❌)
     - Flag partial implementations (⚠️)
   - Prioritize gaps by severity:
     - Critical: Must fix (security, core standards)
     - High: Should fix (best practices, performance)
     - Medium: Nice to have (optimizations)
     - Low: Optional improvements

5. **Generate Fixes for Missing Requirements**
   - For each compliance gap, generate specific fixes:
     - Code changes needed
     - Configuration updates required
     - Documentation updates needed
     - Test additions required
   - Provide actionable recommendations with:
     - Specific file locations
     - Code examples
     - Step-by-step implementation guide

6. **Apply Fixes (Optional)**
   - If user approves, automatically apply fixes:
     - Implement missing error handling patterns
     - Add missing type hints
     - Fix function length violations
     - Add missing tests
     - Update configuration files
     - Add missing documentation
   - Only apply non-breaking fixes automatically
   - Request approval for significant changes

7. **Generate Comprehensive Audit Report**
   - **Complete Rule Inventory**: List all 39+ rules with their status
   - **Relevance Analysis**: Which rules apply to current codebase
   - **Compliance Matrix**: Detailed compliance status for each relevant rule
   - **Gap Analysis**: All missing implementations with severity
   - **Fix Recommendations**: Specific fixes for each gap
   - **Applied Fixes**: Summary of fixes that were applied
   - **Remaining Issues**: Issues that need manual attention
   - **Compliance Score**: Overall compliance percentage per category
   - **Next Steps**: Prioritized action items

## Data Sources
- All `RULE.mdc` files in `.cursor/rules` directory (39+ rules)
- Source code files (Python files, configuration files)
- Test files (`tests/` directory)
- Documentation files
- Configuration files (`.env`, config files)
- Infrastructure files (Docker, CI/CD configs)

## Output
A comprehensive rules audit report including:

- **Complete Rule Inventory**: All 39+ rules with metadata (type, category, description)
- **Relevance Matrix**: Which rules apply to current codebase (with justification)
- **Compliance Status Per Rule**: 
  - ✅ Fully Compliant
  - ⚠️ Partially Compliant (with details)
  - ❌ Non-Compliant (with gap analysis)
  - ➖ Not Applicable (with reason)
- **Detailed Gap Analysis**: 
  - Missing implementations per rule
  - Specific code locations that need changes
  - Required patterns not implemented
  - Standards not followed
- **Fix Recommendations**: 
  - Specific code changes with examples
  - Configuration updates needed
  - Documentation requirements
  - Test additions needed
- **Applied Fixes Summary**: 
  - Fixes that were automatically applied
  - Files modified
  - Changes made
- **Compliance Scoring**:
  - Overall compliance percentage
  - Per-category compliance scores
  - Trend analysis (if previous audit exists)
- **Prioritized Action Items**:
  - Critical issues (must fix)
  - High priority (should fix)
  - Medium priority (nice to have)
  - Low priority (optional)
- **Next Steps**: 
  - Immediate actions required
  - Long-term improvements
  - Rule-specific recommendations
