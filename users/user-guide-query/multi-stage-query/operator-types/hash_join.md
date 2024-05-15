---
description: >-
  Describes the hash join relation operator in the multi-stage query engine.
---

# Hash join relational operator

The hash join operator is used to join two relations using a hash join algorithm. 
It is a binary operator that takes two inputs, the left and right relations, and produces a single output relation. 

This is the only join operator in the multi-stage query engine and it is always created as a result of a query that 
contains a join clause, but can be created by other SQL queries like ones using semi-join.

There are different types of joins that can be performed using the hash join operator.
Apache Pinot supports:
- Inner join, where only the rows that have a match in both relations are returned.
- Left join, where all the rows from the left relation are returned. The ones that have a match with the right relation 
  are returned with the columns from the right relation, and the ones that do not have a match are returned with null 
  values for the columns from the right relation.
- Right join, like the left join but returning all the rows from the right relation, with the columns from the left 
  relation filled with null values for the rows that do not have a match.
- Full outer join, where all the rows from both relations are returned. If a row from any relation does not have a match 
  in the other relation, the columns from the other relation are filled with null values.
- Semi-join, where only the rows from the left relation that have a match in the right relation are returned. This is 
  useful to filter the rows from the left relation based on the existence of a match in the right relation.
- Anti-join, where only the rows from the left relation that do not have a match in the right relation are returned.

## Implementation details

The hash join operator is one of the new operators introduced in the multi-stage query engine.
The current implementation assumes that the right input relation is the smaller one, so it consumes this
input first building a hash table that is then probed with the left input relation.

{% hint style="info" %}
Future optimizations may include advanced heuristics to decide which input relation to consume first, but in the current
implementation, it is important to specify the smaller relation as the right input.
{% endhint %}

Although the whole multi-stage query engine is designed to be able to process the data in memory, the multi-stage query
engine uses the ability to execute each stage in different workers (explained in 
[understanding stages](../understanding-stages.md)) to be able to process the data that may not fit in the memory of a 
single node. Specifically, each worker processes a subset of the data. Inputs are by default partitioned by the join 
keys and each worker process one partition of the data.

This means that data usually needs to be shuffled between workers, which is done by the engine using a mailbox system.
The engine tries to minimize the amount of data that needs to be shuffled by partitioning the data, but some techniques
can be used to reduce the amount of data that needs to be shuffled, like using co-located joins.

### Blocking nature
The hash join operator is a blocking operator. It needs to consume all the input data (from both inputs) before emitting
the result.

### Maximum number of groups
Even using partitioning, the amount of data that needs to be stored in memory can be high, so the engine tries to
protect itself from running out of memory by limiting the number of groups that can be created by the join keys.

The [join_overflow_mode](../hints/join_overflow_mode.md) hint can be used to control the behavior of the engine when the
number of groups exceeds the limit.
This limit can be defined using the [max_rows_in_join](../hints/max_rows_in_join.md) hint.
By default, this limit is slightly above 1 million groups and the default join overflow mode is `THROW`,
which means that the query will fail if the number of groups exceeds the limit.

## Hints

### join_overflow_mode
Type: String

Default: `THROW`

Defines the behavior of the engine when the number of groups exceeds the limit defined by the `max_rows_in_join` hint.
The possible values are:
- `THROW`: The query will fail if the number of groups exceeds the limit.
- `BREAK`: The engine will stop processing the join and return the results that have been computed so far. In this case
  the stat `maxRowsInJoinReached` will be true.

### max_rows_in_join
Type: Integer

Default: 1.048.576

The maximum number of groups that can be created by the join keys. What happens when this limit is reached is defined by
the `join_overflow_mode` hint.

{% hint style="warn" %}
Take care when increasing this limit. If the number of groups is too high, the amount of memory used by the engine can
be very high, which can lead to very large GC pauses and even out of memory errors.
{% endhint %}

<!-- TODO
### join_strategy
Type: List of Strings separated by commas.

Default: `""`
If set, the engine will use the join strategy defined in the hint. The possible values are:
- `hash_table`: The default join strategy. The engine will use a hash join algorithm to join the relations.
- `dynamic_broadcast`: The engine will use a broadcast join algorithm to join the relations. This is useful when the
  right relation is small enough to be broadcasted to all workers.

When this hint is not defined (or if it is defined to `""`), the engine will use the hash join algorithm in most of the
cases but will automatically try to use the broadcast join algorithm used to optimize SEMI-JOIN queries.

{% hint style="warn" %}
By providing this hint, the engine will try to use the join strategy defined in the hint, even if it is not the most 
efficient. This can be useful to test the performance of different join strategies in the SEMI-JOIN case or to
disable co-located joins.
It is not recommended to use this hint in normal queries.
{% endhint %}

### is_colocated_by_join_keys
END OF TODO -->

## Stats
### executionTimeMs
Type: Long

The summation of time spent by all threads executing the operator.
This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows
Type: Long

The number of groups emitted by the operator.
Joins can emit more rows than the input relations, so this value can be higher than the number of rows in the input.
Remember that the number of groups is limited by the `max_rows_in_join` hint and a large number of groups can lead to
high memory usage and long GC pauses, which can affect the performance of the whole system.

### maxRowsInJoinReached
Type: Boolean

This stat is set to true when the number of groups exceeds the limit defined by the `max_rows_in_join` hint.

Notice that by default the engine will throw an exception when this happens in which case no stat will be emitted.
Therefore this stat is only emitted when the `join_overflow_mode` hint is set to `BREAK`.

### timeBuildingHashTableMs
Type: Long

The time spent building the hash table used to probe the join keys, in milliseconds.

A large number here can indicate that the right relation is too large or the right relation is taking too long to be
processed.

## Explain attributes
The hash join operator is represented in the explain plan as a `LogicalJoin` explain node.

### condition
Type: Expression

The condition that is being applied to the rows to join the relations.
The expression may use indexed columns (`$0`, `$1`, etc), functions and literals.
The indexed columns are always 0-based.

For example, the following explain plan:

```
LogicalJoin(condition=[=($0, $1)], joinType=[inner])
  PinotLogicalExchange(distribution=[hash[0]])
    LogicalProject(userUUID=[$6])
      LogicalTableScan(table=[[default, userAttributes]])
  PinotLogicalExchange(distribution=[hash[0]])
    LogicalProject(userUUID=[$4])
      LogicalTableScan(table=[[default, userGroups]])
```

Is saying that the join condition is that the column with index 0 in the left relation is equal to the column with 
index 1 in the right relation.
Given the rest of the explain plan, we can see that the column with index 0 `userUUID` column in the `userAttributes` 
table and the column with index 1 is the `userUUID` column in the `userGroups` table.

### joinType
Type: String

The type of join that is being performed. The possible values are: `inner`, `left`, `right`, `full`, `semi` and `anti`,
as explained in [Implementation details](#implementation-details).

## Tips and tricks

### The order of input relations matter
Apache Pinot does not use table stats to determine the best order to consume the input relations.
Instead, it assumes that the right input relation is the smaller one.
That relation will always be fully consumed to build a hash table and sometimes it will be broadcasted to all workers.
This means that it is important to specify the smaller relation as the right input.

Remember that left and right are relative to the order of the tables in the SQL query.
It is less expensive to do a join between a large table and a small table than the other way around.

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

<!-- TODO
### Co-located joins
END OF TODO -->

<!-- TODO
### Semi-join and pipeline breaker
END OF TODO -->

