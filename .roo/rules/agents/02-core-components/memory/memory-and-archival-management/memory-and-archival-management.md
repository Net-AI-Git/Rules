## Mandate

Use **durable** stores for user/tenant memory (profiles, insights, embeddings). **Short-term** chat stays in LangGraph state; long-term must be **searchable**, **tenant-scoped**, and **retrieved on demand** — not dumped wholesale into the prompt.

## Storage choice

* **Vector DB:** Semantic similarity, embeddings, unstructured insights, RAG-style recall.
* **PostgreSQL:** Structured fields, exact queries, relational data, strong consistency.
* **Hybrid:** Common pattern — metadata/profile in SQL, semantic memories in vectors; link by stable IDs.

**See:** `@examples_memory_storage.py`, `@examples_storage_strategy.py`.

## Retrieval & updates

* **When:** Session start, on-demand, end-of-session, or on triggers; respect token budgets and `@context-compression-and-optimization`.
* **What to store:** Durable, actionable, user-relevant facts — not ephemeral task state or unconsented sensitive data.

**See:** `@examples_memory_retrieval.py`, `@examples_memory_updates.py`.

## Privacy & compliance

Mask/limit PII; consent and delete/export where required; audit access per `@audit-protocol` and `@security-governance-and-observability`.

## Integration

* **LangGraph:** Load/update via dedicated nodes; checkpoints ≠ long-term memory writes.
* **Memory Node:** `@memory-feedback-node` orchestrates calls to this layer.
* **Observability:** Retrieval/update latency and errors to `@monitoring-and-observability`.
