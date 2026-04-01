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

<table>
  <thead>
    <tr>
      <th>Statement</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`SELECT`</td>
      <td>Query data from one or more tables</td>
    </tr>
    <tr>
      <td>`SET`</td>
      <td>Set query options for the session (e.g., `SET useMultistageEngine = true`)</td>
    </tr>
    <tr>
      <td>`EXPLAIN PLAN FOR`</td>
      <td>Display the query execution plan without running the query</td>
    </tr>
  </tbody>
</table>

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

### Column Expressions

A `select_expression` can be any of the following:

- `*` -- all columns
- A column name: `city`
- A qualified column name: `myTable.city`
- An expression: `price * quantity`
- A function call: `UPPER(city)`
- An aggregation function: `COUNT(*)`, `SUM(revenue)`
- A `CASE WHEN` expression

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

<table>
  <thead>
    <tr>
      <th>Join Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`[INNER] JOIN`</td>
      <td>Rows that match in both tables</td>
    </tr>
    <tr>
      <td>`LEFT [OUTER] JOIN`</td>
      <td>All rows from the left table, matching rows from the right</td>
    </tr>
    <tr>
      <td>`RIGHT [OUTER] JOIN`</td>
      <td>All rows from the right table, matching rows from the left</td>
    </tr>
    <tr>
      <td>`FULL [OUTER] JOIN`</td>
      <td>All rows from both tables</td>
    </tr>
    <tr>
      <td>`CROSS JOIN`</td>
      <td>Cartesian product of both tables</td>
    </tr>
    <tr>
      <td>`SEMI JOIN`</td>
      <td>Rows from the left table that have a match in the right table</td>
    </tr>
    <tr>
      <td>`ANTI JOIN`</td>
      <td>Rows from the left table that have no match in the right table</td>
    </tr>
    <tr>
      <td>`ASOF JOIN`</td>
      <td>Rows matched by closest value (e.g., closest timestamp)</td>
    </tr>
    <tr>
      <td>`LEFT ASOF JOIN`</td>
      <td>Like `ASOF JOIN` but keeps all left rows</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Operator</th>
      <th>Description</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`=`</td>
      <td>Equal to</td>
      <td>`WHERE city = 'NYC'`</td>
    </tr>
    <tr>
      <td>`<>` or `!=`</td>
      <td>Not equal to</td>
      <td>`WHERE status <> 'canceled'`</td>
    </tr>
    <tr>
      <td>`<`</td>
      <td>Less than</td>
      <td>`WHERE price < 100`</td>
    </tr>
    <tr>
      <td>`>`</td>
      <td>Greater than</td>
      <td>`WHERE price > 50`</td>
    </tr>
    <tr>
      <td>`<=`</td>
      <td>Less than or equal to</td>
      <td>`WHERE quantity <= 10`</td>
    </tr>
    <tr>
      <td>`>=`</td>
      <td>Greater than or equal to</td>
      <td>`WHERE rating >= 4.0`</td>
    </tr>
  </tbody>
</table>

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

---

## HAVING

Filters groups after aggregation. Use `HAVING` instead of `WHERE` when filtering on aggregated values:

