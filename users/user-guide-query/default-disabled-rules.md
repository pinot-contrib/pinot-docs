# Default Disabled Rules

At this point, Pinot uses Calcite's 
[HepPlanner](https://calcite.apache.org/javadocAggregate/org/apache/calcite/plan/hep/HepPlanner.html) 
for multi-stage query optimization, without cardinality estimation and or cost-based search. This means any 
transformation rule that is enabled will be fired once its condition matches. 

There are certain rules that 
are helpful and only helpful under certain circumstances (with certain selectivity and cardinality conditions). 
We disable them by default and list them here for users to enable on demand.

## Default Disabled Rules

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
