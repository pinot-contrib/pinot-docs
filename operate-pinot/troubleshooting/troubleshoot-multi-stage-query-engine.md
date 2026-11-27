---
description: Troubleshoot issues with the multi-stage engine (MSE).
---

# Troubleshoot issues with the multi-stage engine (MSE)

This page covers behavior differences between the single-stage engine (SSE) and multi-stage engine (MSE), current limitations, and a troubleshooting checklist for diagnosing query issues.

For instructions on enabling the MSE, see [SSE vs MSE](../../build-with-pinot/querying-and-sql/sse-vs-mse.md). For operational guidance on running MSE in production, see [Run the Multi-Stage Engine in Production](../production-guides/run-multi-stage-engine-in-production.md).

## Operator checklist

Run through these steps before investigating further:

1. **Confirm MSE is enabled.** Verify `useMultistageEngine=true` is set in the query options or broker configuration.
2. **Confirm query options.** Check that all required query options (timeouts, resource limits) are set appropriately for your workload.
3. **Inspect the explain plan.** Run `EXPLAIN PLAN FOR <query>` to verify the query compiles and the plan looks reasonable.
4. **Inspect stage stats.** Review stage-level statistics in the query response to identify which stage is slow or producing unexpected results.
5. **Verify guardrail and query-limit settings.** Check that server-side limits (max rows in join, max rows in window, stage timeout) are not causing premature termination.

## Behavior differences from SSE

The MSE enforces stricter SQL semantics than the SSE. The following sections describe specific differences that can affect query results or compatibility.

### Case sensitivity

In the MSE, table and column names are case sensitive. In the SSE, they were not. The following two queries are **not** equivalent in the MSE:

`select * from myTable`

`select * from mytable`

{% hint style="info" %}
**Note:** Function names are not case sensitive in either engine.
{% endhint %}

### Stricter type matching

The SSE automatically performs implicit type casts in many situations. For example:

```
timestampCol >= longCol
```

The SSE converts both values to long before comparison. The MSE enforces stricter datatype conformance, so the query above should be explicitly written as:

```
CAST(timestampCol AS BIGINT) >= longCol
```

### Projection naming differences

Default names for projections with function calls differ between the two engines.

In the MSE, the following query:

```sql
SELECT count(*) from myTable
```

Returns:

```
"columnNames": [
    "EXPR$0"
  ],
```

In the SSE, the same query returns:

```
"columnNames": [
    "count(*)"
  ],
```

If downstream code depends on column names in the response, use explicit aliases:

```sql
SELECT count(*) AS total_count FROM myTable
```

### CAST and type-name differences

The MSE uses SQL-standard type names. Although the original names are still required in schemas and some SQL expressions, the MSE names must be used in `CAST` expressions.

| SSE type name       | MSE type name      |
| ------------------- | ------------------ |
| NULL                | NULL               |
| BOOLEAN             | BOOLEAN            |
| INT                 | INT                |
| LONG                | BIGINT             |
| BIG\_DECIMAL        | DECIMAL            |
| FLOAT               | FLOAT/REAL         |
| DOUBLE              | DOUBLE             |
| INTERVAL            | INTERVAL           |
| TIMESTAMP           | TIMESTAMP          |
| STRING              | VARCHAR            |
| BYTES               | VARBINARY          |
| -                   | ARRAY              |
| JSON                | -                  |

### Varbinary literals

VARBINARY literals in the MSE must be prefixed with `X` or `x`:

```sql
SELECT col1, col2 FROM myTable WHERE bytesCol = X'4a220e6096b25eadb88358cb44068a3248254675'
```

In the SSE, the same query used an unprefixed hex string:

```sql
-- not supported in MSE
SELECT col1, col2 FROM myTable WHERE bytesCol = '4a220e6096b25eadb88358cb44068a3248254675'
```

### Return types for arithmetic operators (+, -, \*, /)

In the SSE, binary arithmetic operators always return `DOUBLE` regardless of operand types. In the MSE, the result type depends on the input types. For example, adding two `LONG` values returns a `LONG`.

### Return types for aggregations (SUM, MIN, MAX)

In the SSE, these aggregations always return `DOUBLE`. In the MSE, the result type matches the data type of the column being aggregated.

### NULL handling and storage

Null handling is not supported when tables use table-based null storing. Use column-based null storing instead. See [null handling support](../../build-with-pinot/querying-and-sql/null-value-support.md).

### Cluster config does not modify query behavior

The MSE does not read cluster-level configuration overrides for function parameters. `distinctcounthll`, `distinctcounthllmv`, `distinctcountrawhll`, and `distinctcountrawhllmv` always use the default value for `log2m` unless the value is explicitly provided in the query. The following query may produce different results between SSE and MSE depending on your cluster configuration (`default.hyperloglog.log2m`):

