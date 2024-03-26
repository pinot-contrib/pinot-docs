---
description: >-
  Explore the fundamental concepts of Apache Pinot™ as a distributed OLAP
  database.
---

# Concepts

Pinot is designed to deliver low latency queries on large datasets. To achieve this performance, Pinot stores data in a columnar format and adds additional indexes to perform fast filtering, aggregation and group by. Pinot breaks raw data into small data shards, and each shard is converted into a [segment](https://docs.pinot.apache.org/pinot-components/segment). One or more segments together form a [table](https://docs.pinot.apache.org/pinot-components/table), which is the logical container for querying Pinot using [SQL](https://docs.pinot.apache.org/user-guide/user-guide-query/pinot-query-language).

To learn about Pinot components, terminology, and gain a conceptual understanding of how data is stored in Pinot, review the following sections:

* Pinot storage model
* [Pinot architecture](architecture.md)
* [Pinot components](components/)
