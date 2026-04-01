# Cluster

## Cluster Configs Definition

These are the properties that be set at the cluster level.

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
      <td>This is a Helix Property that allows any Pinot Server/Broker/Controller to automatically join the cluster. This is true by default. Operators can set this to false for more control. If you set this to false, you will have to explicitly invoke `/Instance/addInstance` API. This property is checked when a Pinot node starts and has no effect once the node is connected to the cluster.</td>
    </tr>
    <tr>
      <td>enable.case.insensitive</td>
      <td>true</td>
      <td>By default, Pinot queries are case insensitive. Table name, column name, etc are case insensitive. Every table requires a schema, so when you set this to `false` Pinot will accept any case for table names and columns based on the schema. This property is applicable to the broker and is read only when the broker starts. Changing this property will require restarting the broker.</td>
    </tr>
    <tr>
      <td>pinot.broker.enable.query.limit.override</td>
      <td>false</td>
      <td>This allows operators to protect the Pinot cluster against bad queries with large limits. By setting this to true, if Pinot broker override query limit when it is larger than broker config:`pinot.broker.query.response.limit (Default is 2147483647).`E.g. If set`pinot.broker.query.response.limit=1000` in Broker conf, then query`SELECT * FROM myTable LIMIT 25000`will be override to `SELECT * FROM myTable LIMIT 1000`.</td>
    </tr>
    <tr>
      <td>default.hyperloglog.log2m</td>
      <td>8</td>
      <td>This is a special config to override for hyperloglog that is used for approximate distinct count. Default value is 8.</td>
    </tr>
    <tr>
      <td>queryConsoleOnlyView</td>
      <td>false</td>
      <td>Only show query console for controller web UI, this is useful when you don't want to expose cluster or ZK UI to Users.</td>
    </tr>
    <tr>
      <td>hideQueryConsoleTab</td>
      <td>false</td>
      <td>Hide query console tab from controller web UI, this is useful when you don't want to expose query console UI to Users.</td>
    </tr>
    <tr>
      <td>pinot.multistage.engine.tls.enabled</td>
      <td>false</td>
      <td>Whether to enable TLS on brokers and servers for the multi-stage query engine. If set to true, TLS will be used for gRPC connections between brokers and servers (query plan dispatch from brokers to servers and final query result from servers to brokers) as well as servers and servers (data shuffle / exchange during execution of multi-stage queries).</td>
    </tr>
    <tr>
      <td>pinot.lucene.max.clause.count</td>
      <td>1024</td>
      <td>Maximum number of clauses allowed in Lucene text search queries. When text search queries contain too many terms or clauses, Lucene throws `TooManyClauses` exceptions, which can cause query failures. Increase this value for complex text search queries.</td>
    </tr>
    <tr>
      <td>pinot.multistage.engine.enabled</td>
      <td>true</td>
      <td>Whether the multi-stage query engine (MSE) is enabled for the cluster. When `false`, all queries use the single-stage engine.</td>
    </tr>
    <tr>
      <td>accounting.factory.name</td>
      <td></td>
      <td>Fully qualified class name for the resource accounting factory. Resource accounting tracks CPU time and memory allocation per query for workload isolation.</td>
    </tr>
    <tr>
      <td>accounting.enable.thread.cpu.sampling</td>
      <td>false</td>
      <td>Enable per-thread CPU time sampling for resource accounting. Provides visibility into CPU usage per query but adds measurement overhead.</td>
    </tr>
    <tr>
      <td>accounting.enable.thread.memory.sampling</td>
      <td>false</td>
      <td>Enable per-thread memory allocation sampling for resource accounting.</td>
    </tr>
    <tr>
      <td>accounting.oom.enable.killing.query</td>
      <td>false</td>
      <td>When `true` and resource accounting is enabled, allows Pinot to kill queries that are consuming excessive memory to prevent OutOfMemoryError.</td>
    </tr>
    <tr>
      <td>accounting.cpu.time.based.killing.enabled</td>
      <td>false</td>
      <td>When `true`, allows killing queries that exceed the CPU time threshold specified by `accounting.cpu.time.based.killing.threshold.ms`.</td>
    </tr>
    <tr>
      <td>accounting.cpu.time.based.killing.threshold.ms</td>
      <td>30000</td>
      <td>CPU time threshold in milliseconds beyond which a query may be killed if CPU-based killing is enabled.</td>
    </tr>
  </tbody>
</table>

## Cluster Configs APIs

## List All Cluster Configs

<mark style="color:blue;">`GET`</mark> `http://<controller>:<port>/cluster/configs`

**Description**

\- Lists all the configurations set at the cluster level

{% tabs %}
{% tab title="200 " %}
```
{
  "allowParticipantAutoJoin": "true",
  "enable.case.insensitive": "false",
  "pinot.broker.enable.query.limit.override": "false",
  "default.hyperloglog.log2m": "8"
}
```
{% endtab %}
{% endtabs %}

## Update Cluster Configs

<mark style="color:green;">`POST`</mark> `http://<controller>:<port>/cluster/configs`

Add new or update existing cluster configs.

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
      <td><p>JSON body contains the configs map for new/updated configs. E.g.</p><p><strong><code>{"queryConsoleOnlyView":"true"}</code></strong></p></td>
    </tr>
  </tbody>
</table>

{% tabs %}
{% tab title="200 " %}
```
{
  "status": "Updated cluster config."
}
```
{% endtab %}
{% endtabs %}

Example:

<!-- Image removed: swagger-cluster-config screenshot was missing from the repository -->
