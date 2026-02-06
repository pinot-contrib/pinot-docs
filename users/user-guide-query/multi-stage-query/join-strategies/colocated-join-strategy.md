# Colocated join strategy

Colocated joins is a strategy Pinot can use execute joins without shuffling data between servers when all the following conditions are met:

1. Both tables are partitioned.
2. The partition function is the same.
3. The number of partitions is the same.
4. The join condition is an equality between the partition columns.
5. The assignment of partitions to servers is the same.
6. For each partition, there is a server that has all the segments of the partition for both tables.

As an example, imagine we want to execute the query

<pre class="language-sql"><code class="lang-sql"><strong>SELECT A.col1, B.col2 
</strong>FROM A
JOIN B
ON A.partitionKeyA = B.partitionKeyB
</code></pre>

in a scenario where we have tables A and B partitioned by the same function in exactly two partitions and distributed in such a way that:

1. The 1st partition of A is formed by segments A0-1 and A0-2, stored on servers 1 and 3.
2. The 2nd partition of A is formed by segments A1-1 and A1-2, stored on server 2.
3. The 1st partition of B is formed by segment B0-1, stored on server 3.
4. The 2nd partition of B is formed by segment B1-1, stored on server 2.

In this case, Pinot will try to execute the query in the following way:

<figure><img src="../../../../.gitbook/assets/image (16).png" alt="" width="563"><figcaption><p>Dotted arrows mean shuffle while solid arrows mean in-server transfer</p></figcaption></figure>

As a side effect, this strategy may not use as many servers as other techniques. For example, the same query using [query time partition](query-time-partition-join-strategy.md) may use 3 servers, while in this case Pinot can only use server 3 and server 2. Server 1 cannot be used because it does not have all the segments for partition 2 of table B.

### **How to enable colocated joins**

Colocated join optimization is disabled by default in Pinot 1.3.0.

It can be enabled cluster wise by setting the following configuration in the broker:

```
pinot.broker.multistage.infer.partition.hint=true
```

It can also be enabled/disabled on a per-query basis by setting the following query option:

```sql
SET inferPartitionHint=true;
SELECT ...
```

<details>

<summary>Advanced configuration</summary>

Colocated joins can also be enabled per-join basis by setting the `tableOptions` hint directly.

```sql
SELECT A.col1, B.col2
FROM A /*+ tableOptions(partition_function='hashcode', partition_key='partitionKeyA', partition_size='4') */
JOIN B /*+ tableOptions(partition_function='hashcode', partition_key='partitionKeyB', partition_size='4') */
ON A.partitionKeyA = B.partitionKeyB
```

In this case, the `partition_function`, `partition_key`, and `partition_size` are required to be the same for both tables and they must be the same as the ones defined in the table configuration.

This is a very advance and error prone way to configure joins that can also be used to change stage parallelism.

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

In order to guarantee that colocated joins can be used it is recommended to instruct Pinot to [assign the same instances](https://docs.pinot.apache.org/basics/releases/1.1.0#preconfiguration-based-mirror-instance-assignment-11578) for each partition in both tables. To read more about how to partition a table, see [Instance Assignment](../../../../operators/operating-pinot/instance-assignment.md) and [Routing](../../../../operators/operating-pinot/tuning/routing.md#data-ingested-partitioned-by-some-column).

### How to verify colocated joins are being used

As explained, the main advantage when this optimization is enabled is that data doesn't need to be shuffled to execute the join. That can be verified with the [`rawMessages`](../operator-types/mailbox-receive.md#rawmessages) and [`inMemoryMessages`](../operator-types/mailbox-send.md#inmemorymessages) stats on the [mailbox send](../operator-types/mailbox-send.md) operator for this stage. All messages should be in memory and `rawMessages` should be 0 (or not listed at all).

Another way to verify this optimization is being applied is to use the [`EXPLAIN IMPLEMENTATION PLAN`](../explain-plan-1.md#workers-plan) command. You need to use the `EXPLAIN IMPLEMENTATION PLAN` command. There you will see that `MAIL_SEND` operators are decorated with `[PARTITIONED]` and each `MAIL_SEND` will send the data to another worker in the same server.

{% hint style="warning" %}
Notice that this optimization cannot be seen in the normal `EXPLAIN PLAN` command.
{% endhint %}
