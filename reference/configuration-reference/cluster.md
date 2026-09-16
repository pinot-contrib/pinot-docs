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
| max.segment.completion.time.millis | 300000 (5 minutes) | Cluster config for the maximum time allowed for LLC real-time segment completion after `segmentCommitStart`. Increase this when large segments, deep-store upload time, or retries can push real-time segment completion beyond 5 minutes. Removing the cluster config reverts Pinot to the default. |
| pinot.field.spec.default.json.max.length | 512 | Default `maxLength` Pinot applies to `JSON` columns when the field spec does not set one explicitly. Set this as a cluster config for a cluster-wide default, or in local instance config for a node-local override. |
| pinot.field.spec.default.json.max.length.exceed.strategy | NO_ACTION | Default `maxLengthExceedStrategy` Pinot applies to `JSON` columns when the field spec does not set one explicitly. Supported values are `TRIM_LENGTH`, `SUBSTITUTE_DEFAULT_VALUE`, `NO_ACTION`, and `ERROR`. Set this as a cluster config for a cluster-wide default, or in local instance config for a node-local override. |

## Query Safety

These settings control broker-side query protection, query-console exposure, and cluster-wide query engine behavior.

| Property | Default | Description |
| --- | --- | --- |
| pinot.broker.enable.query.limit.override | false | Protects the cluster from queries with very large `LIMIT` values. When enabled, Pinot brokers override query limits that exceed the broker config `pinot.broker.query.response.limit` (default `2147483647`). For example, if `pinot.broker.query.response.limit=1000`, then `SELECT * FROM myTable LIMIT 25000` is rewritten to use `LIMIT 1000`. |
| pinot.broker.use.approximate.function | false | When `true`, brokers rewrite eligible exact distinct-count and percentile aggregates to SMART variants for both single-stage and multi-stage queries. Cluster config takes precedence over broker config and updates running brokers without a restart. See [Approximate aggregate guardrail](#approximate-aggregate-guardrail). |
| pinot.broker.approximate.function.distinct.count.params | empty (function defaults) | Optional parameters passed to rewritten distinct-count SMART functions, for example `threshold=10000;log2m=12;dictThreshold=10000`. |
| pinot.broker.approximate.function.percentile.params | empty (function defaults) | Optional parameters passed to rewritten percentile SMART functions, for example `threshold=1000;compression=100`. |
| queryConsoleOnlyView | false | Shows only the query console in the controller web UI. Use this when you do not want to expose cluster or ZooKeeper UI pages to end users. |
| hideQueryConsoleTab | false | Hides the query console tab from the controller web UI. |
| pinot.multistage.engine.tls.enabled | false | Enables TLS on brokers and servers for the multi-stage query engine. When enabled, Pinot uses TLS for gRPC connections between brokers and servers for plan dispatch and final results, and between servers for data shuffle and exchange. |
| pinot.lucene.max.clause.count | 1024 | Maximum number of clauses allowed in Lucene text-search queries. Increase this value when complex text queries hit Lucene `TooManyClauses` exceptions. |
| pinot.multistage.engine.enabled | true | Enables the multi-stage query engine for the cluster. When set to `false`, all queries use the single-stage engine. |
| pinot.beta.multistage.engine.max.server.query.threads | -1 | Cluster-wide fallback for multi-stage query concurrency controls. Brokers use this value when `pinot.broker.mse.max.server.query.threads` is not set to a positive number. Servers also use it as the base value for deriving a hard limit when `pinot.server.query.executor.mse.max.execution.threads` is not set to a positive number. |
| pinot.beta.multistage.engine.max.server.query.threads.hardlimit.factor | 4 | Multiplier used by servers to derive a hard limit for multi-stage executor tasks when no server-local limit is configured. The derived hard limit is `pinot.beta.multistage.engine.max.server.query.threads * pinot.beta.multistage.engine.max.server.query.threads.hardlimit.factor`. If either value is non-positive, server hard limiting is disabled. |
| pinot.metrics.mse.mode | SERVER | Controls where multi-stage engine metrics are emitted. `SERVER` preserves the existing `pinot.server.mse*` / `pinot.server.multiStage*` series, `MSE` emits only `pinot.mse.*`, and `DUAL` emits both during dashboard migration. Brokers and servers read this at startup, so changing it requires a restart. |

### Approximate aggregate guardrail

Enable `pinot.broker.use.approximate.function` to bound per-group memory used by exact `DISTINCTCOUNT` and `PERCENTILE` queries. The broker rewrites `DISTINCTCOUNT`, `DISTINCTCOUNTMV`, `COUNT(DISTINCT x)`, `PERCENTILE`, and `PERCENTILEMV` to their SMART variants. These functions remain exact until an accumulator exceeds its conversion threshold, then use an approximate sketch. The result column type is preserved, but results above the threshold can differ from exact aggregates. This setting is off by default.

For example, set these three keys through the [cluster config API](#update-cluster-configs):

```text
pinot.broker.use.approximate.function=true
pinot.broker.approximate.function.distinct.count.params=threshold=10000;log2m=12;dictThreshold=10000
pinot.broker.approximate.function.percentile.params=threshold=1000;compression=100
```

Cluster values override the same keys in `broker.conf` and take effect on running brokers without a restart. A missing cluster value falls back to `broker.conf`. For an individual query, `SET useApproximateFunction = false` opts out (or `true` opts in); the query option outranks both cluster and broker settings. A table's `QueryConfig.useApproximateFunction` sits between the query option and cluster setting, but applies only to the single-stage engine. See [Query options](../../build-with-pinot/querying-and-sql/query-execution-controls/query-options.md).

Choose thresholds alongside the group-count limit: `numGroupsLimit` limits the number of groups, **not** the values held by each group's accumulator. A very low threshold can increase memory use by allocating a sketch for many small groups. Parameter strings are checked by the broker when configured; check broker logs for rejected values.

When a query is actually rewritten, its broker response sets `approximateFunctionApplied=true`; the broker also increments the `APPROXIMATE_FUNCTION_OVERRIDES` meter. In the single-stage engine, the name of an unaliased output column can change to the rewritten function name. Use an explicit `AS` alias if clients rely on that name. The multi-stage engine preserves the planned output name.

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
- [Broker](broker.md)
- [Multi-Stage Query Engine](../../build-with-pinot/querying-and-sql/sse-vs-mse.md)
