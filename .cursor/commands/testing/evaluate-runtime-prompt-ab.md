# Evaluate Runtime Prompt AB

## Overview
Run runtime A/B evaluation for prompt versions inside agentic workflows, compare outcomes in production-like conditions, and produce a promotion or rollback recommendation.

## Rules Applied
- `prompt-engineering-and-management` - Runtime prompt versioning, routing, and in-loop metrics requirements
- `llm-evaluation-and-metrics` - Evaluation metrics and scoring discipline
- `monitoring-and-observability` - Real-time telemetry collection and analysis
- `cost-and-budget-management` - Cost controls and token budget guardrails
- `commands-management` - Command structure and execution conventions

## Steps

1. **Define Experiment Scope**
   - Select candidate prompt versions (control and variant).
   - Define traffic split strategy (fixed, progressive, or adaptive).
   - Set success criteria across quality, latency, cost, and failure rate.

2. **Configure Runtime Routing**
   - Enable context-aware prompt selection in the runtime router.
   - Ensure deterministic assignment logic (for example per user/session hash).
   - Set fallback behavior to stable production prompt on routing failures.

3. **Collect In-Loop Metrics**
   - Record per-version metrics at key workflow points (node entry, LLM call, node exit, completion).
   - Capture quality signals, latency percentiles, token usage, and errors.
   - Persist experiment metadata and correlation IDs for analysis.

4. **Compare Versions**
   - Compute relative deltas for all success criteria.
   - Segment analysis by context (task type, user segment, complexity).
   - Flag statistical or operational regressions with severity labels.

5. **Execute Decision Policy**
   - Promote variant if criteria are met and no critical regressions exist.
   - Roll back or reduce traffic when quality/safety/cost thresholds are violated.
   - Document decision and next iteration plan.

## Data Sources
- Prompt registry entries and version metadata
- Runtime router configuration and assignment logs
- Workflow execution traces and per-node metrics
- Cost and token usage telemetry

## Output
A runtime A/B evaluation report including:
- **Experiment Configuration**: Versions, traffic split, and success thresholds
- **Per-Version Metrics**: Quality, latency, cost, and reliability
- **Segment Analysis**: Performance by context and task type
- **Risk Findings**: Regressions, anomalies, and threshold breaches
- **Decision**: Promote, continue experiment, reduce traffic, or rollback
