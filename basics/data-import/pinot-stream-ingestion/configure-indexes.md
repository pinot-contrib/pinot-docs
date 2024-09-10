# Configure indexes

Learn how to apply indexes to a Pinot table. This guide assumes that you have followed the [Ingest data from Apache Kafka](import-from-apache-kafka.md) guide.

Pinot supports a series of different indexes that can be used to optimize query performance. In this guide, we'll learn how to add indexes to the `events` table that we set up in the [Ingest data from Apache Kafka](import-from-apache-kafka.md) guide.

### Why do we need indexes?

If no indexes are applied to the columns in a Pinot segment, the query engine needs to scan through every document, checking whether that document meets the filter criteria provided in a query. This can be a slow process if there are a lot of documents to scan.

When indexes are applied, the query engine can more quickly work out which documents satisfy the filter criteria, reducing the time it takes to execute the query.

### What indexes does Pinot support?

By default, Pinot creates a forward index for every column. The forward index generally stores documents in insertion order.

However, before flushing the segment, Pinot does a single pass over every column to see whether the data is sorted. If data is sorted, Pinot creates a sorted (forward) index for that column instead of the forward index.

For real-time tables you can also explicitly tell Pinot that one of the columns should be sorted. For more details, see the \[Sorted Index Documentation]\(https://docs.pinot.apache.org/basics/indexing/forward-index#real-time-tables).

For filtering documents within a segment, Pinot supports the following indexing techniques:

* Inverted index: Used for exact lookups.
* Range index - Used for range queries.
* Text index - Used for phrase, term, boolean, prefix, or regex queries.
* Geospatial index - Based on H3, a hexagon-based hierarchical gridding. Used for finding points that exist within a certain distance from another point.
* JSON index - Used for querying columns in JSON documents.
* Star-Tree index - Pre-aggregates results across multiple columns.

## View events table

Let's see how we can apply these indexing techniques to our data. To recap, the `events` table has the following fields:

| Date Time Fields | Dimensions Fields | Metric Fields |
| ---------------- | ----------------- | ------------- |
| `ts`             | `uuid`            | `count`       |

We might want to write queries that filter on the `ts` and `uuid` columns, so these are the columns on which we would want to configure indexes.

Since the data we're ingesting into the Kafka topic is all implicitly ordered by timestamp, this means that the `ts` column already has a sorted index. This means that any queries that filter on this column are already optimised.

So that leaves us with the `uuid` column.

## Add an inverted index

We're going to add an inverted index to the `uuid` column so that queries that filter on that column will return quicker. We need to add the following line:

```json
"invertedIndexColumns": ["uuid"]
```

To the `tableIndexConfig` section.

Copy the following to the clipboard:

**/tmp/pinot/table-config-stream.json**

```json
{
  "tableName": "events",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "ts",
    "schemaName": "events",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "invertedIndexColumns": ["uuid"],
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "lowlevel",
      "stream.kafka.topic.name": "events",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
      "stream.kafka.broker.list": "kafka:9092",
      "realtime.segment.flush.threshold.rows": "0",
      "realtime.segment.flush.threshold.time": "24h",
      "realtime.segment.flush.threshold.segment.size": "50M",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

Navigate to [localhost:9000/#/tenants/table/events\_REALTIME](http://localhost:9000/#/tenants/table/events\_REALTIME), click on **Edit Table**, paste the next table config, and then click **Save**.

Once you've done that, you'll need to click **Reload All Segments** and then **Yes** to apply the indexing change to all segments.

## Check the index has been applied

We can check that the index has been applied to all our segments by querying Pinot's REST API. You can find Swagger documentation at [localhost:9000/help](http://localhost:9000/help).

The following query will return the indexes defined on the `uuid` column:

```bash
curl -X GET "http://localhost:9000/segments/events/metadata?columns=uuid" \
  -H "accept: application/json" 2>/dev/null | 
  jq '.[] | [.segmentName, .indexes]'
```

**Output**

We're using the [jq command line JSON processor](https://stedolan.github.io/jq/) to extract the fields that we're interested in.

```json
[
  "events__0__1__20220214T1106Z",
  {
    "uuid": {
      "bloom-filter": "NO",
      "dictionary": "YES",
      "forward-index": "YES",
      "inverted-index": "YES",
      "null-value-vector-reader": "NO",
      "range-index": "NO",
      "json-index": "NO"
    }
  }
]
[
  "events__0__0__20220214T1053Z",
  {
    "uuid": {
      "bloom-filter": "NO",
      "dictionary": "YES",
      "forward-index": "YES",
      "inverted-index": "YES",
      "null-value-vector-reader": "NO",
      "range-index": "NO",
      "json-index": "NO"
    }
  }
]
```

We can see from looking at the `inverted-index` property that the index has been applied.

## Querying

You can now run some queries that filter on the `uuid` column, as shown below:

```sql
SELECT * 
FROM events 
WHERE uuid = 'f4a4f'
LIMIT 10
```

You'll need to change the actual `uuid` value to a value that exists in your database, because the UUIDs are generated randomly by our script.
