---
description: This document describes EXPLAIN PLAN syntax for multi-stage engine (v2)
---

# Explain Plan (Multi-Stage)

{% hint style="info" %}
This page explains how to use `EXPLAIN PLAN FOR` syntax to obtain different plans of a query in multi-stage engine. You can read more about how to interpret the plans in the [Understanding multi-stage explain plans](../multi-stage-query/understanding-multi-stage-explain.md) page.

Also remember that plans are logical representations of the query execution. Sometimes it is more useful to study the actual stats of the query execution, which are included on each query result. You can read more about how to interpret the stats in the [Understanding multi-stage stats](../multi-stage-query/understanding-stage-stats.md) page.
{% endhint %}

In [Single-stage engine Explain Plan](explain-plan.md), we do not differentiate any logical/physical plan b/c the structure of the query is fixed. By default it explain the Physical Plan

In multi-stage engine we support EXPLAIN PLAN syntax mostly following Apache Calcite's [EXPLAIN PLAN](https://calcite.apache.org/docs/reference.html) syntax. Here are several examples:

### Explain Logical Plan

Using SSB standard query example:

```
EXPLAIN PLAN FOR 
select 
  P_BRAND1, sum(LO_REVENUE) 
from ssb_lineorder_1, ssb_part_1
where LO_PARTKEY = P_PARTKEY 
  and P_CATEGORY = 'MFGR#12' 
group by P_BRAND1
```

The result field contains 2 columns and 1 row:

```
+-----------------------------------|-------------------------------------------------------------|
| SQL#$%0                           |PLAN#$%1                                                     |
+-----------------------------------|-------------------------------------------------------------|
|"EXPLAIN PLAN FOR                  |"Execution Plan                                              | 
|select                             |LogicalAggregate(group=[{0}], agg#0=[$SUM0($1)])             | 
|  P_BRAND1, sum(LO_REVENUE)        |  PinotLogicalExchange(distribution=[hash[0]])               | 
|from ssb_lineorder_1, ssb_part_1   |    LogicalAggregate(group=[{2}], agg#0=[$SUM0($1)])         | 
|where LO_PARTKEY = P_PARTKEY       |      LogicalJoin(condition=[=($0, $3)], joinType=[inner])   | 
|  and P_CATEGORY = 'MFGR#12'       |        PinotLogicalExchange(distribution=[hash[0]])         | 
|group by P_BRAND1                  |          LogicalProject(LO_PARTKEY=[$12], LO_REVENUE=[$14]) | 
|   and P_CATEGORY = 'MFGR#12'      |            LogicalTableScan(table=[[ssb_lineorder_1]])      | 
|"                                  |        PinotLogicalExchange(distribution=[hash[1]])         | 
|                                   |          LogicalProject(P_BRAND1=[$3], P_PARTKEY=[$9])      | 
|                                   |            LogicalFilter(condition=[=($4, 'MFGR#12')])      | 
|                                   |              LogicalTableScan(table=[[ssb_part_1]])         |
|                                   |"                                                            |
+-----------------------------------|-------------------------------------------------------------|
```

noted that all the normal options for EXPLAIN PLAN in Apache Calcite also works in Pinot with extra information including attributes, type, etc.

One of the most useful options is the `AS <format>`, which support the following formats:

