---
description: Use controller-managed SQL DDL to create, inspect, list, and drop Pinot tables and materialized views.
---

# SQL DDL

Pinot supports a controller-managed SQL DDL surface for table and materialized-view metadata operations. Use it when you want a SQL alternative to the JSON-based `/schemas` and `/tables` workflows.

The controller accepts one DDL statement per request:

- `CREATE TABLE`
- `DROP TABLE`
- `SHOW TABLES`
- `SHOW CREATE TABLE`
- `CREATE MATERIALIZED VIEW`
- `SHOW MATERIALIZED VIEWS`
- `SHOW CREATE MATERIALIZED VIEW`
- `DROP MATERIALIZED VIEW`

{% hint style="info" %}
Run these statements through the controller endpoint `POST /sql/ddl`, not through the broker query API. SSE and MSE still execute query statements; the controller owns table and materialized-view DDL.
{% endhint %}

## How it works

`POST /sql/ddl` compiles SQL into the same Pinot `Schema` and `TableConfig` model used by the existing controller APIs. That means:

- DDL-created tables go through the same controller validation path as `POST /tables`.
- DDL-created materialized views persist as regular `OFFLINE` tables plus the same MV task config the JSON APIs use.
- `SHOW CREATE TABLE` renders a canonical SQL form of the stored schema and table config that you can review, version, or replay.
- `SHOW CREATE MATERIALIZED VIEW` renders canonical MV DDL for the stored definition, including the `AS <query>` clause and MV-specific properties.
- `dryRun=true` lets you compile and validate without persisting any metadata.
- Existing broker query APIs still handle `SELECT` statements. The controller endpoint handles metadata changes.

## Supported statement shapes

| Statement | Notes |
| --- | --- |
| `CREATE TABLE [IF NOT EXISTS] [db.]table (...) [PRIMARY KEY (...)] TABLE_TYPE = OFFLINE|REALTIME [PROPERTIES (...)]` | Creates one table type at a time. Use `PROPERTIES` for table config settings such as replication, tenants, time column, indexes, stream configs, task configs, and nested config blobs. |
| `CREATE TABLE [IF NOT EXISTS] [db.]table WITH (key = value, ...)` | Extension-only form for options-defined tables. A Pinot distribution can install a handler that derives the schema and table config entirely from the `WITH` options. Apache Pinot OSS does not install such a handler, so the default behavior is to reject this form and tell you to use the column-list `TABLE_TYPE = ...` form instead. |
| `DROP TABLE [IF EXISTS] [db.]table [TYPE OFFLINE|REALTIME]` | Omitting `TYPE` targets both table variants. |
| `SHOW TABLES [FROM db]` | Lists tables in the selected database. |
| `SHOW CREATE TABLE [db.]table [TYPE OFFLINE|REALTIME]` | Returns canonical DDL for the stored table metadata. |
| `CREATE MATERIALIZED VIEW [IF NOT EXISTS] [db.]name [(...)] [REFRESH [INTERVAL] EVERY ...] PROPERTIES (...) AS <select>` | Creates an `OFFLINE` MV. Omit the column list to infer the MV schema from the `SELECT` projection, or provide a full column list to override inferred types or roles. |
| `SHOW MATERIALIZED VIEWS [FROM db]` | Lists materialized views in the selected database using raw names without the `_OFFLINE` suffix. |
| `SHOW CREATE MATERIALIZED VIEW [db.]name` | Returns canonical MV DDL for the stored metadata. |
| `DROP MATERIALIZED VIEW [IF EXISTS] [db.]name` | Drops an MV. There is no `TYPE` clause because MVs are always backed by `OFFLINE` tables. |

Use either a `db.table` qualifier or a `Database` header to target a database. If both are present, they must refer to the same database; otherwise Pinot returns `400 Bad Request`.

## Endpoint contract

Send requests to the controller:

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SHOW TABLES"}'
```

To target a database with an HTTP header:

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Database: analytics" \
  -d '{"sql":"SHOW TABLES"}'
```

Use `dryRun=true` when you want validation without persistence:

```bash
curl -X POST "http://localhost:9000/sql/ddl?dryRun=true" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"CREATE TABLE events (id INT DIMENSION) TABLE_TYPE = OFFLINE"}'
```

High-level response behavior:

- `201 Created` for a successful `CREATE TABLE`
- `201 Created` for a successful `CREATE MATERIALIZED VIEW`
- `200 OK` for `DROP TABLE`, `SHOW TABLES`, `SHOW CREATE TABLE`, `SHOW MATERIALIZED VIEWS`, `SHOW CREATE MATERIALIZED VIEW`, dry runs, and idempotent `IF EXISTS` or `IF NOT EXISTS` cases
- `400 Bad Request` for parse errors, semantic validation errors, or oversized SQL
- `404 Not Found` when a requested table or schema does not exist
- `409 Conflict` for duplicate `CREATE TABLE` without `IF NOT EXISTS`, logical-table references that block a drop, or a race with another writer

