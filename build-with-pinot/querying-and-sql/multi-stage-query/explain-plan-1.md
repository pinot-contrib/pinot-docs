# Explain Plan

Query execution within Pinot is modeled as a sequence of operators that are executed in a pipelined manner to produce the final result. The `EXPLAIN PLAN FOR` syntax can be used to obtain the execution plan of a query, which can be useful to further optimize them.

{% hint style="warning" %}
The explain plan output format is still under development and may change in future releases. This under-development label applies to the explain plan output format specifically, not to the core multi-stage engine, which is generally available. Pinot explain plans are human-readable and are intended to be used for debugging and optimization purposes. This is especially important when using the explain plan in automated scripts or tools. The explain plan, even the ones returned as tables or JSON, are not guaranteed to be stable across releases.
{% endhint %}

Pinot supports different type of explain plans depending on the query engine and the granularity or details we want to obtain.

```mermaid
graph LR
    EXPLAIN
    
    STAGE{"single or \n multi-stage?"}
   


    SSE_Q_VERBOSE{verbose?}
    SSE_SIMPLE[brief SSE]
    SSE_EXTENDED[verbose SSE]

    MSE_WORKERS[workers MSE]
    MSE_LOGICAL[logical MSE]
    MSE_Q_VERBOSE{verbose?}
    MSE_IMPL_SIMPLE["brief segment MSE"]
    MSE_IMPL_VERBOSE["verbose segment MSE"]
    
    EXPLAIN --> STAGE
    STAGE -- single --> SSE_Q_VERBOSE
    STAGE -- multi --> MSE_Q_DISTRIBUTION{workers?}
    
    SSE_Q_VERBOSE -- no --> SSE_SIMPLE
    SSE_Q_VERBOSE -- yes --> SSE_EXTENDED
    
    MSE_Q_DISTRIBUTION -- yes --> MSE_WORKERS
    MSE_Q_DISTRIBUTION -- no --> MSE_Q_LOGICAL{logical?}
    
    MSE_Q_LOGICAL -- yes --> MSE_LOGICAL
    MSE_Q_LOGICAL -- no --> MSE_Q_VERBOSE
    
    MSE_Q_VERBOSE -- yes --> MSE_IMPL_VERBOSE
    MSE_Q_VERBOSE -- no --> MSE_IMPL_SIMPLE
```

## Different plans for different segments [](#different-plans-for-different-segments)

Segments are the basic unit of data storage and processing in Pinot. When a query is executed, it is executed on each segment and the results are merged together. Not all segments have the data distribution, indexes, etc. Therefore the query engine may decide to execute the query differently on different segments. This includes:

* Segments that were not refreshed since indexes were added or removed on the table config.
* Realtime segments that are being ingested, where some indexes (like range indexes) cannot be used.
* Data distribution, specially min and max values for columns, which can affect the query plan.

