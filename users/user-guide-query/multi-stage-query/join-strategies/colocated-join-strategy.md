# Colocated join strategy

Colocated joins is a strategy Pinot can use execute joins without shuffling data between servers when all the following conditions are met:

1. Both tables are partitioned.
2. The partition function is the same.
3. The number of partitions is the same.
4. The join condition is an equality between the partition columns.
5. The assignment of partitions to servers is the same.
6. For each partition, there is a server that has all the segments of the partition for both tables.

As an example, imagine the following scenario where we have tables A and B partitioned in a compatible way and distributed in such a way that:

1. The 1st partition of A is formed by segments A0-1 and A0-2, which stored in servers 1 and 3.
2. The 2nd partition of A is formed by segments A1-1 and A1-2, which stored in server 2.
3. The 1st partition of B is formed by segments B0-1 and B0-2, which stored in servers 3.
4. The 2nd partition of B is formed by segments B1-1 and B1-2, which stored in server 2.

If we execute the following query:

```sql
SELECT A.col1, B.col2 
FROM A
JOIN B
ON A.partitionKeyA = B.partitionKeyB
```

Then Pinot would try to execute the query in the following way:

<figure><img src="../../../../.gitbook/assets/image (10).png" alt="" width="563"><figcaption><p>Dotted arrows mean shuffle while strong arrows mean in-server transfer</p></figcaption></figure>

As a side effect, this strategy may not use as many servers as other techniques. For example, the same query using [query time partition](query-time-partition-join-strategy.md) may use 3 servers, while in this case Pinot can only use server 3 and server 2. Server 1 cannot be used because it does not have all the segments for partition 2 of table B.

### **How to enable colocated joins**

Colocated join optimization is disabled by default in Pinot 1.3.0.

It can be enabled cluster wise by setting the following configuration in the broker:

```
pinot.broker.multistage.infer.partition.hint=true
```

It can also be enabled/disabled on a per-query basis by setting the following query option:

```sql
SET inferPartitionHint=true
SELECT ...
```

<details>

<summary>Even lower level configuration (not recommended)</summary>

Colocated joins can also be enabled per-join basis by setting the `tableOptions` hint directly. This is a very advance and error prone way to configure joins that can also be used to change stage parallelism. Therefore it is recommended to delegate on the other ways to enable colocated joins and do not directly use `tableOptions` .

```sql
SELECT A.col1, B.col2
FROM A /*+ tableOptions(partition_function='hashcode', partition_key='partitionKeyA', partition_size='4') */
JOIN B /*+ tableOptions(partition_function='hashcode', partition_key='partitionKeyB', partition_size='4') */
ON A.partitionKeyA = B.partitionKeyB
```

In this case, the `partition_function`, `partition_key`, and `partition_size` are required to be the same for both tables and they must be the same as the ones defined in the table configuration.

\


</details>

### **How to guarantee that colocated joins can be used**

As noticed above, in order to use colocated joins, the assignment of partitions to servers must be the same for both tables. Although we can manually assign partitions to servers when creating the tables, they can be moved between servers at any time as a result of a rebalance.&#x20;

In order to guarantee that colocated joins can be used it is recommended to instruct Pinot to [assign the same instances](https://docs.pinot.apache.org/basics/releases/1.1.0#preconfiguration-based-mirror-instance-assignment-11578) for each partition in both tables. To read more about how to partition a table, see [Instance Assignment](../../../../operators/operating-pinot/instance-assignment.md) and [Routing](../../../../operators/operating-pinot/tuning/routing.md#data-ingested-partitioned-by-some-column).

### How to verify colocated joins are being used

As explained, the main advantage when this optimization is enabled is that data doesn't need to be shuffled to execute the join. That can be verified by with the `rawMessages` and `inMemoryMessages` stats on the mailbox send operator for this stage. All messages should be `inMemoryMessages` and `rawMessages` should be 0 (or being not listed at all).

Another way to verify this optimization is being applied is to use the `EXPLAIN IMPLEMENTATION PLAN` command. In order to see if the optimization is being applied you need to use the `EXPLAIN IMPLEMENTATION PLAN` command. There you will see that `MAIL_SEND` operators are decorated with `[PARTITIONED]` and each `MAIL_SEND` will send the data to another worker in the same server.

{% hint style="warning" %}
Notice that this optimization cannot be seen in the normal `EXPLAIN PLAN` command.
{% endhint %}
