---
description: Batch ingestion of data into Apache Pinot using dimension tables.
---

# Dimension table

Dimension tables are a special kind of offline table designed for join-like enrichment of fact data at query time. They are used together with the [lookup UDF](../../../build-with-pinot/querying-and-sql/lookup-udf-join.md) (single-stage engine) or the [lookup join strategy](../../../build-with-pinot/querying-and-sql/multi-stage-query/join-strategies/lookup-join-strategy.md) (multi-stage engine) to decorate query results with reference data.

## When to use dimension tables

Use a dimension table when you need to enrich a large fact table with attributes from a small, relatively static reference dataset at query time. Common examples include:

* Looking up a human-readable team name from a team ID.
* Enriching clickstream events with product catalog attributes.
* Decorating transaction records with customer or store metadata.

If any of the following apply, a regular offline or real-time table is a better fit:

* The reference data is large (hundreds of millions of rows or multiple gigabytes).
* The data changes frequently and requires real-time ingestion.
* You need time-based partitioning, retention policies, or a hybrid table setup.
* You need to query the reference data with complex aggregations independently.

## How dimension tables work

When a table is marked as a dimension table, Pinot replicates all of its segments to **every server** in the tenant. On each server the data is loaded into an in-memory hash map keyed by the table's primary key, which enables constant-time lookups during query execution.

Because the data is fully replicated and held in memory, dimension tables must be **small enough to fit comfortably in each server's heap**. They are not intended for large datasets.

### Memory loading modes

Pinot supports two loading modes controlled by the `disablePreload` setting in `dimensionTableConfig`:

| Mode | `disablePreload` | Memory usage | Lookup speed | Description |
| --- | --- | --- | --- | --- |
| **Fast lookup** (default) | `false` | Higher | Faster | All rows are fully materialized into an in-memory hash map (`Object[] -> Object[]`). Every column value is stored in the map for constant-time retrieval. |
| **Memory-optimized** | `true` | Lower | Slightly slower | Only the primary key and a segment/docId reference are stored in the hash map. Column values are read from the segment on each lookup. This trades lookup speed for lower heap usage. |

Choose the memory-optimized mode when the dimension table is relatively large and you want to reduce heap pressure, at the cost of slightly slower lookups.

## Size limits and memory considerations

* **Cluster-level maximum size**: The controller configuration property `controller.dimTable.maxSize` sets the maximum storage quota allowed for any single dimension table. The default is **200 MB**. Table creation fails if the requested `quota.storage` exceeds this limit.
* **Heap impact**: In fast-lookup mode, the entire table is materialized in Java heap on every server. A table that is 100 MB on disk may consume significantly more memory after deserialization. Monitor server heap usage when adding or growing dimension tables.
* **Replication overhead**: Because every server in the tenant holds a full copy, adding a dimension table multiplies its memory footprint by the number of servers.

{% hint style="warning" %}
As a guideline, keep dimension tables under a few hundred thousand rows and well under the `controller.dimTable.maxSize` limit. Tables that approach or exceed available heap will cause out-of-memory errors on servers.
{% endhint %}

## Configuration

### Table configuration

Mark a table as a dimension table by setting the following properties in the table config:

| Property | Required | Description |
| --- | --- | --- |
| `isDimTable` | Yes | Set to `true` to designate the table as a dimension table. |
| `ingestionConfig.batchIngestionConfig.segmentIngestionType` | Yes | Must be set to `REFRESH`. Dimension tables use segment replacement rather than append semantics so that the in-memory hash map is rebuilt with the latest data. |
| `validationConfig.segmentAssignmentStrategy` | No | If set, must be `allservers`. Leaving it unset also works because Pinot automatically uses all-servers assignment for dimension tables. |
| `quota.storage` | Recommended | Storage quota for the table. Must not exceed the cluster-level `controller.dimTable.maxSize` (default 200 MB). |
| `dimensionTableConfig.disablePreload` | No | Set to `true` to use memory-optimized mode (store only primary key and segment reference instead of full rows). Defaults to `false` (fast lookup). |
| `dimensionTableConfig.errorOnDuplicatePrimaryKey` | No | Set to `true` to fail segment loading if duplicate primary keys are detected across segments. Defaults to `false` (last-loaded segment wins). |

### Schema configuration

Dimension table schemas use `dimensionFieldSpecs` instead of `metricFieldSpecs`. A `primaryKeyColumns` array is **required** -- it defines the key used for lookups.

{% hint style="warning" %}
Dimension tables always use the `allservers` segment assignment strategy so every segment is replicated to every server in the tenant. Do not configure balanced, replica-group, or round-robin segment assignment for a dimension table. Pinot now rejects those values during table validation.
{% endhint %}

### Example table configuration

