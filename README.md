---
description: A simple introduction to Apache Pinot
---

# Introduction

## What is Pinot?

Pinot is a real-time distributed OLAP datastore, built to deliver scalable real time analytics with low latency. It can ingest data from batch data sources \(such as Hadoop HDFS, Amazon S3, Azure ADLS, Google Cloud Storage\) as well as stream data sources \(such as Apache Kafka\). Pinot is designed to scale horizontally, so that it can scale to larger data sets and higher query rates as needed.

![](.gitbook/assets/pinot-introduction-2.svg)

## Features of Pinot

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

{% page-ref page="powered-by-pinot-1/powered-by-pinot.md" %}

## Tutorial

If you want to learn how to run Pinot, start here:

{% page-ref page="getting-started/" %}

If you prefer some concepts and tutorials first:

{% page-ref page="concepts/" %}

## Installation

Pinot may be deployed to and operated on a cloud provider or a local or virtual machine. You may get started either with a bare-metal installation or a Kubernetes one \(either locally or in the cloud\). To get immediately started with Pinot, check out these quick-start guides. 

{% page-ref page="getting-started/running-pinot-in-docker.md" %}

{% page-ref page="getting-started/quickstart/" %}



