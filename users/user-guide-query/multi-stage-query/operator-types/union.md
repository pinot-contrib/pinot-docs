---
description: >-
  Describes the union relation operator in the multi-stage query engine.
---

# Union relational operator

The union operator combines the results of two or more queries into a single result set.
The result set contains all the rows from the queries.
Contrary to other set operations ([intersect](intersect.md) and [minus](minus.md)), the union operator does not remove
duplicates from the result set.
Therefore its semantic is similar to the SQL `UNION ALL` operator.

There is no guarantee on the order of the rows in the result set.

## Implementation details
The current implementation consumes input relations one by one.
It first returns all rows from the first input relation, then all rows from the second input relation, and so on.

### Blocking nature
The union operator is a streaming operator that consumes the input relations one by one.
The current implementation fully consumes the inputs in order.
See [the order of input relations matter](#the-order-of-input-relations-matter) for more details.

## Hints
None

## Stats
### executionTimeMs
Type: Long

The summation of time spent by all threads executing the operator.
This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows
Type: Long

The number of groups emitted by the operator.

## Explain attributes

## Tips and tricks

### The order of input relations matter
The current implementation of the union operator consumes the input relations one by one starting from the first one.
This means that the second input relation is not consumed until the first one is fully consumed and so on.
Therefore is recommended to put the fastest input relation first to reduce the overall latency.

Usually a good way to set the order of the input relations is to change the input order trying to minimize the
value of the [downstreamWaitMs](mailbox-receive.md#downstreamwaitms) stat of all the inputs.