```json
{
  "OFFLINE": {
    "tableName": "dimBaseballTeams_OFFLINE",
    "tableType": "OFFLINE",
    "segmentsConfig": {
    },
    "validationConfig": {
      "segmentAssignmentStrategy": "allservers"
    },
    "ingestionConfig": {
      "batchIngestionConfig": {
        "segmentIngestionType": "REFRESH"
      }
    },
    "quota": {
      "storage": "200M"
    },
    "isDimTable": true,
    "dimensionTableConfig": {
      "disablePreload": false,
      "errorOnDuplicatePrimaryKey": false
    }
  }
}
```

### Example schema configuration

```json
{
  "schemaName": "dimBaseballTeams",
  "primaryKeyColumns": ["teamID"],
  "dimensionFieldSpecs": [
    {
      "dataType": "STRING",
      "name": "teamID"
    },
    {
      "dataType": "STRING",
      "name": "teamName"
    },
    {
      "dataType": "STRING",
      "name": "teamAddress"
    }
  ]
}
```

## Querying with the LOOKUP function

The primary way to use a dimension table is through the `LOOKUP` UDF in the single-stage query engine. This function performs a primary-key lookup against the dimension table and returns a column value.

### Syntax

```
LOOKUP('dimTable', 'dimColToLookUp', 'dimJoinKey1', factJoinKey1 [, 'dimJoinKey2', factJoinKey2 ]*)
```

* `dimTable` -- name of the dimension table (string literal).
* `dimColToLookUp` -- column to retrieve from the dimension table (string literal).
* `dimJoinKey` / `factJoinKey` -- pairs of join keys: the dimension table column name (string literal) and the corresponding fact table column expression.

### Single-key lookup

```sql
SELECT
  playerName,
  teamID,
  LOOKUP('dimBaseballTeams', 'teamName', 'teamID', teamID) AS teamName,
  LOOKUP('dimBaseballTeams', 'teamAddress', 'teamID', teamID) AS teamAddress
FROM baseballStats
LIMIT 10
```

### Composite-key lookup

When the dimension table has a composite primary key, provide multiple key pairs in the same order as `primaryKeyColumns` in the schema:

```sql
SELECT
  customerId,
  LOOKUP('billing', 'city', 'customerId', customerId, 'creditHistory', creditHistory) AS city
FROM transactions
LIMIT 10
```

### Multi-stage engine

In the multi-stage engine (MSE), use a standard `JOIN` with the lookup join strategy hint instead of the `LOOKUP` UDF:

```sql
SELECT /*+ lookupJoinStrategy(dim_billing) */
  t.customerId,
  b.city
FROM transactions t
JOIN billing b
  ON t.customerId = b.customerId
LIMIT 10
```

For details, see [lookup join strategy](../../../build-with-pinot/querying-and-sql/multi-stage-query/join-strategies/lookup-join-strategy.md).

## Refresh and update strategies

Because dimension tables use `segmentIngestionType: REFRESH`, uploading a new segment **replaces** the existing segment and triggers a full reload of the in-memory hash map on every server. There is no incremental update mechanism.

Typical refresh patterns:

* **Scheduled batch job**: Run a periodic ingestion job (e.g., daily or hourly) that rebuilds the segment from the source of truth and uploads it to Pinot.
* **On-demand refresh**: Trigger a segment upload through the Pinot REST API whenever the reference data changes.

{% hint style="info" %}
During a refresh, the old hash map remains active for lookups until the new one is fully loaded. There is no query downtime during a refresh, but there is a brief period where the old data is served.
{% endhint %}

### Handling duplicate primary keys

When multiple segments contain the same primary key, the default behavior is last-loaded-segment-wins (segments are ordered by creation time). Set `errorOnDuplicatePrimaryKey: true` in `dimensionTableConfig` to fail fast if duplicates are detected. With `REFRESH` ingestion, there is typically only one segment, so duplicates across segments are uncommon.

## Performance best practices

* **Keep tables small.** Dimension tables are loaded entirely into memory on every server. Target thousands to low hundreds of thousands of rows.
* **Use narrow schemas.** Include only the columns needed for lookups to reduce memory consumption.
* **Choose the right loading mode.** Use fast lookup (default) for the best query performance. Switch to memory-optimized mode (`disablePreload: true`) only if heap usage is a concern.
* **Set a storage quota.** Always configure `quota.storage` to prevent accidentally uploading oversized data.
* **Minimize refresh frequency.** Each refresh triggers a full reload of the hash map. Avoid refreshing more often than necessary.
* **Monitor server heap.** After adding a dimension table, check server JVM heap metrics to confirm adequate headroom.

## Limitations

* **Offline only.** Dimension tables must be offline tables. They cannot be real-time or hybrid tables.
* **Full replication.** All segments are replicated to every server in the tenant, so memory usage scales with the number of servers.
* **No incremental updates.** The entire segment must be replaced on each refresh; row-level updates are not supported.
* **Primary key required.** The schema must define `primaryKeyColumns`. Lookups without a primary key are not supported.
* **Single-stage LOOKUP UDF limitations.** Dimension table column references in the `LOOKUP` function must be string literals, not column identifiers, because they reference a table that is not part of the query's FROM clause.
* **No time-based partitioning or retention.** Dimension tables do not support segment retention policies or time-based partitioning.
