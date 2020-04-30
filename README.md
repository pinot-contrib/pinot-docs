---
description: A simple introduction to Apache Pinot
---

# Introduction

## What is Pinot?

Pinot is a real-time distributed OLAP datastore, built to deliver scalable real time analytics with low latency. It can ingest data from batch data sources \(such as Hadoop HDFS, Amazon S3, Azure ADLS, Google Cloud Storage\) as well as stream data sources \(such as Apache Kafka\). Pinot is designed to scale horizontally, so that it can scale to larger data sets and higher query rates as needed.

![](.gitbook/assets/pinot-introduction-2.svg)

## Who uses Pinot in production?

<table>
  <thead>
    <tr>
      <th style="text-align:left">Company</th>
      <th style="text-align:left">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">LinkedIn</td>
      <td style="text-align:left">
        <p>Pinot originated at LinkedIn and it powers more 50+ user facing applications
          such as Who Viewed My Profile, Talent Analytics, Company Analytics, Ad
          Analytics and many more. Pinot also serves as the backend for to visualize
          and monitor 10,000+ business metrics.</p>
        <p>Pinot runs on 1000+ nodes serving 100k+ queries while ingesting 1.5M+
          events per second.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">Uber</td>
      <td style="text-align:left">Pinot powers many internal and external dashboards as well as external
        site facing analytics applications like <a href="https://eng.uber.com/restaurant-manager/">UberEats Restaurant Analytics</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">Microsoft</td>
      <td style="text-align:left">Microsoft Teams uses Pinot for analytics on Teams product usage data.</td>
    </tr>
    <tr>
      <td style="text-align:left">Weibo</td>
      <td style="text-align:left">Weibo uses Pinot for realtime analytics on CDN &amp; Weibo Video data
        to make business decisions, optimize service performance and improve user
        experience.</td>
    </tr>
    <tr>
      <td style="text-align:left">Factual</td>
      <td style="text-align:left">Insight Product - <a href="https://www.factual.com/products/insights/">https://www.factual.com/products/insights/</a>
      </td>
    </tr>
  </tbody>
</table>## Features of Pinot

* A column-oriented database with various compression schemes such as Run Length, Fixed Bit Length
* Pluggable indexing technologies - Sorted Index, Bitmap Index, Inverted Index
* Ability to optimize query/execution plan based on query and segment metadata
* Near real time ingestion from streams and batch ingestion from Hadoop
* SQL-like language that supports selection, aggregation, filtering, group by, order by, distinct queries on data
* Support for multi-valued fields
* Horizontally scalable and fault-tolerant

## When should I use it?

Pinot is designed to execute OLAP queries with low latency. It is suited in contexts where fast analytics, such as aggregations, are needed on immutable data, possibly, with real-time data ingestion.

**User facing Analytics Products**

Pinot was originally built at LinkedIn to power rich interactive real-time analytic applications such as [Who Viewed Profile](https://www.linkedin.com/me/profile-views/urn:li:wvmp:summary/),  [Company Analytics](https://www.linkedin.com/company/linkedin/insights/),  [Talent Insights](https://business.linkedin.com/talent-solutions/talent-insights), and many more. [UberEats Restaurant Manager](https://eng.uber.com/restaurant-manager/) is another example of a customer facing Analytics App. At LinkedIn, Pinot powers 50+ user-facing products, ingesting _**millions of events per second**_ and serving **100k+ queries per second** at millisecond latency.

**Real-time Dashboard for Business Metrics**

Pinot can be also be used to perform typical analytical operations such as **slice** and **dice**, **drill down**, **roll up**, and **pivot** on large scale multi-dimensional data. For instance, at LinkedIn, Pinot powers dashboards for thousands of business metrics. One can connect various BI tools such Superset, Tableau, or PowerBI to visualize data in Pinot. 

Instructions to connect Pinot with Superset can found [here](integrations/superset.md).

**Anomaly Detection** 

In addition to visualizing data in Pinot, one can run Machine Learning Algorithms to detect Anomalies on the data stored in Pinot. See [ThirdEye](integrations/thirdeye.md) for more information on how to use Pinot for Anomaly Detection and Root Cause Analysis.

## When should I not use it?

Pinot is not a replacement for your database, nor a search engine. It addresses fast analytics on immutable data and it not designed to perform data updates or deletions. Joins are currently not supported, but this problem can be overcome by using PrestoDB for querying Pinot \([https://prestodb.io/](https://prestodb.io/)\).  
  
For more information about PrestoDB connector for Pinot see [https://github.com/apache/incubator-pinot/tree/master/kubernetes/examples/helm\#access-pinot-using-presto](https://github.com/apache/incubator-pinot/tree/master/kubernetes/examples/helm#access-pinot-using-presto)  
introduced in [https://github.com/prestodb/presto/pull/13504](https://github.com/prestodb/presto/pull/13504)

## Quick example

Pinot works very well for querying time series data with many dimensions and metrics. Filters and aggregations are both easy and fast.

```sql
SELECT sum(clicks), sum(impressions) FROM AdAnalyticsTable
  WHERE 
       ((daysSinceEpoch >= 17849 AND daysSinceEpoch <= 17856)) AND 
       accountId IN (123456789)
  GROUP BY 
       daysSinceEpoch TOP 100
```

## Who uses Pinot?

Pinot powers several big players, including LinkedIn, Uber, Factual, Weibo, Slack and more.

## Tutorial

If you want to learn how to run Pinot, start here:

{% page-ref page="basics/getting-started/" %}

If you prefer some concepts and tutorials first:

## Installation

Pinot may be deployed to and operated on a cloud provider or a local or virtual machine. You may get started either with a bare-metal installation or a Kubernetes one \(either locally or in the cloud\). To get immediately started with Pinot, check out these quick-start guides. 

{% page-ref page="basics/getting-started/running-pinot-in-docker.md" %}

{% page-ref page="basics/getting-started/quickstart/" %}



