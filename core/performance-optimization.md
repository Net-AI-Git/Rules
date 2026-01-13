# Performance Optimization

## 1. Caching Strategies

* **Redis Caching:**
    * **Use Cases:** Cache frequently accessed data, session data, API responses.
    * **TTL:** Set appropriate Time-To-Live (TTL) for cached data.
    * **Invalidation:** Implement cache invalidation strategies (time-based, event-based).
    * **Serialization:** Use efficient serialization (msgpack, orjson) for better performance.

* **In-Memory Caching:**
    * **Python `functools.lru_cache`:** Use for function result caching.
    * **Cache Size Limits:** Set maximum cache size to prevent memory issues.
    * **Thread Safety:** Use thread-safe caching for multi-threaded applications.

* **CDN Caching:**
    * **Static Assets:** Serve static files (images, CSS, JS) via CDN.
    * **API Responses:** Cache API responses at CDN level when appropriate (with proper cache headers).

* **Cache-Aside Pattern:**
    1. Check cache for data.
    2. If miss, fetch from source.
    3. Store in cache for future requests.
    4. Return data to caller.

* **Write-Through Pattern:**
    * Write to cache and source simultaneously.
    * Ensures cache and source are always in sync.

* **Write-Back Pattern:**
    * Write to cache first, then asynchronously write to source.
    * Improves write performance but requires careful handling of cache failures.

* **See:** `agentic-logic-and-tools.md` for module-level caching patterns specific to agents.

## 2. CDN Usage

* **Static Content:** Serve static files (images, documents, videos) via CDN.
    * **Benefits:** Reduced latency, lower origin server load, global distribution.

* **API Acceleration:**
    * **Edge Caching:** Cache API responses at CDN edge when appropriate.
    * **Cache Headers:** Use proper cache headers (`Cache-Control`, `ETag`, `Last-Modified`).

* **Dynamic Content:**
    * **Edge Computing:** Use CDN edge functions for lightweight processing.
    * **Origin Shield:** Use origin shield to reduce origin requests.

* **Configuration:**
    * **TTL Settings:** Configure appropriate TTL for different content types.
    * **Purge:** Implement cache purge mechanism for immediate updates.

## 3. Database Query Optimization

* **Indexing:**
    * **Primary Keys:** Always define primary keys.
    * **Foreign Keys:** Index foreign key columns.
    * **Query Analysis:** Analyze slow queries and add indexes for frequently filtered/sorted columns.
    * **Composite Indexes:** Create composite indexes for multi-column queries.

* **Query Patterns:**
    * **Avoid N+1 Queries:** Use eager loading or batch queries to fetch related data.
    * **Select Specific Columns:** Select only required columns instead of `SELECT *`.
    * **Limit Results:** Use `LIMIT` to restrict result set size.
    * **Pagination:** Implement cursor-based or offset-based pagination for large datasets.

* **Connection Pooling:**
    * **Pool Size:** Configure appropriate connection pool size.
    * **Timeout:** Set connection timeout and query timeout.
    * **See:** Connection Pooling section below for details.

* **Query Caching:**
    * **Application-Level:** Cache query results in Redis when appropriate.
    * **Database-Level:** Enable database query cache if supported.

* **Batch Operations:**
    * **Bulk Inserts:** Use bulk insert operations instead of individual inserts.
    * **Batch Updates:** Group multiple updates into batch operations.

## 4. Batch Processing Patterns

* **Batching Strategy:**
    * **Size-Based:** Process items in fixed-size batches (e.g., 100 items per batch).
    * **Time-Based:** Process items at fixed intervals (e.g., every 5 minutes).
    * **Hybrid:** Combine size and time-based batching.

* **Parallel Processing:**
    * **Async Batching:** Use `asyncio.gather()` to process batches in parallel.
    * **Worker Pools:** Use worker pools for CPU-intensive batch processing.

