---
description: >-
  This page has a collection of frequently asked questions about ingestion with answers from the
  community.
---

# Ingestion FAQ

{% hint style="info" %}
This is a list of questions frequently asked in our troubleshooting channel on Slack. To contribute additional questions and answers, [make a pull request](https://docs.pinot.apache.org/contributing/contributing).
{% endhint %}

## Data processing

### What is a good segment size?

While Apache Pinot can work with segments of various sizes, for optimal use of Pinot, you want to get your segments sized in the 100MB to 500MB (un-tarred/uncompressed) range. Having too many (thousands or more) tiny segments for a single table creates overhead in terms of the metadata storage in Zookeeper as well as in the Pinot servers' heap. At the same time, having too few really large (GBs) segments reduces parallelism of query execution, as on the server side, the thread parallelism of query execution is at segment level.

### Can multiple Pinot tables consume from the same Kafka topic?

Yes. Each table can be independently configured to consume from any given Kafka topic, regardless of whether there are other tables that are also consuming from the same Kafka topic.

### If I add a partition to a Kafka topic, will Pinot automatically ingest data from this partition?

Pinot automatically detects new partitions in Kafka topics. It checks for new partitions whenever `RealtimeSegmentValidationManager` periodic job runs and starts consumers for new partitions.

You can configure the interval for this job using the`controller.realtime.segment.validation.frequencyPeriod` property in the controller configuration.

### How do I enable partitioning in Pinot, when using Kafka stream?

Set up partitioner in the Kafka producer: [https://docs.confluent.io/current/clients/producer.html](https://docs.confluent.io/current/clients/producer.html)

The partitioning logic in the stream should match the partitioning config in Pinot. Kafka uses `murmur2`, and the equivalent in Pinot is the `Murmur` function.

Set the partitioning configuration as below using same column used in Kafka:

```json
"tableIndexConfig": {
      ..
      "segmentPartitionConfig": {
        "columnPartitionMap": {
          "column_foo": {
            "functionName": "Murmur",
            "numPartitions": 12 // same as number of kafka partitions
          }
        }
      }
```

and also set:

```json
"routing": {
      "segmentPrunerTypes": ["partition"]
    }
```

To learn how partition works, see [routing tuning](operators/operating-pinot/tuning/routing.md).

### How do I store BYTES column in JSON data?

For JSON, you can use a hex encoded string to ingest BYTES.

### How do I flatten my JSON Kafka stream?

See the [json\_format(field)](https://docs.pinot.apache.org/developers/advanced/ingestion-level-transformations#json-functions) function which can store a top level json field as a STRING in Pinot.

Then you can use these [json functions](https://docs.pinot.apache.org/users/user-guide-query/supported-transformations#json-functions) during query time, to extract fields from the json string.

{% hint style="warning" %}
**NOTE**\
This works well if some of your fields are nested json, but most of your fields are top level json keys. If all of your fields are within a nested JSON key, you will have to store the entire payload as 1 column, which is not ideal.
{% endhint %}

### How do I escape Unicode in my Job Spec YAML file?

To use explicit code points, you must double-quote (not single-quote) the string, and escape the code point via "\uHHHH", where HHHH is the four digit hex code for the character. See [https://yaml.org/spec/spec.html#escaping/in%20double-quoted%20scalars/](https://yaml.org/spec/spec.html#escaping/in%20double-quoted%20scalars/) for more details.

### Is there a limit on the maximum length of a string column in Pinot?

By default, Pinot limits the length of a String column to 512 bytes. If you want to overwrite this value, you can set the maxLength attribute in the schema as follows:

```json
    {
      "dataType": "STRING",
      "maxLength": 1000,
      "name": "textDim1"
    },
```

### When are new events queryable when getting ingested into a real-time table?

Events are available to queries as soon as they are ingested. This is because events are instantly indexed in memory upon ingestion.

The ingestion of events into the real-time table is not transactional, so replicas of the open segment are not immediately consistent. Pinot trades consistency for availability upon network partitioning (CAP theorem) to provide ultra-low ingestion latencies at high throughput.

However, when the open segment is closed and its in-memory indexes are flushed to persistent storage, all its replicas are guaranteed to be consistent, with the [commit protocol](https://docs.pinot.apache.org/operators/operating-pinot/decoupling-controller-from-the-data-path).

### How to reset a CONSUMING segment stuck on an offset which has expired from the stream?

This typically happens if:

1. The consumer is lagging a lot.
2. The consumer was down (server down, cluster down), and the stream moved on, resulting in offset not found when consumer comes back up.

In case of Kafka, to recover, set property `"auto.offset.reset":"earliest"` in the `streamConfigs` section and reset the `CONSUMING` segment. See [Real-time table configs](https://docs.pinot.apache.org/configuration-reference/table#indexing-config) for more details about the configuration.

You can also also use the "Resume Consumption" endpoint with "resumeFrom" parameter set to "smallest" (or "largest" if you want). See [Pause Stream Ingestion](https://docs.pinot.apache.org/basics/data-import/pinot-stream-ingestion#pause-stream-ingestion) for more details.

## Indexing

### How to set inverted indexes?

Inverted indexes are set in the `tableConfig`'s `tableIndexConfig` -> `invertedIndexColumns` list. For more info on table configuration, see [Table Config Reference](../../../configuration-reference/table.md). For an example showing how to configure an inverted index, see [Inverted Index](../../indexing/inverted-index.md).

Applying inverted indexes to a table configuration will generate an inverted index for all new segments. To apply the inverted indexes to all existing segments, see [How to apply an inverted index to existing segments?](ingestion-faq.md#how-to-apply-an-inverted-index-to-existing-segments)

### How to apply an inverted index to existing segments?

1. Add the columns you wish to index to the `tableIndexConfig`-> `invertedIndexColumns` list. To update the table configuration use the Pinot Swagger API: [http://localhost:9000/help#!/Table/updateTableConfig](http://localhost:9000/help#!/Table/updateTableConfig).
2. Invoke the reload API: [http://localhost:9000/help#!/Segment/reloadAllSegments](http://localhost:9000/help#!/Segment/reloadAllSegments).

Once you've done that, you can check whether the index has been applied by querying the segment metadata API at [http://localhost:9000/help#/Segment/getServerMetadata](http://localhost:9000/help#/Segment/getServerMetadata). Don't forget to include the names of the column on which you have applied the index.

The output from this API should look something like the following:

```json
{
  "<segment-name>": {
    "segmentName": "<segment-name>",
    "indexes": {
      "<columnName>": {
        "bloom-filter": "NO",
        "dictionary": "YES",
        "forward-index": "YES",
        "inverted-index": "YES",
        "null-value-vector-reader": "NO",
        "range-index": "NO",
        "json-index": "NO"
      }
    }
  }
}
```

### Can I retrospectively add an index to any segment?

Not all indexes can be retrospectively applied to existing segments.

If you want to add or change the [sorted index column](../../indexing/inverted-index.md#sorted-inverted-index) or adjust [the dictionary encoding of the default forward index](../../indexing/forward-index.md#raw-value-forward-index) you will need to manually re-load any existing segments.

### How to create star-tree indexes?

Star-tree indexes are configured in the table config under the `tableIndexConfig` -> `starTreeIndexConfigs` (list) and `enableDefaultStarTree` (boolean). See here for more about how to configure star-tree indexes: [https://docs.pinot.apache.org/basics/indexing/star-tree-index#index-generation](https://docs.pinot.apache.org/basics/indexing/star-tree-index#index-generation)

The new segments will have star-tree indexes generated after applying the star-tree index configurations to the table configuration. Currently, Pinot does not support adding star-tree indexes to the existing segments.

## Handling time in Pinot

### **How does Pinot’s real-time ingestion handle out-of-order events?**

Pinot does not require ordering of event time stamps. Out of order events are still consumed and indexed into the "currently consuming" segment. In a pathological case, if you have a 2 day old event come in "now", it will still be stored in the segment that is open for consumption "now". There is no strict time-based partitioning for segments, but star-indexes and hybrid tables will handle this as appropriate.

See the [Components > Broker](https://docs.pinot.apache.org/basics/components/broker) for more details about how hybrid tables handle this. Specifically, the time-boundary is computed as `max(OfflineTIme) - 1 unit of granularity`. Pinot does store the min-max time for each segment and uses it for pruning segments, so segments with multiple time intervals may not be perfectly pruned.

When generating star-indexes, the time column will be part of the star-tree so the tree can still be efficiently queried for segments with multiple time intervals.

### What is the purpose of a hybrid table not using `max(OfflineTime)` to determine the time-boundary, and instead using an offset?

This lets you have an old event up come in without building complex offline pipelines that perfectly partition your events by event timestamps. With this offset, even if your offline data pipeline produces segments with a maximum timestamp, Pinot will not use the offline dataset for that last chunk of segments. The expectation is if you process offline the next time-range of data, your data pipeline will include any late events.

### Why are segments not strictly time-partitioned?

It might seem odd that segments are not strictly time-partitioned, unlike similar systems such as Apache Druid. This allows real-time ingestion to consume out-of-order events. Even though segments are not strictly time-partitioned, Pinot will still index, prune, and query segments intelligently by time intervals for the performance of hybrid tables and time-filtered data.

When generating offline segments, the segments generated such that segments only contain one time interval and are well partitioned by the time column.
