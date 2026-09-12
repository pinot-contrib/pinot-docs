---
description: >-
  Configure table partitioning for offline, realtime, and hybrid tables so
  brokers can prune segments and queries stay aligned with Kafka and batch
  ingestion.
---

# Configuring Table Partitioning

Table partitioning tells Pinot how rows are distributed across segments. When a query filters on the partition column with `=` or `IN`, the broker can skip segments that cannot contain matching rows.

This page is the operator how-to for **offline**, **realtime**, and **hybrid** tables. For the full property list, see [`segmentPartitionConfig`](../../reference/configuration-reference/table.md#segment-partition-config). For how pruning works at query time, see [Segment Pruning](segment-pruning.md).

## Three meanings of "partition"

Pinot docs use "partition" in three related but different ways:

| What | Where it lives | What it is for |
| --- | --- | --- |
| Stream / Kafka partitions | The topic (or Kinesis shards, Pulsar partitions) | How the producer shards events. Realtime Pinot consumes one stream partition per consuming segment. |
| Segment partition metadata | `tableIndexConfig.segmentPartitionConfig` | The function Pinot uses to tag each segment with partition ids, then prune at the broker. |
| Replica-group *instance* partitions | `instanceAssignmentConfigMap` | How servers are grouped so a query fans out to one replica group. See [Instance Assignment](../instance-assignment.md). |

This page configures the **second** of those. Replica-group assignment is an optional layer on top; it does not replace matching Kafka and Pinot partition functions.

## Minimum table config

Every partitioned table needs both of the following. Pruning does not run if you set only `segmentPartitionConfig`.

```json
{
  "tableIndexConfig": {
    "segmentPartitionConfig": {
      "columnPartitionMap": {
        "memberId": {
          "functionName": "Murmur",
          "numPartitions": 8
        }
      }
    }
  },
  "routing": {
    "segmentPrunerTypes": ["partition"]
  }
}
```

Built-in `functionName` values (case-insensitive): `Modulo`, `Murmur` (alias `Murmur2`), `Murmur3`, `FNV`, `HashCode`, `ByteArray`, and `BoundedColumnValue`. Function-specific options such as `partitionIdNormalizer`, `useRawBytes`, `seed`, `variant`, and `columnValues` are documented in the [table configuration reference](../../reference/configuration-reference/table.md#segment-partition-config).

{% hint style="info" %}
Partition pruning applies only to **EQUALITY** and **IN** filters on the partition column (for example `memberId = 123` or `memberId IN (1, 2)`). Range filters do not prune by partition.
{% endhint %}

## Offline tables

Offline ingestion does not inherit a stream partition. You must **pre-partition the input** with the same function and `numPartitions` that the table config declares, then build segments.

1. Set `segmentPartitionConfig` and `routing.segmentPrunerTypes` as above.
2. Partition files before the Pinot segment build. Each input file should contain as few partition ids as possible — ideally one. Pinot records the partition ids it *sees* in the segment; it does not reshuffle rows across files at query time.
3. Hadoop preprocessing can partition as part of the MapReduce job. Enable `partition` in `preprocessing.operations` and keep `segmentPartitionConfig` on the table. See [Hadoop batch ingestion](../../build-with-pinot/ingestion/batch-ingestion/hadoop.md). Other batch jobs can use a partitioner that honors the table config (`partitionerType: TABLE_PARTITION_CONFIG`).
4. After push, confirm segment metadata, for example:

```
column.memberId.partitionFunction = Murmur
column.memberId.numPartitions = 8
column.memberId.partitionValues = 3
```

If `partitionValues` lists many ids per segment, pruning will not help much. Split the input so each file maps to one partition.

{% hint style="info" %}
**Multi-column partitioning** is supported for **offline** tables: add more entries under `columnPartitionMap`. Realtime tables persist partition metadata only when there is **exactly one** partition column. See [Ingestion FAQ](../troubleshooting/ingestion-faq.md#does-pinot-support-partition-pruning-on-multiple-partition-columns).
{% endhint %}

## Realtime tables

Partition **at the producer**, then tell Pinot to use the same function.

1. Key Kafka (or equivalent) records on the partition column. Kafka's default partitioner uses **murmur2**. The matching Pinot function is `Murmur` (not `Modulo`).
2. Set `numPartitions` to the **full topic** partition count, even if this table consumes only a subset of partitions. Using the subset size breaks broker pruning. Details are in [Segment Pruning](segment-pruning.md#partition-pruning).
3. Pinot tags each consuming LLC segment with that stream partition id. If `columnPartitionConfig.numPartitions` does not match the per-stream partition count, the controller logs a warning and pruning can be wrong.

```json
{
  "tableType": "REALTIME",
  "tableIndexConfig": {
    "segmentPartitionConfig": {
      "columnPartitionMap": {
        "memberId": {
          "functionName": "Murmur",
          "numPartitions": 12
        }
      }
    }
  },
  "routing": {
    "segmentPrunerTypes": ["partition"]
  }
}
```

{% hint style="warning" %}
Upsert and dedup tables should partition on the **primary key** (or a column that is a function of it) so all events for a key land on one partition and one server. Pinot **rejects** table-config updates that add, remove, or change `segmentPartitionConfig` on upsert/dedup tables. Plan the function and count before you create the table. See the warning on [`segmentPartitionConfig`](../../reference/configuration-reference/table.md#segment-partition-config).

Offline upsert tables **require** `segmentPartitionConfig` so segments of the same partition are assigned together.
{% endhint %}

## Hybrid tables

A hybrid table is an **OFFLINE** config plus a **REALTIME** config that share the same raw table name. You do not create a third "hybrid" resource. See [Table](../../basics/components/table/README.md#hybrid-table-creation) and the [Hybrid Real-Time + Offline playbook](../../playbooks/hybrid-offline-realtime.md).

For partitioning to work across both sides:

- Use the **same** partition column, `functionName`, and `numPartitions` on both table configs.
- Partition the Kafka producer and the offline backfill with that same function. If realtime used `Murmur` / Kafka murmur2, the batch job must not silently switch to `Modulo`.
- After the time boundary moves, queries that filter on the partition column still prune on each side independently. Mismatched functions mean the same `memberId = 123` can map to different ids offline vs realtime.

Replica-group / partitioned replica-group **assignment** (which servers hold which partition) is optional and configured separately. See [Segment Assignment](../segment-assignment.md#partitioned-replica-group-segment-assignment) and [Instance Assignment](../instance-assignment.md). Do not confuse `replicaGroupPartitionConfig.numPartitions` (server groups) with `segmentPartitionConfig` `numPartitions` (data partitions).

## Verify pruning

1. Run a query that filters on the partition column with `=` or `IN`.
2. Compare `numSegmentsQueried` with the table's segment count. Broker-side drops show up as `numSegmentsPrunedByBroker`. See [Monitoring pruning effectiveness](segment-pruning.md#monitoring-pruning-effectiveness).
3. If almost every segment is still queried, check that:
   - `routing.segmentPrunerTypes` includes `"partition"`
   - Segment metadata actually lists a small `partitionValues` set
   - Realtime `numPartitions` is the full Kafka topic size
   - Hybrid offline and realtime configs match

You can enable time pruning and partition pruning together: `"segmentPrunerTypes": ["partition", "time"]`.

## Related pages

- [Table configuration: segmentPartitionConfig](../../reference/configuration-reference/table.md#segment-partition-config)
- [Segment Pruning](segment-pruning.md)
- [Routing](routing.md)
- [Instance Assignment](../instance-assignment.md)
- [Ingestion FAQ](../troubleshooting/ingestion-faq.md)
- [Hybrid Real-Time + Offline playbook](../../playbooks/hybrid-offline-realtime.md)