* **Error Handling:**
    * **Partial Success:** Handle partial batch failures gracefully.
    * **Retry Logic:** Implement retry logic for failed batch items.
    * **Dead Letter Queue:** Send failed items to DLQ for manual processing.

* **Monitoring:**
    * **Batch Metrics:** Track batch size, processing time, success/failure rates.
    * **Throughput:** Monitor items processed per second.

## 5. Lazy Loading Strategies

* **Lazy Initialization:**
    * **On-Demand Loading:** Load resources only when needed.
    * **Example:** Load database connections, external clients on first use.

* **Lazy Evaluation:**
    * **Generators:** Use Python generators for large datasets.
    * **Iterator Pattern:** Use iterators to process data incrementally.

* **Deferred Imports:**
    * **Heavy Libraries:** Import heavy libraries only when needed.
    * **Example:** Import ML models only when prediction is required.

* **Lazy Properties:**
    * **`@property` Decorator:** Use `@property` with lazy initialization for expensive computations.
    * **Caching:** Cache computed values to avoid recomputation.

## 6. Resource Pooling

* **Connection Pooling:**
    * **Database Connections:** Use connection pools for database connections.
        * **SQLAlchemy:** Configure pool size, max overflow, pool timeout.
        * **AsyncPG:** Use connection pools for async PostgreSQL connections.
    * **HTTP Connections:** Reuse HTTP connections using connection pools (httpx, aiohttp).

* **Thread/Process Pools:**
    * **ThreadPoolExecutor:** Use for I/O-bound tasks.
    * **ProcessPoolExecutor:** Use for CPU-bound tasks (see `core-python-standards.md`).

* **Object Pooling:**
    * **Reusable Objects:** Pool expensive-to-create objects (parsers, validators).
    * **Example:** Reuse PDF parsers, XML parsers across requests.

* **Pool Configuration:**
    * **Size:** Configure pool size based on expected load and resource limits.
    * **Timeout:** Set timeout for acquiring resources from pool.
    * **Monitoring:** Monitor pool usage and adjust size as needed.

## 7. Connection Pooling

* **Database Connection Pools:**
    * **SQLAlchemy:**
        * **Pool Size:** Set `pool_size` (default: 5).
        * **Max Overflow:** Set `max_overflow` for additional connections.
        * **Pool Timeout:** Set `pool_timeout` for connection acquisition timeout.
        * **Pool Recycle:** Set `pool_recycle` to refresh stale connections.

    * **AsyncPG:**
        * **Min/Max Size:** Configure minimum and maximum pool size.
        * **Max Queries:** Set maximum queries per connection before recycling.

* **HTTP Connection Pools:**
    * **httpx:**
        * **Connection Limits:** Configure connection limits per host.
        * **Keep-Alive:** Enable HTTP keep-alive for connection reuse.

    * **aiohttp:**
        * **Connector Limits:** Set connection limits and TTL.

* **Best Practices:**
    * **Size Appropriately:** Size pools based on expected concurrent requests.
    * **Monitor Usage:** Track pool usage and adjust size as needed.
    * **Handle Exhaustion:** Implement proper error handling when pools are exhausted.

## 8. Performance Monitoring

* **Profiling:**
    * **Application Profiling:** Use profiling tools to identify bottlenecks (see `monitoring-and-observability.md`).
    * **Database Profiling:** Enable slow query logs and analyze query performance.

* **Metrics:**
    * **Latency:** Track P50, P95, P99 latency.
    * **Throughput:** Monitor requests per second.
    * **Resource Usage:** Track CPU, memory, network usage.
    * **Cache Hit Rate:** Monitor cache hit/miss ratios.

* **Performance Testing:**
    * **Load Testing:** Conduct load tests to identify performance limits.
    * **Stress Testing:** Test system behavior under extreme load.
    * **Baseline:** Establish performance baselines and track regressions.

* **Optimization Cycle:**
    1. Measure current performance.
    2. Identify bottlenecks.
    3. Implement optimizations.
    4. Measure improvement.
    5. Repeat as needed.
