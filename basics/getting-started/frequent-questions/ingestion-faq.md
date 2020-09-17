# Ingestion FAQ

## Data processing

### How do I partition data, when using Kafka stream?

### How do I store BYTES column in JSON data?

### How do I flatten my JSON Kafka stream?

We have [json\_format\(field\)](https://docs.pinot.apache.org/developers/advanced/ingestion-level-transformations#json-functions) function which can store a top level json field as a STRING in Pinot.

Then you can use these [json functions](https://docs.pinot.apache.org/users/user-guide-query/supported-transformations#json-functions) during query time, to extract fields from the json string.

{% hint style="warning" %}
**NOTE**  
This works well if some of your fields are nested json, but most of your fields are top level json keys. If all of your fields are within a nested JSON key, you will have to store the entire payload as 1 column, which is not ideal.  
  
Support for flattening during ingestion is on the roadmap: [https://github.com/apache/incubator-pinot/issues/5264](https://github.com/apache/incubator-pinot/issues/5264)
{% endhint %}

## Indexing

### How to set inverted indexes?

Inverted indexes are set in the tableConfig's tableIndexConfig -&gt; invertedIndexColumns list. Here's the documentation for tableIndexConfig: [https://docs.pinot.apache.org/basics/components/table\#tableindexconfig-1](https://docs.pinot.apache.org/basics/components/table#tableindexconfig-1) along with a sample table that has set inverted indexes on some columns.

Applying inverted indexes to a table config will generate inverted index to all new segments. In order to apply the inverted indexes to all existing segments, follow steps in [How to apply inverted index to existing setup?](./#how-to-apply-inverted-index-to-existing-setup)

### How to apply inverted index to existing setup?

1. Add the columns you wish to index to the tableIndexConfig-&gt; invertedIndexColumns list. This sample table config show inverted indexes set: [https://docs.pinot.apache.org/basics/components/table\#offline-table-config ](https://docs.pinot.apache.org/basics/components/table#offline-table-config)To update the table config use the Pinot Swagger API: [http://localhost:9000/help\#!/Table/updateTableConfig](http://localhost:9000/help#!/Table/updateTableConfig)
2. Invoke the reload API: [http://localhost:9000/help\#!/Segment/reloadAllSegments](http://localhost:9000/help#!/Segment/reloadAllSegments)

Right now, there’s no easy way to confirm that reload succeeded. One way it to check out the index\_map file inside the segment metadata, you should see inverted index entries for the new columns. An API for this is coming soon: [https://github.com/apache/incubator-pinot/issues/5390](https://github.com/apache/incubator-pinot/issues/5390)

### How to create star-tree indexes?

Star-tree indexes are configured in the table config under the _tableIndexConfig_ -&gt; _starTreeIndexConfigs_ \(list\) and _enableDefaultStarTree_ \(boolean\). Read more about how to configure star-tree indexes: [https://docs.pinot.apache.org/basics/features/indexing\#index-generation-configuration](https://docs.pinot.apache.org/basics/features/indexing#index-generation-configuration)

The new segments will have star-tree indexes generated after applying the star-tree index configs to the table config. Currently Pinot does not support adding star-tree indexes to the existing segments.

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

