---
description: >-
  Complete reference for SQL syntax, operators, and clauses supported by Apache
  Pinot's single-stage engine (SSE) and multi-stage engine (MSE).
---

# SQL Syntax and Operators Reference

Pinot uses the **Apache Calcite** SQL parser with the **MYSQL\_ANSI** dialect. This page documents every SQL statement, clause, and operator that Pinot supports, and notes where behavior differs between the single-stage engine (SSE) and the multi-stage engine (MSE).

{% hint style="info" %}
To use MSE-only features such as JOINs, subqueries, window functions, and set operations, enable the multi-stage engine with `SET useMultistageEngine = true;` before your query. See [Use the multi-stage query engine](../../build-with-pinot/querying-and-sql/sse-vs-mse.md) for details.
{% endhint %}

---

## Supported Statements

Pinot supports the following top-level statement types:

| Statement | Description |
|---|---|
| `SELECT` | Query data from one or more tables |
| `SET` | Set query options for the session (e.g., `SET useMultistageEngine = true`) |
| `EXPLAIN PLAN FOR` | Display the query execution plan without running the query |

```sql
-- Set a query option, then run a query
SET useMultistageEngine = true;
SELECT COUNT(*) FROM myTable WHERE city = 'San Francisco';
```

```sql
-- View the execution plan
EXPLAIN PLAN FOR
SELECT COUNT(*) FROM myTable GROUP BY city;
```

---

## SELECT Syntax

The full syntax for a `SELECT` statement in Pinot is:

```
SELECT [ DISTINCT ] select_expression [, select_expression ]*
FROM table_reference
[ WHERE filter_condition ]
[ GROUP BY group_expression [, group_expression ]* ]
[ HAVING having_condition ]
[ ORDER BY order_expression [ ASC | DESC ] [ NULLS FIRST | NULLS LAST ] [, ...] ]
[ LIMIT count ]
[ OFFSET offset ]
[ OPTION ( key = value [, key = value ]* ) ]
```

