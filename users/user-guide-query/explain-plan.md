# Explain Plan

Query execution within Pinot is modeled as a sequence of operators that are executed in a pipelined manner to produce the final result. The output of the EXPLAIN PLAN statement can be used to see how queries are being run or to further optimize queries.

## Introduction

EXPLAN PLAN can be run in two modes: verbose and non-verbose (default) via the use of a query option. To enable verbose mode the query option `explainPlanVerbose=true` must be passed.

```
EXPLAIN PLAN FOR SELECT playerID, playerName FROM baseballStats

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

In the non-verbose EXPLAIN PLAN output above, the `Operator` column describes the operator that Pinot will run where as, the `Operator_Id` and `Parent_Id` columns show the parent-child relationship between operators.&#x20;

This parent-child relationship shows the order in which operators execute. For example, `FILTER_MATCH_ENTIRE_SEGMENT` will execute before and pass its output to `PROJECT`. Similarly, `PROJECT` will execute before and pass its output to `TRANSFORM_PASSTHROUGH` operator and so on.&#x20;

Although the EXPLAIN PLAN query produces tabular output, in this document, we show a tree representation of the EXPLAIN PLAN output so that parent-child relationship between operators are easy to see and user can visualize the **bottom-up flow of data** in the operator tree execution.

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

Note a special node with the `Operator_Id` and `Parent_Id` called `PLAN_START(numSegmentsForThisPlan:1)`. This node indicates the number of segments which match a given plan. The EXPLAIN PLAN query can be run with the verbose mode enabled using the query option `explainPlanVerbose=true` which will show the varying deduplicated query plans across all segments across all servers.

EXPLAIN PLAN output should only be used for informational purposes because it is likely to change from version to version as Pinot is further developed and enhanced. Pinot uses a "Scatter Gather" approach to query evaluation (see [Pinot Architecture](https://docs.pinot.apache.org/basics/architecture) for more details). At the Broker, an incoming query is split into several server-level queries for each backend server to evaluate. At each Server, the query is further split into segment-level queries that are evaluated against each segment on the server. The results of segment queries are combined and sent to the Broker. The Broker in turn combines the results from all the Servers and sends the final results back to the user. Note that if the EXPLAIN PLAN query runs without the verbose mode enabled, a single plan will be returned (the heuristic used is to return the deepest plan tree) and this may not be an accurate representation of all plans across all segments. Different segments may execute the plan in a slightly different way.

Reading the EXPLAIN PLAN output from bottom to top will show how data flows from a table to query results. In the example shown above, the `FILTER_MATCH_ENTIRE_SEGMENT` operator shows that all 977889 records of the segment matched the query. The `DOC_ID_SET` over the filter operator gets the set of document IDs matching the filter operator. The `PROJECT` operator over the `DOC_ID_SET` operator pulls only those columns that were referenced in the query. The `TRANSFORM_PASSTHROUGH` operator just passes the column data from `PROJECT` operator to the `SELECT` operator. At `SELECT`, the query has been successfully evaluated against one segment. Results from different data segments are then combined (`COMBINE_SELECT`) and sent to the Broker. The Broker combines and reduces the results from different servers (`BROKER_REDUCE`) into a final result that is sent to the user. The `PLAN_START(numSegmentsForThisPlan:1)` indicates that a single segment matched this query plan. If verbose mode is enabled many plans can be returned and each will contain a node indicating the number of matched segments.

The rest of this document illustrates the EXPLAIN PLAN output with examples and describe the operators that show up in the output of the EXPLAIN PLAN.

## EXPLAIN PLAN using verbose mode for a query that evaluates filters with and without index

```
SET explainPlanVerbose=true;
EXPLAIN PLAN FOR
  SELECT playerID, playerName
    FROM baseballStats
   WHERE playerID = 'aardsda01' AND playerName = 'David Allan'

BROKER_REDUCE(limit:10)
└── COMBINE_SELECT
    └── PLAN_START(numSegmentsForThisPlan:1)
        └── SELECT(selectList:playerID, playerName)
            └── TRANSFORM_PASSTHROUGH(playerID, playerName)
                └── PROJECT(playerName, playerID)
                    └── DOC_ID_SET
                        └── FILTER_AND
                            ├── FILTER_INVERTED_INDEX(indexLookUp:inverted_index,operator:EQ,predicate:playerID = 'aardsda01')
                            └── FILTER_FULL_SCAN(operator:EQ,predicate:playerName = 'David Allan')
    └── PLAN_START(numSegmentsForThisPlan:1)
        └── SELECT(selectList:playerID, playerName)
            └── TRANSFORM_PASSTHROUGH(playerID, playerName)
                └── PROJECT(playerName, playerID)
                    └── DOC_ID_SET
                        └── FILTER_EMPTY