* `JSON`, which returns the plan in a JSON format. This format is useful for parsing the plan in a program and it also provides some extra information that is not present in the default format.
* `XML`, which is similar to `JSON` but in XML format.
* `DOT`, which returns a DOT format that can be used to visualize the plan using tools like [Graphviz](https://graphviz.org/). This format is understandable by different tools, including online stateless pages.

### Explain Implementation Plan

If we want to gather the implementation plan specific to Pinot internal multi-stage engine operator chain. You can use the `EXPLAIN IMPLEMENTATION PLAN` :

```
+-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SQL#$%0                           |PLAN#$%1                                                                                                                                                         |  
+-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
|"EXPLAIN IMPLEMENTATION PLAN FOR   |[0]@local:8843 MAIL_RECEIVE(BROADCAST_DISTRIBUTED)                                                                                                               | 
|select                             |├── [1]@local:8432 MAIL_SEND(BROADCAST_DISTRIBUTED)->{[0]@local@{8843,8843}|[0]} (Subtree Omitted)                                                               | 
|  P_BRAND1, sum(LO_REVENUE)        |├── [1]@local:8432 MAIL_SEND(BROADCAST_DISTRIBUTED)->{[0]@local@{8843,8843}|[0]} (Subtree Omitted)                                                               | 
|from ssb_lineorder_1, ssb_part_1   |└── [1]@local:8432 MAIL_SEND(BROADCAST_DISTRIBUTED)->{[0]@local@{8843,8843}|[0]}                                                                                 | 
|where LO_PARTKEY = P_PARTKEY       |    └── [1]@local:8432 AGGREGATE_FINAL                                                                                                                           | 
|  and P_CATEGORY = 'MFGR#12'       |        └── [1]@local:8432 MAIL_RECEIVE(HASH_DISTRIBUTED)                                                                                                        | 
|group by P_BRAND1                  |            ├── [2]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[1]@local@{8432,8843}|[1],[1]@local@{8432,8843}|[2],[1]@local@{8432,8843}|[0]} (Subtree Omitted)    | 
|   and P_CATEGORY = 'MFGR#12'      |            ├── [2]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[1]@local@{8432,8843}|[1],[1]@local@{8432,8843}|[2],[1]@local@{8432,8843}|[0]} (Subtree Omitted)    | 
|"                                  |            └── [2]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[1]@local@{8432,8843}|[1],[1]@local@{8432,8843}|[2],[1]@local@{8432,8843}|[0]}                      | 
|                                   |                └── [2]@local:8432 AGGREGATE_LEAF                                                                                                                | 
|                                   |                    └── [2]@local:8432 JOIN                                                                                                                      | 
|                                   |                        ├── [2]@local:8432 MAIL_RECEIVE(HASH_DISTRIBUTED)                                                                                        | 
|                                   |                        │   ├── [3]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[2]@local@{8432,8843}|[1],[2]@local@{8432,8843}|[2],[2]@local@{8432,8843}|[0]}      | 
|                                   |                        │   │   └── [3]@local:8432 PROJECT                                                                                                       | 
|                                   |                        │   │       └── [3]@local:8432 TABLE SCAN (ssb_lineorder_1) null                                                                         | 
|                                   |                        │   ├── [3]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[2]@local@{8432,8843}|[1],[2]@local@{8432,8843}|[2],[2]@local@{8432,8843}|[0]}      | 
|                                   |                        │   │   └── [3]@local:8432 PROJECT                                                                                                       | 
|                                   |                        │   │       └── [3]@local:8432 TABLE SCAN (ssb_lineorder_1) null                                                                         | 
|                                   |                        │   └── [3]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[2]@local@{8432,8843}|[1],[2]@local@{8432,8843}|[2],[2]@local@{8432,8843}|[0]}      | 
|                                   |                        │       └── [3]@local:8432 PROJECT                                                                                                       | 
|                                   |                        │           └── [3]@local:8432 TABLE SCAN (ssb_lineorder_1) null                                                                         | 
|                                   |                        └── [2]@local:8432 MAIL_RECEIVE(HASH_DISTRIBUTED)                                                                                        | 
|                                   |                            ├── [4]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[2]@local@{8432,8843}|[1],[2]@local@{8432,8843}|[2],[2]@local@{8432,8843}|[0]}      | 
|                                   |                            │   └── [4]@local:8432 PROJECT                                                                                                       | 
|                                   |                            │       └── [4]@local:8432 FILTER                                                                                                    | 
|                                   |                            │           └── [4]@local:8432 TABLE SCAN (ssb_part_1) null                                                                          | 
|                                   |                            ├── [4]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[2]@local@{8432,8843}|[1],[2]@local@{8432,8843}|[2],[2]@local@{8432,8843}|[0]}      | 
|                                   |                            │   └── [4]@local:8432 PROJECT                                                                                                       | 
|                                   |                            │       └── [4]@local:8432 FILTER                                                                                                    | 
|                                   |                            │           └── [4]@local:8432 TABLE SCAN (ssb_part_1) null                                                                          | 
|                                   |                            └── [4]@local:8432 MAIL_SEND(HASH_DISTRIBUTED)->{[2]@local@{8432,8843}|[1],[2]@local@{8432,8843}|[2],[2]@local@{8432,8843}|[0]}      | 
|                                   |                                └── [4]@local:8432 PROJECT                                                                                                       | 
|                                   |                                    └── [4]@local:8432 FILTER                                                                                                    | 
|                                   |                                        └── [4]@local:8432 TABLE SCAN (ssb_part_1) null                                                                          | 
+-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|

```

Notes that now there is information regarding how many servers were used, and how are data being shuffled between nodes. etc.
