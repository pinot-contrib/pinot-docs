---
description: End-to-end guide for keeping Pinot in sync with a transactional database using CDC and upserts.
---

# CDC / Upsert Pipeline

This playbook covers the pattern of capturing row-level changes from a transactional database (PostgreSQL, MySQL, MongoDB, etc.) via Change Data Capture (CDC), streaming them through Kafka, and ingesting them into Pinot with upsert enabled so that Pinot always reflects the latest state of each row.

## When to use this pattern

Use this playbook when:

- You need Pinot to mirror the current state of rows in an OLTP database (orders, user profiles, inventory, tickets).
- Rows are frequently **updated** or **soft-deleted** after initial creation, and queries must see only the latest version.
- You want real-time analytics on top of transactional data without adding read load to your primary database.
- Your CDC tool (Debezium, Maxwell, AWS DMS) already produces events to Kafka.

If your data is append-only and never updated, the simpler [Real-Time Product Analytics](real-time-product-analytics.md) pattern is a better fit.

## Architecture sketch

```
OLTP DB ──▶ Debezium ──▶ Kafka topic ──▶ Pinot REALTIME table (upsert)
  (WAL)      (CDC)        (per-table)          │
                                      ┌────────┴────────┐
                                      │ Servers with     │
                                      │ primary key map  │
                                      └─────────────────┘
```

Key components:

- **Debezium** (or equivalent) reads the database WAL and produces a Kafka event for every INSERT, UPDATE, and DELETE.
- **Kafka topic** is partitioned by the primary key so all mutations for the same row land on the same partition.
- **Pinot real-time table with upsert** maintains an in-memory map from primary key to the latest segment/doc-id so queries skip stale versions.

{% hint style="warning" %}
Upsert requires that all events for the same primary key arrive at the **same Kafka partition**. Configure your Debezium connector or Kafka producer to partition by the primary key column.
{% endhint %}

## Schema

Use the source table's primary key as Pinot's primary key. Include a comparison column (typically the event timestamp or database transaction sequence number) so Pinot can determine which version is newer.

```json
{
  "schemaName": "orders",
  "primaryKeyColumns": ["orderId"],
  "dimensionFieldSpecs": [
    { "name": "orderId",    "dataType": "STRING" },
    { "name": "customerId", "dataType": "STRING" },
    { "name": "status",     "dataType": "STRING" },
    { "name": "region",     "dataType": "STRING" },
    { "name": "product",    "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "amount",     "dataType": "DOUBLE" },
    { "name": "quantity",   "dataType": "INT" }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "updatedAt",
      "dataType": "TIMESTAMP",
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
```

{% hint style="info" %}
`primaryKeyColumns` is required for upsert. Pinot uses this to look up existing rows in the primary key map. See [Schema and Table Shape](../build-with-pinot/data-modeling/schema.md).
{% endhint %}

## Table configuration

```json
{
  "tableName": "orders",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "updatedAt",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "90",
    "replication": "1"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "invertedIndexColumns": ["status", "region", "customerId"],
    "rangeIndexColumns": ["updatedAt"],
    "sortedColumn": [],
    "noDictionaryColumns": ["orderId", "customerId"],
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "dbserver1.public.orders",
      "stream.kafka.broker.list": "kafka:9092",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "realtime.segment.flush.threshold.rows": "100000",
      "realtime.segment.flush.threshold.time": "4h"
    }
  },
  "upsertConfig": {
    "mode": "FULL",
    "comparisonColumns": ["updatedAt"],
    "hashFunction": "MURMUR3",
    "enableSnapshot": true,
    "enablePreload": true,
    "metadataTTL": 0,
    "deletedKeysTTL": 0
  },
  "routing": {
    "instanceSelectorType": "strictReplicaGroup"
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
| `upsertConfig.mode: FULL` | Every update replaces the entire row. Use `PARTIAL` if CDC events contain only changed columns. See [Upsert Modes](../build-with-pinot/ingestion/upsert-and-dedup/upsert.md) |
| `comparisonColumns: ["updatedAt"]` | Pinot uses this column to resolve out-of-order events — the row with the higher `updatedAt` wins |
| `enableSnapshot: true` | Persists the primary key map to disk so server restarts do not require replaying the full Kafka topic |
| `enablePreload: true` | Loads the snapshot into memory at startup for faster recovery |
| `hashFunction: MURMUR3` | More memory-efficient than the default hash for the primary key map |
| `replication: 1` | Upsert tables currently require replication factor 1. Use `strictReplicaGroup` routing to ensure consistency |
| `routing.instanceSelectorType` | Routes all queries for a partition to the same server, required for correct upsert semantics |

### Handling deletes

If your CDC stream includes tombstone events for deleted rows, configure a `deleteRecordColumn`:

```json
"upsertConfig": {
  "mode": "FULL",
  "comparisonColumns": ["updatedAt"],
  "deleteRecordColumn": "isDeleted",
  "deletedKeysTTL": 86400
}
```

Add `isDeleted` as a boolean dimension in your schema. Set it to `true` in your Debezium SMT (Single Message Transform) for delete events. Pinot will mark the row as deleted and stop returning it in queries.

## Partial upsert

When your CDC events contain only the changed columns (e.g., only `status` changed on an order), use partial upsert to merge the update into the existing row:

```json
"upsertConfig": {
  "mode": "PARTIAL",
  "partialUpsertStrategies": {
    "status":     "OVERWRITE",
    "amount":     "OVERWRITE",
    "quantity":   "OVERWRITE",
    "region":     "OVERWRITE"
  },
  "comparisonColumns": ["updatedAt"],
  "defaultPartialUpsertStrategy": "IGNORE"
}
```

With `IGNORE` as the default, any column not present in the incoming event retains its previous value. Columns listed with `OVERWRITE` are replaced when present.

## Debezium configuration tips

A minimal Debezium connector config for PostgreSQL:

```json
{
  "name": "orders-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${DEBEZIUM_PASSWORD}",
    "database.dbname": "app",
    "topic.prefix": "dbserver1",
    "table.include.list": "public.orders",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "transforms.unwrap.delete.handling.mode": "rewrite"
  }
}
```

The `ExtractNewRecordState` transform flattens the Debezium envelope so Pinot receives a simple JSON object with the row's columns. The `delete.handling.mode: rewrite` adds a `__deleted` field that you can map to your `isDeleted` column via an [ingestion transformation](../build-with-pinot/ingestion/ingestion-level-transformations.md).

## Query patterns

### Current state aggregation

```sql
SELECT status, COUNT(*) AS order_count, SUM(amount) AS total_amount
FROM orders
WHERE region = 'US'
GROUP BY status
```

Because upsert is enabled, this query automatically sees only the latest version of each order.

### Point lookup

```sql
SELECT *
FROM orders
WHERE orderId = 'ORD-78901'
LIMIT 1
```

### Time-range analysis over mutable data

```sql
SELECT
  DATETRUNC('hour', updatedAt, 'MILLISECONDS') AS hour_bucket,
  COUNT(*) AS updates
