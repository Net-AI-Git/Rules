## Mandate

Select models **dynamically** from task complexity and constraints — not a single hardcoded model. Prefer **small/cheap** for classification, routing, extraction; **large** for deep reasoning/synthesis. Implement **multi-provider failover** for production HA.

**See:** `@examples_routing.py`, `@examples_model_tiers.py`, `@examples_multi_provider_failover.py`.

## Routing

1. Classify task (simple / medium / complex) using inputs, required output quality, and latency.
2. Map to a **tier** (fast vs balanced vs strongest) and a concrete model.
3. Respect **remaining budget** (`@cost-and-budget-management`); downgrade or stop when needed.

## SECTIONS

In multi-agent flows, route **per SECTION** when useful; track cost per SECTION (`@multi-agent-systems`).

## Failover

Priority list of providers/models; retry transient errors; circuit breakers; health-aware routing; per-provider cost tracking.

**See:** `@error-handling-and-resilience`.

## Observability

Log model id, tier, and provider per span to `@monitoring-and-observability` (Splunk/SPL for cost and quality).

## Config

Externalize tiers and prices in config (`@configuration-and-dependency-injection`).
