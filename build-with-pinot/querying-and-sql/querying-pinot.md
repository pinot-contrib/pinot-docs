---
description: A practical entry point for querying Pinot.
---

# Querying Pinot

Pinot queries run through the broker and are written in SQL. This page is the wayfinding layer for people who want to query data, understand which engine to use, and know where to look when a query needs tuning.

## How to start

1. Write the query in Pinot SQL.
2. Decide whether the single-stage engine is enough or whether you need multi-stage features such as joins and subqueries.
3. Use query options to control runtime behavior.
4. Inspect the plan or result shape when you need to debug performance.

```sql
SET useMultistageEngine = true;
SELECT city, COUNT(*)
FROM stores
GROUP BY city
LIMIT 10;
```

## What matters most

Pinot SQL uses the Apache Calcite parser with the `MYSQL_ANSI` dialect. In practice, that means you should pay attention to identifier quoting, literal quoting, and engine-specific capabilities.

If you are debugging a slow or surprising query, the most useful follow-up pages are:

- [SQL syntax](sql-syntax.md)
- [Query options](query-execution-controls/query-options.md)
- [Grouping algorithm](grouping-algorithm.md)
- [Query quotas](query-execution-controls/query-quotas.md)
- [Query cancellation](query-execution-controls/query-cancellation.md)
- [Cursor pagination](query-execution-controls/query-using-cursors.md)
- [Correlation IDs](query-execution-controls/query-correlation-id.md)
- [Explain plan](query-execution-controls/explain-plan.md)
- [Multi-stage explain plan](query-execution-controls/explain-plan-multi-stage.md)
- [SSE vs MSE](sse-vs-mse.md)

## Group-by quirks (default LIMIT, trimming, ORDER BY)

These behaviors catch many users by surprise. Details and tuning knobs live in [Grouping algorithm](grouping-algorithm.md) and [Query options](query-execution-controls/query-options.md).

### Default LIMIT is 10

On the **single-stage engine (SSE)**, if a query omits `LIMIT`, the broker applies a default of **10** rows (`pinot.broker.default.query.limit`). This applies to selection queries and `GROUP BY` queries, so an SSE group-by without an explicit `LIMIT` returns at most 10 groups.

```sql
-- SSE: returns at most 10 groups even if many cities exist
SELECT city, COUNT(*) AS cnt
FROM stores
GROUP BY city;
```

The **multi-stage engine (MSE)** does not apply this broker default. Still set an explicit `LIMIT` whenever you care about result size or want intentional truncation.

### Tail trimming on GROUP BY

For SSE group-by with `ORDER BY`, Pinot may **trim tail groups** while aggregating so servers stay within memory limits. Where trimming is enabled, the candidate size is based on `max(minTrimSize, 5 * LIMIT)`; segment trimming is disabled by default, while server and broker reduction have their own defaults. Pinot ranks candidates using the query's `ORDER BY`. See [Grouping algorithm](grouping-algorithm.md) for the stage-specific settings.

Implications:

- Results can be approximate when cardinality is high relative to `LIMIT` and trim thresholds.
- `numGroupsLimitReached=true` means a group operator reached its hard group cap; increasing a trim size cannot recover groups already dropped at that cap.
- Raise the relevant trim sizes when you need a larger candidate set, or raise `LIMIT` when you also need more rows returned. Both choices increase memory use.

### GROUP BY with ORDER BY vs without ORDER BY

| Pattern | Execution behavior |
| --- | --- |
| `GROUP BY ... ORDER BY ... LIMIT N` | Each trim stage ranks candidate groups by the `ORDER BY` expressions and drops lower-ranked candidates. This is the intended top-N shape, although distributed trimming can still make results approximate when candidate sets are too small. |
| `GROUP BY ... LIMIT N` (**no** `ORDER BY`) | There is no ranking. By default, SSE result tables stop admitting unseen group keys after reaching their result size, so processing order can affect which N keys survive. |

