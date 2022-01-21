---
description: Upsert support in Apache Pinot.
---

# Stream Ingestion with Upsert

Pinot provides native support of upsert during the real-time ingestion (v0.6.0+). There are scenarios that the records need modifications, such as correcting a ride fare and updating a delivery status.

With the foundation of full upsert support in Pinot, another category of use cases on partial upsert are enabled (v0.8.0+). Partial upsert is convenient to users so that they only need to specify the columns whose value changes, and ignore the others.

To enable upsert on a Pinot table, there are a couple of configurations to make on the table configurations as well as on the input stream.

## Define the primary key in the schema

To update a record, a primary key is needed to uniquely identify the record. To define a primary key, add the field `primaryKeyColumns` to the schema definition. For example, the schema definition of `UpsertMeetupRSVP` in the quick start example has this definition.

{% code title="upsert_meetupRsvp_schema.json" %}
```javascript
{
    "primaryKeyColumns": ["event_id"]
}
```
{% endcode %}

Note this field expects a list of columns, as the primary key can be composite.

When two records of the same primary key are ingested, _the record with the greater event time (as defined by the time column) is used_. When records with the same primary key and event time, then the order is not determined. In most cases, the later ingested record will be used, but may not be so in the cases when the table has a column to sort by.

## Partition the input stream by the primary key

