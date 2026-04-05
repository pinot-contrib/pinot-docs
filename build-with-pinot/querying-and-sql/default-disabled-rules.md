# Default Disabled Rules

At this point, Pinot uses Calcite's 
[HepPlanner](https://calcite.apache.org/javadocAggregate/org/apache/calcite/plan/hep/HepPlanner.html) 
for multi-stage query optimization, without cardinality estimation and or cost-based search. This means any 
transformation rule that is enabled will be fired once its condition matches. 

There are certain rules that 
are helpful and only helpful under certain circumstances (with certain selectivity and cardinality conditions). 
We disable them by default and list Pinot's built-in default set here for users to enable on demand.

Brokers can replace this built-in set with the `pinot.broker.mse.planner.disabled.rules` config. When they do, the `usePlannerRules` query option applies to the broker-configured set instead of the built-in list below.

## Default Disabled Rules

### JOIN_TO_ENRICHED_JOIN

#### About

Enable Pinot's [JOIN_TO_ENRICHED_JOIN](https://github.com/apache/pinot/blob/master/pinot-query-planner/src/main/java/org/apache/pinot/calcite/rel/rules/PinotEnrichedJoinRule.java) that creates a [EnrichedHashJoinOpeartor](https://github.com/apache/pinot/blob/master/pinot-query-runtime/src/main/java/org/apache/pinot/query/runtime/operator/EnrichedHashJoinOperator.java) that fuses arbitrary combinations of filters, projections, and an optional limit into a HashJoin. This always avoids materializing intermediate results for join executions, which saves memory and speeds up join execution.

#### Use Case

Any case a hash join is followed a by projections and/or filters and/or limit. This is especially useful when there are projections that could not be pushed does the join (e.g. sum of two columns from each side), and filters that are based on such projections. This is also going to be useful when there's a LIMIT immediately after join. Sometimes, the filters and projections are pushed down the join by other optimizer rules, then this would have no effect. 

#### Example

For a simple **Projection-after-join** query over TPC-H, like:
```sql
SET usePlannerRules='JoinToEnrichedJoin';
SELECT l_tax FROM lineitem
JOIN orders ON l_orderkey = o_orderkey;
```
This optimization reduces join allocation by **>30%** and speeds up query by **>15%**.

Other example queries on which this might work includes:
**Limit after join**
```sql
SELECT * FROM lineitem JOIN orders ON l_orderkey = o_orderkey LIMIT 10;
```
**Filter over complex expressions after join**
```sql
SELECT * FROM (
    SELECT <complex_expression> AS result FROM lineitem JOIN orders ON l_orderkey = o_orderkey
) WHERE <complex_expression_over_result>;
```




### AGGREGATE_JOIN_TRANSPOSE_EXTENDED

#### About
Calcite's [AGGREGATE_JOIN_TRANSPOSE_EXTENDED](https://calcite.apache.org/javadocAggregate/org/apache/calcite/rel/rules/CoreRules.html#AGGREGATE_JOIN_TRANSPOSE_EXTENDED). \
This rule pushes / duplicates aggregation function down a join when the aggregation function is splitable.

#### Use case
Consider using this rule when the group-by reduces input cardinality by a large extent, and the aggregation function 
evaluation is inexpensive.
`SET usePlannerRules='AggregateJoinTransposeExtended';`

#### Example
Example query:
```sql
SELECT SUM(t1.b)
FROM t1 INNER JOIN t1
ON t1.a = t2.a
GROUP BY t1.a, t2.a
```

### SORT_JOIN_TRANSPOSE

#### About
Calcite's [SORT_JOIN_TRANSPOSE](https://calcite.apache.org/javadocAggregate/org/apache/calcite/rel/rules/CoreRules.html#SORT_JOIN_TRANSPOSE). 
    This pushes a sort with its limit below left/right outer join's preserve side when it could do so safely. 

#### Use case
Consider using this rule when there's sort-limit on preserve side on a left/right outer join. 
`SET usePlannerRules='SortJoinTranspose';`.

#### Example
Example query with TPC-H:
```sql
SELECT * 
FROM t1 LEFT JOIN t2
ON t1.a = t2.a
ORDER BY t1.a
LIMIT 100
```
