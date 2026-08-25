# Colocated join strategy

Colocated joins is a strategy Pinot can use execute joins without shuffling data between servers when all the following conditions are met:

1. Both tables are partitioned.
2. The partition function is the same.
3. The number of partitions is the same.
4. The join condition is an equality between the partition columns.
5. The assignment of partitions to servers is the same.
6. For each partition, there is a server that has all the segments of the partition for both tables.

As an example, imagine we want to execute the query

```sql
SELECT A.col1, B.col2
FROM A
JOIN B
ON A.partitionKeyA = B.partitionKeyB
```

in a scenario where we have tables A and B partitioned by the same function in exactly two partitions and distributed in such a way that:

1. The 1st partition of A is formed by segments A0-1 and A0-2, stored on servers 1 and 3.
2. The 2nd partition of A is formed by segments A1-1 and A1-2, stored on server 2.
3. The 1st partition of B is formed by segment B0-1, stored on server 3.
4. The 2nd partition of B is formed by segment B1-1, stored on server 2.

In this case, Pinot will try to execute the query in the following way:

![](<../../../../.gitbook/assets/image (16).png>)

*Dotted arrows mean shuffle while solid arrows mean in-server transfer*

As a side effect, this strategy may not use as many servers as other techniques. For example, the same query using [query time partition](query-time-partition-join-strategy.md) may use 3 servers, while in this case Pinot can only use server 3 and server 2. Server 1 cannot be used because it does not have all the segments for partition 2 of table B.

### Empty partitions and partition metadata

A colocated join can run when one participating table has no segments for a partition that another participating table
uses. Pinot keeps one ordered set of partition classes for the stages connected by direct exchanges. For a class used
by the group, a table with no data gets an empty worker colocated with a worker that does have data, so worker IDs and
partition alignment remain consistent across the join.

Pinot removes a partition class only when no table in the colocated group has data for it. For example, a table can
declare eight partitions but populate only three; if the join group uses only those three classes, the leaf stage runs
three workers instead of eight. This reduces fan-out without shifting later partitions onto mismatched worker IDs.

Pinot validates the metadata used to make this assignment:

- A hybrid table whose segment partition metadata disagrees with its table config fails planning. Rebuild or replace
  older segments after changing the partition config; Pinot no longer silently excludes mismatched segments.
- A table distributed across multiple Pinot clusters does not expose partial partition metadata for this optimization,
  because one cluster cannot determine whether another cluster serves a seemingly empty partition.
- A partition that contains segments but has no online replica still fails planning because no server can read the full
  partition.

This empty-partition handling is specific to stages in a colocated direct-exchange group. A partitioned scan outside a
colocated join retains its existing empty-partition behavior.

### Broker pruning for filtered colocated joins

On the default logical-planner path, broker segment pruning can also reduce a colocated join to the partition classes
that can contain rows after filtering. When every table in the colocated group prunes a partition class, Pinot removes
that class from the group while preserving the one-to-one worker alignment for the remaining classes. This can reduce
the number of workers, servers, and segments used by a filtered colocated join.

This optimization requires broker pruning to be enabled and each applicable table to configure the partition segment
pruner with `segmentPrunerTypes: ["partition"]`. Filters on the partition key must reach every side of the group, either
because they are written on both sides or because Calcite propagates the filter through the join equality. A time filter
only prunes segments and does not by itself remove partition classes.

Pinot keeps a partition class when any member of the group can still produce rows. It also keeps all populated classes
when pruning proves that every class is empty, because a zero-worker colocated group cannot be wired. The probe leaf of
a colocated semi-join is not eligible. If a non-colocated stage above the join should retain the reduced server set, set
`useLeafServerForIntermediateStage=true`.

Use the `useBrokerPruning` query option or
`pinot.broker.multistage.logical.planner.use.broker.pruning` broker setting to control this behavior.

### **How to enable colocated joins**

Colocated join optimization is disabled by default in Pinot 1.3.0.

It can be enabled cluster-wide by setting the following configuration in the broker:

```
pinot.broker.multistage.infer.partition.hint=true
```

It can also be enabled/disabled on a per-query basis by setting the following query option:

```sql
SET inferPartitionHint=true;
SELECT ...
```

