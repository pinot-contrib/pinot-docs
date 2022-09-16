# V2 Multi-Stage Query Engine

## Overview

The new multi-stage query engine (a.k.a V2 query engine) is designed to support more complex SQL semantics such as `JOIN`, `OVER` window, `MATCH_RECOGNIZE` and eventually, make Pinot support closer to full ANSI SQL semantics.&#x20;

<figure><img src="https://www.datocms-assets.com/75153/1661707313-query-execution-model.png" alt=""><figcaption><p>Scatter-Gather Query Engine</p></figcaption></figure>



<figure><img src="https://www.datocms-assets.com/75153/1661533401-screenshot_1.png" alt=""><figcaption><p>Multi-Stage Query Engine</p></figcaption></figure>

It also resolves the bottleneck effect for the broker reduce stage where only a single machine is dedicated to perform heavy lifting such as high cardinality `GROUP BY` result merging; `ORDER BY` sorting, etc.

## How to use the V2 query engine

To enable the V2 engine,&#x20;

1. please make sure to either&#x20;
   * [Building Apache Pinot](https://github.com/apache/pinot#building-pinot) using the latest master commit.
   * Download the latest Apache Pinot docker image using the [official guide](https://docs.pinot.apache.org/basics/getting-started/running-pinot-in-docker).
2. Please add the following configurations to your cluster config:
   * ```
     "pinot.multistage.engine.enabled": "true",
     "pinot.server.instance.currentDataTableVersion": "4",
     "pinot.query.server.port": "8421",
     "pinot.query.runner.port": "8442"
     ```
3.  Start the cluster normally.&#x20;

    _<mark style="color:red;">**NOTE:**</mark> <mark style="color:red;"></mark><mark style="color:red;">If the cluster has already been started, please restart all the controller/broker/server components so that they pick up the new cluster config.</mark>_
4.  You should now see the following window in the controller query page:

    <figure><img src="../../.gitbook/assets/image (51).png" alt=""><figcaption><p>Sample Query Screenshot</p></figcaption></figure>



## Troubleshoot

The V2 query engine is still in the beta phase, there might be various performance or feature gaps from the current query engine.&#x20;

Here are the general troubleshooting steps:

### Semantic / Runtime errors

* Try downloading the latest docker image or building from the latest master commit
  * We continuously pushes bug fixes for the V2 engine so bugs you encountered might have already been fixed in the latest master build
* Try rewriting your query
  * Some of the functions previously supported in the V1 engine might have a new way to express in the new engine. Please check and see if you are using any non-standard SQL functions or semantics.

### Timeout errors

* Try reducing the size of the table(s) used:
  * Adding higher selectivity filters to the tables
* Try executing part of the subquery or a simplified version of the query first.
  * This helps to determine the selectivity and scale of the query being executed.
* Try adding more servers
  * The new V2 engine runs distributedly across the entire cluster, adding more servers to partitioned queries such as GROUP BY aggregates, equality JOINs help speed up the query runtime.

### How to share feedbacks

please report any bugs in Apache Pinot Slack [V2 engine feedback channel](https://apache-pinot.slack.com/archives/C03Q4A11GC9). Please include:

* the table/schema config(s)&#x20;
* the cluster config (zookeeper config, and each components config and scale)
* the problematic SQL query string and corresponding ERROR messages.



## Reference: Design Docs

The overall PEP design doc and discussion can be found in the following links

* [PEP discussion Github Issue](https://github.com/apache/pinot/issues/8260)  and
* [PEP design doc](https://docs.google.com/document/d/10-vL\_bUrI-Pi2oYudWyUlQl9Kf0cLrW-Z8hGczkCPik/edit)



