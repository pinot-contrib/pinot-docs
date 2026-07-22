# Default Disabled Rules

At this point, Pinot uses Calcite's
[HepPlanner](https://calcite.apache.org/javadocAggregate/org/apache/calcite/plan/hep/HepPlanner.html)
for multi-stage query optimization without cardinality estimation or cost-based search. This means any
transformation rule that is enabled will fire once its condition matches.

There are certain rules that
are helpful only under certain selectivity and cardinality conditions.
We disable them by default and list Pinot's built-in default set here for users to enable on demand.

Brokers can replace this built-in set with the `pinot.broker.mse.planner.disabled.rules` config. When they do, the `usePlannerRules` query option applies to the broker-configured set instead of the built-in list below.

If you replace the built-in set at the broker level, include any rules that should stay opt-in in that configured list. For example, leaving `SortProjectTranspose` out of `pinot.broker.mse.planner.disabled.rules` removes it from the disabled-by-default set, so queries would no longer need `usePlannerRules` to enable it.

## Default Disabled Rules

### JOIN_TO_ENRICHED_JOIN

#### About

`JOIN_TO_ENRICHED_JOIN` is deprecated. Pinot removed the experimental enriched join optimization, and current brokers no longer register this planner rule. Queries that still request `JoinToEnrichedJoin` continue to plan successfully, but Pinot silently ignores the rule name and produces a normal join plan instead.

#### Use Case

Do not enable this rule for new workloads. Keep older `usePlannerRules='JoinToEnrichedJoin'` references only until you clean them up; Pinot ignores them instead of failing.

#### Example

For example:
```sql
SET usePlannerRules='JoinToEnrichedJoin';
EXPLAIN PLAN FOR
SELECT a.col1 + b.col1
FROM a
JOIN b ON a.col1 = b.col1;
```

The explain plan should contain a regular join such as `LogicalJoin` and should not contain `EnrichedJoin`.




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

### SORT_PROJECT_TRANSPOSE

#### About
Calcite's [SORT_PROJECT_TRANSPOSE](https://calcite.apache.org/javadocAggregate/org/apache/calcite/rel/rules/CoreRules.html#SORT_PROJECT_TRANSPOSE).
This rule pushes a `Sort` below a `Project`, which lets Pinot apply `ORDER BY ... LIMIT` before it evaluates the projection expressions.

Pinot keeps this rule disabled by default. Enabling it in the main logical phase can prevent the semi-join rewrite used by partition-hinted `IN (SELECT)` queries, so Pinot exposes it as an opt-in rule through `usePlannerRules`.

#### Use case
Consider enabling this rule when a query has projection work above a sort-limit and you want Pinot to trim the rows before evaluating the projected expressions.
`SET usePlannerRules='SortProjectTranspose';`

#### Example
Example query:
```sql
SET usePlannerRules='SortProjectTranspose';
SELECT city_name
FROM (
    SELECT LOWER(city) AS city_name, eventTime
    FROM dimStore
)
ORDER BY eventTime DESC
LIMIT 100
```
