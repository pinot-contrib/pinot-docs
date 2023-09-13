---
description: >-
  Apache Pinot is a real-time distributed OLAP datastore purpose-built for
  low-latency, high-throughput analytics.
---

# Introduction

{% hint style="info" %}
We'd love to hear from you! [Join us in our Slack channel](https://communityinviter.com/apps/apache-pinot/apache-pinot) to ask questions, troubleshoot, and share feedback.
{% endhint %}

Apache Pinot is a real-time distributed online analytical processing (OLAP) datastore. Use Pinot to ingest and immediately query data from streaming or batch data sources (including, Apache Kafka, Amazon Kinesis, Hadoop HDFS, Amazon S3, Azure ADLS, and Google Cloud Storage).

Apache Pinot includes the following:

* **Ultra low-latency analytics** even at extremely high throughput.
* **Columnar data store** with several smart indexing and pre-aggregation techniques.
* **Scaling up and out** with no upper bound.
* **Consistent performance** based on the size of your cluster and an expected query per second (QPS) threshold.

It's perfect for user-facing real-time analytics and other analytical use cases, including internal dashboards, anomaly detection, and ad hoc data exploration.

{% embed url="https://youtu.be/_lqdfq2c9cQ" %}
What is Apache Pinot? (and User-Facing Analytics) by Tim Berglund
{% endembed %}

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

If you're new to Pinot, take a look at our Getting Started guide:

{% content-ref url="basics/getting-started/" %}
[getting-started](basics/getting-started/)
{% endcontent-ref %}

To start importing data into Pinot, see how to import batch and stream data:

{% content-ref url="basics/data-import/" %}
[data-import](basics/data-import/)
{% endcontent-ref %}

To start querying data in Pinot, check out our Query guide:

{% content-ref url="users/user-guide-query/" %}
[user-guide-query](users/user-guide-query/)
{% endcontent-ref %}

## Learn

For a conceptual overview that explains how Pinot works, check out the Concepts guide:

{% content-ref url="basics/concepts.md" %}
[concepts.md](basics/concepts.md)
{% endcontent-ref %}

To understand the distributed systems architecture that explains Pinot's operating model, take a look at our basic architecture section:

{% content-ref url="basics/architecture.md" %}
[architecture.md](basics/architecture.md)
{% endcontent-ref %}