FROM orders
WHERE updatedAt > ago('PT24H')
GROUP BY hour_bucket
ORDER BY hour_bucket
```

## Segment compaction

Over time, upsert tables accumulate stale row versions inside completed segments. These invalid records waste storage and slow full-table scans. Schedule the **Upsert Compaction Task** via Minion to rewrite segments and physically remove stale rows:

```json
{
  "task": {
    "taskTypeConfigsMap": {
      "UpsertCompactionTask": {
        "schedule": "0 0 2 * * ?",
        "invalidRecordsThresholdPercent": "30",
        "invalidRecordsThresholdCount": "100000"
      }
    }
  }
}
```

See [Segment Compaction on Upserts](../build-with-pinot/ingestion/upsert-and-dedup/segment-compaction-on-upserts.md) for tuning guidance.

## Operational checklist

### Before go-live

- [ ] Verify Kafka topic is partitioned by primary key. Run a test with duplicate keys across partitions — queries will return wrong results if this is misconfigured.
- [ ] Enable `enableSnapshot` and `enablePreload` to avoid full-topic replay on server restarts.
- [ ] Set `replication: 1` and `strictReplicaGroup` routing. Multi-replica upsert is not supported in the current release.
- [ ] Run an initial load of the full table snapshot before starting CDC to avoid missing historical data.
- [ ] Set segment flush thresholds small enough that the primary key map fits in server memory. Monitor heap usage.

### Monitoring

- **Primary key map size**: Monitor `pinot.server.upsertPrimaryKeysCount`. If this exceeds available memory, consider TTL-based eviction or larger servers.
- **Invalid record ratio**: Track the percentage of invalidated (stale) records per segment. Schedule compaction when this exceeds 30%.
- **Kafka consumer lag**: Same as real-time tables — growing lag means Pinot queries show stale data.
- **Debezium connector status**: Monitor via Kafka Connect REST API. A stopped connector means no updates flow to Pinot.

### Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Out-of-order events cause old values to overwrite new ones | Use `comparisonColumns` with a monotonically increasing column (database sequence, event timestamp) |
| Memory pressure from large primary key map | Enable `metadataTTL` to evict keys for rows not updated within a time window, or use `hashFunction: MURMUR3` to reduce per-key overhead |
| Queries return deleted rows | Ensure `deleteRecordColumn` is configured and the CDC transform sets it correctly for delete events |
| Server restart takes minutes | Enable `enableSnapshot` and `enablePreload` — without them, Pinot replays the Kafka topic from the last committed offset |

## Further reading

- [Stream Ingestion with Upsert](../build-with-pinot/ingestion/upsert-and-dedup/upsert.md)
- [Offline Table Upsert](../build-with-pinot/ingestion/upsert-and-dedup/offline-table-upsert.md)
- [Segment Compaction on Upserts](../build-with-pinot/ingestion/upsert-and-dedup/segment-compaction-on-upserts.md)
- [Upsert Compaction Task](../operate-pinot/upsert-compaction-task.md)
- [Ingestion Transformations](../build-with-pinot/ingestion/ingestion-level-transformations.md)
