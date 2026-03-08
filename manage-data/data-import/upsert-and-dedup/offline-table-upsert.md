---
description: Use upsert semantics on batch-ingested offline tables.
---

# Offline Table Upsert

Pinot supports upsert on `OFFLINE` tables in builds that include [PR #17789](https://github.com/apache/pinot/pull/17789).

Use it for batch corrections, replays, and late-arriving records.

## How offline upsert works

Pinot keeps one row per primary key.

For duplicate keys, Pinot keeps the row with the greatest comparison value.

If you do not set `comparisonColumns`, Pinot uses the table time column.

Offline upsert replaces full rows.

It does not merge partial rows.

## Configure offline upsert

{% stepper %}
{% step %}
### Define a primary key

Add `primaryKeyColumns` to the schema.

```json
{
  "schemaName": "orders",
  "primaryKeyColumns": ["order_id"]
}
```
{% endstep %}

{% step %}
### Enable upsert on the offline table

Set `tableType` to `OFFLINE`.

Set `upsertConfig.mode` to `FULL`.

```json
{
  "tableName": "orders_OFFLINE",
  "tableType": "OFFLINE",
  "segmentsConfig": {
    "timeColumnName": "event_time",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "30",
    "replication": "3"
  },
  "upsertConfig": {
    "mode": "FULL",
    "comparisonColumns": ["event_time"]
  }
}
```
{% endstep %}

{% step %}
### Ingest or replace segments

Generate and upload offline segments as usual.

Pinot applies upsert semantics when it loads those segments.

Use append-style uploads for incremental corrections.

Use refresh-style uploads when replacing an existing batch.
{% endstep %}
{% endstepper %}

## When to use it

Use offline upsert when updates arrive in files.

Use it for daily corrections.

Use it for backfills.

Use it for replaying snapshots into offline segments.

## Differences from real-time upsert

Offline upsert does not consume a stream.

It does not require low-level consumers.

It does not depend on stream partitioning.

It fits batch ingestion and segment replacement workflows.

For stream-based updates, use [Stream ingestion with Upsert](upsert.md).

## Operational notes

Changing the primary key needs a full rebuild.

Changing comparison columns also needs a full rebuild.

Reload alone is not enough for these changes.

If you use a hybrid table, avoid overlapping offline and realtime time ranges.

## Related topics

* [Batch Ingestion](../batch-ingestion/)
* [Backfill Data](../batch-ingestion/backfill-data.md)
* [Create and update a table configuration](../../../basics/getting-started/create-and-update-table-config.md)
* [Stream ingestion with Upsert](upsert.md)
