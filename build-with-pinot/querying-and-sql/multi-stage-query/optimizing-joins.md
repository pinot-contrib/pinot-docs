---
description: Tips and tricks that can be used to optimize joins
---

# Optimizing joins

{% hint style="info" %}
Read the [join operator](operator-types/hash_join.md) page for a detailed explanation of how joins are implemented.
{% endhint %}

### The order of input relations matter

Apache Pinot does not rely on table statistics to optimize the join order. Instead, it prioritizes the input relations from right to left (based on the order of the tables in the SQL query). This relation is fully consumed to create an in-memory hash table and may be broadcast to all workers. It is less expensive to do a join between a large table and a small table than the other way around, therefore it's important to specify the smaller relation as the right input

{% hint style="info" %}
Here _left_ means the first relation in the explain plan and _right_ the second one. In SQL, when two tables are joined, the left relation is the first one to specify and the right the second one. But this gets more complicated when three or more tables are joined. It is strongly recommended to use the explain plan to be sure about which input is _left_ and _right._
{% endhint %}

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

Or

```sql
SELECT customer.c_address, customer.c_nationkey
FROM customer
WHERE c_custkey IN (SELECT o_custkey FROM orders)
```

In order to use indexes Pinot needs to know the actual values on the subquery at optimization time. Therefore what Pinot does internally is to execute the subquery first and then replace the subquery with the actual values in the main query.

For example, if the subquery in the previous example returns the values 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, the query is transformed into:

```sql
SELECT customer.c_address, customer.c_nationkey
FROM customer
WHERE customer.c_custkey IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```

Which can then be optimized using indexes.

Currently, this optimization cannot be seen in the Pinot explain plan.

#### Rewriting joins as semi-joins

Sometimes, inner or left joins can be converted into semi-joins. Specifically, the requirements are:

1. Only columns from the left side must be projected.
2. The join condition must be equality.
3. The right side must be unique.

For example, the following two queries are equivalent:

```sql
SELECT customer.c_address, customer.c_nationkey
FROM customer
JOIN (SELECT DISTINCT o_custkey FROM orders) AS distinct_orders
on customer.c_custkey = distinct_orders.o_custkey
```

```sql
SELECT customer.c_address, customer.c_nationkey
FROM customer
WHERE c_custkey IN (SELECT o_custkey FROM orders)
```

But they won't be equivalent if instead of `distinct_orders` we were using `orders` . This is because a join repeats rows from the left side if there are repetitions on the right side, while a semi-join never repeats rows.

Pinot applies this optimization automatically if the three conditions explained above are fulfilled. Given that columns in Pinot cannot be marked as unique, the only way to indicate Pinot that the right-hand side is unique is to apply a SQL expression that guarantees that, for example `DISTINCT` or `GROUP BY` the columns used in the join condition. Sometimes, it is just easier to rewrite the original SQL to substitute the `JOIN` with a `WHERE EXISTS` .

### Reduce data shuffle <a href="#reducing-data-shuffle" id="reducing-data-shuffle"></a>

Pinot supports different types of [join strategies](../../../build-with-pinot/querying-and-sql/multi-stage-query/join-strategies). It is important to understand them and try to use when possible. This data shuffle is expensive and can be a bottleneck for the query performance. Remember to use `stageStats`  (specially [mailbox send](operator-types/mailbox-send.md) and [mailbox receive](operator-types/mailbox-receive.md)) and different explain plan modes to understand how your data is being shuffled.
