## Data Structures — Use the Right One

| Structure | Use When | Commands |
|-----------|----------|----------|
| **String** | Single value, simple cache | `SET key value EX ttl`, `GET key` |
| **Hash** | Object with fields (read/write individual fields without loading all) | `HSET key field value`, `HGET key field`, `HGETALL key` |
| **Sorted Set** | Ranking, priority queue, leaderboard | `ZADD key score member`, `ZRANGE key 0 -1`, `ZPOPMIN key` |
| **List** | FIFO queue, recent items log | `LPUSH key value`, `RPOP key`, `LRANGE key 0 9` |
| **Set** | Uniqueness, membership test, intersections | `SADD key member`, `SISMEMBER key member`, `SINTER key1 key2` |

* **String vs Hash:** If you only ever read/write the whole object → String (JSON serialized with `orjson`). If you need to read/update individual fields → Hash.
* **List vs Sorted Set for queues:** List = simple FIFO. Sorted Set = priority-based (score determines order).
* **TTL:** Always set expiration (`EX` for seconds, `PX` for milliseconds). Never store without TTL unless intentionally permanent.
* **Serialization:** Use `orjson` for JSON serialization (3x faster than `json.dumps`).