Given a Pinot query can touch thousands of segments, Pinot tries to minimize the number of [different queries](#user-content-fn-1)[^1] shown when explaining a query. By default, Pinot tries to analyze the plan for each segment and returns a simplified plan. How this simplification is done depends on the query engine, you can read more about that below.

There is a verbose mode that can be used to show the plan for each segment. This mode is activated by setting the `explainPlanVerbose` query option to true, prefixing `SET explainPlanVerbose=true;` to the explain plan sentence.

## Explain on multi-stage query engine

Following the more complex nature of the multi-stage query engine, its explain plan can be customized to get a plan specialized[^2] on different aspects of the query execution.

There are 3 different types of explain plans for the multi-stage query engine:

| Mode         | Syntax by default                                                                                          | Syntax if segment plan is enabled         | Description                                                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Segment plan | `SET explainAskingServers=true;` `EXPLAIN PLAN FOR` | `EXPLAIN PLAN FOR` | Includes the segment specific information (like indexes). |
| Logical plan | `EXPLAIN PLAN FOR` or `EXPLAIN PLAN WITHOUT IMPLEMENTATION FOR` | `EXPLAIN PLAN WITHOUT IMPLEMENTATION FOR` | Simplest multi-stage plan. No index or data shuffle information. |
| Workers plan | `EXPLAIN IMPLEMENTATION PLAN FOR` | `EXPLAIN IMPLEMENTATION PLAN FOR` | Used to understand data shuffle between servers. Note: The name of this mode is open to discussion and may change in the future. |



{% hint style="info" %}
The syntax used to select each explain plan mode is confusing and it may be changed in the future.
{% endhint %}

### Segment plan [](#segment-plan)

The plan with segments is a detailed representation of the query execution plan that includes the segment specific information, like data distribution, indexes, etc.

This mode was introduced in Pinot 1.3.0 and it is planned to be the default in future releases. Meanwhile it can be used by setting the `explainAskingServers` query option to true, prefixing `SET explainAskingServers=true;` to the explain plan sentence. Alternatively this mode can be activated by default by changing the broker configuration `pinot.query.multistage.explain.include.segment.plan` to true.

Independently of how it is activated, once this mode is enabled, `EXPLAIN PLAN FOR` syntax will include segment information.

#### Verbose and brief mode

As explained in `Different plans for different segments`, by default Pinot tries to minimize the number of [different query](#user-content-fn-3)[^3] shown when explaining a query. In multi-stage, the brief mode groups distinct segment plans into `Alternative(segments=[n])` branches, where `n` is the number of segments using that plan. Equivalent plans are aggregated into the same branch, so if the same plan is executed on 100 segments, the brief mode will show it only once and additive stats such as the number of docs will be summed.

If some segments use a different plan, brief mode keeps one `Alternative` branch per distinct plan instead of falling back to one child per segment. When every segment shares the same plan, Pinot removes the redundant single `Alternative` wrapper after merging, so the common case still renders as a single child under the combine node.

In the verbose mode, one plan is shown per segment, including the segment name and all the segment specific information. This may be useful to know which segments are not using indexes, or which segments are using a different data distribution.

#### Example

```sql
-- SET explainAskingServer= true is required if 
-- pinot.query.multistage.explain.include.segment.plan is false, 
-- optional otherise
SET explainAskingServers=true;
EXPLAIN PLAN FOR
SELECT DISTINCT deviceOS, groupUUID
FROM userAttributes AS a
JOIN userGroups AS g
ON a.userUUID = g.userUUID
WHERE g.groupUUID = 'group-1'
LIMIT 100
```

Returns

```
Execution Plan
LogicalSort(offset=[0], fetch=[100])
  PinotLogicalSortExchange(distribution=[hash], collation=[[]], isSortOnSender=[false], isSortOnReceiver=[false])
    LogicalSort(fetch=[100])
      PinotLogicalAggregate(group=[{0, 1}])
        PinotLogicalExchange(distribution=[hash[0, 1]])
          PinotLogicalAggregate(group=[{0, 2}])
            LogicalJoin(condition=[=($1, $3)], joinType=[inner])
              PinotLogicalExchange(distribution=[hash[1]])
                LeafStageCombineOperator(table=[userAttributes])
                  StreamingInstanceResponse
                    StreamingCombineSelect
                      SelectStreaming(table=[userAttributes], totalDocs=[10000])
                        Project(columns=[[deviceOS, userUUID]])
                          DocIdSet(maxDocs=[40000])
                            FilterMatchEntireSegment(numDocs=[10000])
              PinotLogicalExchange(distribution=[hash[1]])
                LeafStageCombineOperator(table=[userGroups])
                  StreamingInstanceResponse
                    StreamingCombineSelect
                      SelectStreaming(table=[userGroups], totalDocs=[2478])
                        Project(columns=[[groupUUID, userUUID]])
                          DocIdSet(maxDocs=[50000])
                            FilterInvertedIndex(predicate=[groupUUID = 'group-1'], indexLookUp=[inverted_index], operator=[EQ])
                      SelectStreaming(segment=[userGroups_OFFLINE_4], table=[userGroups], totalDocs=[4])
                        Project(columns=[[groupUUID, userUUID]])
                          DocIdSet(maxDocs=[10000])
                            FilterEmpty
                      SelectStreaming(segment=[userGroups_OFFLINE_6], table=[userGroups], totalDocs=[4])
                        Project(columns=[[groupUUID, userUUID]])
                          DocIdSet(maxDocs=[10000])
                            FilterMatchEntireSegment(numDocs=[4])
```

### Logical Plan

The logical plan is a high-level representation of the query execution plan. This plan is calculated on the broker without asking the servers for their segment specific plans. This means that the logical plan does not include the segment specific information, like data distribution, indexes, etc.

In Pinot 1.3.0, the logical plan is enabled by default and can be obtained by using `EXPLAIN PLAN FOR` syntax. Optionally, the segment plan can be enabled by default, in which case the logical plan can be obtained by using `EXPLAIN PLAN WITHOUT IMPLEMENTATION FOR` syntax.

{% hint style="info" %}
The recommended way to ask for logical plan is to use `EXPLAIN PLAN WITHOUT IMPLEMENTATION FOR` given this syntax is available in all versions of Pinot, independently of the configuration.
{% endhint %}

#### Example:

```sql
-- WITHOUT IMPLENTATION qualifier can be used to ensure logical plan is used
-- It can be used in any version of Pinot even when segment plan is enabled by default
EXPLAIN PLAN WITHOUT IMPLEMENTATION FOR 
SELECT DISTINCT deviceOS, groupUUID
FROM userAttributes AS a
JOIN userGroups AS g
ON a.userUUID = g.userUUID
WHERE g.groupUUID = 'group-1'
LIMIT 100
```

Returns:

```
Execution Plan
LogicalSort(offset=[0], fetch=[100])
  PinotLogicalSortExchange(distribution=[hash], collation=[[]], isSortOnSender=[false], isSortOnReceiver=[false])
    LogicalSort(fetch=[100])
      PinotLogicalAggregate(group=[{0, 1}])
        PinotLogicalExchange(distribution=[hash[0, 1]])
          PinotLogicalAggregate(group=[{0, 2}])
            LogicalJoin(condition=[=($1, $3)], joinType=[inner])
              PinotLogicalExchange(distribution=[hash[1]])
                LogicalProject(deviceOS=[$4], userUUID=[$6])
                  LogicalTableScan(table=[[default, userAttributes]])
              PinotLogicalExchange(distribution=[hash[1]])
                LogicalProject(groupUUID=[$3], userUUID=[$4])
                  LogicalFilter(condition=[=($3, _UTF-8'group-1')])
                    LogicalTableScan(table=[[default, userGroups]])
```

### Workers plan

{% hint style="info" %}
There have been some discussion about how to name this explain mode and it may change in future versions. The term _worker_ is leaking an implementation detail that is not explained anywhere else in the user documentation.
{% endhint %}

The workers plan is a detailed representation of the query execution plan that includes information on how the query is distributed among different servers and workers inside them. This plan does not include the segment specific information, like data distribution, indexes, etc. and it is probably the less[^4] useful of the plans for normal use cases.

Their main use case is to try to reduce data shuffling between workers by verifying that, for example, a join is executed in colocated fashion.

#### Example

```sql
EXPLAIN IMPLEMENTATION PLAN FOR
SELECT DISTINCT deviceOS, groupUUID
FROM userAttributes AS a
JOIN userGroups AS g
ON a.userUUID = g.userUUID
WHERE g.groupUUID = 'group-1'
LIMIT 100
```

Returns:

```
0]@192.168.0.98:54196|[0] MAIL_RECEIVE(BROADCAST_DISTRIBUTED)
├── [1]@192.168.0.98:54227|[3] MAIL_SEND(BROADCAST_DISTRIBUTED)->{[0]@192.168.0.98:54196|[0]} (Subtree Omitted)
├── [1]@192.168.0.98:54220|[2] MAIL_SEND(BROADCAST_DISTRIBUTED)->{[0]@192.168.0.98:54196|[0]} (Subtree Omitted)
├── [1]@192.168.0.98:54214|[1] MAIL_SEND(BROADCAST_DISTRIBUTED)->{[0]@192.168.0.98:54196|[0]} (Subtree Omitted)
└── [1]@192.168.0.98:54206|[0] MAIL_SEND(BROADCAST_DISTRIBUTED)->{[0]@192.168.0.98:54196|[0]}
    └── [1]@192.168.0.98:54206|[0] SORT LIMIT 100
        └── [1]@192.168.0.98:54206|[0] MAIL_RECEIVE(HASH_DISTRIBUTED)
            ├── [2]@192.168.0.98:54227|[3] MAIL_SEND(HASH_DISTRIBUTED)->{[1]@192.168.0.98:54207|[0],[1]@192.168.0.98:54215|[1],[1]@192.168.0.98:54221|[2],[1]@192.168.0.98:54228|[3]} (Subtree Omitted)
            ├── [2]@192.168.0.98:54220|[2] MAIL_SEND(HASH_DISTRIBUTED)->{[1]@192.168.0.98:54207|[0],[1]@192.168.0.98:54215|[1],[1]@192.168.0.98:54221|[2],[1]@192.168.0.98:54228|[3]} (Subtree Omitted)
            ├── [2]@192.168.0.98:54214|[1] MAIL_SEND(HASH_DISTRIBUTED)->{[1]@192.168.0.98:54207|[0],[1]@192.168.0.98:54215|[1],[1]@192.168.0.98:54221|[2],[1]@192.168.0.98:54228|[3]} (Subtree Omitted)
            └── [2]@192.168.0.98:54206|[0] MAIL_SEND(HASH_DISTRIBUTED)->{[1]@192.168.0.98:54207|[0],[1]@192.168.0.98:54215|[1],[1]@192.168.0.98:54221|[2],[1]@192.168.0.98:54228|[3]}
                └── [2]@192.168.0.98:54206|[0] SORT LIMIT 100
                    └── [2]@192.168.0.98:54206|[0] AGGREGATE_FINAL
                        └── [2]@192.168.0.98:54206|[0] MAIL_RECEIVE(HASH_DISTRIBUTED)
                            ├── [3]@192.168.0.98:54227|[3] MAIL_SEND(HASH_DISTRIBUTED)->{[2]@192.168.0.98:54207|[0],[2]@192.168.0.98:54215|[1],[2]@192.168.0.98:54221|[2],[2]@192.168.0.98:54228|[3]} (Subtree Omitted)
                            ├── [3]@192.168.0.98:54220|[2] MAIL_SEND(HASH_DISTRIBUTED)->{[2]@192.168.0.98:54207|[0],[2]@192.168.0.98:54215|[1],[2]@192.168.0.98:54221|[2],[2]@192.168.0.98:54228|[3]} (Subtree Omitted)
                            ├── [3]@192.168.0.98:54214|[1] MAIL_SEND(HASH_DISTRIBUTED)->{[2]@192.168.0.98:54207|[0],[2]@192.168.0.98:54215|[1],[2]@192.168.0.98:54221|[2],[2]@192.168.0.98:54228|[3]} (Subtree Omitted)
                            └── [3]@192.168.0.98:54206|[0] MAIL_SEND(HASH_DISTRIBUTED)->{[2]@192.168.0.98:54207|[0],[2]@192.168.0.98:54215|[1],[2]@192.168.0.98:54221|[2],[2]@192.168.0.98:54228|[3]}
                                └── [3]@192.168.0.98:54206|[0] AGGREGATE_LEAF
                                    └── [3]@192.168.0.98:54206|[0] JOIN
                                        ├── [3]@192.168.0.98:54206|[0] MAIL_RECEIVE(HASH_DISTRIBUTED)
                                        │   ├── [4]@192.168.0.98:54227|[1] MAIL_SEND(HASH_DISTRIBUTED)->{[3]@192.168.0.98:54207|[0],[3]@192.168.0.98:54215|[1],[3]@192.168.0.98:54221|[2],[3]@192.168.0.98:54228|[3]} (Subtree Omitted)
                                        │   └── [4]@192.168.0.98:54214|[0] MAIL_SEND(HASH_DISTRIBUTED)->{[3]@192.168.0.98:54207|[0],[3]@192.168.0.98:54215|[1],[3]@192.168.0.98:54221|[2],[3]@192.168.0.98:54228|[3]}
                                        │       └── [4]@192.168.0.98:54214|[0] PROJECT
                                        │           └── [4]@192.168.0.98:54214|[0] TABLE SCAN (userAttributes) null
                                        └── [3]@192.168.0.98:54206|[0] MAIL_RECEIVE(HASH_DISTRIBUTED)
                                            ├── [5]@192.168.0.98:54227|[1] MAIL_SEND(HASH_DISTRIBUTED)->{[3]@192.168.0.98:54207|[0],[3]@192.168.0.98:54215|[1],[3]@192.168.0.98:54221|[2],[3]@192.168.0.98:54228|[3]} (Subtree Omitted)
                                            └── [5]@192.168.0.98:54214|[0] MAIL_SEND(HASH_DISTRIBUTED)->{[3]@192.168.0.98:54207|[0],[3]@192.168.0.98:54215|[1],[3]@192.168.0.98:54221|[2],[3]@192.168.0.98:54228|[3]}
                                                └── [5]@192.168.0.98:54214|[0] PROJECT
                                                    └── [5]@192.168.0.98:54214|[0] FILTER
                                                        └── [5]@192.168.0.98:54214|[0] TABLE SCAN (userGroups) null
```

## Interpreting multi-stage explain plans [](#interpreting-multi-stage-explain-plans)

Multi-stage plans are more complex than single-stage plans. This section explains how to interpret them.

You can use the `EXPLAIN PLAN` syntax to obtain the logical plan of a query. There are different formats for the output, but all of them represent the logical plan of the query.

The query

```sql
explain plan for
select customer.c_address, orders.o_shippriority
from customer
join orders
    on customer.c_custkey = orders.o_custkey
limit 10
```

Can produce the following output:

```
LogicalSort(offset=[0], fetch=[10])
  PinotLogicalSortExchange(distribution=[hash], collation=[[]], isSortOnSender=[false], isSortOnReceiver=[false])
    LogicalSort(fetch=[10])
      LogicalProject(c_address=[$0], o_shippriority=[$3])
        LogicalJoin(condition=[=($1, $2)], joinType=[inner])
          PinotLogicalExchange(distribution=[hash[1]])
            LogicalProject(c_address=[$4], c_custkey=[$6])
              LogicalTableScan(table=[[default, customer]])
          PinotLogicalExchange(distribution=[hash[0]])
            LogicalProject(o_custkey=[$5], o_shippriority=[$10])
              LogicalTableScan(table=[[default, orders]])
```

Each node in the tree represents an operation, and each operator has attributes. For example the `LogicalJoin` operator has a `condition` attribute that specifies the join condition and a `joinType`.

### Understanding indexed references

Expressions like `$2` are indexed references into the input row for each operator. To understand them, look at the operator's children to see which attributes are being referenced, usually starting from the leaf operators.

For example, `LogicalTableScan` always returns the whole row of the table, so its attributes are the columns of the table:

```
         PinotLogicalExchange(distribution=[hash[0]])
            LogicalProject(o_custkey=[$5], o_shippriority=[$10])
              LogicalTableScan(table=[[default, orders]])
```

The `LogicalProject` operator selects columns `o_custkey` and `o_shippriority` (at positions `$5` and `$10` in the table row) and generates a row with two columns. The `PinotLogicalExchange` distributes rows using `hash[0]`, meaning the hash of the first column from `LogicalProject` — which is `o_custkey`.

### Virtual rows in joins

The `LogicalJoin` operator receives rows from two upstream stages. The virtual row seen by the join is the concatenation of the left-hand side plus the right-hand side.

In the example above, the left stage sends `[c_address, c_custkey]` and the right stage sends `[o_custkey, o_shippriority]`. The join sees a row with columns `[c_address, c_custkey, o_custkey, o_shippriority]`. The condition `=($1, $2)` joins on `c_custkey` and `o_custkey`. The join passes through all columns unchanged, so its downstream `LogicalProject` selecting `$0` and `$3` produces `[c_address, o_shippriority]`.

### LogicalSort without ORDER BY

A `LogicalSort` operator can appear even when the SQL query has no `ORDER BY`. In relational algebra, a sort node is used to express `LIMIT`. When no sort condition is specified, no actual sorting is performed — only the row limit is applied.

## Explain on single stage query engine

{% hint style="info" %}
Explain plan for single stage query engine is described in deep in [explain-plan.md](../query-execution-controls/explain-plan.md)
{% endhint %}

Explain plan for single stage query engine is simpler and less customized, but returns the information in a tabular format. For example, the query `EXPLAIN PLAN FOR SELECT playerID, playerName FROM baseballStats`.&#x20;

\
Returns the following table:

```
+---------------------------------------------|------------|---------|
| Operator                                    | Operator_Id|Parent_Id|
+---------------------------------------------|------------|---------|
|BROKER_REDUCE(limit:10)                      | 1          | 0       |
|COMBINE_SELECT                               | 2          | 1       |
|PLAN_START(numSegmentsForThisPlan:1)         | -1         | -1      |
|SELECT(selectList:playerID, playerName)      | 3          | 2       |
|TRANSFORM_PASSTHROUGH(playerID, playerName)  | 4          | 3       |
|PROJECT(playerName, playerID)                | 5          | 4       |
|DOC_ID_SET                                   | 6          | 5       |
|FILTER_MATCH_ENTIRE_SEGMENT(docs:97889)      | 7          | 6       |
+---------------------------------------------|------------|---------|
```

Where `Operator` column describes the operator that Pinot will run whereas the `Operator_Id` and `Parent_Id` columns show the parent-child relationship between operators, which forms the execution tree. For example, the plan above should be understood as:

```
BROKER_REDUCE(limit:10)
└── COMBINE_SELECT
    └── PLAN_START(numSegmentsForThisPlan:1)
        └── SELECT(selectList:playerID, playerName)
            └── TRANSFORM_PASSTHROUGH(playerID, playerName)
                └── PROJECT(playerName, playerID)
                    └── DOC_ID_SET
                        └── FILTER_MATCH_ENTIRE_SEGMENT(docs:97889)
```

\


[^1]: 'different query plans' ?

[^2]: focused?

[^3]: different plans?

[^4]: least?
