---
description: End-to-end guide for building sub-second dashboards over Kafka event streams with Apache Pinot.
---

# Real-Time Product Analytics

This playbook walks through a complete setup for powering user-facing or internal analytics dashboards with sub-second query latency over streaming data. Think page-view counters, transaction dashboards, click-through-rate monitors, or any workload where events arrive continuously and dashboards must refresh in real time.

## When to use this pattern

Use this playbook when:

- Events are produced to Kafka (or Kinesis/Pulsar) and must be queryable within seconds of arrival.
- Dashboards aggregate over time windows (last 1 hour, last 24 hours) with filters on dimensions such as country, device, or product category.
- You need high query concurrency (hundreds of concurrent dashboard users) with P99 latency under one second.
- Data is append-only; you do not need to update previously ingested rows. If you do, see the [CDC / Upsert Pipeline](cdc-upsert-pipeline.md) playbook instead.

## Architecture sketch

```
Producers ──▶ Kafka topic ──▶ Pinot Real-Time Table ──▶ Broker ──▶ Dashboard
                                    │
                          ┌─────────┴─────────┐
                          │  Real-time servers │
                          │  (consuming segments)
                          └───────────────────┘
```

Key components:

- **Kafka topic** partitioned by a high-cardinality key (e.g., `userId`) to distribute load.
- **Real-time table** with one consuming segment per Kafka partition per server.
- **Star-tree index** for pre-aggregated rollups on the most common dashboard group-by/filter combinations.
- **Brokers** that fan out queries to servers and merge results.

## Schema

Design the schema around the queries your dashboards will issue. A product-analytics event stream typically looks like this:

```json
{
  "schemaName": "product_events",
  "dimensionFieldSpecs": [
    { "name": "eventType",  "dataType": "STRING" },
    { "name": "userId",     "dataType": "STRING" },
    { "name": "country",    "dataType": "STRING" },
    { "name": "device",     "dataType": "STRING" },
    { "name": "productId",  "dataType": "STRING" },
    { "name": "category",   "dataType": "STRING" },
    { "name": "sessionId",  "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "revenue",    "dataType": "DOUBLE" },
    { "name": "quantity",   "dataType": "INT" }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "eventTimestamp",
      "dataType": "TIMESTAMP",
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
```

{% hint style="info" %}
Keep the schema narrow. Every dimension column you add increases segment size and potentially slows queries. Only include columns your dashboards actually filter or group on. See [Schema and Table Shape](../build-with-pinot/data-modeling/schema.md) for design guidance.
{% endhint %}

## Table configuration

```json
{
  "tableName": "product_events",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "eventTimestamp",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "30",
    "replication": "2",
    "segmentPushType": "APPEND"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "invertedIndexColumns": ["eventType", "country", "device", "category"],
    "rangeIndexColumns": ["eventTimestamp"],
    "sortedColumn": ["eventType"],
    "bloomFilterColumns": ["userId"],
    "noDictionaryColumns": ["sessionId", "userId"],
    "starTreeIndexConfigs": [
      {
        "dimensionsSplitOrder": ["country", "device", "category", "eventType"],
        "skipStarNodeCreationForDimensions": [],
        "functionColumnPairs": [
          "COUNT__*",
          "SUM__revenue",
          "SUM__quantity"
        ],
        "maxLeafRecords": 10000
      }
    ],
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "product-events",
      "stream.kafka.broker.list": "kafka:9092",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "realtime.segment.flush.threshold.rows": "500000",
      "realtime.segment.flush.threshold.time": "6h"
    }
  },
  "tenants": {
    "broker": "DefaultTenant",
    "server": "DefaultTenant"
  },
  "metadata": {}
}
```

### Configuration highlights

| Setting | Why |
| --- | --- |
| `invertedIndexColumns` on dimensions | Enables fast filtering on dashboard filter dropdowns |
| `rangeIndexColumns` on `eventTimestamp` | Speeds up time-range predicates like `WHERE eventTimestamp > ago('PT1H')` |
| `starTreeIndexConfigs` | Pre-aggregates the most common rollup queries so they return in single-digit milliseconds |
| `bloomFilterColumns` on `userId` | Accelerates point lookups when a dashboard drills into a single user |
| `noDictionaryColumns` on high-cardinality IDs | Saves memory; dictionary encoding is wasteful for columns with millions of unique values |
| `retentionTimeValue: 30` | Automatically purges data older than 30 days. Adjust to your retention needs |

