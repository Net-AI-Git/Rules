# Run All Review

## Overview
Execute all review commands in sequence: code review checklist and final compliance check. This master command runs the complete review workflow to ensure code quality and compliance before commit.

## Rules Applied
- `code-review-and-collaboration` - Code review standards
- `final-review-protocol` - Final review compliance checklist
- `core-python-standards` - Code quality standards
- All relevant governance rules

## Steps

1. **Code Review Checklist**
   - Execute `/review/code-review-checklist` command
   - Wait for completion and review results
   - **Error Handling**:
     - If code review fails: Stop execution and report blocking issues
     - If code review finds issues: Continue with warning, include in final report
     - If code review passes: Proceed to next step
   - **Output**: Code review report with checklist status

2. **Final Compliance Check**
   - Execute `/review/final-compliance-check` command (uses results from code review)
   - Wait for completion and review results
   - **Error Handling**:
     - If compliance check fails: Report blocking issues
     - If compliance issues found: Include in final report with severity
     - If compliance passes: Generate final report
   - **Output**: Comprehensive compliance report

3. **Generate Comprehensive Review Report**
   - Aggregate results from both commands
   - Create summary with overall review status
   - Highlight code quality issues and compliance gaps
   - Provide prioritized recommendations
   - Include links to detailed reports from each command

## Data Sources
- Results from `/review/code-review-checklist` command
- Results from `/review/final-compliance-check` command

## Output
A comprehensive review report including:
- **Overall Review Status**: Pass/Fail/Needs Attention
- **Code Review Summary**: Code quality, functionality, testing, documentation, security
- **Compliance Summary**: Architecture, testing, error handling, performance, documentation, deployment, security
- **Critical Issues**: Blocking issues that must be fixed before commit
- **Recommendations**: Prioritized suggestions for improvements
- **Next Steps**: Actionable items before proceeding with commit

## Execution Flow
```
code-review-checklist → final-compliance-check → Final Report
         ↓ Fail                      ↓ Fail
      [Stop]                      [Stop]
```

## Notes
- Each command can be run independently if needed
- Master command provides workflow orchestration
- Final compliance check uses results from code review
- All reports are preserved for detailed analysis
