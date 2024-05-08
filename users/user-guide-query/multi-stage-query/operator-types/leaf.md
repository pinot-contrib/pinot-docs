---
description: >-
  Describes the leaf operator in the multi-stage query engine.
---

# Leaf operator

The leaf operator is the last operator in the query execution plan.
This is in fact a meta-operator that wraps the single-stage query engine and executes all the operators in the leaf
stage of the query plan.

## Implementation details

The leaf operator is not a relational operator itself but a meta-operator that wraps the single-stage query engine.
When servers execute a leaf stage, they compile all operations in the stage but the send operator into the equivalent
single-stage query and execute that using a slightly modified version of the single-stage engine.

As a result, there may be slight differences when an operator is executed in a leaf stage compared to when it is 
executed in an intermediate stage.
For example, operations pushed down to the leaf stage may use indexes 
(see [how to know if indexes are used](./filter#how-to-know-if-indexes-are-used)) or the semantics can be slightly
different.

You can read [Troubleshoot issues with the multi-stage query engine (v2)](../../../../reference/troubleshooting/troubleshoot-multi-stage-query-engine.md)
for more information on the differences between the leaf and intermediate stages, but the main ones are:
* Null handling is different.
* Some functions are only supported in multi-stage and some others only in single-stage.
* Type coercion is different. While the single-stage engine always operates with generic types (ie uses doubles when 
  mathematical operations are used), the multi-stage engine tries to keep the types (ie adding two integers will result 
  in an integer).

### Blocking nature
One of the slight differences between the leaf and the normal single-stage engine is that the leaf engine tries to
be not blocking.

## Hints

### partition_key
### partition_function
### partition_size
### partition_parallelism

## Stats
### executionTimeMs
Type: Long

The summation of time spent by all threads executing the operator.
This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows
Type: Long

The number of groups emitted by the operator.

### table
Type: String

The name of the table that is scanned. This is the name without the type suffix (so without `_REALTIME` or `_OFFLINE`).
This is very useful to understand which table is being scanned by this leaf stage in case of complex queries.

### numDocsScanned
Type: Long

Similar to the same stat in single-stage queries, this stat indicates the number of rows selected _after_ the 
filter phase.

If it is very high, that means the selectivity for the query is low and lots of rows need to be processed after the
filtering. 
Consider refining the filter to increase the selectivity of the query.

### numEntriesScannedInFilter
Type: Long

Similar to the same stat in single-stage queries, this stat indicates the number of entries (aka scalar values) scanned 
in the filtering phase of query execution.

Can be larger than the total scanned doc count because of multiple filtering predicates or multi-value entries.
Can also be smaller than the total scanned doc count if indexing is used for filtering.

This along with `numEntriesScannedPostFilter` indicates where most of the time is spent during table scan processing. 
If this value is high, enabling indexing for affected columns is a way to bring it down.
Another option is to partition the data based on the dimension most heavily used in your filter queries.

### numEntriesScannedPostFilter
Type: Long

Similar to the same stat in single-stage queries, this stat indicates the number of entries (aka scalar values) scanned
after the filtering phase of query execution, ie. aggregation and/or group-by phases. 
This is equivalent to `numDocScanned * number of projected columns`.

This along with `numEntriesScannedInFilter` indicates where most of the time is spent during table scan processing.
A high number for this means the selectivity is low (that is, Pinot needs to scan a lot of records to answer the query).
If this is high, consider using star-tree index, given a regular index won't improve performance.

### numSegmentsQueried
Type: Integer

Similar to the same stat in single-stage queries, this stat indicates the total number of segment queried for a query. 
May be less than the total number of segments if the broker applies optimizations. <!-- Can this happen in V2? -->

The broker decides how many segments to query on each server, based on broker pruning logic.
The server decides how many of these segments to actually look at, based on server pruning logic. 
After processing segments for a query, fewer may have the matching records. 

In general, `numSegmentsQueried >= numSegmentsProcessed >= numSegmentsMatched`.

### numSegmentsProcessed
Type: Integer

Similar to the same stat in single-stage queries, this stat indicates the number of segments processed with at least one
document matched in the query response.

The more segments are processed, the more IO has to be done.
This is why selective queries where `numSegmentsProcessed` is close to `numSegmentsQueried` can be optimized by
changing the data distribution.

### numSegmentsMatched
Type: Integer

Similar to the same stat in single-stage queries, this stat indicates the number of segment operators used to process 
segments. Indicates the effectiveness of the pruning logic.

### NUM_CONSUMING_SEGMENTS_QUERIED
Type: Integer

### MIN_CONSUMING_FRESHNESS_TIME_MS
Type: Long

### totalDocs
Type: Long

Similar to the same stat in single-stage queries, this stat indicates the number of rows in the table.

### numGroupsLimitReached
Type: Boolean

Similar to the same stat in single-stage queries and the same in [aggregate](./aggregate.md#numgroupslimitreached) 
operators, this stat indicates if the max group limit has been reached in a `group by` aggregation operator executed
in the leaf stage. 

If this boolean is set to true, the query result may not be accurate. 
The default value for `numGroupsLimit` is 100k, and should be sufficient for most use cases.

### NUM_RESIZES
Type: Integer

### RESIZE_TIME_MS
Type: Long

### THREAD_CPU_TIME_NS
Type: Long

### SYSTEM_ACTIVITIES_CPU_TIME_NS
Type: Long

### RESPONSE_SER_CPU_TIME_NS
Type: Long

### numServersPrunedByServer
Type: Integer

The number of segments pruned by the server.

### numSegmentsPrunedInvalid
Type: Integer

The number of segments pruned because they are invalid.
Segments are invalid when the schema has changed and the segment has not been refreshed.

For example, if a column is added to the schema, the segment will be invalid for queries that use that column until it
is refreshed.

### numSegmentsPrunedByLimit
Type: Integer

The number of segments pruned because they are not needed for the query due to the limit clause.

Pinot keeps a count of the number of rows returned by each segment.
Once is guaranteed that no more segments need to be read to satisfy the limit clause without breaking semantics, the 
remaining segments are pruned.

For example, a query like `SELECT col1 FROM table2 LIMIT 10` can be pruned for this reason while a query like
`SELECT col1 FROM table2 ORDER BY col1 DESC LIMIT 10` cannot because Pinot needs to read all segments to guarantee the
larger values of `col1` are returned.

### numSegmentsPrunedByValue
Type: Integer

The number of segments pruned because they are not needed for the query due to a value clause, usually a `where`.

Pinot keeps the maximum and minimum values of each segment for each column.
If the value clause is such that the segment cannot contain any rows that satisfy the clause, the segment is pruned.

### NUM_CONSUMING_SEGMENTS_PROCESSED
Type: Integer

### NUM_CONSUMING_SEGMENTS_MATCHED
Type: Integer

### NUM_BLOCKS
Type: Integer

### operatorExecutionTimeMs
Type: Long

The time spent by the operator executing.

### operatorExecStartTimeMs
Type: Long

The instant in time when the operator started executing.

### OPERATOR_EXEC_END_TIME_MS
Type: Long

The instant in time when the operator finished executing.

## Explain attributes

## Tips and tricks