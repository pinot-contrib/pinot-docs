---
description: Create offline Pinot materialized views for recurring time-windowed aggregations.
---

# Materialized Views

Materialized views in Pinot are offline tables that store pre-aggregated results for a recurring query shape. Pinot validates the materialized view definition when you create the table, refreshes it with the `MaterializedViewTask` minion workflow, and exposes discovery and runtime state in the controller UI and REST API.

{% hint style="warning" %}
Transparent query rewrite is not part of the current materialized-view feature surface. Query the MV table directly today instead of expecting Pinot to rewrite base-table queries automatically.
{% endhint %}

## Current scope

- Time-windowed materialized views only.
- The MV table itself must be `OFFLINE`.
- Create the MV by posting a schema and an offline table config. The table config must include `task.taskTypeConfigsMap.MaterializedViewTask`.
- Use a flat `SELECT` over one source table. Pinot validates the SQL, schema mapping, bucket definition, and aggregation set when the MV table is created.
- The source table must be append-only. Pinot rejects realtime, upsert, dedup, dimension, and `REFRESH`-push source tables.
- The source table time column and the MV time column must both be `TIMESTAMP` `dateTimeFieldSpecs`.
- The MV time column must be a `TIMESTAMP` `dateTimeFieldSpec`.
- Supported MV aggregations in `definedSQL` today are `SUM`, `COUNT`, `MIN`, `MAX`, `DISTINCTCOUNTRAWHLL`, `DISTINCTCOUNTRAWHLLPLUS`, and `DISTINCTCOUNTRAWTHETASKETCH`.

Pinot also validates the expression that produces the MV time column. The supported shapes today are a direct `TIMESTAMP` passthrough or a `DATETRUNC(...)` whose unit matches `bucketTimePeriod`.

## Before you create one

- Run at least one Minion.
- Enable controller task scheduling with `controller.task.scheduler.enabled=true`.
- Keep the base table on the validated append-only `OFFLINE` path described above.

## Define the schema and MV table

Create the schema first, then create the MV table as an offline table with a `MaterializedViewTask` block.

The task config needs at least these keys:

- `definedSQL`: the aggregation query Pinot runs for each time window.
- `bucketTimePeriod`: the window size, such as `1h` or `1d`.

The `SELECT` output must line up with the MV schema exactly. Bare column references keep their source names. Any expression or aggregation needs an `AS` alias that matches the destination schema column.

Example schema:

```json
{
  "schemaName": "salesByHourMv",
  "dimensionFieldSpecs": [
    {
      "name": "region",
      "dataType": "STRING"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "sum_revenue",
      "dataType": "DOUBLE"
    },
    {
      "name": "row_count",
      "dataType": "LONG"
    }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "bucket_start_ts",
      "dataType": "TIMESTAMP",
      "format": "1:MILLISECONDS:TIMESTAMP",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
```

Example table config:

```json
{
  "tableName": "salesByHourMv",
  "tableType": "OFFLINE",
  "segmentsConfig": {
    "timeColumnName": "bucket_start_ts",
    "segmentPushType": "APPEND",
    "replication": "1"
  },
  "task": {
    "taskTypeConfigsMap": {
      "MaterializedViewTask": {
        "definedSQL": "SELECT DATETRUNC('HOUR', event_ts) AS bucket_start_ts, region, SUM(revenue) AS sum_revenue, COUNT(*) AS row_count FROM sales GROUP BY DATETRUNC('HOUR', event_ts), region",
        "bucketTimePeriod": "1h"
      }
    }
  }
}
```

Post the schema and table config through the controller:

```bash
curl -X POST "http://localhost:9000/schemas" \
  -H "Content-Type: application/json" \
  -d @salesByHourMv_schema.json

curl -X POST "http://localhost:9000/tables" \
  -H "Content-Type: application/json" \
  -d @salesByHourMv_offline_table_config.json
```

Pinot generates MV segments through `MaterializedViewTask`. The controller task manager can schedule those tasks automatically, or you can trigger them manually:

```text
POST /tasks/schedule?taskType=MaterializedViewTask&tableName=<mvTable>_OFFLINE
```

## Query the MV table directly

Query the MV table name directly and re-aggregate its stored values as needed:

```sql
SELECT region, SUM(sum_revenue) AS total_revenue, SUM(row_count) AS total_rows
FROM salesByHourMv
WHERE bucket_start_ts BETWEEN 1746057600000 AND 1746144000000
GROUP BY region
ORDER BY total_revenue DESC
LIMIT 20;
```

If your MV stores raw sketch columns, query them with the matching merge function on the MV table:

- `DISTINCTCOUNTHLL(raw_hll_col)`
- `DISTINCTCOUNTHLLPLUS(raw_hllplus_col)`
- `DISTINCTCOUNTTHETASKETCH(raw_theta_col)`

## Try the bundled quickstart

Pinot ships a full local example that loads the base table, creates the MV table, runs the minion task, and compares base-table answers with MV-table re-aggregation:

```bash
bin/pinot-admin.sh QuickStart -type MATERIALIZED_VIEW
```

The quickstart creates `airlineStatsMv`, triggers `MaterializedViewTask`, and queries the MV table directly to validate `SUM`, `COUNT`, `MIN`, `MAX`, `DISTINCTCOUNTHLL`, and `DISTINCTCOUNTHLLPLUS` style rollups.

## Inspect and manage materialized views

In the Data Explorer, use **Data Sources** to discover both physical tables and materialized views:

- **Data Sources** shows cards for **Tables** and **Materialized Views**.
- **Materialized Views** lists each MV with its base tables, watermark, VALID and STALE partition counts, last refresh time, staleness SLO, and any metadata errors.
- Clicking an MV opens a detail page with the stored `definedSQL`, split spec, partition state, raw runtime metadata, and controls to refresh the page data or drop the MV.

The controller also exposes dedicated MV endpoints:

- `GET /materializedViews`
- `GET /materializedViews/{materializedViewTableName}`
- `DELETE /materializedViews/{materializedViewTableName}`

## What this page covered

This page covered the current materialized-view feature surface in Pinot: how to define the schema and offline table, which source tables and aggregations are supported, why callers query the MV table directly today, and where to inspect the MV in the UI and controller API.

## Next step

Read [Querying Pinot](querying-pinot.md) for the broader query path, or [Pinot Data Explorer](../../basics/components/exploring-pinot.md) for the UI walkthrough.

## Related pages

- [Querying & SQL](README.md)
- [Querying Pinot](querying-pinot.md)
- [Pinot Data Explorer](../../basics/components/exploring-pinot.md)
- [Functions](../../functions/README.md)
