---
description: Use controller-managed SQL DDL to create, inspect, list, and drop Pinot tables.
---

# SQL Table DDL

Pinot supports a controller-managed SQL DDL surface for table metadata operations. Use it when you want a SQL alternative to the JSON-based `/schemas` and `/tables` workflows.

The controller accepts these statements:

- `CREATE TABLE`
- `DROP TABLE`
- `SHOW TABLES`
- `SHOW CREATE TABLE`

{% hint style="info" %}
Run these statements through the controller endpoint `POST /sql/ddl`, not through the broker query API. SSE and MSE still execute query statements; the controller owns table DDL.
{% endhint %}

## How it works

`POST /sql/ddl` compiles SQL into the same Pinot `Schema` and `TableConfig` model used by the existing controller APIs. That means:

- DDL-created tables go through the same controller validation path as `POST /tables`.
- `SHOW CREATE TABLE` renders a canonical SQL form of the stored schema and table config.
- `dryRun=true` lets you compile and validate without persisting any metadata.

## Supported statement shapes

| Statement | Notes |
| --- | --- |
| `CREATE TABLE [IF NOT EXISTS] [db.]table (...) TABLE_TYPE = OFFLINE|REALTIME [PROPERTIES (...)]` | Creates one table type at a time. Use `PROPERTIES` for table config settings such as replication, tenants, time column, stream configs, and nested config blobs. |
| `DROP TABLE [IF EXISTS] [db.]table [TYPE OFFLINE|REALTIME]` | Omitting `TYPE` targets both table variants. |
| `SHOW TABLES [FROM db]` | Lists tables in the selected database. |
| `SHOW CREATE TABLE [db.]table [TYPE OFFLINE|REALTIME]` | Returns canonical DDL for the stored table metadata. |

Use either a `db.table` qualifier or a `Database` header to target a database.

## Endpoint contract

Send requests to the controller:

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SHOW TABLES"}'
```

Use `dryRun=true` when you want validation without persistence:

```bash
curl -X POST "http://localhost:9000/sql/ddl?dryRun=true" \
  -H "Content-Type: application/json" \
  -d '{"sql":"CREATE TABLE events (id INT DIMENSION) TABLE_TYPE = OFFLINE"}'
```

High-level response behavior:

- `201 Created` for a successful `CREATE TABLE`
- `200 OK` for `DROP TABLE`, `SHOW TABLES`, `SHOW CREATE TABLE`, dry runs, and idempotent `IF EXISTS` or `IF NOT EXISTS` cases
- `400 Bad Request` for parse errors, semantic validation errors, or oversized SQL
- `404 Not Found` when a requested table or schema does not exist

## Example: create an offline table

```sql
CREATE TABLE events (
  id INT NOT NULL DIMENSION,
  city STRING DIMENSION,
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
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"sql":"CREATE TABLE events (id INT NOT NULL DIMENSION, city STRING DIMENSION, ts TIMESTAMP DATETIME FORMAT 'TIMESTAMP' GRANULARITY '1:MILLISECONDS') TABLE_TYPE = OFFLINE PROPERTIES ('timeColumnName' = 'ts', 'replication' = '3', 'brokerTenant' = 'DefaultTenant', 'serverTenant' = 'DefaultTenant')"}
EOF
```

## Example: show the stored table definition

```bash
curl -X POST "http://localhost:9000/sql/ddl" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SHOW CREATE TABLE events TYPE OFFLINE"}'
```

Pinot returns canonical SQL that you can review, version, or replay later.

## When to keep using JSON APIs

If you already manage table metadata through `POST /schemas`, `POST /tables`, or `PUT /tables/{tableName}`, those APIs still work. SQL DDL is an additional interface, not a replacement for the existing controller metadata APIs.

## Related pages

- [SQL syntax](sql-syntax.md)
- [SQL Reference](sql-reference.md)
- [Controller API Examples](../../reference/api-reference/controller-api.md)
- [Schema and Table Shape](../data-modeling/schema.md)
