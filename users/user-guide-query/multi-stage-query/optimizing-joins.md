---
description: Tips and tricks that can be used to optimize joins
---

# Optimizing joins

{% hint style="info" %}
Remember to read the [join operator](operator-types/hash\_join.md) page to have a more in deep view of how joins are implemented
{% endhint %}

### The order of input relations matter

Apache Pinot does not use table stats to determine the best order to consume the input relations. Instead, it assumes that the right input relation is the smaller one. That relation will always be fully consumed to build a hash table and sometimes it will be broadcasted to all workers. This means that it is important to specify the smaller relation as the right input.

Remember that left and right are relative to the order of the tables in the SQL query. It is less expensive to do a join between a large table and a small table than the other way around.

For example, this query:

```sql
select largeTable.col1, smallTable.col2
from largeTable 
cross join smallTable
```

is more efficient than:

```sql
select largeTable.col1, smallTable.col2
from smallTable 
cross join largeTable
```

### Predicate push-down <a href="#predicate-push-down" id="predicate-push-down"></a>

Usually it is faster to filter data before joining it. Pinot automatically pushes down predicates to the individual tables before joining them when it can prove the change doesn't break semantics.

For example, consider the following query:

```sql
SELECT customer.c_address, orders.o_shippriority
FROM customer
JOIN orders
    ON customer.c_custkey = orders.o_custkey
WHERE customer.c_nationkey = 1
```

Is automatically transformed by Pinot into:

```sql
SELECT customer.c_address, orders.o_shippriority
FROM (customer WHERE c_nationkey = 1) as customer
JOIN orders
    ON customer.c_custkey = orders.o_custkey
```

This optimization not only reduces the amount of data that needs to be shuffled and joined but also opens the possibility of using indexes to speed up the query.

Remember that sometimes the predicate push-down is not possible. One example is when one of the inputs is a subquery with a limit like:

```sql
SELECT customer.c_address, orders.o_shippriority
FROM (select * from customer LIMIT 10) as customer
JOIN orders
    ON customer.c_custkey = orders.o
WHERE customer.c_nationkey = 1
```

In this case, although Pinot will push down the predicate into the subquery, it won't be able to push it down into the table scan of the subquery because it would break the semantics of the original limit.

Therefore the final query will be

```sql
SELECT customer.c_address, orders.o_shippriority
FROM (select * from 
        (select * from customer LIMIT 10) as temp where WHERE temp.c_nationkey = 1
     ) as customer
JOIN orders
    ON customer.c_custkey = orders.o
```

This new query is equivalent to the original one and reduce the amount of data that needs to be shuffled and joined but cannot use indexes to speed up the query. In case you want to apply the filter before the limit, you can rewrite the query as:

```sql
SELECT customer.c_address, orders.o_shippriority
FROM (select * from customer WHERE temp.c_nationkey = 1 LIMIT 10) as customer
JOIN orders
    ON customer.c_custkey = orders.o
```

This optimization can be easily seen in the explain plan, where the filter operator will be pushed as one of the sides of the join.

### Optimizing semi-join to use indexes <a href="#optimizing-semi-join-to-use-indexes" id="optimizing-semi-join-to-use-indexes"></a>

Semi-joins are a special case of joins where the result of the join is not the result of the join itself but the rows of the first table that have a match in the second table.

Queries using semi-joins are usually not written as such but as a query with a subquery in the WHERE clause like:

```sql
SELECT customer.c_address, customer.c_nationkey
FROM customer
WHERE EXISTS (SELECT 1 FROM orders WHERE customer.c_custkey = orders.o_custkey)
```

In order to use indexes Pinot needs to know the actual values on the subquery at optimization time. Therefore what Pinot does internally is to execute the subquery first and then replace the subquery with the actual values in the main query.

For example, if the subquery in the previous example returns the values 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, the query is transformed into:

```sql
SELECT customer.c_address, customer.c_nationkey
FROM customer
WHERE customer.c_custkey IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```

Which can then be optimized using indexes.

At this moment this optimization cannot be seen in the Pinot explain plan.

### Co-located join <a href="#co-located-join" id="co-located-join"></a>

The co-located join is a special case of join where the data of the two tables to be joined is already co-located. When two tables that are partitioned in the same way are equi-joined on the partitioning key, the join can be optimized by avoiding the shuffle of the data. To read more about how to partition a table, see [Instance Assignment](../../../operators/operating-pinot/instance-assignment.md) and [Routing](../../../operators/operating-pinot/tuning/routing.md#data-ingested-partitioned-by-some-column).

In Pinot 1.3.0 this optimization is disabled by default. It can be enabled for specific queries by specifying the `tableOptions` hint after each table in the query.

For example:

```sql
SELECT customer.c_address, orders.o_shippriority
FROM customer /*+ tableOptions(partition_function='hashcode', partition_key='c_custkey', partition_size='4') */
JOIN orders /*+ tableOptions(partition_function='hashcode', partition_key='o_custkey', partition_size='4') */
    ON customer.c_custkey = orders.o_custkey
```

Pinot can also be configured to automatically apply this optimization when it makes sense by changing the broker configuration property `pinot.broker.multistage.implicit.colocate` to true.

As explained, the main difference when this optimization is enabled is that data doesn't need to be shuffled to execute the join. That can be verified by with the `rawMessages` and `inMemoryMessages` stats on the mailbox send operator for this stage. All messages should be `inMemoryMessages` and `rawMessages` should be 0 (or being not listed at all).

Another way to verify this optimization is being applied is to use the `EXPLAIN IMPLEMENTATION PLAN` command. In order to see if the optimization is being applied you need to use the `EXPLAIN IMPLEMENTATION PLAN` command. There you will see that `MAIL_SEND` operators are decorated with `[PARTITIONED]` and each `MAIL_SEND` will send the data to another worker in the same server.

{% hint style="warning" %}
Notice that this optimization cannot be seen in the normal `EXPLAIN PLAN` command.
{% endhint %}

