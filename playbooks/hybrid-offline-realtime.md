---
description: End-to-end guide for combining low-latency streaming with high-quality batch backfills in a single Pinot table.
---

# Hybrid Real-Time + Offline

This playbook covers the hybrid table pattern: a single logical table backed by both a **real-time** table (for low-latency streaming data) and an **offline** table (for batch-corrected, deduplicated, or enriched historical data). Queries seamlessly span both, and Pinot's time boundary mechanism ensures each time range is served by the best-quality source.

## When to use this pattern

Use this playbook when:

- You need real-time freshness (seconds of latency) **and** batch-quality historical data (deduplicated, enriched, or reprocessed) in the same query.
- Nightly or hourly batch jobs produce higher-quality data than what arrives via the stream (e.g., after joining with dimension tables, fixing late-arriving data, or running ML enrichment).
- You want to reduce storage costs by replacing many small real-time segments with fewer, optimized offline segments.
- Your workload resembles a Lambda architecture, but you want a single query interface instead of querying two systems.

If you only need real-time data and never backfill, use the [Real-Time Product Analytics](real-time-product-analytics.md) playbook. If your data mutates in place, see [CDC / Upsert Pipeline](cdc-upsert-pipeline.md).

## Architecture sketch

```
                                ┌──────────────────┐
Kafka topic ──────────────────▶ │  REALTIME table   │ (fresh, last few hours)
                                └────────┬─────────┘
                                         │
                              Pinot query │  time boundary
                              spans both  │
                                         │
                                ┌────────┴─────────┐
Spark / Flink batch job ──────▶ │  OFFLINE table    │ (historical, optimized)
                                └──────────────────┘
```

How the time boundary works:

1. Pinot maintains a **time boundary** — a timestamp that separates offline from real-time data.
2. For queries covering time ranges **before** the boundary, Pinot routes to offline segments.
3. For time ranges **after** the boundary, Pinot routes to real-time segments.
4. Each time a new offline segment is pushed that covers a recent time range, the boundary advances, and the overlapping real-time segments are automatically dropped.

## Schema

The schema is shared between the offline and real-time tables. Both must use exactly the same `schemaName`.

