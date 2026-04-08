---
description: >-
  Learn what Apache Pinot is, what problems it solves, and whether it is the
  right tool for your use case.
---

# What is Pinot?

## Outcome

By the end of this page you will understand what Apache Pinot is, what problems it solves, and whether it is the right tool for your use case.

## Prerequisites

None. This is the starting point of the onboarding path.

## What Apache Pinot does

Apache Pinot is a real-time distributed online analytical processing (OLAP) datastore. It ingests data from streaming sources (such as Apache Kafka and Amazon Kinesis) and batch sources (such as Hadoop HDFS, Amazon S3, Azure ADLS, and Google Cloud Storage) and makes that data immediately available for analytic queries with sub-second latency.

### Key capabilities

* **Ultra-low-latency analytics** -- Queries return in milliseconds, even at hundreds of thousands of queries per second.
* **Columnar storage with smart indexing** -- Purpose-built storage format with inverted, sorted, range, text, and other indexes to accelerate query patterns.
* **Horizontal scaling** -- Scale out by adding nodes with no upper bound on cluster size.
* **Consistent performance** -- Latency stays predictable as data volume and query load grow, based on cluster sizing and expected throughput.
* **Real-time ingestion** -- Data is available for querying within seconds of arriving at the streaming source.

{% embed url="https://youtu.be/_lqdfq2c9cQ" %}
What is Apache Pinot? (and User-Facing Analytics) by Tim Berglund
{% endembed %}

## When to use Pinot

### User-facing real-time analytics

Pinot was built at LinkedIn to power interactive analytics features such as Who Viewed Profile and Company Analytics. UberEats Restaurant Manager is another production example. These applications serve personalized analytics to every end user, generating hundreds of thousands of queries per second with strict latency requirements.

### Real-time dashboards

Pinot supports slice-and-dice, drill-down, roll-up, and pivot operations on high-dimensional data. Connect business intelligence tools such as Apache Superset, Tableau, or PowerBI to Pinot to build live dashboards over streaming data.

### Enterprise analytics

Pinot works well as a highly scalable platform for business intelligence. It converges the capabilities of a big data platform with the traditional role of a data warehouse, making it suitable for analysis and reporting at scale.

### Aggregate store for microservices

Application developers can use Pinot as an aggregate store that consumes events from streaming sources and exposes them through SQL. This is useful for building a unified, queryable view across a microservice architecture. Query models are eventually consistent, as with all aggregate stores.

## When NOT to use Pinot

{% hint style="warning" %}
Pinot is not a general-purpose transactional database. It does not support row-level updates, deletes, or transactions in the way that PostgreSQL or MySQL do. If your workload requires ACID transactions or frequent single-row mutations, a relational database is a better fit.
{% endhint %}

{% hint style="info" %}
If your dataset is small enough to fit comfortably in a single PostgreSQL or MySQL instance (a few million rows or less) and you do not need sub-second query latency at high concurrency, a traditional database will be simpler to operate and sufficient for your needs.
{% endhint %}

## Verify

You now know:

* What Apache Pinot is and how it differs from transactional databases.
* The four main categories of use cases where Pinot excels.
* When a simpler tool would be a better choice.

## Next step

Continue to the 10-minute quickstart to launch a local Pinot cluster and run your first query:

{% content-ref url="ten-minute-quickstart.md" %}
[ten-minute-quickstart.md](ten-minute-quickstart.md)
{% endcontent-ref %}