```sql
SELECT city, COUNT(*) AS order_count
FROM orders
GROUP BY city
HAVING COUNT(*) > 100
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

If no `LIMIT` is specified, Pinot defaults to returning 10 rows for selection queries.

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

<table>
  <thead>
    <tr>
      <th>Operator</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`AND`</td>
      <td>True if both conditions are true</td>
    </tr>
    <tr>
      <td>`OR`</td>
      <td>True if either condition is true</td>
    </tr>
    <tr>
      <td>`NOT`</td>
      <td>Negates a condition</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Operator</th>
      <th>Description</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`+`</td>
      <td>Addition</td>
      <td>`price + tax`</td>
    </tr>
    <tr>
      <td>`-`</td>
      <td>Subtraction</td>
      <td>`total - discount`</td>
    </tr>
    <tr>
      <td>`*`</td>
      <td>Multiplication</td>
      <td>`price * quantity`</td>
    </tr>
    <tr>
      <td>`/`</td>
      <td>Division</td>
      <td>`total / count`</td>
    </tr>
    <tr>
      <td>`%`</td>
      <td>Modulo (remainder)</td>
      <td>`id % 10`</td>
    </tr>
  </tbody>
</table>

```sql
SELECT order_id, price * quantity AS line_total
FROM line_items
WHERE (price * quantity) > 1000
```

---

## Type Casting

Use `CAST` to convert a value from one type to another:

```sql
SELECT CAST(revenue AS BIGINT) FROM orders
```

### Supported Target Types

<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`INT` / `INTEGER`</td>
      <td>32-bit signed integer</td>
    </tr>
    <tr>
      <td>`BIGINT` / `LONG`</td>
      <td>64-bit signed integer</td>
    </tr>
    <tr>
      <td>`FLOAT`</td>
      <td>32-bit floating point</td>
    </tr>
    <tr>
      <td>`DOUBLE`</td>
      <td>64-bit floating point</td>
    </tr>
    <tr>
      <td>`BOOLEAN`</td>
      <td>Boolean value</td>
    </tr>
    <tr>
      <td>`TIMESTAMP`</td>
      <td>Timestamp value</td>
    </tr>
    <tr>
      <td>`VARCHAR` / `STRING`</td>
      <td>Variable-length string</td>
    </tr>
    <tr>
      <td>`BYTES`</td>
      <td>Byte array</td>
    </tr>
    <tr>
      <td>`JSON`</td>
      <td>JSON value</td>
    </tr>
  </tbody>
</table>

```sql
SELECT CAST(event_time AS TIMESTAMP), CAST(user_id AS VARCHAR)
FROM events
```

---

## Set Operations (MSE Only)

The multi-stage engine supports combining results from multiple queries:

<table>
  <thead>
    <tr>
      <th>Operation</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`UNION ALL`</td>
      <td>Combine all rows from both queries (including duplicates)</td>
    </tr>
    <tr>
      <td>`UNION`</td>
      <td>Combine rows from both queries, removing duplicates</td>
    </tr>
    <tr>
      <td>`INTERSECT`</td>
      <td>Return rows that appear in both queries</td>
    </tr>
    <tr>
      <td>`EXCEPT`</td>
      <td>Return rows from the first query that do not appear in the second</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`timeoutMs`</td>
      <td>Query timeout in milliseconds</td>
    </tr>
    <tr>
      <td>`useMultistageEngine`</td>
      <td>Use the multi-stage engine (`true`/`false`)</td>
    </tr>
    <tr>
      <td>`enableNullHandling`</td>
      <td>Enable three-valued null logic</td>
    </tr>
    <tr>
      <td>`maxExecutionThreads`</td>
      <td>Limit CPU threads used by the query</td>
    </tr>
    <tr>
      <td>`useStarTree`</td>
      <td>Enable or disable star-tree index usage</td>
    </tr>
    <tr>
      <td>`skipUpsert`</td>
      <td>Query all records in an upsert table, ignoring deletes</td>
    </tr>
  </tbody>
</table>

For the complete list of query options, see [Query Options](query-options.md).

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

<table>
  <thead>
    <tr>
      <th>`A`</th>
      <th>`B`</th>
      <th>`A AND B`</th>
      <th>`A OR B`</th>
      <th>`NOT A`</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>TRUE</td>
      <td>TRUE</td>
      <td>TRUE</td>
      <td>TRUE</td>
      <td>FALSE</td>
    </tr>
    <tr>
      <td>TRUE</td>
      <td>FALSE</td>
      <td>FALSE</td>
      <td>TRUE</td>
      <td>FALSE</td>
    </tr>
    <tr>
      <td>TRUE</td>
      <td>NULL</td>
      <td>NULL</td>
      <td>TRUE</td>
      <td>NULL</td>
    </tr>
    <tr>
      <td>FALSE</td>
      <td>FALSE</td>
      <td>FALSE</td>
      <td>FALSE</td>
      <td>TRUE</td>
    </tr>
    <tr>
      <td>FALSE</td>
      <td>NULL</td>
      <td>FALSE</td>
      <td>NULL</td>
      <td>TRUE</td>
    </tr>
    <tr>
      <td>NULL</td>
      <td>NULL</td>
      <td>NULL</td>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
  </tbody>
</table>

Key behaviors with null handling enabled:

- Comparisons with NULL (e.g., `col = NULL`) return NULL (not TRUE or FALSE). Use `IS NULL` / `IS NOT NULL` instead.
- `NULL IN (...)` returns NULL, not FALSE.
- `NULL NOT IN (...)` returns NULL, not TRUE.
- Aggregate functions like `SUM`, `AVG`, `MIN`, `MAX` ignore NULL values.
- `COUNT(*)` counts all rows; `COUNT(col)` counts only non-null values.

For more details, see [Null value support](../../developers/advanced/null-value-support.md).

---

## Identifier and Literal Rules

- **Double quotes** (`"`) delimit identifiers (column names, table names). Use double quotes for reserved keywords or special characters: `SELECT "timestamp", "date" FROM myTable`.
- **Single quotes** (`'`) delimit string literals: `WHERE city = 'NYC'`. Escape an embedded single quote by doubling it: `'it''s'`.
- **Decimal literals** should be enclosed in single quotes to preserve precision.

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

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>SSE</th>
      <th>MSE</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SELECT, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>DISTINCT</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Aggregation functions</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>CASE WHEN</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>BETWEEN, IN, LIKE, IS NULL</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Arithmetic operators (+, -, *, /, %)</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>CAST</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>OPTION / SET query hints</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>EXPLAIN PLAN</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>OFFSET</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>JOINs (INNER, LEFT, RIGHT, FULL, CROSS)</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Semi / Anti joins</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>ASOF / LEFT ASOF joins</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Subqueries</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Set operations (UNION, INTERSECT, EXCEPT)</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Window functions (OVER, PARTITION BY)</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Correlated subqueries</td>
      <td>No</td>
      <td>No</td>
    </tr>
    <tr>
      <td>INSERT INTO (from file)</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>CREATE TABLE / DROP TABLE DDL</td>
      <td>No</td>
      <td>No</td>
    </tr>
    <tr>
      <td>DISTINCT with *</td>
      <td>No</td>
      <td>No</td>
    </tr>
    <tr>
      <td>DISTINCT with GROUP BY</td>
      <td>No</td>
      <td>No</td>
    </tr>
  </tbody>
</table>
