## Mandate

Monitor context size; **compress, summarize, or trim** before windows overflow — preserving user intent, critical decisions, and retrieval-friendly memory hooks. Align with **budget** (`@cost-and-budget-management`) and **memory** (`@memory-and-archival-management`).

**See:** `@examples_compression.py`, `@examples_retention.py`.

## Triggers

Warn as context fills (e.g. ~80%); compress/trim by ~85–95% of model limit; model-specific limits; accurate token counting (`tiktoken` or provider counters).

## Strategies

* **Summarize:** abstractive or extractive for older turns; hierarchical summaries for long threads.
* **Trim:** FIFO or **importance** scoring (role, recency, task relevance) — never drop current request, system instructions, or critical errors without policy.

## Coherence

Compressed history must stay consistent with **GraphState** and **checkpoints**; log compression events to Splunk (`compressed`, token counts) per `@monitoring-and-observability`.

## Integration

* **Memory Node:** load within allocated token slice.
* **Cost:** smaller context → lower cost.
