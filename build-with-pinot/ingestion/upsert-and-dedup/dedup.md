---
description: Deduplication support in Apache Pinot.
---

# Stream ingestion with Dedup

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

The dedup Pinot table can use only the low-level consumer for the input streams. As a result, it uses the [partitioned replica-group assignment](../../../operate-pinot/segment-assignment.md#partitioned-replica-group-segment-assignment) for the segments. Moreover, dedup poses the additional requirement that all segments of the same partition must be served from the same server to ensure the data consistency across the segments. Accordingly, it requires `strictReplicaGroup` as the routing strategy. To use that, configure `instanceSelectorType` in `Routing` as the following:

{% code title="routing" %}
```json
{
  "routing": {
    "instanceSelectorType": "strictReplicaGroup"
  }
}
```
{% endcode %}

{% hint style="warning" %}
instance assignment is persisted. Note that `numInstancesPerPartition` should always be `1` in `replicaGroupPartitionConfig`.
{% endhint %}

### Other limitations

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

## Metadata TTL

Server stores the existing primary keys in dedup metadata map kept on JVM heap. As the dedup metadata grows, the heap memory pressure increases, which may affect the performance of ingestion and queries. One can set a positive metadata TTL to enable the TTL mechanism to keep the metadata size bounded. By default, the table's time colum is used as the dedup time column. The time unit of  TTL is the same as the dedup time column. The TTL should be set long enough so that new records can be deduplicated before the primary keys gets removed. Time column must be `NUMERIC` data type when `metadataTTl` is enabled.  

```json
{ 
 ...
  "dedupConfig": { 
        "dedupEnabled": true, 
        "hashFunction": "NONE",
        "dedupTimeColumn": "mtime",
        "metadataTTL": 30000
   }, 
 ...
}
```

## Enable preload for faster server restarts

When ingesting new records, the server has to read the metadata map to check for duplicates. But when server restarts, the documents in existing segments are all unique as ensured by the dedup logic during real-time ingestion. So we can do write-only to bootstrap the metadata map faster. Set `preload` to `ENABLE` to turn this on.&#x20;

```json
{ 
 ...
  "dedupConfig": { 
        "dedupEnabled": true, 
        "hashFunction": "NONE",
        "dedupTimeColumn": "mtime",
        "metadataTTL": 30000,
        "preload": "ENABLE"
   }, 
 ...
}
```

The feature also requires you to specify `pinot.server.instance.max.segment.preload.threads: N` in the server config where N should be replaced with the number of threads that should be used for preload. It's 0 by default to disable the preloading feature. This preloading thread pool is shared with [upsert table's preloading](upsert.md#enable-preload-for-faster-server-restarts).

## Ignore non-default tier segments during dedup metadata construction

When real-time segments are moved to a non-default tier, they are often already outside the metadata TTL window. In that case, you can skip them when Pinot rebuilds dedup metadata on the server.

Set `dedupConfig.ignoreNonDefaultTiers` to one of the following values:

* `ENABLE`: Always skip immutable segments on non-default tiers when constructing dedup metadata.
* `DISABLE`: Always include immutable segments on non-default tiers.
* `DEFAULT`: Use the server-level default from `pinot.server.instance.dedup.default.ignore.non.default.tiers`.

```json
{
  "dedupConfig": {
    "dedupEnabled": true,
    "ignoreNonDefaultTiers": "ENABLE"
  }
}
```

The server-level default is `false`, so tables with `ignoreNonDefaultTiers: "DEFAULT"` continue to include non-default-tier segments unless you override the server setting.

## Parallel consumption during commit, download, and replacement

Pinot protects dedup correctness by limiting how much a slow replica can keep consuming while the previous segment is still being finalized.

* For non-pauseless dedup tables, Pinot disallows parallel consumption during commit by default.
* For pauseless dedup tables, Pinot still allows consumption during the build phase, but it stops the slow replica during segment download and replacement so the dedup metadata stays consistent with the lead replica.

For backward compatibility, dedup tables still accept the deprecated table-level flag `dedupConfig.allowDedupConsumptionDuringCommit`. Setting it to `true` restores the older behavior and allows the replica to continue consuming throughout commit handling, including download and replacement:

```json
{
  "dedupConfig": {
    "dedupEnabled": true,
    "allowDedupConsumptionDuringCommit": true
  }
}
```

If the table-level flag is left at its default `false`, the server-level fallback `pinot.server.instance.dedup.default.allow.dedup.consumption.during.commit` can enable the same legacy behavior for dedup tables on that server. New deployments should prefer `parallelSegmentConsumptionPolicy` in `streamIngestionConfig` when they need explicit control over parallel consumption.

## Immutable dedup configuration fields

{% hint style="danger" %}
**Certain dedup and schema configuration fields cannot be modified after table creation.**

Changing these fields on an existing dedup table can lead to data inconsistencies or data loss between replicas. Pinot uses these configurations to determine which records to keep or discard, so altering them after data has been ingested will cause existing metadata to become inconsistent with the new configuration.

The following fields are immutable after table creation:

**Schema fields:**
* `primaryKeyColumns`

**dedupConfig fields:**
* `hashFunction`
* `dedupTimeColumn`
* `timeColumnName` (when used as the default dedup time column)

Attempting to update these fields will return an error:

```
Failed to update table '<tableName>': Cannot modify [<field>] as it may lead to data inconsistencies. Please create a new table instead.
```

**Recommended workaround:** Create a new table with the desired configuration and reingest all data.

**Alternative (use with caution):** If you must modify these fields without recreating the table, you can use the `force=true` query parameter on the table config update API. Before doing so, pause consumption and restart all servers. Note that this approach only guarantees consistency for newly ingested keys; existing data may remain inconsistent.
{% endhint %}

## Best practices

Unlike other real-time tables, Dedup table takes up more memory resources as it needs to bookkeep the primary key and its corresponding segment reference, in memory. As a result, it's important to plan the capacity beforehand, and monitor the resource usage. Here are some recommended practices of using Dedup table.

* Create the Kafka topic with more partitions. The number of Kafka partitions determines the partition numbers of the Pinot table. The more partitions you have in the Kafka topic, more Pinot servers you can distribute the Pinot table to and therefore more you can scale the table horizontally. **But note that**, [like upsert tables](upsert.md#create-the-topicstream-with-more-partitions.), you can't increase the partitions in future for dedup enabled tables so you need to start with good enough partitions (atleast 2-3X the number of pinot servers).
* For Dedup tables, updating primary key columns or the dedupTimeColumn is not recommended, as it may lead to data loss and inconsistencies between replicas. If a change is unavoidable, ensure that consumption is paused and all servers are restarted for the change to take effect. Even then, consistency is not guaranteed.
* Dedup table maintains an in-memory map from the primary key to the segment reference. So it's recommended to use a simple primary key type and avoid composite primary keys to save the memory cost. In addition, consider the `hashFunction` config in the Dedup config, which can be `MD5` or `MURMUR3`, to store the 128-bit hashcode of the primary key instead. This is useful when your primary key takes more space. But keep in mind, this hash may introduce collisions, though the chance is very low.
* **Monitoring**: Set up a dashboard over the metric `pinot.server.dedupPrimaryKeysCount.tableName` to watch the number of primary keys in a table partition. It's useful for tracking its growth which is proportional to the memory usage growth.
* **Capacity planning:** It's useful to plan the capacity beforehand to ensure you will not run into resource constraints later. A simple way is to measure the amount of the primary keys in the Kafka throughput per partition and time the primary key space cost to approximate the memory usage. A heap dump is also useful to check the memory usage so far on an dedup table instance.
