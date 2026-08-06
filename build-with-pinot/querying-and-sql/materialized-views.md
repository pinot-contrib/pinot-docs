---
description: Create and manage offline Pinot materialized views for recurring time-windowed aggregations.
---

# Materialized Views

Materialized views in Pinot are offline tables that store pre-aggregated results for a recurring query shape. Use controller-managed SQL DDL through `POST /sql/ddl` to create, inspect, list, and drop them. Pinot validates the materialized view definition when you create it, refreshes it with the `MaterializedViewTask` minion workflow, and exposes discovery and runtime state in the controller UI and REST API. Pinot can also transparently rewrite eligible single-stage base-table queries to a materialized view when the broker rewrite feature is enabled.

{% hint style="info" %}
Transparent materialized-view rewrite is available for eligible Single-Stage Engine (SSE) queries. Keep querying the MV table directly when you want explicit control over the table name or when broker rewrite is disabled.
{% endhint %}

## Current scope

- Time-windowed materialized views only.
- The MV table itself must be `OFFLINE`.
- Create and manage MVs through controller SQL DDL: `CREATE MATERIALIZED VIEW`, `SHOW MATERIALIZED VIEWS`, `SHOW CREATE MATERIALIZED VIEW`, and `DROP MATERIALIZED VIEW`.
- Transparent rewrite applies to eligible SSE queries only.
- Broker-side rewrite is off by default until you set `pinot.broker.query.enable.materialized.view.rewrite=true` on brokers.
- `CREATE MATERIALIZED VIEW` accepts either a full column list or no column list at all. If you omit the column list, Pinot infers the MV schema from the `AS SELECT` projection.
- Use a flat `SELECT` over one source table. Pinot validates the SQL, schema mapping, bucket definition, and aggregation set when the MV table is created.
- The source table must be append-only. Pinot rejects realtime, upsert, dedup, dimension, and `REFRESH`-push source tables.
- The source table time column and the MV time column must both be `TIMESTAMP` `dateTimeFieldSpecs`.
- The MV time column must be a `TIMESTAMP` `dateTimeFieldSpec`.
- Supported MV aggregations in `definedSQL` today are `SUM`, `COUNT`, `MIN`, `MAX`, `DISTINCTCOUNTRAWHLL`, `DISTINCTCOUNTRAWHLLPLUS`, and `DISTINCTCOUNTRAWTHETASKETCH`.

These limits describe the built-in OSS materialized-view path. Pinot registers a default `MaterializedViewDdlHandler` that still validates a single-source SSE definition and still routes the table under `MaterializedViewTask`. Downstream distributions can replace that handler at controller startup to target a different engine or task type, but that is an extension point rather than a change to the default OSS behavior.

Pinot also validates the expression that produces the MV time column. The supported shapes today are a direct `TIMESTAMP` passthrough or a `DATETRUNC(...)` whose unit matches `bucketTimePeriod`.

## Before you create one

- Run at least one Minion.
- Enable controller task scheduling with `controller.task.scheduler.enabled=true`.
- Keep the base table on the validated append-only `OFFLINE` path described above.
- Decide whether Pinot should infer the MV schema from the `SELECT` list or whether you need to provide a full explicit column list to override inferred types or roles.

## Create an MV with SQL DDL

Run MV DDL through the controller endpoint `POST /sql/ddl`, not through the broker query API.

The controller accepts these MV statements:

- `CREATE MATERIALIZED VIEW [IF NOT EXISTS] [db.]name [(...)] [REFRESH [INTERVAL] EVERY ...] PROPERTIES (...) AS <select>`
- `SHOW MATERIALIZED VIEWS [FROM db]`
- `SHOW CREATE MATERIALIZED VIEW [db.]name`
- `DROP MATERIALIZED VIEW [IF EXISTS] [db.]name`

If you omit the column list, Pinot infers the MV schema from the `SELECT` projection. If you provide a column list, declare every projected column and alias every computed expression or aggregation so it matches the destination column name.

Schema inference is part of the built-in single-source handler. A custom handler can require an explicit column list instead.

The DDL needs at least these properties:

