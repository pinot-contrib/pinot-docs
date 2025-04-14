---
description: Describes the union relation operator in the multi-stage query engine.
---

# Union

The union operator combines the results of two or more queries into a single result set. The result set contains all the rows from the queries. Contrary to other set operations ([intersect](intersect.md) and [minus](minus.md)), the union operator does not remove duplicates from the result set. Therefore its semantic is similar to the SQL `UNION` or `UNION ALL` operator.

There is no guarantee on the order of the rows in the result set.

{% hint style="info" %}
While `EXCEPT` and `INTERSECT` SQL clauses do not support the `ALL` modifier, the `UNION` clause does.
{% endhint %}

## Implementation details

The current implementation consumes input relations one by one. It first returns all rows from the first input relation, then all rows from the second input relation, and so on.

### Blocking nature

The union operator is a streaming operator that consumes the input relations one by one. The current implementation fully consumes the inputs in order. See [the order of input relations matter](union.md#the-order-of-input-relations-matter) for more details.

## Hints

None

## Stats

### executionTimeMs

Type: Long

The summation of time spent by all threads executing the operator. This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows

Type: Long

The number of groups emitted by the operator.

## Explain attributes

The union operator is represented in the explain plan as a `LogicalUnion` explain node.

### all

Type: Boolean

Whether the union operator should remove duplicates from the result set.

Although Pinot supports the SQL `UNION` and `UNION ALL` _clauses_, the union _operator_ does only support the `UNION ALL` semantic. In order to implement the `UNION` semantic, the multi-stage query engine adds an extra [aggregate](aggregate.md) to calculate the _distinct_.

For example the plan of:

```sql
select userUUID
from (select userUUID from userAttributes)
UNION ALL
(select userUUID from userGroups)
```

Is expected to be:

```
LogicalUnion(all=[true])
  PinotLogicalExchange(distribution=[hash[0]])
    LogicalProject(userUUID=[$6])
      LogicalTableScan(table=[[default, userAttributes]])
  PinotLogicalExchange(distribution=[hash[0]])
    LogicalProject(userUUID=[$4])
      LogicalTableScan(table=[[default, userGroups]])
```

While the plan of:

```sql
explain plan for
select userUUID
from (select userUUID from userAttributes)
UNION -- without ALL!
(select userUUID from userGroups)
```

Is a bit more complex

```
LogicalAggregate(group=[{0}])
  PinotLogicalExchange(distribution=[hash[0]])
    LogicalAggregate(group=[{0}])
      LogicalUnion(all=[true])
        PinotLogicalExchange(distribution=[hash[0]])
          LogicalProject(userUUID=[$6])
            LogicalTableScan(table=[[default, userAttributes]])
        PinotLogicalExchange(distribution=[hash[0]])
          LogicalProject(userUUID=[$4])
            LogicalTableScan(table=[[default, userGroups]])
```

Notice that `LogicalUnion` is still using `all=[true]` but the `LogicalAggregate` is used to remove the duplicates. This also means that while the union _operator_ is always streaming, the union _clause_ results in a blocking plan (given the [aggregate](aggregate.md#blocking-nature) operator is blocking).

## Tips and tricks

### The order of input relations matters

The current implementation of the union operator consumes the input relations one by one starting from the first one. This means that the second input relation is not consumed until the first one is fully consumed and so on. Therefore is recommended to put the fastest input relation first to reduce the overall latency.

Usually a good way to set the order of the input relations is to change the input order trying to minimize the value of the [downstreamWaitMs](mailbox-receive.md#downstreamwaitms) stat of all the inputs.
