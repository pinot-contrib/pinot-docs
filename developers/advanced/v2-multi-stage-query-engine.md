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
3.  Start the cluster normally, you should see the following window in the controller query page:

    <figure><img src="../../.gitbook/assets/image (51).png" alt=""><figcaption><p>Sample Query Screenshot</p></figcaption></figure>



## Design Details

The overall PEP design doc and discussion can be found in the following links

* [PEP discussion Github Issue](https://github.com/apache/pinot/issues/8260)  and
* [PEP design doc](https://docs.google.com/document/d/10-vL\_bUrI-Pi2oYudWyUlQl9Kf0cLrW-Z8hGczkCPik/edit)



