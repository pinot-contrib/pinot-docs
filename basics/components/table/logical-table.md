---
description: >-
  Learn about Logical Tables in Apache Pinot, which provide a unified query
  interface over multiple physical tables for flexible data organization.
---

# Logical Table

A logical table in Pinot provides a unified query interface over multiple physical tables. Instead of querying individual tables separately, users can query a single logical table that transparently routes the query to all underlying physical tables and aggregates the results.

## Overview

Logical tables are useful for:

* **Geographic/Regional partitioning**: Split data by region (e.g., `ordersUS`, `ordersEU`, `ordersAPAC`) while providing a unified `orders` table for queries
* **Table partitioning strategies**: Organize data across multiple physical tables based on business logic
* **Time-based table splitting**: Combine historical and recent data from different physical tables

{% hint style="info" %}
Logical tables require that all underlying physical tables share the same schema structure. A schema with the same name as the logical table must be created before creating the logical table.
{% endhint %}

## How It Works

When you query a logical table, Pinot:

1. Resolves the logical table name to its list of physical tables
2. Routes the query to all relevant physical tables (both offline and realtime)
3. Aggregates results from all physical tables
4. Returns a unified result set to the client

For hybrid logical tables (containing both offline and realtime physical tables), Pinot uses a configurable time boundary strategy to determine which segments to query from each table type, avoiding duplicate data.

## Logical Table Configuration

A logical table configuration defines the mapping between the logical table and its physical tables.

### Configuration Properties

| Property | Description | Required |
|----------|-------------|----------|
| `tableName` | Name of the logical table | Yes |
| `brokerTenant` | The broker tenant to use for routing | Yes |
| `physicalTableConfigMap` | Map of physical table names to their configurations | Yes |
| `refOfflineTableName` | Reference offline table for table config metadata | Required if offline tables exist |
| `refRealtimeTableName` | Reference realtime table for table config metadata | Required if realtime tables exist |
| `query` | Query configuration (timeout, response size limits, etc.) | No |
| `quota` | Quota configuration for rate limiting | No |
| `timeBoundaryConfig` | Time boundary configuration for hybrid tables | Required for hybrid logical tables |

### Example Configuration

```json
{
  "tableName": "orders",
  "brokerTenant": "DefaultTenant",
  "physicalTableConfigMap": {
    "ordersUS_OFFLINE": {},
    "ordersEU_OFFLINE": {},
    "ordersAPAC_OFFLINE": {}
  },
  "refOfflineTableName": "ordersUS_OFFLINE"
}
```

### Hybrid Logical Table Configuration

For logical tables that combine both offline and realtime physical tables:

```json
{
  "tableName": "events",
  "brokerTenant": "DefaultTenant",
  "physicalTableConfigMap": {
    "eventsHistorical_OFFLINE": {},
    "eventsRecent_OFFLINE": {},
    "eventsLive_REALTIME": {}
  },
  "refOfflineTableName": "eventsHistorical_OFFLINE",
  "refRealtimeTableName": "eventsLive_REALTIME",
  "timeBoundaryConfig": {
    "boundaryStrategy": "min",
    "parameters": {
      "includedTables": ["eventsRecent_OFFLINE"]
    }
  }
}
```

## Creating a Logical Table

### Step 1: Create the Schema

Create a schema that matches the structure of your physical tables:

```json
{
  "schemaName": "orders",
  "dimensionFieldSpecs": [
    { "name": "orderId", "dataType": "STRING" },
    { "name": "customerId", "dataType": "STRING" },
    { "name": "region", "dataType": "STRING" },
    { "name": "productId", "dataType": "STRING" },
    { "name": "status", "dataType": "STRING" }
  ]
}
```

Upload the schema:

```bash
curl -F schemaName=@orders_schema.json localhost:9000/schemas
```

### Step 2: Create the Logical Table

```bash
curl -X POST -H 'Content-Type: application/json' \
  -d '{
    "tableName": "orders",
    "brokerTenant": "DefaultTenant",
    "physicalTableConfigMap": {
      "ordersUS_OFFLINE": {},
      "ordersEU_OFFLINE": {},
      "ordersAPAC_OFFLINE": {}
    },
    "refOfflineTableName": "ordersUS_OFFLINE"
  }' \
  http://localhost:9000/logicalTables
```

## Managing Logical Tables

### List Logical Tables

```bash
curl http://localhost:9000/logicalTables
```

### Get Logical Table Configuration

```bash
curl http://localhost:9000/logicalTables/{tableName}
```

### Update Logical Table

```bash
curl -X PUT -H 'Content-Type: application/json' \
  -d '{
    "tableName": "orders",
    "brokerTenant": "DefaultTenant",
    "physicalTableConfigMap": {
      "ordersUS_OFFLINE": {},
      "ordersEU_OFFLINE": {},
      "ordersAPAC_OFFLINE": {},
      "ordersANZ_OFFLINE": {}
    },
    "refOfflineTableName": "ordersUS_OFFLINE"
  }' \
  http://localhost:9000/logicalTables/orders
```

### Delete Logical Table

```bash
curl -X DELETE http://localhost:9000/logicalTables/{tableName}
```

{% hint style="warning" %}
Deleting a logical table only removes the logical table configuration. The underlying physical tables and their data are not affected.
{% endhint %}

## Querying Logical Tables

Query a logical table just like any other Pinot table:

```sql
-- Query the logical table
SELECT COUNT(*) FROM orders

-- Filter by region
SELECT orderId, customerId, region, status
FROM orders
WHERE region = 'us'
LIMIT 10

-- Aggregate across all regions
SELECT region, COUNT(*) as orderCount
FROM orders
GROUP BY region
ORDER BY region
```

