---
description: Learn more about multi-stage stages and how to extract stages from query plans.
---

## Deep dive into stages
As explained in the [Multi-stage query engine](../../../reference/multi-stage-engine.md) reference documentation, 
the multi-stage query engine breaks down a query into multiple stages.
Each stage corresponds to a subset of the query plan and is executed independently.
Stages are connected in a tree-like structure where the output of one stage is the input to another stage.
The stage that is at the root of the tree sends the final results to the client.
The stages that are at the leaves of the tree read from the tables.
The intermediate stages process the data and send it to the next stage.

When the broker receives a query, it generates a query plan.
This is a tree-like structure where each node is an operator.
The plan is then optimized, moving and changing nodes to generate a plan that is semantically equivalent 
(it returns the same rows) but more efficient.
During this phase the broker colors the nodes of the plan, assigning them to a stage.
The broker also assigns a parallelism to each stage and defines which servers are going to execute each stage.
For example, if a stage has a parallelism of 10, then at most 10 servers will execute that stage in parallel.
One single server can execute multiple stages in parallel and it can even execute multiple instances of the same stage 
in parallel.

Stages are identified by their stage ID, which is a unique identifier for each stage.
In the current implementation the stage ID is a number and the root stage has a stage ID of 0, 
although this may change in the future.

The current implementation has some properties that are worth mentioning:
* The leaf stages execute a slightly modified version of the single-stage query engine. 
  Therefore these stages cannot execute joins or aggregations, which are always executed in the intermediate stages.
* Intermediate stages execute operations using a new query execution engine that has been created for the multi-stage 
  query engine. This is why some of the functions that are supported in the single-stage query engine are not supported
  in the multi-stage query engine and vice versa.
* An intermediate stage can only have one join, one window function or one set operation. If a query has more than one 
  of these operations, the broker will create multiple stages, each with one of these operations.


## Extracting Stages from Query Plans
As explained in [Explain Plan (Multi-Stage)](../query-syntax/explain-plan-multi-stage.md), you can use the 
`EXPLAIN PLAN` syntax to obtain the logical plan of a query.
This logical plan can be used to extract the stages of the query.

For example, if the query is:
```sql
explain plan for
select customer.c_address, orders.o_shippriority
from customer
join orders
    on customer.c_custkey = orders.o_custkey
limit 10
```

A possible output of the `EXPLAIN PLAN` command is:
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

As it happens with all queries, the logical plan forms a tree-like structure. 
In this default explain format, the tree-like structure is represented with indentation. 
The root of the tree is the first line, which is the last operator to be executed and marks the root stage.
The boundary between stages are the PinotLogicalExchange operators. In the example above, there are four stages:
* The root stage starts with the `LogicalSort` operator in the root of operators and ends with the 
  `PinotLogicalSortExchange` operator. 
  This is the last stage to be executed and the only one that is executed in the broker, which will directly send the 
  result to the client once it is computed.
* The next stage starts with this `PinotLogicalSortExchange` operator and includes the `LogicalSort` operator, 
  the `LogicalProject` operator, the `LogicalJoin` operator and the two `PinotLogicalExchange` operators. 
  This stage clearly is not a root stage and it is not reading data from the segments, so it is not a leaf stage. 
  Therefore it has to be an intermediate stage.
* The join has two children, which are the `PinotLogicalExchange` operators. 
  In this specific case, both sides are very similar. 
  They start with a `PinotLogicalExchange` operator and end with a `LogicalTableScan` operator. 
  All stages that end with a `LogicalTableScan` operator are leaf stages.

Now that we have identified the stages, we can understand what each stage is doing by 
[understanding multi-stage explain plans](./understanding-multi-stage-explain.md).