Response bodies include only fields that apply to the executed operation.

| Field | Applies to | Notes |
| --- | --- | --- |
| `operation` | all responses | One of `SHOW_TABLES`, `SHOW_MATERIALIZED_VIEWS`, `CREATE_TABLE`, `SHOW_CREATE_TABLE`, `DROP_TABLE`, `CREATE_MATERIALIZED_VIEW`, `SHOW_CREATE_MATERIALIZED_VIEW`, or `DROP_MATERIALIZED_VIEW`. |
| `databaseName` | create, drop, show create | The database scope used for the operation when available. |
| `tableName` | create, drop, show create | The resolved Pinot table name, often with `_OFFLINE` or `_REALTIME`. MV operations still target `OFFLINE` storage under the hood. |
| `tableType` | table create, typed table drop, table show create | `OFFLINE` or `REALTIME`. MV-specific statements do not take a `TYPE` clause. |
| `schema` | create | The compiled Pinot schema JSON. Returned for dry runs and persisted creates, including MV creates. |
| `tableConfig` | create | The compiled Pinot table config JSON after table config tuner processing. Returned for dry runs and persisted creates, including MV creates. |
| `warnings` | create | Non-fatal compile warnings, such as ignored `DECIMAL(p,s)` precision details. |
| `dryRun` | create, drop | Whether the request validated without persisting or deleting metadata. |
| `ifNotExists` | create | Whether the statement used `IF NOT EXISTS`. |
| `ifExists` | drop | Whether the statement used `IF EXISTS`. |
| `deletedTables` | drop | Typed table names removed by the drop. |
| `tableNames` | catalog listings | Tables or materialized views visible in the selected database, depending on the statement. |
| `ddl` | show create | Canonical `CREATE TABLE` or `CREATE MATERIALIZED VIEW` SQL for the stored metadata. |
| `message` | most responses | Human-readable operation summary. |

## Columns, types, and defaults

Every column has a Pinot data type and an optional role. If you omit the role, Pinot treats the column as a single-value dimension.

| Column form | Result |
| --- | --- |
| `name STRING` | Single-value dimension. |
| `name STRING DIMENSION` | Single-value dimension. |
| `tags STRING DIMENSION ARRAY` | Multi-value dimension. |
| `score DOUBLE METRIC` | Metric column. |
| `ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS'` | Date-time column. |

Supported data type names:

| SQL type name | Pinot type |
| --- | --- |
| `INT`, `INTEGER` | `INT` |
| `BIGINT`, `LONG` | `LONG` |
| `FLOAT`, `REAL` | `FLOAT` |
| `DOUBLE` | `DOUBLE` |
| `DECIMAL`, `NUMERIC`, `BIG_DECIMAL` | `BIG_DECIMAL` |
| `BOOLEAN` | `BOOLEAN` |
| `TIMESTAMP` | `TIMESTAMP` |
| `VARCHAR`, `CHAR`, `STRING` | `STRING` |
| `VARBINARY`, `BINARY`, `BYTES` | `BYTES` |
| `JSON` | `JSON` |

`SMALLINT` and `TINYINT` are intentionally rejected. Use `INT` until Pinot exposes narrower integer types.

Use `NOT NULL` to set a non-nullable field and `DEFAULT` to set Pinot's default null value:

```sql
CREATE TABLE users (
  id INT NOT NULL DIMENSION,
  name STRING NOT NULL DEFAULT 'unknown' DIMENSION,
  score DOUBLE DEFAULT 0.0 METRIC,
  active BOOLEAN DEFAULT TRUE DIMENSION
)
TABLE_TYPE = OFFLINE;
```

`DEFAULT NULL` is rejected. Default literals must be compatible with the declared column type. `TIMESTAMP` defaults are emitted by `SHOW CREATE TABLE` in UTC ISO-8601 form, and `BYTES` defaults are emitted as quoted hex strings.

## Properties mapping

Use the `PROPERTIES (...)` clause for table config values that are not part of the column list or `TABLE_TYPE` clause. Property keys and values are string literals.

```sql
PROPERTIES (
  'timeColumnName' = 'ts',
  'replication' = '3',
  'brokerTenant' = 'DefaultTenant',
  'serverTenant' = 'DefaultTenant'
)
```

Pinot routes properties with these rules:

