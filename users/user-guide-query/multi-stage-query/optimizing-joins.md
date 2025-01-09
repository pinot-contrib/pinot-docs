---
description: Tips and tricks that can be used to optimize joins
---

# Optimizing joins

{% hint style="info" %}
Remember to read the [join operator](operator-types/hash_join.md) page to have a more in depth view of how joins are implemented
{% endhint %}

### The order of input relations matter

Apache Pinot does not use table stats to determine the best order to consume the input relations. Instead, it assumes that the right input relation is the smaller one. That relation will always be fully consumed to build an in-memory hash table and sometimes it will be broadcasted to all workers. This means that it is important to specify the smaller relation as the right input.

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

### Reduce data shuffle <a href="#reducing-data-shuffle" id="reducing-data-shuffle"></a>

Pinot supports different types of [join strategies](join-strategies/). It is important to understand them and try to use them when possible. This data shuffle is expensive and can be a bottleneck for the query performance. Remember to use `stageStats`  (specially [mailbox send](operator-types/mailbox-send.md) and [mailbox receive](operator-types/mailbox-receive.md)) and different explain plans to understand how your data is being shuffled.
