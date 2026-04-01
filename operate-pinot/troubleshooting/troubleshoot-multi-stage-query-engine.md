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

Support for multi-value columns in the MSE is limited to projections. Predicates, GROUP BY, and ORDER BY clauses that reference multi-value columns must use the `arrayToMv` function. For example, to run:

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

Rewrite the query using `arrayToMv`:

{% code overflow="wrap" %}
```sql
-- example 1: GROUP BY
SELECT count(*), arrayToMv(RandomAirports) FROM airlineStats
GROUP BY arrayToMv(RandomAirports)

-- example 2: predicate
SELECT * FROM airlineStats WHERE arrayToMv(RandomAirports) IN ('SFO', 'JFK')

-- example 3: ORDER BY
SELECT count(*), arrayToMV(RandomAirports) FROM airlineStats
GROUP BY arrayToMV(RandomAirports)
ORDER BY arrayToMV(RandomAirports) DESC
```
{% endcode %}

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