```sql
SELECT distinctcounthll(col) FROM myTable
```

To get consistent results across both engines, specify the `log2m` parameter explicitly:


```sql
SELECT distinctcounthll(col, 8) FROM myTable
```

### Multi-value column behavior

In the MSE, a multi-value (MV) column has the SQL type `ARRAY`. You can project an MV column without changes. To filter or group by the elements of an MV column, wrap the column in the `arrayToMv` function. `arrayToMv` and `ARRAY_TO_MV` are two names for the same function.

These queries work in the SSE, but the MSE rejects them:

{% code overflow="wrap" %}
```sql
-- example 1: GROUP BY
SELECT count(*), RandomAirports FROM airlineStats
GROUP BY RandomAirports

-- example 2: predicate
SELECT * FROM airlineStats WHERE RandomAirports IN ('SFO', 'JFK')

-- example 3: ORDER BY
SELECT count(*), RandomAirports FROM airlineStats
GROUP BY RandomAirports
ORDER BY RandomAirports DESC
```
{% endcode %}

Rewrite the queries with `arrayToMv`:

{% code overflow="wrap" %}
```sql
-- example 1: GROUP BY
SELECT count(*), arrayToMv(RandomAirports) FROM airlineStats
GROUP BY arrayToMv(RandomAirports)

-- example 2: predicate
SELECT * FROM airlineStats WHERE arrayToMv(RandomAirports) IN ('SFO', 'JFK')

-- example 3: ORDER BY
SELECT count(*), arrayToMv(RandomAirports) FROM airlineStats
GROUP BY arrayToMv(RandomAirports)
ORDER BY arrayToMv(RandomAirports) DESC
```
{% endcode %}

#### GROUP BY arrayToMv

`GROUP BY arrayToMv(col)` groups each row by every element of the MV column. It gives the same groups as `GROUP BY col` in the SSE. The query works in every stage of the plan: directly on a table scan, above a join, in a subquery, and with group trimming.

{% code overflow="wrap" %}
```sql
SELECT arrayToMv(s.RandomAirports) AS airport, count(*)
FROM airlineStats AS s
JOIN carriers AS c ON s.Carrier = c.code
WHERE c.country = 'US'
GROUP BY arrayToMv(s.RandomAirports)
```
{% endcode %}

The MSE plans the aggregate in one of two ways:

* **Plain aggregate.** The aggregate reads a table scan, directly or through filters and projections. The leaf stage sends the aggregate to the SSE, which groups by each element. This is the plan of earlier releases. The same is true when a `WHERE k IN (subquery)` semi-join runs in the leaf stage.
* **MV aggregate.** All other aggregates use the MV aggregate. Its LEAF part expands each row into the elements of its MV keys. An exchange sends the elements to the FINAL part, which is a plain aggregate. `EXPLAIN PLAN FOR` shows it as `PinotLogicalMvAggregate`.

With the hint `is_skip_leaf_stage_group_by`, the MSE uses the MV aggregate also on a table scan. The MV aggregate ignores the hint `is_partitioned_by_group_by_keys`. The hint `is_leaf_return_final_result` and group trimming work as for a plain aggregate.

Both plans use these rules:

* A row goes into the group of each of its elements.
* If an element occurs two times in one row, the row counts two times in the group of that element.
* An empty array goes into no group. A stored MV value is never empty, but a function such as `filterMv` can return an empty array.
* When null handling is on (`enableNullHandling=true`), a null MV value goes into one null group.
* Above a join, a null MV value from an outer join goes into the null group, also when null handling is off.
* Two or more MV keys give, for each row, the cartesian product of their elements.

As a result, the sum of `count(*)` over all groups can be larger than the number of rows.

A few rows with large arrays can give a very large number of combinations. The MV aggregate expands them in batches and stops when the query is cancelled or times out. A row with more than 2,147,483,647 combinations fails the query with `SERVER_RESOURCE_LIMIT_EXCEEDED`.

You can repeat the group key `arrayToMv(col)` in the SELECT list, in ORDER BY, and in HAVING. There, it refers to the group key. For example, `HAVING arrayToMv(col) = 'SFO'` keeps only the group of `SFO`. A filter on the group key in an outer query does the same.

The filter on the group key stays above the aggregate, so the leaf stage groups every element. If the number of groups is more than `numGroupsLimit`, the leaf stage can drop the group that the filter selects. The response then has `numGroupsLimitReached`.

The argument of `arrayToMv` can also be an array expression, for example `arrayToMv(valueIn(RandomAirports, 'SFO', 'JFK'))`.