| Property shape | Destination | Examples |
| --- | --- | --- |
| Promoted scalar table config keys | Dedicated `TableConfig` fields | `replication`, `brokerTenant`, `serverTenant`, `timeColumnName`, `retentionTimeUnit`, `retentionTimeValue`, `loadMode`, `sortedColumn`, `nullHandlingEnabled`, `aggregateMetrics`, `segmentVersion`, `tags`, `invertedIndexColumns`, `noDictionaryColumns`, `bloomFilterColumns`, `rangeIndexColumns`, `jsonIndexColumns` |
| JSON blob table config keys | Nested `TableConfig` objects | `ingestionConfig`, `upsertConfig`, `dedupConfig`, `routingConfig`, `queryConfig`, `quotaConfig`, `tierConfigs`, `tunerConfigs`, `fieldConfigs`, `instanceAssignmentConfigMap`, `tagOverrideConfig`, `starTreeIndexConfigs`, `segmentPartitionConfig`, `jsonIndexConfigs` |
| `streamType`, `stream.*`, `realtime.*` | Realtime stream configs | `stream.kafka.topic.name`, `stream.kafka.decoder.class.name`, `stream.kafka.consumer.factory.class.name`, `realtime.segment.flush.threshold.rows` |
| `task.<taskType>.<key>` | Minion task config | `task.RealtimeToOfflineSegmentsTask.bucketTimePeriod` |
| Any other key | Table custom config | `owner`, `team.pipeline`, `custom.flag` |

List-valued promoted properties use comma-separated strings, for example `'invertedIndexColumns' = 'userId,country'`. Stream and realtime properties are valid only on `REALTIME` tables.

## Extension form: options-defined `CREATE TABLE`

Some Pinot distributions expose an extension form where the controller derives the schema and table config from a `WITH` option map instead of a column list:

```sql
CREATE TABLE trips_analytics WITH (
  type = 'iceberg',
  catalog_type = 'rest',
  catalog_uri = 'https://unity-catalog.company.com/api/2.1/unity-catalog/iceberg',
  schema_name = 'transportation',
  table_name = 'nyc_taxi_trips',
  storage.region = 'us-west-2',
  refresh_interval = '5m',
  enable_schema_evolution = true
);
```

For this form:

- Keys can be quoted string literals or unquoted identifiers, including dotted names such as `storage.region`.
- Values can be quoted strings, booleans, or unsigned numeric literals.
- Pinot normalizes the parsed options to ordered string key/value pairs before handing them to the installed table handler.

Apache Pinot OSS does not ship a built-in options-defined table handler, so the default controller behavior is to reject this form with guidance to use the column-list `CREATE TABLE ... TABLE_TYPE = OFFLINE | REALTIME` syntax instead.

## Example: create an offline table

```sql
CREATE TABLE events (
  id INT NOT NULL DIMENSION,
  city STRING DIMENSION,
  amount DOUBLE METRIC,
  ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS'
)
TABLE_TYPE = OFFLINE
PROPERTIES (
  'timeColumnName' = 'ts',
  'replication' = '3',
  'brokerTenant' = 'DefaultTenant',
  'serverTenant' = 'DefaultTenant'
);
```

