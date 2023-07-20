# Multi-Stage Query Engine

## Overview

The new Pinot query engine version 2 (a.k.a Multi-Stage V2 query engine) is designed to support more complex SQL semantics such as `JOIN`, `OVER` window, `MATCH_RECOGNIZE` and eventually, make Pinot support closer to full ANSI SQL semantics.

<figure><img src="../../.gitbook/assets/Multi-Stage-Pinot-Query-Engine-v1.png" alt=""><figcaption><p>Scatter-Gather Query Engine</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Multi-Stage-Query-Engine-2.png" alt=""><figcaption><p>Multi-Stage Query Engine</p></figcaption></figure>

It also resolves the bottleneck effect for the broker reduce stage where only a single machine is dedicated to perform heavy lifting such as high cardinality `GROUP BY` result merging; `ORDER BY` sorting, etc.

## How to enable the multi-stage query engine

### Check if the multi-stage engine is enabled

The multi-stage engine should be default enabled on the latest master branch. To check whether your version of Pinot has enabled the multi-stage engine, run a query via the controller console with the "use V2 Engine" flag checked and you should see results similar to the following page.

<figure><img src="../../.gitbook/assets/image (51).png" alt=""><figcaption><p>Sample Query Screenshot</p></figcaption></figure>

### Manually enable the multi-stage engine.

For some older master release versions of Pinot, the multi-stage engine might not be default enabled. If upgrading to latest master is not an option and you see the "use V2 Engine" flag option on the controller query console, follow the instruction below to manually enable it

1.  Add the following configurations to your cluster config

    ```
    "pinot.multistage.engine.enabled": "true",
    "pinot.server.instance.currentDataTableVersion": "4",
    "pinot.query.server.port": "8421",
    "pinot.query.runner.port": "8442"
    ```
2. Restart the cluster.

_<mark style="color:red;">**Noted that**</mark>_

* <mark style="color:red;">Cluster configs can be edited using the POST API under</mark> [<mark style="color:blue;">this section</mark>](https://docs.pinot.apache.org/users/api/controller-api-reference#cluster) <mark style="color:red;">(you can find it on Swagger under the Cluster section)</mark>
* <mark style="color:red;">the</mark> <mark style="color:red;"></mark><mark style="color:red;">`"pinot.query.server.port"`</mark> <mark style="color:red;"></mark><mark style="color:red;">and</mark> <mark style="color:red;"></mark><mark style="color:red;">`"pinot.query.runner.port"`</mark> <mark style="color:red;"></mark><mark style="color:red;">option should only be added if every Pinot component is launched within its own network environment, otherwise, port conflict will occur.</mark>&#x20;
* <mark style="color:red;">If the cluster has already been started, restart all the controller/broker/server components so that they pick up the new cluster config.</mark>

## How to programmatically access the multi-stage query engine

There are 2 main ways to make a query against the multi-stage engine:

### Via REST APIs

The Controller query API and the Broker query API allow optional JSON payload for configuration. For example:

* For Controller REST API

```bash
curl -X POST http://localhost:9000/sql -d 
'
{
  "sql": "select * from baseballStats limit 10",
  "trace": false,
  "queryOptions": "useMultistageEngine=true"
}
'
```

* For Broker REST API

```bash
curl -X POST http://localhost:8000/query/sql -d '
{
  "sql": "select * from baseballStats limit 10",
  "trace": false,
  "queryOptions": "useMultistageEngine=true"
}
'
```

### Via Query Options

When executing a query via a non-REST API route. we also support enabling the multi-stage engine via the query option. simply attach a query option at the top of your query will enable the multi-stage engine

```sql
SET useMultistageEngine=true; -- indicator to enable the multi-stage engine.
SELECT * from baseballStats limit 10
```

## Troubleshoot

The V2 query engine is still in the beta phase, there might be various performance or feature gaps from the current query engine.

Here are the general troubleshooting steps:

### Cluster errors

If you can't get the cluster to run and received an error indicating the multi-stage engine is not available:

* Make sure your pinot-servers have access to the configured port: The default setting above assumes all pinot-servers are run on individual networks and all of them have access to the same port number available within that environment. If your cluster is not set up this way, you will have to manually configure them directly in your pinot-server config file.

### Semantic / Runtime errors

* Try downloading the latest docker image or building from the latest master commit
  * We continuously push bug fixes for the multi-stage engine so bugs you encountered might have already been fixed in the latest master build
* Try rewriting your query
  * Some of the functions previously supported in the original engine might have a new way to express in the new engine. Check and see if you are using any non-standard SQL functions or semantics.

### Timeout errors

* Try reducing the size of the table(s) used:
  * Adding higher selectivity filters to the tables
* Try executing part of the subquery or a simplified version of the query first.
  * This helps to determine the selectivity and scale of the query being executed.
* Try adding more servers
  * The new multi-stage engine runs distributedly across the entire cluster, adding more servers to partitioned queries such as GROUP BY aggregates, equality JOINs help speed up the query runtime.

### How to share feedbacks

Report any bugs in Apache Pinot Slack [multi-stage engine feedback channel](https://apache-pinot.slack.com/archives/C03Q4A11GC9). Include:

* the table/schema config(s)
* the cluster config (zookeeper config, and each components config and scale)
* the problematic SQL query string and corresponding ERROR messages.

## Limitations

We are continuously improving the multi-stage engine. However, since the multi-stage engine is still in beta-testing phase, there are some limitations to call out:

* Incomplete data type support: multi-value columns and some other non-primitive data types are not supported. For example `SELECT *` with multi-value columns will fail.
* The intermediate stages of the multi-stage engine are running purely on heap memory, thus executing a large table join will cause potential out-of-memory errors
  * Because of this, the table scan phase for join queries is limited to 10 million rows.
* Currently, it doesn't incorporate table statistics into plan optimization.
* Currently, it doesn't support complex aggregation functions, such as `COVAR_POP`.
* Currently, it doens't support tenant isolation, only `DEFAULT_TENANT` is visible to the multi-stage engine.

For more up-to-date tracking of feature and performance support follow the Github tracking issues:

* SQL feature tracker: [https://github.com/apache/pinot/issues/9223](https://github.com/apache/pinot/issues/9223)
* Performance and stability tracker: [https://github.com/apache/pinot/issues/9273](https://github.com/apache/pinot/issues/9273)

## Reference: Design Docs

The overall PEP design doc and discussion can be found in the following links

* [PEP discussion Github Issue](https://github.com/apache/pinot/issues/8260) and
* [PEP design doc](https://docs.google.com/document/d/10-vL\_bUrI-Pi2oYudWyUlQl9Kf0cLrW-Z8hGczkCPik/edit)
