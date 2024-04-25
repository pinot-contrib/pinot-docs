---
description: >-
  Explore the fundamental concepts of Apache Pinot™ as a distributed OLAP
  database.
---

# Concepts

Apache Pinot™ is a database designed to deliver highly concurrent, ultra-low-latency queries on large datasets through a set of common data model abstractions. Delivering on these goals requires several foundational architectural commitments, including:

* Storing data in columnar form to support high-performance scanning
* Sharding of data to scale both storage and computation
* A distributed architecture designed to scale capacity linearly
* A tabular data model read by SQL queries

To learn about Pinot components, terminology, and gain a conceptual understanding of how data is stored in Pinot, review the following sections:

* [Pinot storage model](pinot-storage-model.md)
* [Pinot architecture](../architecture.md)
* [Pinot components](../components/)
