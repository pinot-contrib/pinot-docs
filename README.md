---
description: >-
  Apache Pinot is a real-time distributed OLAP datastore purpose-built for
  low-latency, high-throughput analytics, and perfect for user-facing analytical
  workloads.
---

# Introduction

Apache Pinot™ is a real-time distributed online analytical processing (OLAP) datastore. Use Pinot to ingest and immediately query data from streaming or batch data sources (including, Apache Kafka, Amazon Kinesis, Hadoop HDFS, Amazon S3, Azure ADLS, and Google Cloud Storage).

{% hint style="info" %}
We'd love to hear from you! [Join us in our Slack channel](https://inviter.co/apache-pinot) to ask questions, troubleshoot, and share feedback.&#x20;
{% endhint %}

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

{% content-ref url="manage-data/data-import/" %}
[data-import](manage-data/data-import/)
{% endcontent-ref %}

To start querying data in Pinot, check out our Query guide:

{% content-ref url="users/user-guide-query/" %}
[user-guide-query](users/user-guide-query/)
{% endcontent-ref %}

## Learn

For a conceptual overview that explains how Pinot works, check out the Concepts guide:

{% content-ref url="basics/concepts/" %}
[concepts](basics/concepts/)
{% endcontent-ref %}

To understand the distributed systems architecture that explains Pinot's operating model, take a look at our basic architecture section:

{% content-ref url="basics/architecture.md" %}
[architecture.md](basics/architecture.md)
{% endcontent-ref %}

To understand how Pinot accelerates queries, explore the indexing documentation:

{% content-ref url="basics/indexing/README.md" %}
[README.md](basics/indexing/README.md)
{% endcontent-ref %}

## Build applications on Pinot

To query Pinot from applications and BI tools, start with the user-facing guides:

{% content-ref url="users/user-guide-query/" %}
[user-guide-query](users/user-guide-query/)
{% endcontent-ref %}

{% content-ref url="users/api/" %}
[README.md](users/api/)
{% endcontent-ref %}

{% content-ref url="users/clients/" %}
[README.md](users/clients/)
{% endcontent-ref %}

## Operate Pinot in production

To run Pinot reliably in production, use the operator guides and troubleshooting reference:

{% content-ref url="operators/operating-pinot/" %}
[README.md](operators/operating-pinot/)
{% endcontent-ref %}

{% content-ref url="reference/troubleshooting/" %}
[README.md](reference/troubleshooting/)
{% endcontent-ref %}

## Extend and contribute

If you are extending Pinot or contributing back to the project, start here:

{% content-ref url="developers/developers-and-contributors/" %}
[README.md](developers/developers-and-contributors/)
{% endcontent-ref %}

{% content-ref url="developers/plugin-architecture/" %}
[README.md](developers/plugin-architecture/)
{% endcontent-ref %}

{% content-ref url="contributing/contributing.md" %}
[contributing.md](contributing/contributing.md)
{% endcontent-ref %}
