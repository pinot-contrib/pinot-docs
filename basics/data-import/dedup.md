---
description: Deduplication support in Apache Pinot.
---

# Stream ingestion with deduplication

Pinot provides native support for deduplication (dedup) during the real-time ingestion (v0.11.0+).

## Prerequisites for enabling dedup

To enable dedup on a Pinot table, make the following table configuration and schema changes:

### Define the primary key in the schema

To be able to dedup records, a primary key is needed to uniquely identify a given record. To define a primary key, add the field `primaryKeyColumns` to the schema definition.

{% code title="schemaWithPK.json" %}
```javascript
{
    "primaryKeyColumns": ["id"]
}
```
{% endcode %}

Note this field expects a list of columns, as the primary key can be composite.

While ingesting a record, if its primary key is found to be already present, the record will be dropped.

### Partition the input stream by the primary key

An important requirement for the Pinot dedup table is to partition the input stream by the primary key. For Kafka messages, this means the producer shall set the key in the [`send`](https://kafka.apache.org/20/javadoc/index.html?org/apache/kafka/clients/producer/KafkaProducer.html) API. If the original stream is not partitioned, then a streaming processing job (e.g. Flink) is needed to shuffle and repartition the input stream into a partitioned one for Pinot's ingestion.

### Use strictReplicaGroup for routing

The dedup Pinot table can use only the low-level consumer for the input streams. As a result, it uses the [partitioned replica-group assignment](../../operators/operating-pinot/segment-assignment.md#partitioned-replica-group-segment-assignment) for the segments. Moreover, dedup poses the additional requirement that all segments of the same partition must be served from the same server to ensure the data consistency across the segments. Accordingly, it requires `strictReplicaGroup` as the routing strategy. To use that, configure `instanceSelectorType` in `Routing` as the following:

{% code title="routing" %}
```json
{
  "routing": {
    "instanceSelectorType": "strictReplicaGroup"
  }
}
```
{% endcode %}

### Other limitations

* The high-level consumer is not allowed for the input stream ingestion, which means `stream.kafka.consumer.type` must be `lowLevel`.
* The incoming stream must be partitioned by the primary key such that, all records with a given primaryKey must be consumed by the same Pinot server instance.

## Enable dedup in the table configurations

To enable dedup for a REALTIME table, add the following to the table config.

{% code title="tableConfigWithDedup.json" %}
```json
{ 
 ...
  "dedupConfig": { 
        "dedupEnabled": true, 
        "hashFunction": "NONE" 
   }, 
 ...
}
```
{% endcode %}

Supported values for `hashFunction` are `NONE`, `MD5` and `MURMUR3`, with the default being `NONE`.

## Best practices

Unlike other real-time tables, Dedup table takes up more memory resources as it needs to bookkeep the primary key and its corresponding segment reference, in memory. As a result, it's important to plan the capacity beforehand, and monitor the resource usage. Here are some recommended practices of using Dedup table.

* Create the Kafka topic with more partitions. The number of Kafka partitions determines the partition numbers of the Pinot table. The more partitions you have in the Kafka topic, more Pinot servers you can distribute the Pinot table to and therefore more you can scale the table horizontally.
* Dedup table maintains an in-memory map from the primary key to the segment reference. So it's recommended to use a simple primary key type and avoid composite primary keys to save the memory cost. In addition, consider the `hashFunction` config in the Dedup config, which can be `MD5` or `MURMUR3`, to store the 128-bit hashcode of the primary key instead. This is useful when your primary key takes more space. But keep in mind, this hash may introduce collisions, though the chance is very low.
* **Monitoring**: Set up a dashboard over the metric `pinot.server.dedupPrimaryKeysCount.tableName` to watch the number of primary keys in a table partition. It's useful for tracking its growth which is proportional to the memory usage growth.
* **Capacity planning:** It's useful to plan the capacity beforehand to ensure you will not run into resource constraints later. A simple way is to measure the amount of the primary keys in the Kafka throughput per partition and time the primary key space cost to approximate the memory usage. A heap dump is also useful to check the memory usage so far on an dedup table instance.