When `inferPartitionHint=true`, Pinot fills in missing partition metadata for eligible table scans. If you also add a partial `tableOptions` hint, any explicit `partition_key` or `partition_function` value overrides the inferred value, and Pinot validates the combined hint against the table configuration. A mismatch fails planning instead of being ignored. Scans already hinted with `tableOptions(is_replicated='true')` are excluded from this inference and keep that explicit replicated hint unchanged.

<details>

<summary>Advanced configuration</summary>

Colocated joins can also be enabled per-join basis by setting the `tableOptions` hint directly.

```sql
SELECT A.col1, B.col2
FROM A /*+ tableOptions(partition_function='hashcode', partition_key='partitionKeyA', partition_size='4') */
JOIN B /*+ tableOptions(partition_function='hashcode', partition_key='partitionKeyB', partition_size='4') */
ON A.partitionKeyA = B.partitionKeyB
```

When you provide the full `tableOptions` hint yourself, the `partition_function`, `partition_key`, and `partition_size` must match across both tables and must also match the table configuration.

If `inferPartitionHint` is already enabled, you can use a partial `tableOptions` hint to pin only the value you want to override or validate. For example, `tableOptions(partition_key='partitionKeyA')` keeps the inferred partition function and size, but Pinot still validates the explicit key against the table metadata and fails planning if they do not match.

This is a very advanced and error-prone way to configure joins that can also be used to change stage parallelism.

Note that this can also be used to enable colocated joins on tables that have a different number of physical partitions. Consider a case where table A has 16 partitions and table B has 4 partitions and the assignment is such that partitions 0, 4, 8, 12 of table A are assigned to the same server hosting partition 0 of table B (similarly, partitions 1, 5, 9, 13 of table A should be colocated with partition 1 of table B and so on). In this case, co-located joins can be leveraged by explicitly setting the `partition_size` on the larger side to match the smaller side - i.e., in this case both sides would use `/*+ tableOptions(partition_size='4') */`.

</details>

#### **Force colocated join**

Even when colocated joins are enabled, Pinot only uses them if it can guarantee that the conditions listed at the beginning of the document are fulfilled. For example, in a join between two tables, Pinot will not apply colocated joins if it cannot guarantee, using the table configuration, that the same keys partition both tables in the same way (number of partitions, etc).

On some complex deployments, Pinot may not be able to guarantee these constraints even when users know that colocation could be used. In these situations, users can add the `/*+ joinOptions(is_colocated_by_join_keys='true') */` hint to force Pinot to use colocated joins blindly.

{% hint style="warning" %}
Note: `is_colocated_by_join_keys` is only recommended when the tables are to be joined on a non-partition column. When joining on the partition column in colocated fashion, please use either `inferPartitionHint` or `tableOptions` hint as described above.
{% endhint %}

### **How to guarantee that colocated joins can be used**

As noticed above, in order to use colocated joins, the assignment of partitions to servers must be the same for both tables. Although we can manually assign partitions to servers when creating the tables, they can be moved between servers at any time as a result of a rebalance.&#x20;

In order to guarantee that colocated joins can be used it is recommended to instruct Pinot to [assign the same instances](../../../../reference/releases/1.1.0.md#preconfiguration-based-mirror-instance-assignment-11578) for each partition in both tables. To read more about how to partition a table, see [Instance Assignment](../../../../operate-pinot/instance-assignment.md) and [Routing](../../../../operate-pinot/tuning/routing.md#data-ingested-partitioned-by-some-column).

### How to verify colocated joins are being used

As explained, the main advantage when this optimization is enabled is that data doesn't need to be shuffled to execute the join. That can be verified with the [`rawMessages`](../operator-types/mailbox-receive.md#rawmessages) and [`inMemoryMessages`](../operator-types/mailbox-send.md#inmemorymessages) stats on the [mailbox send](../operator-types/mailbox-send.md) operator for this stage. All messages should be in memory and `rawMessages` should be 0 (or not listed at all).

Another way to verify this optimization is being applied is to use the [`EXPLAIN IMPLEMENTATION PLAN`](../explain-plan-1.md#workers-plan) command. You need to use the `EXPLAIN IMPLEMENTATION PLAN` command. There you will see that `MAIL_SEND` operators are decorated with `[PARTITIONED]` and each `MAIL_SEND` will send the data to another worker in the same server.

{% hint style="warning" %}
Notice that this optimization cannot be seen in the normal `EXPLAIN PLAN` command.
{% endhint %}
