---
description: Cluster-level configuration reference.
---

# Cluster Configuration

Cluster configuration values are stored centrally and applied across Pinot components. Use this page when the setting should affect the cluster as a whole instead of a single broker, server, or controller process.

## Key Areas

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Why it matters</th>
      <th>Jump to</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Cluster configs](#cluster-configs)</td>
      <td>Global config values stored in ZooKeeper and read by Pinot components</td>
      <td>Core cluster behavior</td>
    </tr>
    <tr>
      <td>[Query safety](#query-safety)</td>
      <td>Broker query limits, query-console visibility, and multi-stage engine controls</td>
      <td>Query guardrails</td>
    </tr>
    <tr>
      <td>[Resource accounting](#resource-accounting)</td>
      <td>CPU and memory sampling plus automatic query killing</td>
      <td>Workload isolation</td>
    </tr>
    <tr>
      <td>[Cluster config APIs](#cluster-config-apis)</td>
      <td>Controller endpoints for reading and updating cluster config</td>
      <td>Operational workflows</td>
    </tr>
  </tbody>
</table>

## Cluster Configs

These settings control baseline cluster behavior and compatibility semantics.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>allowParticipantAutoJoin</td>
      <td>true</td>
      <td>Helix property that allows Pinot servers, brokers, and controllers to automatically join the cluster. When set to `false`, you must explicitly invoke the `/Instance/addInstance` API. Pinot checks this property only when a node starts and it has no effect once the node is already connected.</td>
    </tr>
    <tr>
      <td>enable.case.insensitive</td>
      <td>true</td>
      <td>Pinot queries are case insensitive by default, including table and column names. If you set this to `false`, Pinot uses the exact case defined in the schema. This property is applicable to brokers and is read only when the broker starts, so changing it requires a broker restart.</td>
    </tr>
    <tr>
      <td>default.hyperloglog.log2m</td>
      <td>8</td>
      <td>Default `log2m` value for HyperLogLog-based approximate distinct-count functions.</td>
    </tr>
  </tbody>
</table>

## Query Safety

These settings control broker-side query protection, query-console exposure, and cluster-wide query engine behavior.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>pinot.broker.enable.query.limit.override</td>
      <td>false</td>
      <td>Protects the cluster from queries with very large `LIMIT` values. When enabled, Pinot brokers override query limits that exceed the broker config `pinot.broker.query.response.limit` (default `2147483647`). For example, if `pinot.broker.query.response.limit=1000`, then `SELECT * FROM myTable LIMIT 25000` is rewritten to use `LIMIT 1000`.</td>
    </tr>
    <tr>
      <td>queryConsoleOnlyView</td>
      <td>false</td>
      <td>Shows only the query console in the controller web UI. Use this when you do not want to expose cluster or ZooKeeper UI pages to end users.</td>
    </tr>
    <tr>
      <td>hideQueryConsoleTab</td>
      <td>false</td>
      <td>Hides the query console tab from the controller web UI.</td>
    </tr>
    <tr>
      <td>pinot.multistage.engine.tls.enabled</td>
      <td>false</td>
      <td>Enables TLS on brokers and servers for the multi-stage query engine. When enabled, Pinot uses TLS for gRPC connections between brokers and servers for plan dispatch and final results, and between servers for data shuffle and exchange.</td>
    </tr>
    <tr>
      <td>pinot.lucene.max.clause.count</td>
      <td>1024</td>
      <td>Maximum number of clauses allowed in Lucene text-search queries. Increase this value when complex text queries hit Lucene `TooManyClauses` exceptions.</td>
    </tr>
    <tr>
      <td>pinot.multistage.engine.enabled</td>
      <td>true</td>
      <td>Enables the multi-stage query engine for the cluster. When set to `false`, all queries use the single-stage engine.</td>
    </tr>
  </tbody>
</table>

## Resource Accounting

These settings enable per-query CPU and memory tracking plus optional protection against runaway queries.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>accounting.factory.name</td>
      <td></td>
      <td>Fully qualified class name for the resource-accounting factory. Resource accounting tracks CPU time and memory allocation per query for workload isolation.</td>
    </tr>
    <tr>
      <td>accounting.enable.thread.cpu.sampling</td>
      <td>false</td>
      <td>Enables per-thread CPU time sampling for resource accounting. This adds visibility into CPU usage per query, but also adds measurement overhead.</td>
    </tr>
    <tr>
      <td>accounting.enable.thread.memory.sampling</td>
      <td>false</td>
      <td>Enables per-thread memory-allocation sampling for resource accounting.</td>
    </tr>
    <tr>
      <td>accounting.oom.enable.killing.query</td>
      <td>false</td>
      <td>When `true` and resource accounting is enabled, Pinot can kill queries that consume excessive memory in order to prevent `OutOfMemoryError`.</td>
    </tr>
    <tr>
      <td>accounting.cpu.time.based.killing.enabled</td>
      <td>false</td>
      <td>When `true`, Pinot can kill queries that exceed the CPU time threshold configured by `accounting.cpu.time.based.killing.threshold.ms`.</td>
    </tr>
    <tr>
      <td>accounting.cpu.time.based.killing.threshold.ms</td>
      <td>30000</td>
      <td>CPU time threshold in milliseconds beyond which a query may be killed when CPU-based killing is enabled.</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>string</td>
      <td>JSON body containing the configs map for new or updated values. Example: `{\"queryConsoleOnlyView\":\"true\"}`</td>
    </tr>
  </tbody>
</table>

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
- [Multi-Stage Query Engine](../../build-with-pinot/querying-and-sql/sse-vs-mse.md)