- `timeColumnName`: the MV column Pinot uses to track watermark progress.
- `bucketTimePeriod`: the materialization window size, such as `1h` or `1d`.
- `stalenessThresholdMs`: optional freshness SLO for broker rewrite. `0` disables the SLO check.

`REFRESH EVERY` is optional. When you provide it, Pinot stores a per-MV schedule using minute, hour, or day units. When you omit it, the MV runs on the cluster-wide `MaterializedViewTask` schedule.

Example DDL:

```sql
CREATE MATERIALIZED VIEW salesByHourMv
REFRESH EVERY 1 HOUR
PROPERTIES (
  'timeColumnName' = 'bucket_start_ts',
  'bucketTimePeriod' = '1h',
  'stalenessThresholdMs' = '900000',
  'replication' = '1'
)
AS
SELECT DATETRUNC('HOUR', event_ts) AS bucket_start_ts,
       region,
       SUM(revenue) AS sum_revenue,
       COUNT(*) AS row_count
FROM sales
GROUP BY DATETRUNC('HOUR', event_ts), region;
```

Submit the statement through the controller:

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"sql":"CREATE MATERIALIZED VIEW salesByHourMv REFRESH EVERY 1 HOUR PROPERTIES ('timeColumnName' = 'bucket_start_ts', 'bucketTimePeriod' = '1h', 'stalenessThresholdMs' = '900000', 'replication' = '1') AS SELECT DATETRUNC('HOUR', event_ts) AS bucket_start_ts, region, SUM(revenue) AS sum_revenue, COUNT(*) AS row_count FROM sales GROUP BY DATETRUNC('HOUR', event_ts), region"}
EOF
```

Pinot generates MV segments through `MaterializedViewTask`. The controller task manager can schedule those tasks automatically, or you can trigger them manually:

```text
POST /tasks/schedule?taskType=MaterializedViewTask&tableName=<mvTable>_OFFLINE
```

## Understand recovery and tuning

When a retention delete or an empty refresh clears a covered MV bucket, Pinot keeps tracking that bucket as an empty covered partition instead of dropping it outright. If source data is later backfilled into the same time window, the controller consistency manager re-marks that bucket `STALE` and the next overwrite cycle rebuilds it.

By default, the consistency manager runs this empty-bucket recovery sweep every `300000` ms (5 minutes). You can change that interval live, without restarting controllers, through the cluster config key `pinot.materialized.view.consistency.empty.sweep.interval.ms`. Set it with `pinot-admin.sh ClusterConfig` or the controller `/cluster/configs` endpoint. Non-positive values fall back to the 5-minute default.

## When to keep using JSON APIs

The existing `POST /schemas`, `POST /tables`, and `PUT /tables/{tableName}` APIs still work for materialized views. Keep using them when your automation already depends on raw Pinot metadata payloads, or when you need a hand-written `MaterializedViewTask` cron that cannot be expressed as `REFRESH EVERY <N> MINUTES|HOURS|DAYS` or `'<N>m|h|d'`.

If you are building a downstream extension that needs a different MV task type or query-engine contract, see [Plugins](../../developers/plugin-architecture/README.md). Custom `MaterializedViewDdlHandler` implementations own that alternate task wiring and any engine-specific validation.

## Enable transparent rewrite for SSE queries

To let brokers rewrite eligible base-table queries to a materialized view, set this broker config:

```properties
pinot.broker.query.enable.materialized.view.rewrite=true
```

With that switch enabled, Pinot still falls back to the base table unless the MV has usable coverage. In practice, the MV must have a non-zero watermark, and if you set `stalenessThresholdMs`, the MV must still be within that freshness bound.

{% hint style="warning" %}
Today Pinot splits MV rewrites by watermark only. If a bucket below the watermark is already marked `STALE` or is still tracked as an empty covered bucket waiting for re-materialization, Pinot can still route that time range to the MV until the next overwrite cycle completes. The exposure window is bounded by the consistency-manager debounce plus one scheduling cycle, and delete/backfill races can add up to one empty-bucket recovery sweep interval.
{% endhint %}

Pinot currently rewrites eligible SSE query shapes that are subsumed by the MV, including exact matches, projection-subset scan queries, and supported aggregation rollups. Scalar expressions used as grouping keys, such as `DATETRUNC`, `UPPER`, `LOWER`, and `SUBSTR`, can match the corresponding projected expression in the MV. Aggregate expressions still require a supported aggregation rollup rule. When a rewrite happens, the broker response includes `materializedViewQueried` with the MV table name that served the query.

If you need one eligible query to stay on the base table while leaving broker-side rewrite enabled for everything else, set `enableMaterializedViewRewrite=false` on that query:

```sql
SET enableMaterializedViewRewrite = false;
SELECT region, SUM(revenue) AS total_revenue, COUNT(*) AS total_rows
FROM sales
GROUP BY region
ORDER BY total_revenue DESC
LIMIT 20;
```

This option defaults to `true`, so queries only opt out when they set it to `false`. It disables MV rewrite for that query only and forces the normal base-table path. Pinot also uses the same option internally for the `MaterializedViewTask` materialization query so the minion always reads from the base table instead of rewriting back onto an MV.

For example, once the MV is built and the broker switch is on, this base-table query can be served by the MV without changing the SQL:

```sql
SELECT region, SUM(revenue) AS total_revenue, COUNT(*) AS total_rows
FROM sales
GROUP BY region
ORDER BY total_revenue DESC
LIMIT 20;
```

The response includes the MV table name when rewrite succeeds:

```json
{
  "materializedViewQueried": "salesByHourMv_OFFLINE"
}
```

Scalar grouping expressions can also participate in the rewrite. For example, an MV defined with `DATETRUNC('DAY', event_ts)` as a projected grouping key can serve this base-table query:

```sql
SELECT DATETRUNC('DAY', event_ts) AS event_day,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY DATETRUNC('DAY', event_ts);
```

The scalar expression must match a projected MV expression. Wrapping an aggregate in another function, such as `ROUND(SUM(revenue))`, is an aggregate expression and rewrites only when Pinot has a compatible aggregation equivalence rule.

## Query the MV table directly

You can still query the MV table name directly and re-aggregate its stored values as needed:

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

The quickstart creates `airlineStatsMv`, triggers `MaterializedViewTask`, and gives you a local setup for validating direct MV queries. After you enable the broker rewrite switch, it is also a convenient way to test transparent rewrite behavior.

## Inspect and manage materialized views

In the Data Explorer, use **Data Sources** to discover both physical tables and materialized views:

- **Data Sources** shows cards for **Tables** and **Materialized Views**.
- **Materialized Views** lists each MV with its base tables, watermark, VALID and STALE partition counts, last refresh time, staleness SLO, and any metadata errors.
- Clicking an MV opens a detail page with the stored `definedSQL`, split spec, partition state, raw runtime metadata, and controls to refresh the page data or drop the MV.

The same controller DDL surface also lets you inspect and remove MVs from SQL:

```sql
SHOW MATERIALIZED VIEWS;
SHOW CREATE MATERIALIZED VIEW salesByHourMv;
DROP MATERIALIZED VIEW IF EXISTS salesByHourMv;
```

`SHOW MATERIALIZED VIEWS` returns raw MV names without the `_OFFLINE` suffix. `SHOW CREATE MATERIALIZED VIEW` emits canonical DDL for the stored MV definition, including an explicit column list even when the original `CREATE MATERIALIZED VIEW` used inferred columns.

The controller also exposes dedicated MV endpoints:

- `GET /materializedViews`
- `GET /materializedViews/{materializedViewTableName}`
- `DELETE /materializedViews/{materializedViewTableName}`

## What this page covered

This page covered the current materialized-view feature surface in Pinot: how to create and manage an MV through controller SQL DDL, which source tables and aggregations are supported, how broker-side SSE rewrite works, how to query the MV table directly, and where to inspect the MV in the UI and controller API.

## Next step

Read [Querying Pinot](querying-pinot.md) for the broader query path, or [Pinot Data Explorer](../../basics/components/exploring-pinot.md) for the UI walkthrough.

## Related pages

- [Querying & SQL](README.md)
- [Querying Pinot](querying-pinot.md)
- [Pinot Data Explorer](../../basics/components/exploring-pinot.md)
- [Functions](../../functions/README.md)