```sql
-- Ordered top-N cities by count (trim keeps high counts when ORDER BY matches the ranking)
SELECT city, COUNT(*) AS cnt
FROM stores
GROUP BY city
ORDER BY cnt DESC
LIMIT 20;

-- Unordered: at most 20 groups, but not a defined "top" set
SELECT city, COUNT(*) AS cnt
FROM stores
GROUP BY city
LIMIT 20;
```

Do **not** assume a stable or ranked group set without `ORDER BY`. For a deterministic subset, set `accurateGroupByWithoutOrderBy=true`; SSE then keeps the lexicographically smallest group keys during server and broker reduction. This does not rank by an aggregate and cannot recover keys dropped by `numGroupsLimit`. See [Query options](query-execution-controls/query-options.md).

### HAVING and post-aggregation

On SSE, `HAVING` filters the merged group candidates **after** aggregation and any earlier group trimming. If `HAVING` prefers groups that trimming already dropped (for example `HAVING SUM(x) < 100` with `ORDER BY SUM(x) DESC`), matching groups may be missing—increase trim sizes or adjust ordering.

```sql
SELECT city, COUNT(*) AS cnt, SUM(revenue) AS total
FROM stores
GROUP BY city
HAVING COUNT(*) > 100
ORDER BY total DESC
LIMIT 50;
```

**Post-aggregation** expressions combine aggregated values (and group keys) in `SELECT`, `HAVING`, or `ORDER BY` after the aggregates are computed:

```sql
SELECT
  city,
  SUM(revenue) AS total,
  COUNT(*) AS cnt,
  SUM(revenue) / COUNT(*) AS avg_revenue
FROM stores
GROUP BY city
HAVING SUM(revenue) / COUNT(*) > 10
ORDER BY avg_revenue DESC
LIMIT 50;
```

### Query options (names and syntax)

Use `SET` statements or `OPTION (...)` to pass per-query options. Recognized keys resolve **case-insensitively** to the canonical camelCase names listed in [Query options](query-execution-controls/query-options.md) (for example `timeoutMs`, `numGroupsLimit`, `minSegmentGroupTrimSize`, `useMultistageEngine`). Prefer canonical spelling: unknown names can be accepted but ignored.

```sql
SET timeoutMs = 5000;
SET minSegmentGroupTrimSize = 5000;
SELECT city, COUNT(*) AS cnt
FROM stores
GROUP BY city
ORDER BY cnt DESC
LIMIT 100;
```

## When to use which engine

Single-stage execution is the default path for straightforward filtering, aggregation, and top-K style queries.

Use multi-stage execution when you need features that are not available in single-stage mode, such as:

- joins
- subqueries
- window functions
- more complex distributed query shapes

As a rule of thumb: use SSE for simple filtering, aggregation, and top-K queries; use MSE when your query shape requires joins, subqueries, window functions, or other advanced relational operators. For a detailed comparison, see [SSE vs MSE](sse-vs-mse.md).

## Next step

Read [SQL syntax](sql-syntax.md) for the query language itself, then move to [Query options](query-execution-controls/query-options.md) or [Explain plan](query-execution-controls/explain-plan.md) when you need control or diagnostics.

## Related pages

- [Querying & SQL controls](query-execution-controls/README.md)
- [SQL syntax](sql-syntax.md)
- [Query options](query-execution-controls/query-options.md)
- [Grouping algorithm](grouping-algorithm.md)
- [Explain plan](query-execution-controls/explain-plan.md)
- [Multi-stage explain plan](query-execution-controls/explain-plan-multi-stage.md)
- [SSE vs MSE](sse-vs-mse.md)
- [SQL syntax and operators reference](sql-reference.md)

## Identifier vs Literal

In Pinot SQL:

