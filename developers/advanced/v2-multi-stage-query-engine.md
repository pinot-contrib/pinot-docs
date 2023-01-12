# Multi-Stage Query Engine

## Overview

The new Pinot query engine version 2 (a.k.a Multi-Stage V2 query engine) is designed to support more complex SQL semantics such as `JOIN`, `OVER` window, `MATCH_RECOGNIZE` and eventually, make Pinot support closer to full ANSI SQL semantics.

<figure><img src="../../.gitbook/assets/Multi-Stage-Pinot-Query-Engine-v1.png" alt=""><figcaption><p>Scatter-Gather Query Engine</p></figcaption></figure>

<figure><img src="../../.gitbook/assets/Multi-Stage-Query-Engine-2.png" alt=""><figcaption><p>Multi-Stage Query Engine</p></figcaption></figure>

It also resolves the bottleneck effect for the broker reduce stage where only a single machine is dedicated to perform heavy lifting such as high cardinality `GROUP BY` result merging; `ORDER BY` sorting, etc.

## How to use the multi-stage query engine

To enable the multi-stage engine,

1. please make sure to either
   * [Building Apache Pinot](https://github.com/apache/pinot#building-pinot) using the latest master commit.
   * Download the latest Apache Pinot docker image using the [official guide](https://docs.pinot.apache.org/basics/getting-started/running-pinot-in-docker).
2. Please add the following configurations to your cluster config:. Cluster configs can be edited using the POST API under [this](https://docs.pinot.apache.org/users/api/controller-api-reference#cluster) section (you can find it on Swagger under Cluster section)
   * ```
     "pinot.multistage.engine.enabled": "true",
     "pinot.server.instance.currentDataTableVersion": "4",
     "pinot.query.server.port": "8421",
     "pinot.query.runner.port": "8442"
     ```
3.  Start the cluster normally.

    _<mark style="color:red;">**NOTE:**</mark>  <mark style="color:red;">If the cluster has already been started, please restart all the controller/broker/server components so that they pick up the new cluster config.</mark>_
4.  You should now see the following window in the controller query page:

    <figure><img src="../../.gitbook/assets/image (51).png" alt=""><figcaption><p>Sample Query Screenshot</p></figcaption></figure>

## Troubleshoot

The V2 query engine is still in the beta phase, there might be various performance or feature gaps from the current query engine.

Here are the general troubleshooting steps:

### Semantic / Runtime errors

* Try downloading the latest docker image or building from the latest master commit
  * We continuously push bug fixes for the multi-stage engine so bugs you encountered might have already been fixed in the latest master build
* Try rewriting your query
  * Some of the functions previously supported in the original engine might have a new way to express in the new engine. Please check and see if you are using any non-standard SQL functions or semantics.

### Timeout errors

* Try reducing the size of the table(s) used:
  * Adding higher selectivity filters to the tables
* Try executing part of the subquery or a simplified version of the query first.
  * This helps to determine the selectivity and scale of the query being executed.
* Try adding more servers
  * The new multi-stage engine runs distributedly across the entire cluster, adding more servers to partitioned queries such as GROUP BY aggregates, equality JOINs help speed up the query runtime.

### How to share feedbacks

please report any bugs in Apache Pinot Slack [multi-stage engine feedback channel](https://apache-pinot.slack.com/archives/C03Q4A11GC9). Please include:

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
* Some functions that lack implementation with `@ScalarFunction` annotation will not be supported in intermediate stages.

For more up-to-date tracking of feature and performance support please follow the Github tracking issues:

* SQL feature tracker: [https://github.com/apache/pinot/issues/9223](https://github.com/apache/pinot/issues/9223)
* Performance and stability tracker: [https://github.com/apache/pinot/issues/9273](https://github.com/apache/pinot/issues/9273)

## Reference: Design Docs

The overall PEP design doc and discussion can be found in the following links

* [PEP discussion Github Issue](https://github.com/apache/pinot/issues/8260) and
* [PEP design doc](https://docs.google.com/document/d/10-vL\_bUrI-Pi2oYudWyUlQl9Kf0cLrW-Z8hGczkCPik/edit)
