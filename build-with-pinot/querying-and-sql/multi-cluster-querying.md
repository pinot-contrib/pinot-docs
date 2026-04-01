---
description: Query data across multiple Pinot clusters using multi-cluster querying (federation)
---

# Multi-Cluster Querying

Multi-cluster querying (also known as federation) enables Apache Pinot brokers to execute queries across multiple Pinot clusters using logical tables. By creating a logical table that references physical tables in different clusters, you can query data distributed across clusters as if it were in a single unified table.

## Overview

Multi-cluster querying allows you to:

- Create logical tables that combine physical tables from multiple clusters
- Query federated logical tables as a single unified view
- Execute cross-cluster joins using the multi-stage query engine
- Aggregate data from multiple clusters in a single query

{% hint style="info" %}
**Important:** Only logical tables support multi-cluster federation. Physical tables in remote clusters cannot be queried directly — you must create a logical table that references them.
{% endhint %}

This feature is particularly useful for:
- **Geographic distribution**: Query data from clusters in different regions
- **Data isolation**: Query across clusters with different data retention policies or security boundaries
- **Logical table federation**: Combine physical tables from different clusters into a single logical view

## How It Works

Multi-cluster querying extends the broker's routing capabilities to include remote clusters:

1. **Broker startup**: The broker connects to remote clusters as a Helix spectator via their ZooKeeper instances
2. **Routing table building**: The broker maintains routing tables for both local and all remote clusters, periodically checking for table changes
3. **Query execution**: When `enableMultiClusterRouting=true` is set:
   - The broker queries routing managers for all clusters
   - Routes are combined across local and remote clusters
   - Queries are scattered to servers in all applicable clusters
   - Results are merged before returning to the client

<!-- TODO: Add architecture diagram showing:
     - Primary broker connected to primary ZK and remote ZKs
     - Routing to servers in both local and remote clusters
     - Query flow from client -> broker -> multiple cluster servers -> merged result -->

## Prerequisites

Before enabling multi-cluster querying:

1. All clusters must be accessible via ZooKeeper from the broker host
2. Network connectivity must exist between the broker and servers in all clusters
3. For logical table federation, table schemas must be compatible across clusters

## Configuration

### Broker Configuration

To enable multi-cluster querying, configure your broker to use `MultiClusterHelixBrokerStarter` and specify remote cluster connections:

**Configuration Properties:**

- `pinot.remote.cluster.names`: Comma-separated list of remote cluster names
- `pinot.remote.zk.server.<clusterName>`: ZooKeeper address for each remote cluster

**Example Configuration:**

```properties
# Local cluster configuration
pinot.cluster.name=PrimaryCluster
pinot.zk.server=localhost:2181

# Remote cluster configuration
pinot.remote.cluster.names=SecondaryCluster,TertiaryCluster
pinot.remote.zk.server.SecondaryCluster=secondary-zk:2181
pinot.remote.zk.server.TertiaryCluster=tertiary-zk:2181
```

### Broker Startup Class

Add the multi-cluster broker starter to your configuration file:

```properties
pinot.broker.startable.class=org.apache.pinot.broker.broker.helix.MultiClusterHelixBrokerStarter
```

{% hint style="info" %}
The `pinot.broker.startable.class` property is required. Without it, the broker uses the default `HelixBrokerStarter` which only supports single-cluster querying.
{% endhint %}

### Starting the Broker

Start the broker with your configuration file:

```bash
bin/pinot-admin.sh StartBroker \
  -configFileName /path/to/broker.conf
```

Or use config overrides for quick testing:

```bash
bin/pinot-admin.sh StartBroker \
  -zkAddress localhost:2181 \
  -clusterName PrimaryCluster \
  -configOverrides "pinot.remote.cluster.names=SecondaryCluster,pinot.remote.zk.server.SecondaryCluster=secondary-zk:2181,pinot.broker.startable.class=org.apache.pinot.broker.broker.helix.MultiClusterHelixBrokerStarter"
```

### Verifying Broker Startup

Check the broker logs for successful remote cluster connections:

```
[multi-cluster] Starting multi-cluster broker
[multi-cluster] Connected to remote cluster 'SecondaryCluster' at ZK: secondary-zk:2181
[multi-cluster] Multi-cluster broker started successfully
```

If a remote cluster fails to connect, you'll see warnings but the broker will still start:

```
[multi-cluster] Failed to connect to cluster 'TertiaryCluster'
[multi-cluster] The following clusters are unavailable: [TertiaryCluster]
```

## Running Multi-Cluster Queries

Multi-cluster routing must be explicitly enabled for each query using the `enableMultiClusterRouting` query option.

{% hint style="warning" %}
Without `enableMultiClusterRouting=true`, queries only execute against the local cluster, even if the broker is configured for multi-cluster.
{% endhint %}

### Using SET Statement

```sql
SET enableMultiClusterRouting=true;
SELECT COUNT(*) FROM unified_sales
```

### Cross-Cluster Joins with Multi-Stage Engine

Multi-cluster querying works with the multi-stage query engine for complex queries including joins:

```sql
SET enableMultiClusterRouting=true;
SET useMultistageEngine=true;

SELECT
  o.order_id,
  o.customer_name,
  p.product_name,
  o.quantity
FROM unified_orders o
JOIN unified_products p ON o.product_id = p.product_id
WHERE o.order_date > '2024-01-01'
LIMIT 100
```

Each table in the join must still be a logical table. Multi-cluster routing rejects direct queries to physical tables.

## Logical Tables with Multi-Cluster

