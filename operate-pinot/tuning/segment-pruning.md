---
description: >-
  Understand how Pinot prunes irrelevant segments to reduce query latency and resource usage.
---

# Segment Pruning

Segment pruning is a query optimization technique that eliminates irrelevant segments before scanning data. By skipping segments that cannot contain matching records, Pinot significantly reduces query latency, I/O, and CPU usage.

Pruning happens at two levels: **broker-side** (during query routing) and **server-side** (during query execution).

## Broker-Side Pruning

The broker prunes segments before dispatching queries to servers. This reduces the number of segments that servers need to process. Configure broker-side pruning in the table's `routing` configuration.

### Time Pruning

Time pruning skips segments whose time range does not overlap with the query's time filter. This is the most commonly used pruning strategy for time-series workloads.

**Configuration:**

```json
{
  "routing": {
    "segmentPrunerTypes": ["time"]
  }
}
```

**Requirements:**
- The schema must define a primary time column (`dateTimeFieldSpecs` with `"granularity": "1:MILLISECONDS:EPOCH"` or similar)
- Data should be ingested in approximate chronological order for best results

**Supported filter operators:** `=`, `<`, `<=`, `>`, `>=`, `RANGE`, `BETWEEN`, `AND`, `OR`

**Example query that benefits from time pruning:**

```sql
SELECT count(*) FROM events
WHERE ts > 1700000000000 AND ts < 1700100000000
```

{% hint style="info" %}
Time pruning is more selective when data is strictly time-ordered. With out-of-order data, segments may have overlapping time ranges, reducing pruning effectiveness.
{% endhint %}

### Partition Pruning

Partition pruning skips segments that do not contain records matching the query's partition column filter. This is effective for queries that filter on a partitioned column.

**Configuration:**

First, define the partition scheme in the table's index config:

```json
{
  "tableIndexConfig": {
    "segmentPartitionConfig": {
      "columnPartitionMap": {
        "memberId": {
          "functionName": "Modulo",
          "numPartitions": 8
        }
      }
    }
  },
  "routing": {
    "segmentPrunerTypes": ["partition"]
  }
}
```

**Supported partition functions:** `Modulo`, `Murmur`, `ByteArray`, `HashCode`

**Supported filter operators:** `=` (equality), `IN`

**Example query that benefits from partition pruning:**

```sql
SELECT * FROM userEvents
WHERE memberId = 12345
```

{% hint style="tip" %}
For maximum partition pruning effectiveness, ensure each segment contains data from only one partition. When using Kafka, configure the Kafka topic partitioning to match the Pinot partition configuration.
{% endhint %}

### Combining Pruners

You can enable both time and partition pruning simultaneously:

```json
{
  "routing": {
    "segmentPrunerTypes": ["partition", "time"]
  }
}
```

## Server-Side Pruning

Server-side pruning happens after the broker routes the query but before the server scans segment data. These pruners use segment-level metadata and indexes.

### Column Value Pruning

Prunes segments based on min/max column statistics stored in segment metadata. If a query filters on a column value outside a segment's min/max range, that segment is skipped.

This pruner works automatically and requires no special configuration. Column statistics are maintained as part of the segment metadata.

### Bloom Filter Pruning

When a [Bloom filter index](../../build-with-pinot/indexing/bloom-filter.md) is configured on a column, the server uses it to prune segments that definitely do not contain a queried value. This is especially effective for high-cardinality equality lookups.

**Configuration** (in `fieldConfigList`):

```json
{
  "fieldConfigList": [
    {
      "name": "userId",
      "indexes": {
        "bloom": {
          "fpp": 0.05,
          "maxSizeInBytes": 1048576
        }
      }
    }
  ]
}
```

{% hint style="info" %}
Bloom filter pruning for `IN` clauses is limited to 10 values or fewer to minimize overhead.
{% endhint %}

## Multi-Stage Query Engine (MSE)

The multi-stage query engine supports broker-side pruning via the `useBrokerPruning` query option (enabled by default):

```sql
SET "useBrokerPruning" = true;
SELECT count(*) FROM events WHERE ts > 1700000000000
```

When the [physical optimizer](../../build-with-pinot/querying-and-sql/multi-stage-query/physical-optimizer.md) is enabled, time and partition pruning are automatically applied to the Leaf Stage of multi-stage queries.

## Monitoring Pruning Effectiveness

Use the following metrics to assess pruning effectiveness:

| Metric | Description |
|---|---|
| `SEGMENT_PRUNING` | Time spent pruning segments (part of server query latency) |
| `NUM_SEGMENTS_PRUNED_BY_VALUE` | Number of segments pruned by value-based pruning |
| `numSegmentsQueried` | Segments sent to servers by the broker |
| `numSegmentsProcessed` | Segments actually scanned by servers |

A large gap between `numSegmentsQueried` and `numSegmentsProcessed` indicates that server-side pruning is doing significant work. If `numSegmentsQueried` is close to the total segment count, consider enabling broker-side pruning.

**Diagnosis:** If `NUM_DOCS_SCANNED` or `NUM_ENTRIES_SCANNED_POST_FILTER` is high relative to the result set, review:
1. Whether time pruning is enabled and effective
2. Whether the table would benefit from partitioning
3. Whether bloom filters would help for high-cardinality equality lookups

## Best Practices

1. **Always enable time pruning** for tables with a time column — it has minimal overhead and significant benefit
2. **Partition tables** on frequently filtered columns (e.g., tenant ID, user ID) for equality-based queries
3. **Match Kafka partitioning** with Pinot partitioning for real-time tables to ensure segments contain single partitions
4. **Use bloom filters** on high-cardinality columns used in equality lookups (e.g., UUIDs, session IDs)
5. **Ingest data in time order** when possible, to maximize time pruning selectivity
6. **Monitor pruning metrics** to identify tables where pruning could be improved