`CROSS JOIN UNNEST` gives the same groups, with one difference: `UNNEST` drops a null MV value. `GROUP BY arrayToMv` puts it in the null group.

#### Null MV values

A null MV value comes from a column with column-based null handling, or from the null side of an outer join. For such a value, `arrayToMv(col)` is null. The MSE evaluates `arrayToMv(col) IS NULL`, `arrayToMv(col) IS NOT NULL`, and `CASE WHEN arrayToMv(col) IS NULL ...` on it. A null array forms the null group.

For example, above a `LEFT JOIN`, `CASE WHEN arrayToMv(col) IS NULL THEN 'none' ELSE arrayToMv(col) END` as the group key gives the group `none`.

On a nullable MV column, these expressions fail when the query runs, because the leaf stage cannot run `COALESCE` or `CASE` with a multi-value result:

* `coalesce(arrayToMv(col), 'x')` in a leaf filter or as a group key.
* `CASE WHEN arrayToMv(col) IS NULL THEN 'x' ELSE arrayToMv(col) END` as a group key on a table scan.

Above a join, `coalesce(arrayToMv(col), 'x')` as a group key fails at planning time, because `coalesce` puts `arrayToMv` inside another expression.

#### Supported uses of arrayToMv

`arrayToMv` is supported in two places only:

1. As a complete GROUP BY key: `GROUP BY arrayToMv(expr)`. Here, `expr` is an MV column or an array expression.
2. In a WHERE predicate that runs in the leaf stage, which means directly on a table scan.

These uses are not supported:

* `arrayToMv` inside another expression in a group key, for example `GROUP BY lower(arrayToMv(col))`. Directly on a table scan, the SSE evaluates the expression on the MV column. There, `CAST` applies to each element. Most other functions fail when the query runs. Above a join or in a subquery, the query fails at planning time.
* `arrayToMv` in the SELECT list, if it is not a repeat of a GROUP BY key.
* `arrayToMv` in a filter above a join or an aggregate, in a JOIN condition, or in a window function.
* `arrayToMv` in an aggregate argument, for example `sum(arrayToMv(col))`. This works only when the aggregate reads a table scan. An MV key column can also be in an aggregate argument or in the `FILTER (WHERE ...)` clause of an aggregate. Then the MSE uses the plain aggregate. The query then works only on a table scan.
* `GROUP BY arrayToMv(col)` with `GROUPING SETS`, `ROLLUP`, or `CUBE`. The MSE uses the plain aggregate, so the query works only on a table scan.
* `GROUP BY arrayToMv(col)` with a `WITHIN GROUP` aggregate, when the query needs the MV aggregate.
* A plain `GROUP BY col` on an MV column. The error message contains `Use ARRAY_TO_MV() to group by multi-value column`. This is also true when the query groups by both `arrayToMv(col)` and `col`.

Most of these queries fail at planning time with a `QUERY_PLANNING` error. The error message ends with this text:

{% code overflow="wrap" %}
```text
ARRAY_TO_MV is supported only: (1) as a complete GROUP BY key, GROUP BY ARRAY_TO_MV(expr), where expr is a multi-value column or an array expression; (2) in WHERE predicates that run in the leaf stage (directly on a table scan). It is not supported nested inside another expression (for example CASE WHEN ARRAY_TO_MV(col) IS NOT NULL ...), in the SELECT list, in aggregate arguments, in filters above a join or an aggregate, in JOIN conditions, or in window functions.
```
{% endcode %}

There are two exceptions:

* With a `WITHIN GROUP` aggregate, the message is `GROUP BY ARRAY_TO_MV() is not supported with WITHIN GROUP ordered aggregates in the multi-stage query engine`.
* A nested group key directly on a table scan fails in the SSE when the query runs. The error message comes from the SSE.

These limits also apply:

* The physical optimizer (`usePhysicalOptimizer=true`) does not use the MV aggregate. With the physical optimizer, `GROUP BY arrayToMv(col)` works only on a table scan.
* `GROUP BY arrayToMv(col)` with `WHERE k IN (subquery)` needs the dynamic broadcast semi-join. If `pinot.broker.enable.dynamic.filtering.semijoin=false`, the query fails at planning time.

#### Changes from earlier releases

Before the MV aggregate, `GROUP BY arrayToMv(col)` worked only on a table scan. Most queries that worked before keep their plan and their results. These queries change:

