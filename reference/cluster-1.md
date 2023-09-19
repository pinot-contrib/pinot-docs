---
description: An overview of the multi-stage query engine.
---

# Multi-stage query engine (v2)

The Pinot multi-stage query engine (v2) includes an intermediate compute stage (shown in the following diagram) that shares the workload across servers, eliminating the potential bottleneck on the Pinot broker.&#x20;

This document covers:

* [Why to use the multi-stage query engine](cluster-1.md#why-use-the-multi-stage-query-engine)
* [When not to use the multi-stage query engine](cluster-1.md#when-not-to-use-the-multi-stage-query-engine)
* [An overview of the multi-stage query execution model](cluster-1.md#multi-stage-query-execution-model)
* [How queries are processed](cluster-1.md#how-queries-are-processed)

For more information on the multi-stage query engine (v2), see the following:

* See how to [enable and use the multi-stage query engine](../developers/advanced/v2-multi-stage-query-engine.md)
* Review [limitations](../developers/advanced/troubleshoot-multi-stage-query-engine.md#limitations-of-the-multi-stage-query-engine) of the multi-stage query engine and [troubleshooting tips](../developers/advanced/troubleshoot-multi-stage-query-engine.md#troubleshoot-errors)
* Query [Window functions](../users/user-guide-query/windows-functions.md) and [JOINs](../users/user-guide-query/joins.md)

## Why use the multi-stage query engine?

You must use the multi-stage query engine (v2) to query distributed joins, window functions, other multi-stage operators in real time. See how to enable and [use the multi-stage query engine (v2)](../developers/advanced/v2-multi-stage-query-engine.md).

The multi-stage query engine is built to run real-time facing, complex ANSI SQL. Highlights include joins and data correlations, particularly optimized for dynamic broadcast fact-dim joins, and partitioned-based or colocated table joins.

## When not to use the multi-stage query engine?

Although the multi-stage query engine can generally execute any complex ANSI SQL ([ISO/IEC 9075](https://en.wikipedia.org/wiki/ISO/IEC\_9075)). It is not designed to run any generic ANSI SQL in the most efficient way.&#x20;

Some **use cases to avoid**:

* **Large-scale, long-running queries designed to access and transform entire datasets** are not recommended, as the multistage engine is a pure in-memory system.
* **Complex correlation, join algorithms** that touch many tables or have many non-trivial join conditions are not recommended.
* **Long-running, complex queries such as ETL-type** (extract, transform, and load) use cases are not recommended.

## Multi-stage query execution model

The multi-stage query engine improves query performance over the [single-stage scatter-gather query engine ( v1)](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/\~/changes/1760/reference/cluster), effectively decoupling the data exchange layer and the query engine layer.

<figure><img src="../.gitbook/assets/Multi-Stage-Query-Engine-2 (2).png" alt=""><figcaption></figcaption></figure>

The intermediate compute stage includes a set of processing servers and a data exchange mechanism.&#x20;

**Processing servers** in the intermediate compute stage can be assigned to any Pinot component. Multiple servers can process data in the intermediate stage, the goal being to offload the computation from the brokers. Each server in the intermediate stage executes the same processing logic, but against different sets of data.&#x20;

The **data exchange service** coordinates the transfer of the different sets of data to and from the processing servers.

The multi-stage query engine also includes a **new query plan optimizer** to produce optimal process logic in each stage and minimize data shuffling overhead.

## How queries are processed

With a multi-stage query engine, Pinot first breaks down the [single scatter-gather query plan used in v1](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/\~/changes/1760/reference/cluster) into multiple query sub-plans that run across different sets of servers. We call these sub-plans “stage plans,” and refer to each execution as a “stage.”

Consider the following JOIN query example, which illustrates the breakdown of a query into stages. This query joins a real-time `orderStatus` table with an `offline customer` table:

```sql
SELECT 
  os.uid,               -- user ID
  os.rName,             -- restaurant Name
  c.ltv                 -- life-time value
FROM
  orderStatus AS os 
  INNER JOIN customer AS c
    ON os.uid = c.uid
WHERE
  os.ic < 10            -- item count
  AND c.lto > 5         –- life-time order count
```

### Stage 1

In the first stage, the query is processed as follows:

1. Real-time servers execute the filter query on the `orderStatus` table:

{% code overflow="wrap" %}
```sql
SELECT os.uid, os.rName FROM orderStatus AS os WHERE os.ic < 10
```
{% endcode %}

2. Offline servers execute the filter query offline `customer` table:

{% code overflow="wrap" %}
```sql
SELECT c.uid c.ltv FROM customer AS c WHERE c.lto > 5
```
{% endcode %}

3. The data exchange service shuffles data shuffle, so all data with the same unique customer ID is sent to the same processing server for the next stage.

### Stage 2

1. On each processing server, an inner JOIN is performed.
2.  Each intermediary servers (shown in [_Figure 1: Multi-stage query execution model_](cluster-1.md#multi-stage-query-execution-model)) performs a local join, and

    runs the same join algorithm, but on different `uids.`

### Stage 3

* After the join algorithm completes, the results are sent back to the broker, and then sent to clients.&#x20;
