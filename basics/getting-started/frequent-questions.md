---
description: >-
  This page has a collection of frequently asked questions with answers from the
  community.
---

# Frequently Asked Questions \(FAQs\)

{% hint style="info" %}
This is a list of frequent questions most often asked in our troubleshooting channel on Slack. Feel free to contribute your questions and answers here and make a pull request.
{% endhint %}

## Ingestion

### Flatten my JSON Kafka stream

We have [json\_format\(field\)](https://docs.pinot.apache.org/developers/advanced/ingestion-level-transformations#json-functions) function which can store a top level json field as a STRING in Pinot.

Then you can use these [json functions](https://docs.pinot.apache.org/users/user-guide-query/supported-transformations#json-functions) during query time, to extract fields from the json string.

{% hint style="warning" %}
**NOTE**  
This works well if some of your fields are nested json, but most of your fields are top level json keys. If all of your fields are within a nested JSON key, you will have to store the entire payload as 1 column, which is not ideal.  
  
Support for flattening during ingestion is on the roadmap: [https://github.com/apache/pinot/issues/5264](https://github.com/apache/pinot/issues/5264)
{% endhint %}

## Indexing

### Set inverted indexes

Inverted indexes are set in the tableConfig's tableIndexConfig -&gt; invertedIndexColumns list. Here's the documentation for tableIndexConfig: [https://docs.pinot.apache.org/basics/components/table\#tableindexconfig-1](https://docs.pinot.apache.org/basics/components/table#tableindexconfig-1) along with a sample table that has set inverted indexes on some columns.

Applying inverted indexes to a table config will generate inverted index to all new segments. In order to apply the inverted indexes to all existing segments, follow steps in [How to apply inverted index to existing setup?](frequent-questions.md#how-to-apply-inverted-index-to-existing-setup)

### Apply inverted index to existing setup

1. Add the columns you wish to index to the tableIndexConfig-&gt; invertedIndexColumns list. This sample table config show inverted indexes set: [https://docs.pinot.apache.org/basics/components/table\#offline-table-config ](https://docs.pinot.apache.org/basics/components/table#offline-table-config)To update the table config use the Pinot Swagger API: [http://localhost:9000/help\#!/Table/updateTableConfig](http://localhost:9000/help#!/Table/updateTableConfig)
2. Invoke the reload API: [http://localhost:9000/help\#!/Segment/reloadAllSegments](http://localhost:9000/help#!/Segment/reloadAllSegments)

This will trigger a reload operation on each of the servers hosting the table's segments.
The API response has a reloadJobId which can be used to monitor the status of the reload operation using the segment reload status API: [http://localhost:18998/help#/Segment/getReloadJobStatus](http://localhost:18998/help#/Segment/getReloadJobStatus)

### Create star-tree indexes

Star-tree indexes are configured in the table config under the _tableIndexConfig_ -&gt; _starTreeIndexConfigs_ \(list\) and _enableDefaultStarTree_ \(boolean\). Read more about how to configure star-tree indexes: [https://docs.pinot.apache.org/basics/features/indexing\#index-generation-configuration](https://docs.pinot.apache.org/basics/features/indexing#index-generation-configuration)

The new segments will have star-tree indexes generated after applying the star-tree index configs to the table config. Currently Pinot does not support adding star-tree indexes to the existing segments.

## Querying

### What are all the fields in the Pinot query's JSON response?

Here's the page explaining the Pinot response format: [https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format](https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format)

### SQL Query fails with "Encountered 'timestamp' was expecting one of..."

"timestamp" is a reserved keyword in SQL. Escape timestamp with double quotes. 

```text
select "timestamp" from myTable
```

Other commonly encountered reserved keywords are date, time, table.

### Filtering on STRING column WHERE column = "foo" does not work?

For filtering on STRING columns, use single quotes

```text
SELECT COUNT(*) from myTable WHERE column = 'foo'
```

### ORDER BY using an alias doesn't work?

The fields in the `ORDER BY` clause must be one of the group by clauses or aggregations, _**BEFORE**_ applying the alias. Therefore, this will not work

```text
SELECT count(colA) as aliasA, colA from tableA GROUP BY colA ORDER BY aliasA
```

Instead, this will work

```text
SELECT count(colA) as sumA, colA from tableA GROUP BY colA ORDER BY count(colA)
```

### Does pagination work in GROUP BY queries?

No. Pagination only works for SELECTION queries

## Operations

### Can I change a column name in my table, without losing data?

### How to change number of replicas of a table?

You can change the number of replicas by updating the table config's [segmentsConfig](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1) section. Make sure you have at least as many servers as the replication.

For OFFLINE table, update [replication](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1)

```text
{ 
    "tableName": "pinotTable", 
    "tableType": "OFFLINE", 
    "segmentsConfig": {
      "replication": "3", 
      ... 
    }
    ..
```

For REALTIME table update [replicasPerPartition](https://docs.pinot.apache.org/basics/components/table#segmentsconfig)

```text
{ 
    "tableName": "pinotTable", 
    "tableType": "REALTIME", 
    "segmentsConfig": {
      "replicasPerPartition": "3", 
      ... 
    }
    ..
```

After changing the replication, run a [table rebalance](frequent-questions.md#how-to-run-a-rebalance-on-a-table). 

### How to run a rebalance on a table?

Refer to [Rebalance](../../operators/operating-pinot/rebalance/).

### How to control number of segments generated?

The number of segments generated depends on the number of input files. If you provide only 1 input file, you will get 1 segment. If you break up the input file into multiple files, you will get as many segments as the input files. 

## Tuning and Optimizations

### Do replica groups work for real-time? <a id="docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3"></a>

Yes, replica groups work for real-time. There's 2 parts to enabling replica groups:

1. Replica groups segment assignment
2. Replica group query routing

**Replica group segment assignment**

Replica group segment assignment is achieved in real time, if number of servers is a multiple of number of replicas. The partitions get uniformly sprayed across the servers, creating replica groups.  
  
For example, consider we have 6 partitions, 2 replicas, and 4 servers.

|  | r1 | r2 |
| :--- | :--- | :--- |
| p1 | S0 | S1 |
| p2 | S2 | S3 |
| p3 | S0 | S1 |
| p4 | S2 | S3 |
| p5 | S0 | S1 |
| p6 | S2 | S3 |

As you can see, the set \(S0, S2\) contains r1 of every partition, and \(s1, S3\) contains r2 of every partition. The query will only be routed to one of the sets, and not span every server.  
If you are are adding/removing servers from an existing table setup, you have to run [rebalance](frequent-questions.md#how-to-run-a-rebalance-on-a-table) for segment assignment changes to take effect.

**Replica group query routing**

Once replica group segment assignment is in effect, the query routing can take advantage of it. For replica group based query routing, set the following in the table config's [routing](https://docs.pinot.apache.org/basics/components/table#routing) section, and then restart brokers

```text
{
    "tableName": "pinotTable", 
    "tableType": "REALTIME",
    "routing": {
        "instanceSelectorType": "replicaGroup"
    }
    ..
}
```

## Handling time in Pinot

### **How does Pinot’s real-time ingestion handle out-of-order events?**

Pinot does not require ordering of event time stamps. Out of order events are still consumed and indexed into the "currently consuming" segment. In a pathological case, if you have a 2 day old event come in "now", it will still be stored in the segment that is open for consumption "now". There is no strict time-based partitioning for segments, but star-indexes and hybrid tables will handle this as appropriate.

See the [Components &gt; Broker](https://docs.pinot.apache.org/basics/components/broker) for more details about how hybrid tables handle this. Specifically, the time-boundary is computed as `max(OfflineTIme) - 1 unit of granularity`. Pinot does store the min-max time for each segment and uses it for pruning segments, so segments with multiple time intervals may not be perfectly pruned.

When generating star-indexes, the time column will be part of the star-tree so the tree can still be efficiently queried for segments with multiple time intervals.

### **What is the purpose of a hybrid table not using `max(OfflineTime)` to determine the time-boundary, and instead using an offset?**

This lets you have an old event up come in without building complex offline pipelines that perfectly partition your events by event timestamps. With this offset, even if your offline data pipeline produces segments with a maximum timestamp, Pinot will not use the offline dataset for that last chunk of segments. The expectation is if you process offline the next time-range of data, your data pipeline will include any late events.

### **Why are segments not strictly time-partitioned?**

It might seem odd that segments are not strictly time-partitioned, unlike similar systems such as Apache Druid. This allows real-time ingestion to consume out-of-order events. Even though segments are not strictly time-partitioned, Pinot will still index, prune, and query segments intelligently by time-intervals to for performance of hybrid tables and time-filtered data.

When generating offline segments, the segments generated such that segments only contain one time-interval and are well partitioned by the time column.