Submit that statement with `POST /sql/ddl`:

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"sql":"CREATE TABLE events (id INT NOT NULL DIMENSION, city STRING DIMENSION, amount DOUBLE METRIC, ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS') TABLE_TYPE = OFFLINE PROPERTIES ('timeColumnName' = 'ts', 'replication' = '3', 'brokerTenant' = 'DefaultTenant', 'serverTenant' = 'DefaultTenant')"}
EOF
```

## Example: create a realtime Kafka table

```sql
CREATE TABLE clicks (
  user_id STRING DIMENSION,
  url STRING DIMENSION,
  ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS'
)
TABLE_TYPE = REALTIME
PROPERTIES (
  'timeColumnName' = 'ts',
  'replication' = '2',
  'streamType' = 'kafka',
  'stream.kafka.topic.name' = 'click_events',
  'stream.kafka.decoder.class.name' = 'org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder',
  'stream.kafka.consumer.factory.class.name' = 'org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory',
  'stream.kafka.broker.list' = 'kafka-broker:9092',
  'stream.kafka.consumer.prop.auto.offset.reset' = 'smallest',
  'realtime.segment.flush.threshold.rows' = '500000'
);
```

## Example: create an upsert table

Use `PRIMARY KEY` with a realtime table and pass the upsert configuration as a JSON property:

```sql
CREATE TABLE upsertOrders (
  orderId INT NOT NULL DIMENSION,
  userId STRING NOT NULL DIMENSION,
  amount DOUBLE METRIC,
  ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS'
)
PRIMARY KEY (orderId)
TABLE_TYPE = REALTIME
PROPERTIES (
  'timeColumnName' = 'ts',
  'replication' = '2',
  'streamType' = 'kafka',
  'stream.kafka.topic.name' = 'orders',
  'stream.kafka.decoder.class.name' = 'org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder',
  'stream.kafka.consumer.factory.class.name' = 'org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory',
  'stream.kafka.broker.list' = 'kafka-broker:9092',
  'stream.kafka.consumer.prop.auto.offset.reset' = 'smallest',
  'upsertConfig' = '{"mode":"FULL"}'
);
```

## Example: multi-value dimension

Use `DIMENSION ARRAY` for multi-value dimensions:

```sql
CREATE TABLE products (
  id INT DIMENSION,
  tags STRING DIMENSION ARRAY
)
TABLE_TYPE = OFFLINE;
```

## Example: indexes and ingestion config

Promoted list properties use comma-separated strings. Nested table configs use JSON strings.

```sql
CREATE TABLE pageviews (
  userId STRING DIMENSION,
  country STRING DIMENSION,
  payload JSON DIMENSION,
  ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS'
)
TABLE_TYPE = OFFLINE
PROPERTIES (
  'timeColumnName' = 'ts',
  'invertedIndexColumns' = 'userId,country',
  'jsonIndexColumns' = 'payload',
  'ingestionConfig' = '{"batchIngestionConfig":{"segmentIngestionType":"APPEND","segmentIngestionFrequency":"DAILY"}}'
);
```

## Example: task config

Use `task.<taskType>.<key>` properties for minion task configs:

```sql
CREATE TABLE events (
  id INT DIMENSION,
  ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS'
)
TABLE_TYPE = OFFLINE
PROPERTIES (
  'timeColumnName' = 'ts',
  'task.RealtimeToOfflineSegmentsTask.bucketTimePeriod' = '1d',
  'task.RealtimeToOfflineSegmentsTask.maxNumRecordsPerSegment' = '5000000',
  'task.SegmentRefreshTask.tableMaxNumTasks' = '5'
);
```

## Example: create and inspect a materialized view

Use `CREATE MATERIALIZED VIEW` when you want the controller to persist an MV as an `OFFLINE` table plus `MaterializedViewTask` metadata. The column list is optional: omit it to infer the schema from the `SELECT` projection, or provide a full column list if you need to override inferred types or roles.

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

Use the same endpoint to list, inspect, and drop MVs:

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SHOW MATERIALIZED VIEWS"}'
```

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SHOW CREATE MATERIALIZED VIEW salesByHourMv"}'
```

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"DROP MATERIALIZED VIEW IF EXISTS salesByHourMv"}'
```

`SHOW CREATE MATERIALIZED VIEW` emits canonical DDL for the stored MV definition, including an explicit column list even if the original create statement relied on inferred columns.

## Example: show the stored table definition

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SHOW CREATE TABLE events TYPE OFFLINE"}'
```

Example response:

```json
{
  "operation": "SHOW_CREATE_TABLE",
  "tableName": "events_OFFLINE",
  "tableType": "OFFLINE",
  "ddl": "CREATE TABLE events (\n  id INT NOT NULL DIMENSION,\n  city STRING DIMENSION,\n  amount DOUBLE METRIC,\n  ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS'\n)\nTABLE_TYPE = OFFLINE\nPROPERTIES (\n  'brokerTenant' = 'DefaultTenant',\n  'replication' = '3',\n  'serverTenant' = 'DefaultTenant',\n  'timeColumnName' = 'ts'\n)",
  "message": "Rendered canonical CREATE TABLE for events_OFFLINE."
}
```

Canonical DDL uses deterministic ordering for properties and normalizes values where Pinot stores a canonical form. For example, a `TIMESTAMP` date-time column emits `FORMAT 'TIMESTAMP'`, boolean defaults emit `TRUE` or `FALSE`, and identifiers that need quoting are double-quoted.

## Example: list and drop tables

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Database: analytics" \
  -d '{"sql":"SHOW TABLES"}'
```

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"DROP TABLE events TYPE OFFLINE"}'
```

Use `DROP TABLE events` without `TYPE` to drop both the offline and realtime variants when they exist. Use `DROP TABLE IF EXISTS events` when a missing table should be a successful no-op.

## When to keep using JSON APIs

If you already manage table metadata through `POST /schemas`, `POST /tables`, or `PUT /tables/{tableName}`, those APIs still work. SQL DDL is an additional interface, not a replacement for the existing controller metadata APIs. For materialized views, keep using raw JSON metadata if you need a `MaterializedViewTask` schedule that is not expressible as `REFRESH EVERY <N> MINUTES|HOURS|DAYS` or `'<N>m|h|d'`.

## Related pages

- [SQL syntax](sql-syntax.md)
- [SQL Reference](sql-reference.md)
- [Controller API Examples](../../reference/api-reference/controller-api.md)
- [Schema and Table Shape](../data-modeling/schema.md)