```json
{
  "schemaName": "web_analytics",
  "dimensionFieldSpecs": [
    { "name": "pageUrl",    "dataType": "STRING" },
    { "name": "userId",     "dataType": "STRING" },
    { "name": "country",    "dataType": "STRING" },
    { "name": "browser",    "dataType": "STRING" },
    { "name": "campaign",   "dataType": "STRING" },
    { "name": "enrichedSegment", "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "durationMs", "dataType": "LONG" },
    { "name": "revenue",    "dataType": "DOUBLE" }
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
The `enrichedSegment` column is filled by the batch job but may be null in real-time data. This is fine — Pinot handles null values gracefully. See [Null Value Support](../build-with-pinot/querying-and-sql/null-value-support.md).
{% endhint %}

## Real-time table configuration

```json
{
  "tableName": "web_analytics",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "eventTimestamp",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "3",
    "replication": "2",
    "segmentPushType": "APPEND"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "invertedIndexColumns": ["country", "browser", "campaign"],
    "rangeIndexColumns": ["eventTimestamp"],
    "noDictionaryColumns": ["userId", "pageUrl"],
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "web-analytics-events",
      "stream.kafka.broker.list": "kafka:9092",
      "stream.kafka.consumer.type": "lowlevel",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
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

Set `retentionTimeValue` to a small window (e.g., 3 days). This is only the fallback — in normal operation, the time boundary mechanism drops real-time segments as offline segments replace them.

## Offline table configuration

```json
{
  "tableName": "web_analytics",
  "tableType": "OFFLINE",
  "segmentsConfig": {
    "timeColumnName": "eventTimestamp",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "365",
    "replication": "2",
    "segmentPushType": "APPEND"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "invertedIndexColumns": ["country", "browser", "campaign", "enrichedSegment"],
    "rangeIndexColumns": ["eventTimestamp"],
    "sortedColumn": ["country"],
    "noDictionaryColumns": ["userId", "pageUrl"],
    "starTreeIndexConfigs": [
      {
        "dimensionsSplitOrder": ["country", "browser", "campaign"],
        "functionColumnPairs": ["COUNT__*", "SUM__revenue", "SUM__durationMs"],
        "maxLeafRecords": 10000
      }
    ]
  },
  "tenants": {
    "broker": "DefaultTenant",
    "server": "DefaultTenant"
  },
  "metadata": {}
}
```

### Why the offline table can be more aggressively indexed

- **Star-tree index**: Batch segments are written once, so the star-tree build cost is paid once. Real-time consuming segments rebuild star-tree on every flush, which is more expensive.
- **Sorted column**: Offline segments can be globally sorted during the batch job, yielding perfect sort order. Real-time segments are sorted only within each flush.
- **Longer retention**: Historical data lives only in offline segments, so set retention to months or years.

## Batch ingestion job

Use Spark or a standalone ingestion job to push daily offline segments. Example Spark job spec:

```yaml
executionFrameworkSpec:
  name: spark
  segmentGenerationJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentGenerationJobRunner
  segmentTarPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentTarPushJobRunner

jobType: SegmentCreationAndTarPush

inputDirURI: s3://data-lake/web_analytics/dt=2026-03-31/
outputDirURI: s3://pinot-segments/web_analytics/
overwriteOutput: true

pinotFSSpecs:
  - scheme: s3
    className: org.apache.pinot.plugin.filesystem.S3PinotFS

recordReaderSpec:
  dataFormat: parquet
  className: org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader

tableSpec:
  tableName: web_analytics
  schemaURI: http://pinot-controller:9000/schemas/web_analytics
  tableConfigURI: http://pinot-controller:9000/tables/web_analytics

segmentNameGeneratorSpec:
  type: normalizedDate
  configs:
    segment.name.prefix: web_analytics
    exclude.sequence.id: false

pushJobSpec:
  pushAttempts: 3
  pushParallelism: 2
```

Schedule this job to run daily (or hourly) after your data pipeline finishes. Each push advances the time boundary automatically.

See [Batch Ingestion Guide](../build-with-pinot/ingestion/batch-ingestion/README.md) and [Spark Connector](../build-with-pinot/ingestion/batch-ingestion/spark.md) for details.

## How the time boundary advances

1. Controller computes the time boundary as the **maximum end time** across all offline segments.
2. Broker uses this boundary at query time: segments with time ranges before the boundary come from offline; segments after come from real-time.
3. When a new offline segment covers time that was previously served by real-time, the real-time segments for that time range become redundant and are dropped by the retention manager.

You can inspect the current time boundary:

```
GET /tables/web_analytics/timeBoundary
```

See [Time Boundary](../basics/concepts/time-boundary.md) for the full algorithm.

## Query patterns

Queries are identical to single-table queries — the broker handles routing transparently:

```sql
SELECT
  DATETRUNC('day', eventTimestamp, 'MILLISECONDS') AS day,
  country,
  COUNT(*) AS page_views,
  SUM(revenue) AS total_revenue
FROM web_analytics
WHERE eventTimestamp > ago('P30D')
GROUP BY day, country
ORDER BY day
LIMIT 10000
```

For recent data (last few hours), the query hits real-time segments. For older data, it hits offline segments. The result is merged seamlessly.

## Operational checklist

### Before go-live

- [ ] Verify that both offline and real-time tables use the same `schemaName` and `tableName`.
- [ ] Set real-time table retention to at least 2x the batch job interval (e.g., 3 days for a daily job) to handle batch delays.
- [ ] Validate the time boundary advances after the first batch push by checking `GET /tables/{tableName}/timeBoundary`.
- [ ] Ensure offline segments do not have time gaps — missing days cause the time boundary to stop advancing, and real-time data for that gap is lost when its retention expires.

### Monitoring

- **Time boundary freshness**: If the boundary is more than one batch interval behind, the batch pipeline may be failing.
- **Segment overlap**: Check that real-time segments for time ranges covered by offline segments are being purged by retention.
- **Offline segment push success**: Monitor the controller API for push failures. A failed push means stale data in the real-time table continues to serve — this is safe but lower quality.

### Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Time boundary does not advance | Ensure offline segment time ranges are contiguous and cover up to the expected boundary |
| Real-time segments are not dropped after offline push | Check that real-time retention is configured and the retention manager is running |
| Double-counting for the boundary time range | This can happen if offline and real-time segments overlap for the same millisecond. Pinot's time boundary logic handles this, but verify with a COUNT query at the boundary |
| Batch job produces segments with wrong time column | Ensure `timeColumnName` matches in both table configs and the batch job reads the same column |

## Further reading

- [Table Types (Offline, Real-Time, Hybrid)](../basics/components/table/README.md)
- [Time Boundary](../basics/concepts/time-boundary.md)
- [Batch Ingestion Guide](../build-with-pinot/ingestion/batch-ingestion/README.md)
- [Spark Connector](../build-with-pinot/ingestion/batch-ingestion/spark.md)
- [Backfill Data](../build-with-pinot/ingestion/batch-ingestion/backfill-data.md)
- [Pinot Managed Offline Flows](../operators/operating-pinot/pinot-managed-offline-flows.md)