{% hint style="warning" %}
**Only logical tables can be federated across clusters.** Physical tables cannot be directly queried across clusters. To query data from multiple clusters, you must create a logical table that references the physical tables in each cluster.
{% endhint %}

Multi-cluster querying integrates with logical tables, allowing physical tables from different clusters to be combined:

### Creating a Federated Logical Table

**Step 1:** Ensure physical tables exist in each cluster:
- `sales_east_OFFLINE` in PrimaryCluster (local)
- `sales_west_OFFLINE` in SecondaryCluster (remote)

**Step 2:** Create the logical table configuration:

```json
{
  "tableName": "unified_sales",
  "physicalTableConfigMap": {
    "sales_east_OFFLINE": {
      "multiCluster": false
    },
    "sales_west_OFFLINE": {
      "multiCluster": true
    }
  },
  "brokerTenant": "DefaultTenant",
  "refOfflineTableName": "sales_east_OFFLINE"
}
```

| Field | Description |
|-------|-------------|
| `tableName` | Name of the logical table |
| `physicalTableConfigMap` | Map of physical table names to their configurations |
| `multiCluster` | Set to `true` for tables in remote clusters, `false` for local tables |
| `refOfflineTableName` | Reference table for schema and config inheritance |

**Step 3:** Create the logical table via the Controller API:

```bash
curl -X POST 'http://localhost:9000/logicalTables' \
  -H 'Content-Type: application/json' \
  -d @unified_sales_logical_table.json
```

**Step 4:** Query the logical table:

```sql
SET enableMultiClusterRouting=true;
SELECT region, SUM(revenue)
FROM unified_sales
GROUP BY region
```

{% hint style="info" %}
The logical table must be created on each cluster's controller, with appropriate `multiCluster` flags indicating which tables are local vs. remote from that cluster's perspective.
{% endhint %}

## Query Behavior

### Unavailable Clusters

If a remote cluster is unavailable (cannot connect to its ZooKeeper), the broker will:
- Continue processing queries using available clusters
- Add a warning to the query response indicating which clusters are unavailable
- Query results may be incomplete if data exists only in unavailable clusters

**Example Response with Unavailable Cluster:**

```json
{
  "resultTable": { ... },
  "exceptions": [
    {
      "errorCode": 510,
      "message": "Remote cluster 'SecondaryCluster' is not connected. Query results may be incomplete."
    }
  ]
}
```

Error code 510 (`RemoteClusterUnavailable`) indicates query results may be incomplete.

## Configuration Reference

### Broker Properties

| Property | Description | Required |
|----------|-------------|----------|
| `pinot.remote.cluster.names` | Comma-separated list of remote cluster names | Yes |
| `pinot.remote.zk.server.<clusterName>` | ZooKeeper address for the specified remote cluster | Yes (per cluster) |
| `pinot.broker.startable.class` | Must be `org.apache.pinot.broker.broker.helix.MultiClusterHelixBrokerStarter` | Yes |

### Query Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enableMultiClusterRouting` | boolean | `false` | Enable querying across all configured clusters |

## Performance Considerations

| Factor | Impact | Recommendation |
|--------|--------|----------------|
| Network latency | Cross-cluster queries add network RTT | Place brokers with low latency to all clusters |
| Query timeouts | Timeout applies to entire federated query | Set timeout considering worst-case cluster latency |
| Routing table size | Broker memory increases with remote tables | Monitor broker heap usage |
| ZK connections | Broker maintains spectator connections to all ZKs | Ensure ZK can handle additional connections |

## Limitations

- **Logical tables only**: Only logical tables can be federated across clusters; physical tables cannot be directly queried from remote clusters
- **No cross-cluster ingestion**: Multi-cluster querying is read-only; data ingestion is cluster-specific
- **Schema compatibility**: Logical tables require compatible schemas across physical tables
- **Single query timeout**: Cannot set per-cluster timeouts
- **ZK accessibility**: All remote ZooKeepers must be reachable from the broker host

## Troubleshooting

### Broker fails to start or connect to remote cluster

**Symptoms:** Broker logs show connection failures to remote ZooKeeper

**Resolution:**
1. Verify ZooKeeper address is correct: `pinot.remote.zk.server.<clusterName>`
2. Test network connectivity: `nc -zv <zk-host> <zk-port>`
3. Check ZooKeeper is running and accessible
4. Verify no firewall rules blocking the connection

### Queries don't return data from remote clusters

**Symptoms:** Query results seem to only include local data

**Resolution:**
1. Confirm `enableMultiClusterRouting=true` is set in query
2. Check broker logs for remote cluster connection status
3. Verify table exists in remote cluster
4. For logical tables, verify `multiCluster: true` is set correctly

### Error code 510 in query response

**Symptoms:** Query response contains exception with error code 510

**Resolution:**
This indicates a remote cluster was unavailable. Check:
1. Remote cluster health and ZooKeeper status
2. Network connectivity from broker to remote ZooKeeper
3. If temporary, results may be incomplete but query succeeds

### High query latency

**Symptoms:** Multi-cluster queries are significantly slower than single-cluster

**Resolution:**
1. Check network latency to remote cluster servers (not just ZK)
2. Use `EXPLAIN PLAN FOR` to understand query execution
3. Consider data locality optimizations

## Related Documentation

- [Query Options](query-execution-controls/query-options.md) - Complete list of query options including `enableMultiClusterRouting`
- [Multi-Stage Query Engine](multi-stage-query/README.md) - Advanced query execution across clusters
- [Tables](../../basics/components/table/README.md) - Table types and concepts including logical tables
- [Broker Configuration](../../reference/configuration-reference/broker.md) - Broker configuration reference
