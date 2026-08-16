---
description: Use upsert semantics on batch-ingested offline tables.
---

# Offline Table Upsert

Pinot supports upsert on `OFFLINE` tables in builds that include [PR #17789](https://github.com/apache/pinot/pull/17789).

Use it for batch corrections, replays, and late-arriving records.

For a full overview of upsert features (comparison columns, delete columns, TTL, metadata management), see the main [Upsert](upsert.md) page. This page covers the OFFLINE-specific configuration and differences.

## How offline upsert works

Pinot keeps one row per primary key.

For duplicate keys, Pinot keeps the row with the greatest comparison value.

If you do not set `comparisonColumns`, Pinot uses the table time column.

An offline upsert table must define either `upsertConfig.comparisonColumns` or `segmentsConfig.timeColumnName`. Pinot rejects the table configuration when neither is set; segment creation time is not used as an implicit comparison value.

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
### Generate a missing comparison column (optional)

For an `OFFLINE` table, `ingestionConfig.transformConfigs` can use registered scalar functions from any volatility category. If a batch file has no row-version or timestamp column, declare the comparison column in the schema and populate it during ingestion. For example:

```json
{
  "upsertConfig": {
    "mode": "FULL",
    "comparisonColumns": ["ingestionTime"]
  },
  "ingestionConfig": {
    "transformConfigs": [
      {
        "columnName": "ingestionTime",
        "transformFunction": "now()"
      }
    ]
  }
}
```

Declare `ingestionTime` as a `LONG` date-time field with millisecond epoch format in the schema. Real-time table-level transforms still require immutable functions.
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

### Preload upsert metadata during server restart

Builds that include [PR #19271](https://github.com/apache/pinot/pull/19271) support upsert preload for `OFFLINE` table data managers. Before loading or replacing an offline segment, Pinot restores the partition's upsert metadata from persisted `validDocIds` snapshots. This can reduce recovery time when a server restarts.

Enable snapshots and preload in the table configuration:

```json
{
  "upsertConfig": {
    "mode": "FULL",
    "snapshot": "ENABLE",
    "preload": "ENABLE"
  }
}
```

Also configure a positive preload thread count on the server:

```properties
pinot.server.instance.max.segment.preload.threads=4
```

The preload path is a no-op when upsert is not configured or preload is disabled. Each offline segment must have partition metadata so Pinot can restore the correct partition manager. For the shared snapshot lifecycle and restart caveats, see [Enable preload for faster server restarts](upsert.md#enable-preload-for-faster-server-restarts).

## Related topics

* [Batch Ingestion](../batch-ingestion)
* [Backfill Data](../batch-ingestion/backfill-data.md)
* [Create and update a table configuration](../../../operate-pinot/setup-table.md)
* [Stream ingestion with Upsert](upsert.md)