* **Double quotes(")** are used to force string identifiers, e.g. column names
* **Single quotes(')** are used to enclose string literals. If the string literal also contains a single quote, escape this with a single quote e.g `'''Pinot'''` to match the string literal `'Pinot'`

Misusing those might cause unexpected query results, like the following examples:

* `WHERE a='b'` means the predicate on the column `a` equals to a string literal value `'b'`
* `WHERE a="b"` means the predicate on the column `a` equals to the value of the column `b`

If your column names use reserved keywords (e.g. `timestamp` or `date`) or special characters, you will need to use double quotes when referring to them in queries.

Note: Define decimal literals within quotes to preserve precision.

## Example Queries

### Selection

```
//default to limit 10
SELECT * 
FROM myTable 

SELECT * 
FROM myTable 
LIMIT 100
```

```
SELECT "date", "timestamp"
FROM myTable 
```

### Aggregation

```sql
SELECT COUNT(*), MAX(foo), SUM(bar) 
FROM myTable
```

### Grouping on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo), bar, baz 
FROM myTable
GROUP BY bar, baz 
LIMIT 50
```

{% hint style="info" %}
On the single-stage engine, omitting `LIMIT` defaults to **10 groups**. Without `ORDER BY`, which group keys survive a small result size can depend on processing order. See [Group-by quirks](#group-by-quirks-default-limit-trimming-order-by).
{% endhint %}

### Ordering on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo), bar, baz 
FROM myTable
GROUP BY bar, baz 
ORDER BY bar, MAX(foo) DESC 
LIMIT 50
```

### Filtering groups with HAVING

```sql
SELECT bar, SUM(foo) AS total
FROM myTable
GROUP BY bar
HAVING SUM(foo) > 1000
ORDER BY total DESC
LIMIT 50
```

### Post-aggregation expressions

```sql
SELECT bar, SUM(foo) AS total, COUNT(*) AS cnt, SUM(foo) / COUNT(*) AS avg_foo
FROM myTable
GROUP BY bar
ORDER BY avg_foo DESC
LIMIT 50
```

### Filtering

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE foo = 'foo'
  AND bar BETWEEN 1 AND 20
  OR (baz < 42 AND quux IN ('hello', 'goodbye') AND quuux NOT IN (42, 69))
```

For performant filtering of IDs in a list, see [Filtering with IdSet](../../build-with-pinot/querying-and-sql/filtering-with-idset.md).

### Filtering with NULL predicate

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE foo IS NOT NULL
  AND foo = 'foo'
  AND bar BETWEEN 1 AND 20
  OR (baz < 42 AND quux IN ('hello', 'goodbye') AND quuux NOT IN (42, 69))
```

### Selection (Projection)

```sql
SELECT * 
FROM myTable
  WHERE quux < 5
  LIMIT 50
```

### Ordering on Selection

```sql
SELECT foo, bar 
FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 100
```

### Pagination on Selection

Note that results might not be consistent if the `ORDER BY` column has the same value in multiple rows.

```sql
SELECT foo, bar 
FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 50, 100
```

### Wild-card match (in WHERE clause only)

The example below counts rows where the column `airlineName` starts with `U`:

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE REGEXP_LIKE(airlineName, '^U.*')
  GROUP BY airlineName LIMIT 10
```

**Note:** REGEXP_LIKE also supports case insensitive search using the `i` flag as the third parameter.

### Case-When Statement

Pinot supports the `CASE-WHEN-ELSE` statement, as shown in the following two examples:

```sql
SELECT
    CASE
      WHEN price > 30 THEN 3
      WHEN price > 20 THEN 2
      WHEN price > 10 THEN 1
      ELSE 0
    END AS price_category
FROM myTable
```

```sql
SELECT
  SUM(
    CASE
      WHEN price > 30 THEN 30
      WHEN price > 20 THEN 20
      WHEN price > 10 THEN 10
      ELSE 0
    END) AS total_cost
FROM myTable
```

### UDF

Pinot doesn't currently support injecting functions.  Functions have to be implemented within Pinot, as shown below:

```sql
SELECT COUNT(*)
FROM myTable
GROUP BY DATETIMECONVERT(timeColumnName, '1:MILLISECONDS:EPOCH', '1:HOURS:EPOCH', '1:HOURS')
```

For more examples, see [Transform Function in Aggregation Grouping](../../functions/transformations.md).

### BYTES column

Pinot supports queries on BYTES column using hex strings. The query response also uses hex strings to represent bytes values.

The query below fetches all the rows for a given UID:

```sql
SELECT * 
FROM myTable
WHERE UID = 'c8b3bce0b378fc5ce8067fc271a34892'
```