Logical tables work with both the single-stage and multi-stage query engines.

## Time Boundary Configuration

For hybrid logical tables that contain both offline and realtime physical tables, you must configure a time boundary strategy to avoid querying duplicate data.

### Available Strategies

| Strategy | Description |
|----------|-------------|
| `min` | Uses the minimum time boundary from the specified tables |

### Configuration Example

```json
{
  "timeBoundaryConfig": {
    "boundaryStrategy": "min",
    "parameters": {
      "includedTables": ["eventsRecent_OFFLINE"]
    }
  }
}
```

The `includedTables` parameter specifies which physical tables should be considered when computing the time boundary.

## Query Configuration

Logical tables support query-level configurations:

```json
{
  "tableName": "orders",
  "brokerTenant": "DefaultTenant",
  "physicalTableConfigMap": { ... },
  "refOfflineTableName": "ordersUS_OFFLINE",
  "query": {
    "timeoutMs": 30000,
    "disableGroovy": true,
    "maxServerResponseSizeBytes": 1000000,
    "maxQueryResponseSizeBytes": 5000000
  }
}
```

| Property | Description |
|----------|-------------|
| `timeoutMs` | Query timeout in milliseconds |
| `disableGroovy` | Disable Groovy functions in queries |
| `maxServerResponseSizeBytes` | Maximum response size from each server |
| `maxQueryResponseSizeBytes` | Maximum total query response size |

## Quota Configuration

Apply rate limiting to logical tables:

```json
{
  "tableName": "orders",
  "brokerTenant": "DefaultTenant",
  "physicalTableConfigMap": { ... },
  "refOfflineTableName": "ordersUS_OFFLINE",
  "quota": {
    "maxQueriesPerSecond": 100
  }
}
```

{% hint style="info" %}
Storage quota (`quota.storage`) is not supported for logical tables since they don't store data directly.
{% endhint %}

## Managing Logical Tables via the Controller UI

The Pinot Controller UI provides full CRUD management for logical tables, accessible directly from the main Tables page.

### Accessing Logical Tables

1. Open the Controller UI (default: `http://<controller-host>:9000`).
2. Navigate to **Tables** in the left sidebar.
3. The Tables page displays physical tables and logical tables in separate sections.
4. Click a logical table name to open its detail page, which shows:
   - Current configuration (JSON)
   - Physical table mappings

### Supported Operations

| Operation | Description |
|---|---|
| **List** | View all logical tables with search and filter |
| **View** | Inspect the logical table's configuration and physical table assignments |
| **Update** | Edit the logical table configuration in-place |
| **Delete** | Remove a logical table from the cluster |

{% hint style="tip" %}
All operations are also available via the REST API at `/logicalTables/{tableName}` using GET, PUT, and DELETE.
{% endhint %}

## Quick Start Example

Try the logical table quickstart to see the feature in action:

{% tabs %}
{% tab title="Docker" %}
```bash
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type LOGICAL_TABLE
```
{% endtab %}

{% tab title="Launcher scripts" %}
```bash
./bin/pinot-admin.sh QuickStart -type LOGICAL_TABLE
```
{% endtab %}
{% endtabs %}

This quickstart:

1. Creates three physical tables: `ordersUS_OFFLINE`, `ordersEU_OFFLINE`, and `ordersAPAC_OFFLINE`
2. Creates a logical table `orders` that unifies all three
3. Demonstrates queries on both physical and logical tables

## Validation Rules

When creating or updating a logical table, Pinot validates:

* Table name does not end with `_OFFLINE` or `_REALTIME`
* All physical tables exist (unless marked as `multiCluster`)
* Physical tables are in the same database as the logical table
* Schema with the same name as the logical table exists
* Broker tenant exists
* Reference table names (`refOfflineTableName`, `refRealtimeTableName`) are set correctly
* Time boundary config is provided for hybrid tables

## Limitations

* All physical tables must have compatible schemas
* Storage quota is not supported
* Physical tables in the same logical table should ideally have consistent indexing for optimal query performance

## Pluggable LogicalTableConfig Serialization

By default, `LogicalTableConfig` is serialized to and deserialized from ZooKeeper using a built-in JSON format. For advanced use cases requiring a custom storage format, implement `LogicalTableConfigSerDe` and register it via `LogicalTableConfigSerDeProvider`.

### When to Use This

- You need a compact binary format for deployments with a very large number of logical tables
- Your ZooKeeper schema requires a specific non-default encoding
- You are integrating Pinot with an external metadata system with its own serialization requirements

### Implementation

**Step 1:** Implement the `LogicalTableConfigSerDe` interface:

```java
public class MyCustomSerDe implements LogicalTableConfigSerDe {
    @Override
    public byte[] serialize(LogicalTableConfig config) { /* ... */ }

    @Override
    public LogicalTableConfig deserialize(byte[] bytes) { /* ... */ }
}
```

**Step 2:** Implement `LogicalTableConfigSerDeProvider` to return your custom SerDe.

**Step 3:** Register the provider using the Java Service Provider Interface (SPI) by creating the file:
```
META-INF/services/org.apache.pinot.spi.config.table.logical.LogicalTableConfigSerDeProvider
```
containing the fully-qualified class name of your provider implementation.

{% hint style="note" %}
This is an advanced extension point for specialized deployments. Most users should rely on the default JSON-based serialization.
{% endhint %}

## See Also

* [Table Configuration](../../../configuration-reference/table.md)
* [Schema Configuration](schema.md)