| Query | Earlier releases | With the MV aggregate |
|---|---|---|
| `GROUP BY arrayToMv(col) HAVING arrayToMv(col) = 'x'`, or an outer filter on the group key | Also returns the other elements of a matching row ([apache/pinot#20295](https://github.com/apache/pinot/issues/20295)) | Returns only the group `x` |
| `arrayToMv(col) IS NULL`, `IS NOT NULL`, or `CASE WHEN arrayToMv(col) IS NULL` on a null MV value | Folded as if `arrayToMv(col)` is never null ([apache/pinot#20294](https://github.com/apache/pinot/issues/20294)) | Evaluated. A null array is null and forms the null group |
| `coalesce(arrayToMv(col), 'x')` or `CASE WHEN arrayToMv(col) IS NULL` on a nullable MV column, in the leaf stage | The null check is removed ([apache/pinot#20294](https://github.com/apache/pinot/issues/20294)) | Fails when the query runs |
| Physical optimizer with `enableNullHandling`: `... LEFT JOIN ... GROUP BY arrayToMv(col) HAVING arrayToMv(col) IS NULL` | Returns no rows | Fails at planning time |

{% hint style="info" %}
**Rolling upgrades.** Pinot upgrades brokers before servers. A plain aggregate runs on servers from earlier releases. A plan with an MV aggregate fails on those servers with `Caught exception while deserializing stage plan`. Almost all of these queries also failed before the upgrade. The exception is the outer-join query with `IS NULL` and `enableNullHandling`. Before the upgrade, it returns no rows. During the upgrade, it fails until the servers are upgraded.
{% endhint %}

## Current limitations

The following are known limitations of the MSE.

### Schema and other prefixes are not supported

Queries cannot use schema or database prefixes. The following queries are **not** supported:

```
SELECT * FROM default.myTable;
SELECT * FROM schemaName.myTable;
```

Use unqualified table names instead:

```
SELECT * FROM myTable;
```

### Ambiguous reference to a projected column

If a column appears more than once in the SELECT list, subsequent clauses cannot reference it by name without aliasing. The following query is ambiguous:

```sql
SELECT colA, colA, COUNT(*)
FROM myTable GROUP BY colA ORDER BY colA
```

Use aliases to disambiguate:

```sql
SELECT colA AS tmpA, colA AS tmpB, COUNT(*)
FROM myTable GROUP BY tmpA, tmpB ORDER BY tmpA
```

Or use index-based referencing:

```sql
SELECT colA, colA, COUNT(*)
FROM myTable GROUP BY 1, 2 ORDER BY 1
```

### Arbitrary number of arguments is not supported

Variadic arguments are not supported for functions that accept a fixed signature. For example, the following query works in the SSE but not in the MSE:

```
SELECT add(1,2,3,4,5) FROM myTable
```

In the MSE, rewrite with nested calls:

```
SELECT add(1, add(2, add(3, add(4, 5)))) FROM myTable
```

{% hint style="info" %}
**Note:** `SELECT 1 + 2 + 3 + 4 + 5 FROM myTable` is valid in the MSE.
{% endhint %}

### Unsupported transform functions

* `histogram` is not supported.
* `timeConvert` is not supported; use `dateTimeConvert` instead.
* `dateTimeConvertWindowHop` is not supported.
* Array and map-related functions are not supported.

### Aggregate functions with literal inputs

Aggregate functions that require literal input (such as `percentile`, `firstWithTime`) may produce a non-compilable query plan.

## Troubleshooting checklist

### Semantic and runtime errors

1. **Reproduce on your current stable release.** Confirm the issue is present on the latest stable release you run in production.
2. **Capture diagnostics.** Collect the following before investigating further:
   * The full query text and query options
   * `EXPLAIN PLAN FOR <query>` output
   * Stage-level statistics from the query response
3. **Check for behavior differences.** Review the [behavior differences from SSE](#behavior-differences-from-sse) section above. Many errors result from stricter SQL semantics in the MSE.
4. **Rewrite the query.** Some functions supported in the SSE have different syntax in the MSE. Check whether you are using any non-standard SQL functions or semantics.
5. **Search existing issues.** Check the [Apache Pinot issue tracker](https://github.com/apache/pinot/issues) for known issues matching your error.
6. **File a new issue.** If no existing issue matches, file a new one with the query text, query options, EXPLAIN output, and stage stats attached.

### Timeout errors

* **Reduce the data scanned.** Add higher-selectivity filters to reduce the volume of data processed.
* **Simplify the query.** Execute a subquery or simplified version of the query first to determine the scale and selectivity of each stage.
* **Add more servers.** The MSE distributes work across the cluster. Adding servers helps with partitioned queries such as GROUP BY aggregates and equality JOINs.
* **Review stage stats.** Identify which stage is the bottleneck and whether it is CPU-bound, memory-bound, or waiting on data transfer.