Both query engines accept grouping constructs in the `GROUP BY` clause, such as
`ROLLUP(...)`, `CUBE(...)`, and `GROUPING SETS (...)`. See [GROUP BY](#group-by) for syntax and limits.

### Column Expressions

A `select_expression` can be any of the following:

- `*` -- all columns
- A column name: `city`
- A qualified column name: `myTable.city`
- An expression: `price * quantity`
- A function call: `UPPER(city)`
- An aggregation function: `COUNT(*)`, `SUM(revenue)`
- A `CASE WHEN` expression

### MAP Element Access

If a column is declared as `MAP`, use bracket syntax to read a value by key:

```sql
mapColumn['key']
```

Pinot treats map lookups as scalar expressions, so you can use them in `SELECT`, `WHERE`, `GROUP BY`, and `ORDER BY`:

```sql
SELECT attributes['country'] AS country, metrics['latencyMs'] AS latency
FROM events
WHERE metrics['latencyMs'] > 100
ORDER BY metrics['latencyMs']

SELECT attributes['country'] AS country, COUNT(*)
FROM events
GROUP BY attributes['country']
```

If a key is missing, Pinot returns the value type's default null value. For example, a missing STRING map value returns `"null"` and a missing INT map value returns `Integer.MIN_VALUE`.

For schema syntax, see [Schema Configuration](../../reference/configuration-reference/schema.md#complexfieldspecs).

### Aliases

Use `AS` to assign an alias to any select expression:

```sql
SELECT city AS metro_area, COUNT(*) AS total_orders
FROM orders
GROUP BY city
```

### DISTINCT

Use `SELECT DISTINCT` to return unique combinations of column values:

```sql
SELECT DISTINCT city, state
FROM stores
LIMIT 100
```

{% hint style="warning" %}
In the SSE, `DISTINCT` is implemented as an aggregation function. `DISTINCT *` is not supported; you must list specific columns. `DISTINCT` with `GROUP BY` is also not supported.
{% endhint %}

---

## FROM Clause

### Table References

The simplest `FROM` clause references a single table:

```sql
SELECT * FROM myTable
```

### Subqueries (MSE Only)

With the multi-stage engine, you can use a subquery as a data source:

```sql
SET useMultistageEngine = true;
SELECT city, avg_revenue
FROM (
  SELECT city, AVG(revenue) AS avg_revenue
  FROM orders
  GROUP BY city
) AS sub
WHERE avg_revenue > 1000
```

### JOINs (MSE Only)

The multi-stage engine supports the following join types:

| Join Type | Description |
|---|---|
| `[INNER] JOIN` | Rows that match in both tables |
| `LEFT [OUTER] JOIN` | All rows from the left table, matching rows from the right |
| `RIGHT [OUTER] JOIN` | All rows from the right table, matching rows from the left |
| `FULL [OUTER] JOIN` | All rows from both tables |
| `CROSS JOIN` | Cartesian product of both tables |
| `SEMI JOIN` | Rows from the left table that have a match in the right table |
| `ANTI JOIN` | Rows from the left table that have no match in the right table |
| `ASOF JOIN` | Rows matched by closest value (e.g., closest timestamp) |
| `LEFT ASOF JOIN` | Like `ASOF JOIN` but keeps all left rows |

```sql
SET useMultistageEngine = true;
SELECT o.order_id, c.name
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.id
WHERE o.amount > 100
```

For detailed join syntax and examples, see [JOINs](joins.md).

---

## WHERE Clause

The `WHERE` clause filters rows using predicates. Multiple predicates can be combined with [logical operators](#logical-operators).

### Comparison Operators

| Operator | Description | Example |
|---|---|---|
| `=` | Equal to | `WHERE city = 'NYC'` |
| `<>` or `!=` | Not equal to | `WHERE status <> 'canceled'` |
| `<` | Less than | `WHERE price < 100` |
| `>` | Greater than | `WHERE price > 50` |
| `<=` | Less than or equal to | `WHERE quantity <= 10` |
| `>=` | Greater than or equal to | `WHERE rating >= 4.0` |

### BETWEEN

Tests whether a value falls within an inclusive range:

```sql
SELECT * FROM orders
WHERE amount BETWEEN 100 AND 500
```

`NOT BETWEEN` is also supported:

```sql
SELECT * FROM orders
WHERE amount NOT BETWEEN 100 AND 500
```

### IN

Tests whether a value matches any value in a list:

```sql
SELECT * FROM orders
WHERE city IN ('NYC', 'LA', 'Chicago')
```

`NOT IN` is also supported:

```sql
SELECT * FROM orders
WHERE status NOT IN ('canceled', 'refunded')
```

{% hint style="info" %}
For large value lists, consider using [Filtering with IdSet](filtering-with-idset.md) for better performance.
{% endhint %}

### LIKE

Pattern matching with wildcards. `%` matches any sequence of characters; `_` matches any single character:

```sql
SELECT * FROM customers
WHERE name LIKE 'John%'
```

`NOT LIKE` is also supported.

### IS NULL / IS NOT NULL

Tests whether a value is null:

```sql
SELECT * FROM orders
WHERE discount IS NOT NULL
```

See [NULL Semantics](#null-semantics) for details on how nulls work in Pinot.

### REGEXP\_LIKE

Filters rows using regular expression matching:

```sql
SELECT * FROM airlines
WHERE REGEXP_LIKE(airlineName, '^U.*')
```

{% hint style="info" %}
`REGEXP_LIKE` supports case-insensitive matching via a third parameter: `REGEXP_LIKE(col, pattern, 'i')`.
{% endhint %}

### TEXT\_MATCH

Full-text search on columns with a text index:

```sql
SELECT * FROM logs
WHERE TEXT_MATCH(message, 'error AND timeout')
```

### JSON\_MATCH

Predicate matching on columns with a JSON index:

```sql
SELECT * FROM events
WHERE JSON_MATCH(payload, '"$.type" = ''click''')
```

### VECTOR\_SIMILARITY

Approximate nearest-neighbor search on vector-indexed columns:

```sql
SELECT * FROM embeddings
WHERE VECTOR_SIMILARITY(vector_col, ARRAY[0.1, 0.2, 0.3], 10)
```

---

## GROUP BY

Groups rows that share values in the specified columns, typically used with aggregation functions:

```sql
SELECT city, COUNT(*) AS order_count, SUM(amount) AS total
FROM orders
GROUP BY city
```

**Rules:**

- Every non-aggregated column in the `SELECT` list must appear in the `GROUP BY` clause.
- Aggregation functions and non-aggregation columns cannot be mixed in the `SELECT` list without a `GROUP BY`.
- Aggregate expressions are not allowed inside the `GROUP BY` clause.

### GROUPING SETS, ROLLUP, and CUBE

Both Pinot query engines support grouped subtotal queries. To run a grouping-set query on the multi-stage engine,
enable it with `SET useMultistageEngine=true`.

```sql
SELECT country, city, SUM(revenue) AS total_revenue
FROM sales
GROUP BY ROLLUP(country, city)
```

Use the following forms:

- `GROUP BY ROLLUP(a, b, c)` expands to `GROUPING SETS ((a, b, c), (a, b), (a), ())`
- `GROUP BY CUBE(a, b, c)` expands to every combination of those grouping columns
- `GROUP BY GROUPING SETS ((a, b), (a), ())` uses exactly the grouping sets you list
- `GROUP BY a, ROLLUP(b, c)` is valid; Pinot cross-multiplies plain keys with grouping constructs

`()` represents the grand-total grouping set. Pinot de-duplicates repeated grouping sets, so
`GROUPING SETS ((a), (a), ())` returns only one `(a)` subtotal.

```sql
SELECT country, city, SUM(revenue) AS total_revenue
FROM sales
GROUP BY GROUPING SETS ((country, city), (country), ())
```

Important limits and caveats:

- Pinot requires at least one aggregation function somewhere in the query (`SELECT`, `HAVING`, or `ORDER BY`)
- A query can expand to at most `4096` grouping sets. In particular, a `CUBE` can contain at most `12` grouping levels.
- The number of grouping columns is unlimited, but each `GROUPING()` or `GROUPING_ID()` call accepts at most `31` arguments.
- MSE grouping-set queries do not support ordered aggregate expressions with `WITHIN GROUP` or aggregate hints.
- With `usePhysicalOptimizer=true`, MSE grouping-set queries do not support joins.
- Rolled-up columns are returned as real `NULL` values even when null handling is disabled
- Existing non-grouping-set queries remain wire-compatible during a rolling upgrade, but do not issue grouping-set queries until all servers are upgraded

### GROUPING() and GROUPING_ID()

Use `GROUPING()` and `GROUPING_ID()` to tell subtotal rows apart from genuine data `NULL`s:

```sql
SELECT
  country,
  city,
  SUM(revenue) AS total_revenue,
  GROUPING(country) AS country_rolled_up,
  GROUPING(city) AS city_rolled_up,
  GROUPING_ID(country, city) AS grouping_id
FROM sales
GROUP BY ROLLUP(country, city)
ORDER BY GROUPING_ID(country, city)
```

- `GROUPING(col)` returns `1` when `col` is rolled up in the current row and `0` otherwise
- `GROUPING_ID(c1, c2, ...)` returns the grouping bitmask, with the first argument as the most significant bit
- Each argument must also appear in the `GROUP BY` columns for the query
- Pinot supports these functions in `SELECT`, `HAVING`, and `ORDER BY`

---

## HAVING

Filters groups after aggregation. Use `HAVING` instead of `WHERE` when filtering on aggregated values:

```sql
SELECT city, COUNT(*) AS order_count
FROM orders
GROUP BY city
HAVING COUNT(*) > 100
```

On SSE, `HAVING` runs on the merged group candidates after any earlier group trim. If trimming already dropped groups that would match `HAVING`, those groups do not reappear. See [Grouping algorithm](grouping-algorithm.md#having-behavior) and [Querying Pinot](querying-pinot.md#group-by-quirks-default-limit-trimming-order-by).

You can use **post-aggregation** expressions (arithmetic or functions over aggregates and group keys) in `SELECT`, `HAVING`, and `ORDER BY`:

```sql
SELECT city, SUM(amount) AS total, COUNT(*) AS cnt, SUM(amount) / COUNT(*) AS avg_amount
FROM orders
GROUP BY city
HAVING SUM(amount) / COUNT(*) > 25
ORDER BY avg_amount DESC
LIMIT 50
```

---

## ORDER BY

Sorts the result set by one or more expressions:

```sql
SELECT city, SUM(amount) AS total
FROM orders
GROUP BY city
ORDER BY total DESC
```

Without `ORDER BY`, Pinot does not guarantee row or group order. For SSE `GROUP BY` without `ORDER BY`, result tables can also stop admitting unseen group keys after reaching a small `LIMIT`, so processing order can affect which keys survive. See [Querying Pinot](querying-pinot.md#group-by-quirks-default-limit-trimming-order-by).

### Ordering Direction

- `ASC` -- ascending order (default)
- `DESC` -- descending order

### NULL Ordering

- `NULLS FIRST` -- null values appear first
- `NULLS LAST` -- null values appear last

```sql
SELECT city, revenue
FROM stores
ORDER BY revenue DESC NULLS LAST
```

---

## LIMIT / OFFSET

### LIMIT

Restricts the number of rows returned:

```sql
SELECT * FROM orders LIMIT 50
```

On the **single-stage engine**, if no `LIMIT` is specified, the broker defaults to returning 10 rows (`pinot.broker.default.query.limit`); this also caps SSE `GROUP BY` results at 10 groups. The multi-stage engine does not apply this broker default. Prefer an explicit `LIMIT` on every production query. See [Grouping algorithm](grouping-algorithm.md#group-by-behavior) and [Querying Pinot](querying-pinot.md#group-by-quirks-default-limit-trimming-order-by).

### OFFSET

Skips a number of rows before returning results. Requires `ORDER BY` for consistent pagination:

```sql
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 20 OFFSET 40
```

Pinot also supports the legacy `LIMIT offset, count` syntax:

```sql
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 40, 20
```

---

## Logical Operators

| Operator | Description |
|---|---|
| `AND` | True if both conditions are true |
| `OR` | True if either condition is true |
| `NOT` | Negates a condition |

### Precedence

From highest to lowest:

1. `NOT`
2. `AND`
3. `OR`

Use parentheses to override default precedence:

```sql
SELECT * FROM orders
WHERE (status = 'completed' OR status = 'shipped')
  AND amount > 100
```

---

## Arithmetic Operators

Arithmetic expressions can be used in `SELECT` expressions, `WHERE` clauses, and other contexts:

| Operator | Description | Example |
|---|---|---|
| `+` | Addition | `price + tax` |
| `-` | Subtraction | `total - discount` |
| `*` | Multiplication | `price * quantity` |
| `/` | Division | `total / count` |
| `%` | Modulo (remainder) | `id % 10` |

```sql
SELECT order_id, price * quantity AS line_total
FROM line_items
WHERE (price * quantity) > 1000
```

### Unary Operators

Unary `-` and `+` are prefix operators on numeric expressions. They can be used anywhere a scalar expression is valid: `SELECT` list, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `JOIN` conditions, `CASE` branches, `CAST` inputs, `IN` lists, subqueries, and inside aggregates and window functions.

| Operator | Description | Example |
|---|---|---|
| `-` (unary) | Negation (numeric) | `-price`, `ORDER BY -score` |
| `+` (unary) | Identity (numeric) | `+price` |

```sql
SELECT order_id, -discount AS adjustment
FROM line_items
```

```sql
SELECT order_id
FROM line_items
WHERE -profit > 100
```

```sql
SELECT order_id, score
FROM line_items
ORDER BY -score
```

Notes:

- Supported on `INT`, `LONG`, `FLOAT`, `DOUBLE`, and `BIG_DECIMAL`. The result preserves the input type.
- `NULL` input returns `NULL`.
- `-col` is equivalent to [`negate(col)`](../../functions/math/negate.md).
- Negation uses `Math.negateExact` semantics, so `-INT_MIN` and `-LONG_MIN` overflow at runtime.

---

## Type Casting

Use `CAST` to convert a value from one type to another:

```sql
SELECT CAST(revenue AS BIGINT) FROM orders
```

### Supported Target Types

| Type | Description |
|---|---|
| `INT` / `INTEGER` | 32-bit signed integer |
| `BIGINT` / `LONG` | 64-bit signed integer |
| `FLOAT` | 32-bit floating point |
| `DOUBLE` | 64-bit floating point |
| `BOOLEAN` | Boolean value |
| `TIMESTAMP` | Timestamp value |
| `VARCHAR` / `STRING` | Variable-length string |
| `BYTES` | Byte array |
| `UUID` | Logical UUID stored as 16 bytes |
| `JSON` | JSON value |

Pinot also accepts `TINYINT UNSIGNED`, `SMALLINT UNSIGNED`, and `INTEGER UNSIGNED` as cast targets. These return the
smallest signed Pinot type that preserves the full range: `TINYINT UNSIGNED` and `SMALLINT UNSIGNED` behave like
`INTEGER`, while `INTEGER UNSIGNED` behaves like `BIGINT` / `LONG`. `BIGINT UNSIGNED` is not supported.

```sql
SELECT CAST(event_time AS TIMESTAMP), CAST(user_id AS VARCHAR)
FROM events
```

Cast canonical UUID strings or 16-byte values to the logical `UUID` type. UUID results render as canonical lowercase dashed strings, and casting a UUID expression to `STRING` uses the same representation. Invalid UUID strings and byte arrays that are not 16 bytes are rejected. These conversions support single-value and multi-value expressions.

```sql
SELECT CAST('550e8400-e29b-41d4-a716-446655440000' AS UUID)
FROM events
```

UUID expressions support `CASE`, `IN`, and binary comparisons. In these expressions, a bare UUID literal must be the fixed-width 32-character hexadecimal encoding of the stored 16 bytes. Cast canonical dashed text explicitly to `UUID`:

```sql
SELECT CASE
  WHEN user_id IN (CAST('550e8400-e29b-41d4-a716-446655440000' AS UUID))
  THEN user_id
  ELSE CAST('00000000-0000-0000-0000-000000000000' AS UUID)
END
FROM events
```

A bare canonical dashed string is not implicitly converted to UUID inside `CASE` or `IN`.

Filter predicates against a UUID column accept canonical dashed, dashless, and mixed-case UUID strings. This applies to `=`, `!=`, `IN`, `NOT IN`, and range predicates on both dictionary-encoded and raw UUID columns:

```sql
SELECT *
FROM events
WHERE user_id IN (
  '550e8400-e29b-41d4-a716-446655440000',
  '6BA7B8109DAD11D180B400C04FD430C8'
)
```

Malformed UUID predicate literals are rejected.

---

## Set Operations (MSE Only)

The multi-stage engine supports combining results from multiple queries:

| Operation | Description |
|---|---|
| `UNION ALL` | Combine all rows from both queries (including duplicates) |
| `UNION` | Combine rows from both queries, removing duplicates |
| `INTERSECT` | Return rows that appear in both queries |
| `EXCEPT` | Return rows from the first query that do not appear in the second |

```sql
SET useMultistageEngine = true;

SELECT city FROM stores
UNION ALL
SELECT city FROM warehouses
```

```sql
SET useMultistageEngine = true;

SELECT customer_id FROM orders_2024
INTERSECT
SELECT customer_id FROM orders_2025
```

---

## Window Functions (MSE Only)

Window functions compute a value across a set of rows related to the current row, without collapsing them into a single output row.

### Syntax

```
function_name ( expression ) OVER (
  [ PARTITION BY partition_expression [, ...] ]
  [ ORDER BY order_expression [ ASC | DESC ] [, ...] ]
  [ frame_clause ]
)
```

### Frame Clause

```
{ ROWS | RANGE } BETWEEN frame_start AND frame_end

frame_start / frame_end:
  UNBOUNDED PRECEDING
  | offset PRECEDING
  | CURRENT ROW
  | offset FOLLOWING
  | UNBOUNDED FOLLOWING
```

### Example

```sql
SET useMultistageEngine = true;

SELECT
  city,
  order_date,
  amount,
  SUM(amount) OVER (PARTITION BY city ORDER BY order_date) AS running_total,
  ROW_NUMBER() OVER (PARTITION BY city ORDER BY amount DESC) AS rank
FROM orders
```

For the full list of supported window functions and detailed syntax, see [Window Functions](../../functions/window).

---

## OPTION Clause

The `OPTION` clause provides Pinot-specific query hints. These are not standard SQL but allow you to control engine behavior:

```sql
SELECT * FROM orders
WHERE city = 'NYC'
OPTION(timeoutMs=5000)
```

The preferred approach is to use `SET` statements before the query:

```sql
SET timeoutMs = 5000;
SET useMultistageEngine = true;
SELECT * FROM orders WHERE city = 'NYC'
```

Common query options include:

| Option | Description |
|---|---|
| `timeoutMs` | Query timeout in milliseconds |
| `useMultistageEngine` | Use the multi-stage engine (`true`/`false`) |
| `enableNullHandling` | Enable three-valued null logic |
| `maxExecutionThreads` | Limit CPU threads used by the query |
| `useStarTree` | Enable or disable star-tree index usage |
| `skipUpsert` | Query all records in an upsert table, ignoring deletes |

For the complete list of query options, see [Query Options](query-execution-controls/query-options.md).

---

## NULL Semantics

### Default Behavior

By default, Pinot treats null values as the **default value for the column type** (0 for numeric types, empty string for strings, etc.). This avoids the overhead of null tracking and maintains backward compatibility.

### Nullable Columns

To enable full null handling:

1. Mark columns as nullable in the schema (do not set `notNull: true`).
2. Enable null handling at query time:

```sql
SET enableNullHandling = true;
SELECT * FROM orders WHERE discount IS NULL
```

### Three-Valued Logic

When null handling is enabled, Pinot follows standard SQL three-valued logic:

| `A` | `B` | `A AND B` | `A OR B` | `NOT A` |
|---|---|---|---|---|
| TRUE | TRUE | TRUE | TRUE | FALSE |
| TRUE | FALSE | FALSE | TRUE | FALSE |
| TRUE | NULL | NULL | TRUE | NULL |
| FALSE | FALSE | FALSE | FALSE | TRUE |
| FALSE | NULL | FALSE | NULL | TRUE |
| NULL | NULL | NULL | NULL | NULL |

Key behaviors with null handling enabled:

- Comparisons with NULL (e.g., `col = NULL`) return NULL (not TRUE or FALSE). Use `IS NULL` / `IS NOT NULL` instead.
- `NULL IN (...)` returns NULL, not FALSE.
- `NULL NOT IN (...)` returns NULL, not TRUE.
- Aggregate functions like `SUM`, `AVG`, `MIN`, `MAX` ignore NULL values.
- `COUNT(*)` counts all rows; `COUNT(col)` counts only non-null values.

For more details, see [Null value support](../../build-with-pinot/querying-and-sql/null-value-support.md).

---

## Identifier and Literal Rules

- **Double quotes** (`"`) delimit identifiers (column names, table names). Use double quotes for reserved keywords or special characters: `SELECT "timestamp", "date" FROM myTable`.
- **Single quotes** (`'`) delimit string literals: `WHERE city = 'NYC'`. Escape an embedded single quote by doubling it: `'it''s'`.
- **Decimal literals** should be enclosed in single quotes to preserve precision.
- **Binary literals** use hexadecimal SQL syntax such as `X'0102'`. Construct a `BYTES_ARRAY` with `ARRAY[X'00', X'0102', X'FF']`. Pinot supports these literals in projections, nested expressions, and predicates in both query engines; response values are hexadecimal strings and result metadata reports `BYTES_ARRAY`.

---

## CASE WHEN

Pinot supports `CASE WHEN` expressions for conditional logic:

```sql
SELECT
  order_id,
  CASE
    WHEN amount > 1000 THEN 'high'
    WHEN amount > 100 THEN 'medium'
    ELSE 'low'
  END AS tier
FROM orders
```

`CASE WHEN` can be used inside aggregation functions:

```sql
SELECT
  SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS completed_revenue
FROM orders
```

{% hint style="warning" %}
Aggregation functions inside the `ELSE` clause are not supported.
{% endhint %}

---

## Engine Compatibility Matrix

The following table summarizes feature support across the single-stage engine (SSE) and multi-stage engine (MSE):

| Feature | SSE | MSE |
|---|---|---|
| SELECT, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT | Yes | Yes |
| GROUPING SETS / ROLLUP / CUBE | Yes | Yes |
| GROUPING() / GROUPING_ID() | Yes | Yes |
| DISTINCT | Yes | Yes |
| Aggregation functions | Yes | Yes |
| CASE WHEN | Yes | Yes |
| BETWEEN, IN, LIKE, IS NULL | Yes | Yes |
| Arithmetic operators (+, -, *, /, %) | Yes | Yes |
| CAST | Yes | Yes |
| OPTION / SET query hints | Yes | Yes |
| EXPLAIN PLAN | Yes | Yes |
| OFFSET | Yes | Yes |
| JOINs (INNER, LEFT, RIGHT, FULL, CROSS) | No | Yes |
| Semi / Anti joins | No | Yes |
| ASOF / LEFT ASOF joins | No | Yes |
| Subqueries | No | Yes |
| Set operations (UNION, INTERSECT, EXCEPT) | No | Yes |
| Window functions (OVER, PARTITION BY) | No | Yes |
| Correlated subqueries | No | No |
| INSERT INTO (from file) | No | Yes |
| Controller DDL (tables and materialized views) | No | No |
| DISTINCT with * | No | No |
| DISTINCT with GROUP BY | No | No |

`Controller DDL (tables and materialized views)` stays `No` in this matrix because broker-routed SSE and MSE queries do not execute controller metadata DDL. Pinot exposes SQL DDL through the controller endpoint `POST /sql/ddl`; see [SQL DDL](sql-ddl.md) and [Materialized Views](materialized-views.md).