An important requirement for the Pinot upsert table is to partition the input stream by the primary key. For Kafka messages, this means the producer shall set the key in the [`send`](https://kafka.apache.org/20/javadoc/index.html?org/apache/kafka/clients/producer/KafkaProducer.html) API. If the original stream is not partitioned, then a streaming processing job (e.g. Flink) is needed to shuffle and repartition the input stream into a partitioned one for Pinot's ingestion.

## Enable upsert in the table configurations

There are a few configurations needed in the table configurations to enable upsert.

### Upsert mode

For append-only tables, the upsert mode defaults to `NONE`. To enable the full upsert, set the `mode` to `FULL` for the full update. For example:

{% code title="upsert mode: full" %}
```javascript
{
  "upsertConfig": {
    "mode": "FULL"
  }
}
```
{% endcode %}

Pinot also added the partial update support in v0.8.0+. To enable the partial upsert, set the `mode` to `PARTIAL` and specify `partialUpsertStrategies` for partial upsert columns. Since v0.10.0, `defaultPartialUpsertStrategy` is introduced as the default merge strategy for columns without specified strategy. For example:

{% code title="upsert mode: partial (v0.8.0)" %}
```javascript
{
  "upsertConfig": {
    "mode": "PARTIAL",
    "partialUpsertStrategies":{
      "rsvp_count": "INCREMENT",
      "group_name": "UNION",
      "venue_name": "APPEND"
    }
  }
}
```

{% code title="upsert mode: partial (v0.10.0+)" %}
```javascript
{
  "upsertConfig": {
    "mode": "PARTIAL",
    "defaultPartialUpsertStrategy": "OVERWRITE",
    "partialUpsertStrategies":{
      "rsvp_count": "INCREMENT",
      "group_name": "UNION",
      "venue_name": "APPEND"
    }
  }
}
```
{% endcode %}

Pinot supports the following partial upsert strategies -

| Strategy  | Description                                               |
| --------- | --------------------------------------------------------- |
| OVERWRITE | Overwrite the column of the last record                   |
| INCREMENT | Add the new value to the existing values                  |
| APPEND    | Add the new item to the Pinot unordered set               |
| UNION     | Add the new item to the Pinot unordered set if not exists |
| IGNORE    | Ignore the new value, keep the existing value (v0.10.0+)  |

{% hint style="info" %}
**Note**: If you don't specify any strategy for a given column, by default the value will always be overwritten by the new value for that column. In v0.10.0+, we added support for defaultPartialUpsertStrategy. The default value of defaultPartialUpsertStrategy is OVERWRITE.
{% endhint %}

### Comparison Column

By default, Pinot uses the value in the time column to determine the latest record. That means, for two records with the same primary key, the record with the larger value of the time column is picked as the latest update. However, there are cases when users need to use another column to determine the order. In such case, you can use option `comparisonColumn` to override the column used for comparison. For example,

{% code title="comparison column" %}
```
```
{% endcode %}

```javascript
{
  "upsertConfig": {
    "mode": "FULL",
    "comparisonColumn": "anotherTimeColumn",
    "hashFunction": "NONE"
  }
}
```

For partial upsert table, the out-of-order events won't be consumed and indexed. For example, for two records with the same primary key, if the record with the smaller value of the comparison column came later than the other record, it will be skipped. 

### Use strictReplicaGroup for routing

The upsert Pinot table can use only the low-level consumer for the input streams. As a result, it uses the [partitioned replica-group assignment](../../operators/operating-pinot/segment-assignment.md#partitioned-replica-group-segment-assignment) for the segments. Moreover,upsert poses the additional requirement that all segments of the same partition must be served from the same server to ensure the data consistency across the segments. Accordingly, it requires to use `strictReplicaGroup` as the routing strategy. To use that, configure `instanceSelectorType` in `Routing` as the following:

{% code title="routing" %}
```javascript
{
  "routing": {
    "instanceSelectorType": "strictReplicaGroup"
  }
}
```
{% endcode %}

### Limitations

There are some limitations for the upsert Pinot tables.

First, the high-level consumer is not allowed for the input stream ingestion, which means `stream.kafka.consumer.type` must be `lowLevel`.

Second, the star-tree index cannot be used for indexing, as the star-tree index performs pre-aggregation during the ingestion.

Third, unlike append-only tables, out-of-order events won't be consumed and indexed by Pinot partial upsert table, these late events will be skipped.

### Best practices

Unlike other real-time tables, Upsert table takes up more memory resources as it needs to bookkeep the record locations in memory. As a result, it's important to plan the capacity beforehand, and monitor the resource usage. Here are some recommended practices of using Upsert table.

 - Create the Kafka topic with more partitions. The number of Kafka partitions determines the partition numbers of the Pinot table. The more partitions you have in the Kafka topic, more Pinot servers you can distribute the Pinot table to and therefore more you can scale the table horizontally. 
 - Upsert table maintains an in-memory map from the primary key to the record location. So it's recommended to use a simple primary key type and avoid composite primary keys to save the memory cost. In addition, consider the `hashFunction` config in the Upsert config, which can be `MD5` or `MURMUR3`, to store the 128-bit hashcode of the primary key instead. This is useful when your primary key takes more space. But keep in mind, this hash may introduce collisions, though the chance is very low. 
 - Set up a dashboard over the metric `pinot.server.upsertPrimaryKeysCount.tableName` to watch the number of primary keys in a table partition. It's useful for tracking its growth which is proportional to the memory usage growth.
 - Capacity planning. It's useful to plan the capacity beforehand to ensure you will not run into resource constraints later. A simple way is to measure the amount of the primary keys in the Kafka throughput per partition and time the primary key space cost to approximate the memory usage. A heap dump is also useful to check the memory usage so far on an upsert table instance.


### Example

Putting these together, you can find the table configurations of the quick start example as the following:

{% code title="upsert_meetupRsvp_realtime_table_config.json" %}
```javascript
{
  "tableName": "meetupRsvp",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "mtime",
    "timeType": "MILLISECONDS",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "1",
    "segmentPushType": "APPEND",
    "segmentAssignmentStrategy": "BalanceNumSegmentAssignmentStrategy",
    "schemaName": "meetupRsvp",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "lowLevel",
      "stream.kafka.topic.name": "meetupRSVPEvents",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.hlc.zk.connect.string": "localhost:2191/kafka",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
      "stream.kafka.zk.broker.url": "localhost:2191/kafka",
      "stream.kafka.broker.list": "localhost:19092",
      "realtime.segment.flush.threshold.rows": 30
    }
  },
  "metadata": {
    "customConfigs": {}
  },
  "routing": {
    "instanceSelectorType": "strictReplicaGroup"
  },
  "upsertConfig": {
    "mode": "FULL"
  }
}
```
{% endcode %}

## Quick Start

To illustrate how the full upsert works, the Pinot binary comes with a quick start example. Use the following command to creates a realtime upsert table `meetupRSVP`.

```bash
# stop previous quick start cluster, if any
bin/quick-start-upsert-streaming.sh
```

You can also run partial upsert demo with the following command

```bash
# stop previous quick start cluster, if any
bin/quick-start-partial-upsert-streaming.sh
```

As soon as data flows into the stream, the Pinot table will consume it and it will be ready for querying. Head over to the Query Console to checkout the realtime data.

![Query the upsert table](../../.gitbook/assets/screen-shot-2021-06-15-at-10.02.46-am.png)

For partial upsert you can see only the value from configured column changed based on specified partial upsert strategy.

![Query the partial upsert table](../../.gitbook/assets/screen-shot-2021-07-13-at-12.40.24-pm.png)

An example for partial upsert is shown below, each of the event\_id kept being unique during ingestion, meanwhile the value of rsvp\_count incremented.

![Explain partial upsert table](../../.gitbook/assets/screen-shot-2021-07-13-at-12.41.42-pm.png)

To see the difference from the append-only table, you can use a query option `skipUpsert` to skip the upsert effect in the query result.

![Disable the upsert during query via query option](../../.gitbook/assets/screen-shot-2021-06-15-at-10.03.22-am.png)