## Indexing strategy

Start with the indexes shown above and iterate:

1. **Inverted indexes** on every column used in `WHERE` equality filters.
2. **Range index** on the time column and any numeric column used in range filters.
3. **Sorted index** on the column with the most common equality filter (only one sorted column per table).
4. **Star-tree index** for the top 3-5 dashboard queries that dominate traffic. Profile your queries before adding more star-tree configs — each one adds ingestion overhead and segment size.
5. **Bloom filter** on columns used for point lookups with very high cardinality.

See [Choosing Indexes](../build-with-pinot/indexing/choosing-indexes.md) for a decision framework.

## Query patterns

### Dashboard time-series aggregation

```sql
SELECT
  DATETIMECONVERT(eventTimestamp, '1:MILLISECONDS:EPOCH', '1:MINUTES:EPOCH', '5:MINUTES') AS ts_bucket,
  country,
  COUNT(*) AS event_count,
  SUM(revenue) AS total_revenue
FROM product_events
WHERE eventTimestamp > ago('PT1H')
  AND eventType = 'PURCHASE'
GROUP BY ts_bucket, country
ORDER BY ts_bucket
LIMIT 1000
```

### Top-N with filters

```sql
SELECT
  productId,
  SUM(revenue) AS total_revenue,
  COUNT(*) AS purchase_count
FROM product_events
WHERE eventTimestamp > ago('PT24H')
  AND country = 'US'
  AND eventType = 'PURCHASE'
GROUP BY productId
ORDER BY total_revenue DESC
LIMIT 20
```

### Single-user drill-down

```sql
SELECT eventType, eventTimestamp, productId, revenue
FROM product_events
WHERE userId = 'u-123456'
  AND eventTimestamp > ago('PT7D')
ORDER BY eventTimestamp DESC
LIMIT 100
```

{% hint style="info" %}
Use `OPTION(timeoutMs=5000)` on dashboard queries so a single slow query does not hold the connection pool. See [Query Options](../build-with-pinot/querying-and-sql/query-execution-controls/query-options.md).
{% endhint %}

## Operational checklist

### Before go-live

- [ ] Confirm Kafka topic partitions match the desired parallelism. Pinot creates one consuming segment per partition per server.
- [ ] Set `realtime.segment.flush.threshold.rows` and `realtime.segment.flush.threshold.time` so completed segments are a reasonable size (300 MB-1 GB). Overly small segments increase metadata overhead; overly large ones slow queries.
- [ ] Validate that the star-tree index covers your most frequent queries by running `EXPLAIN PLAN` and checking for `StarTreeIndex` in the output.
- [ ] Set table-level [query quotas](../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md) if multiple teams share the cluster.

### Monitoring

- **`CONSUMING` segment lag**: Monitor Kafka consumer lag via `pinot.server.realtimeConsumptionCatchupRatio`. If lag grows, add more servers or partitions.
- **Query latency P99**: Track via broker metrics. If P99 exceeds your SLA, consider adding star-tree indexes or scaling brokers.
- **Segment count per table**: A very large number of small segments degrades query performance. Use the [Minion Merge Rollup Task](../operate-pinot/minion-merge-rollup-task.md) to compact completed segments.
- **Heap and direct memory**: Real-time servers hold consuming segments in memory. Monitor JVM heap and off-heap usage.

See [Monitoring](../operate-pinot/monitoring.md) and [Running Pinot in Production](../operate-pinot/running-pinot-in-production.md) for a comprehensive metric list.

### Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Dashboard queries scan all 30 days of data | Add a time-range predicate; without it, the broker routes the query to every segment |
| Star-tree does not activate | Verify the query's GROUP BY and aggregation functions exactly match the star-tree config |
| High GC pauses on servers | Move high-cardinality `noDictionary` columns out of the dictionary, or increase direct memory for MMAP |
| Kafka rebalance causes brief query gaps | Set `replication: 2` so a second server can serve the data while one server is catching up |

## Further reading

- [Stream Ingestion Guide](../build-with-pinot/ingestion/stream-ingestion/README.md)
- [Star-Tree Index](../build-with-pinot/indexing/star-tree-index.md)
- [Real-Time Tuning](../operate-pinot/tuning/realtime.md)
- [Performance Optimization Configurations](../operate-pinot/performance-optimization-configurations.md)
