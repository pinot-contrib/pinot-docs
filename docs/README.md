---
description: >-
  Apache Pinot is a real-time distributed OLAP datastore purpose-built for
  low-latency, high-throughput analytics, and perfect for user-facing analytical
  workloads.
---

# Introduction

Apache Pinot™ is a real-time distributed online analytical processing (OLAP) datastore. Use Pinot to ingest and immediately query data from streaming or batch data sources (including, Apache Kafka, Amazon Kinesis, Hadoop HDFS, Amazon S3, Azure ADLS, and Google Cloud Storage).

!!! note
    We'd love to hear from you! [Join us in our Slack channel](https://communityinviter.com/apps/apache-pinot/apache-pinot) to ask questions, troubleshoot, and share feedback.&#x20;

Apache Pinot includes the following:

* **Ultra low-latency analytics** even at extremely high throughput.
* **Columnar data store** with several smart indexing and pre-aggregation techniques.
* **Scaling up and out** with no upper bound.
* **Consistent performance** based on the size of your cluster and an expected query per second (QPS) threshold.

It's perfect for user-facing real-time analytics and other analytical use cases, including internal dashboards, anomaly detection, and ad hoc data exploration.

<iframe width="100%" height="400" src="https://www.youtube.com/embed/_lqdfq2c9cQ" title="What is Apache Pinot? (and User-Facing Analytics) by Tim Berglund" frameborder="0" allowfullscreen></iframe>

### User-facing real-time analytics

User-facing analytics refers to the analytical tools exposed to the end users of your product. In a user-facing analytics application, all users receive personalized analytics on their devices, resulting in hundreds of thousands of queries per second. Queries triggered by apps may grow quickly in proportion to the number of active users on the app, as many as millions of events per second. Data generated in Pinot is immediately available for analytics in latencies under one second.

User-facing real-time analytics requires the following:

* **Fresh data.** The system needs to be able to ingest data in real time and make it available for querying, also in real time.
* **Support for high-velocity, highly dimensional event data** from a wide range of actions and from multiple sources.
* **Low latency.** Queries are triggered by end users interacting with apps, resulting in hundreds of thousands of queries per second with arbitrary patterns.
* **Reliability and high availability.**
* **Scalability.**
* **Low cost to serve.**

## Why Pinot?

Pinot is designed to execute OLAP queries with low latency. It works well where you need fast analytics, such as aggregations, on both mutable and immutable data.

**User-facing, real-time analytics**

Pinot was originally built at LinkedIn to power rich interactive real-time analytics applications, such as [Who Viewed Profile](https://www.linkedin.com/me/profile-views/urn:li:wvmp:summary/), [Company Analytics](https://www.linkedin.com/company/linkedin/insights/), [Talent Insights](https://business.linkedin.com/talent-solutions/talent-insights), and many more. [UberEats Restaurant Manager](https://eng.uber.com/restaurant-manager/) is another example of a user-facing analytics app built with Pinot.

**Real-time dashboards for business metrics**

Pinot can perform typical analytical operations such as slice and dice, drill down, roll up, and pivot on large scale multi-dimensional data. For instance, at LinkedIn, Pinot powers dashboards for thousands of business metrics. Connect various business intelligence (BI) tools such as [Superset](https://superset.apache.org/docs/intro/), [Tableau](https://www.tableau.com/resource/business-intelligence), or [PowerBI](https://powerbi.microsoft.com/en-us/) to visualize data in Pinot.

**Enterprise business intelligence**

For analysts and data scientists, Pinot works well as a highly-scalable data platform for business intelligence. Pinot converges big data platforms with the traditional role of a data warehouse, making it a suitable replacement for analysis and reporting.

**Enterprise application development**

For application developers, Pinot works well as an aggregate store that sources events from streaming data sources, such as Kafka, and makes it available for a query using SQL. You can also use Pinot to aggregate data across a microservice architecture into one easily queryable view of the domain.

Pinot [tenants](https://docs.pinot.apache.org/basics/components/tenant) prevent any possibility of sharing ownership of database tables across microservice teams. Developers can create their own query models of data from multiple systems of record depending on their use case and needs. As with all aggregate stores, query models are eventually consistent.

## Get started

<div class="grid cards" markdown>

-   :material-rocket:{ .lg .middle } __Getting Started__

    ---
    Quick start guide for Pinot

    [:octicons-arrow-right-24: Getting started](basics/getting-started/)

-   :material-database-import:{ .lg .middle } __Import Data__

    ---
    How to import batch and stream data into Pinot

    [:octicons-arrow-right-24: Data Import](manage-data/data-import/)

-   :material-magnify:{ .lg .middle } __Query Guide__

    ---
    Learn how to query data in Pinot
    
    [:octicons-arrow-right-24: Query Guide](users/user-guide-query/)

</div>

## Learn

<div class="grid cards" markdown>

-   :material-lightbulb:{ .lg .middle } __Concepts__

    ---
    Conceptual overview explaining how Pinot works

    [:octicons-arrow-right-24: Concepts](basics/concepts/)

-   :fontawesome-solid-diagram-project:{ .lg .middle } __Architecture__
    
    ---
    Distributed systems architecture and Pinot's operating model

    [:octicons-arrow-right-24: Architecture](basics/architecture.md)

</div>
