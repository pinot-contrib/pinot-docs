---
description: Cluster-level configuration reference.
---

# Cluster Configuration

Cluster configuration values are stored centrally and applied across Pinot components. Use this page when the setting should affect the cluster as a whole instead of a single broker, server, or controller process.

## Key Areas

| Area | Why it matters | Jump to |
| --- | --- | --- |
| [Cluster configs](#cluster-configs) | Global config values stored in ZooKeeper and read by Pinot components | Core cluster behavior |
| [Query safety](#query-safety) | Broker query limits, query-console visibility, and multi-stage engine controls | Query guardrails |
| [Resource accounting](#resource-accounting) | CPU and memory sampling plus automatic query killing | Workload isolation |
| [Cluster config APIs](#cluster-config-apis) | Controller endpoints for reading and updating cluster config | Operational workflows |

## Cluster Configs

These settings control baseline cluster behavior and compatibility semantics.

| Property | Default | Description |
| --- | --- | --- |
| allowParticipantAutoJoin | true | Helix property that allows Pinot servers, brokers, and controllers to automatically join the cluster. When set to `false`, you must explicitly invoke the `/Instance/addInstance` API. Pinot checks this property only when a node starts and it has no effect once the node is already connected. |
| enable.case.insensitive | true | Pinot queries are case insensitive by default, including table and column names. If you set this to `false`, Pinot uses the exact case defined in the schema. This property is applicable to brokers and is read only when the broker starts, so changing it requires a broker restart. |
| default.hyperloglog.log2m | 8 | Default `log2m` value for HyperLogLog-based approximate distinct-count functions. |

## Query Safety

These settings control broker-side query protection, query-console exposure, and cluster-wide query engine behavior.

| Property | Default | Description |
| --- | --- | --- |
| pinot.broker.enable.query.limit.override | false | Protects the cluster from queries with very large `LIMIT` values. When enabled, Pinot brokers override query limits that exceed the broker config `pinot.broker.query.response.limit` (default `2147483647`). For example, if `pinot.broker.query.response.limit=1000`, then `SELECT * FROM myTable LIMIT 25000` is rewritten to use `LIMIT 1000`. |
| queryConsoleOnlyView | false | Shows only the query console in the controller web UI. Use this when you do not want to expose cluster or ZooKeeper UI pages to end users. |
| hideQueryConsoleTab | false | Hides the query console tab from the controller web UI. |
| pinot.multistage.engine.tls.enabled | false | Enables TLS on brokers and servers for the multi-stage query engine. When enabled, Pinot uses TLS for gRPC connections between brokers and servers for plan dispatch and final results, and between servers for data shuffle and exchange. |
| pinot.lucene.max.clause.count | 1024 | Maximum number of clauses allowed in Lucene text-search queries. Increase this value when complex text queries hit Lucene `TooManyClauses` exceptions. |
| pinot.multistage.engine.enabled | true | Enables the multi-stage query engine for the cluster. When set to `false`, all queries use the single-stage engine. |

## Resource Accounting

These settings enable per-query CPU and memory tracking plus optional protection against runaway queries.

| Property | Default | Description |
| --- | --- | --- |
| accounting.factory.name |  | Fully qualified class name for the resource-accounting factory. Resource accounting tracks CPU time and memory allocation per query for workload isolation. |
| accounting.enable.thread.cpu.sampling | false | Enables per-thread CPU time sampling for resource accounting. This adds visibility into CPU usage per query, but also adds measurement overhead. |
| accounting.enable.thread.memory.sampling | false | Enables per-thread memory-allocation sampling for resource accounting. |
| accounting.oom.enable.killing.query | false | When `true` and resource accounting is enabled, Pinot can kill queries that consume excessive memory in order to prevent `OutOfMemoryError`. |
| accounting.cpu.time.based.killing.enabled | false | When `true`, Pinot can kill queries that exceed the CPU time threshold configured by `accounting.cpu.time.based.killing.threshold.ms`. |
| accounting.cpu.time.based.killing.threshold.ms | 30000 | CPU time threshold in milliseconds beyond which a query may be killed when CPU-based killing is enabled. |

## Cluster Config APIs

Use the controller APIs to inspect or update cluster-level configuration.

### List All Cluster Configs

<mark style="color:blue;">`GET`</mark> `http://<controller>:<port>/cluster/configs`

**Description**

- Lists all configurations set at the cluster level.

{% tabs %}
{% tab title="200 " %}
```json
{
  "allowParticipantAutoJoin": "true",
  "enable.case.insensitive": "false",
  "pinot.broker.enable.query.limit.override": "false",
  "default.hyperloglog.log2m": "8"
}
```
{% endtab %}
{% endtabs %}

### Update Cluster Configs

<mark style="color:green;">`POST`</mark> `http://<controller>:<port>/cluster/configs`

Add new cluster configs or update existing ones.

#### Request Body

| Name | Type | Description |
| --- | --- | --- |
|  | string | JSON body containing the configs map for new or updated values. Example: `{\"queryConsoleOnlyView\":\"true\"}` |

{% tabs %}
{% tab title="200 " %}
```json
{
  "status": "Updated cluster config."
}
```
{% endtab %}
{% endtabs %}

Example:

<!-- Image removed: swagger-cluster-config screenshot was missing from the repository -->

## Related Pages

- [Configuration Reference](README.md)
- [Table Configuration](table.md)
- [Broker](../../configuration-reference/broker.md)
- [Multi-Stage Query Engine](../multi-stage-engine.md)