```

Since verbose mode is enabled, the EXPLAIN PLAN output returns two plans matching one segment each (assuming 2 segments for this table). The first EXPLAIN PLAN output above shows that Pinot used an inverted index to evaluate the predicate "playerID = 'aardsda01'" (`FILTER_INVERTED_INDEX`). The result was then fully scanned (`FILTER_FULL_SCAN`) to evaluate the second predicate "playerName = 'David Allan'". Note that the two predicates are being combined using `AND` in the query; hence, only the data that satsified the first predicate needs to be scanned for evaluating the second predicate. However, if the predicates were being combined using `OR`, the query would run very slowly because the entire "playerName" column would need to be scanned from top to bottom to look for values satisfying the second predicate. To improve query efficiency in such cases, one should consider indexing the "playerName" column as well. The second plan output shows a `FILTER_EMPTY` indicating that no matching documents were found for one segment.

## EXPLAIN PLAN ON GROUP BY QUERY

```
EXPLAIN PLAN FOR
  SELECT playerID, count(*)
    FROM baseballStats
   WHERE playerID != 'aardsda01'
   GROUP BY playerID

BROKER_REDUCE(limit:10)
└── COMBINE_GROUPBY_ORDERBY
    └── PLAN_START(numSegmentsForThisPlan:1)
        └── AGGREGATE_GROUPBY_ORDERBY(groupKeys:playerID, aggregations:count(*))
            └── TRANORM_PASSTHROUGH(playerID)
                └── PROJECT(playerID)
                    └── DOC_ID_SET
                        └── FILTER_INVERTED_INDEX(indexLookUp:inverted_index,operator:NOT_EQ,predicate:playerID != 'aardsda01')
```

The EXPLAIN PLAN output above shows how GROUP BY queries are evaluated in Pinot. GROUP BY results are created on the server (`AGGREGATE_GROUPBY_ORDERBY`) for each segment on the server. The server then combines segment-level GROUP BY results (`COMBINE_GROUPBY_ORDERBY`) and sends the combined result to the Broker. The Broker combines GROUP BY result from all the servers to produce the final result which is send to the user. Note that the `COMBINE_SELECT` operator from the previous query was not used here, instead a different `COMBINE_GROUPBY_ORDERBY` operator was used. Depending upon the type of query different combine operators such as `COMBINE_DISTINCT` and `COMBINE_ORDERBY` etc may be seen.

## EXPLAIN PLAN OPERATORS

The root operator of the EXPLAIN PLAN output is `BROKER_REDUCE`. `BROKER_REDUCE` indicates that Broker is processing and combining server results into final result that is sent back to the user. `BROKER_REDUCE` has a COMBINE operator as its child. Combine operator combines the results of query evaluation from each segment on the server and sends the combined result to the Broker. There are several combine operators (`COMBINE_GROUPBY_ORDERBY`, `COMBINE_DISTINCT`, `COMBINE_AGGREGATE`, etc.) that run depending upon the operations being performed by the query. Under the Combine operator, either a Select (`SELECT`, `SELECT_ORDERBY`, etc.) or an Aggregate (`AGGREGATE`, `AGGREGATE_GROUPBY_ORDERBY`, etc.) can appear. Aggreate operator is present when query performs aggregation (`count(*)`, `min`, `max`, etc.); otherwise, a Select operator is present. If the query performs scalar transformations (Addition, Multiplication, Concat, etc.), then one would see TRANSFORM operator appear under the SELECT operator. Often a `TRANSFORM_PASSTHROUGH` operator is present instead of the TRANSFORM operator. `TRANSFORM_PASSTHROUGH` just passes results from operators that appear lower in the operator execution heirarchy to the SELECT operator. `DOC_ID_SET` operator usually appear above FILTER operators and indicate that a list of matching document IDs are assessed. FILTER operators usually appear at the bottom of the operator heirarchy and show index use. For example, the presence of FILTER\_FULL\_SCAN indicates that index was not used (and hence the query is likely to run relatively slow). However, if the query used an index one of the indexed filter operators (`FILTER_SORTED_INDEX`, `FILTER_RANGE_INDEX`, `FILTER_INVERTED_INDEX`, `FILTER_JSON_INDEX`, etc.) will show up.
