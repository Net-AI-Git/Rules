# Example SPL Queries for Observability

Reference: [Splunk Search Reference](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/9.2/introduction/welcome-to-the-search-reference).

Use these patterns in Splunk to analyze logs and metrics ingested via HEC. Assume index `main` (or your app index) and structured JSON with fields: `timestamp`, `correlation_id`, `operation_name`, `duration_ms`, `start_timestamp`, `end_timestamp`.

## Latency (P50, P95, P99) by operation

```spl
index=main duration_ms=*
| stats perc50(duration_ms) as p50_ms, perc95(duration_ms) as p95_ms, perc99(duration_ms) as p99_ms, count by operation_name
| sort - p99_ms
```

## Error rate and count by operation

```spl
index=main (result="failure" OR result="error" OR level="ERROR")
| stats count by operation_name
| sort - count
```

## Trace by correlation_id (all spans for a request)

```spl
index=main correlation_id="<uuid>"
| sort start_timestamp
| table start_timestamp, end_timestamp, operation_name, duration_ms
```

## Transaction (group events by correlation_id)

```spl
index=main correlation_id=*
| transaction correlation_id startswith="operation_name=*" endswith="operation_name=*"
| stats sum(duration_ms) as total_ms, count by correlation_id
```

## Time chart: request count and P95 latency over time

```spl
index=main duration_ms=*
| timechart span=1h count, perc95(duration_ms) as p95_ms
```

## Filter by time and operation

```spl
index=main operation_name="llm_call" earliest=-24h
| stats avg(duration_ms), perc95(duration_ms), count by model
```
