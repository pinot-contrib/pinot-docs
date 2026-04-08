# Row Expression Comparison

Pinot supports implicit row-style comparisons in multi-stage queries. These comparisons are useful for keyset pagination and other lexicographic comparisons across multiple columns.

Pinot does not materialize a row type at runtime. Instead, it rewrites the comparison during planning using the same lexicographic semantics described in the [jOOQ row-value comparison transformations](https://www.jooq.org/doc/latest/manual/sql-building/conditional-expressions/comparison-predicate-degree-n/).

## Supported syntax

Use a parenthesized list of expressions on both sides of one of the supported comparison operators:

```sql
WHERE (col1, col2, col3) > (val1, val2, val3)
```

Supported comparison operators:

```text
=, <>, <, <=, >, >=
```

{% hint style="info" %}
Explicit `ROW()` syntax is not supported. Use implicit parenthesized expressions such as `(col1, col2) > (1, 2)` instead of `ROW(col1, col2) > ROW(1, 2)`.
{% endhint %}

## Validation rules

Pinot validates row-style comparisons before planning the query:

* Both sides of the comparison must be row expressions.
* Both row expressions must have the same number of fields.
* Row expressions cannot be empty.
* Row expressions are only supported in comparison predicates.

If any of these checks fail, Pinot rejects the query during validation.

## Supported contexts

Row-style comparisons are supported in comparison predicates, including:

* `WHERE` clauses
* comparison predicates inside subqueries
* comparison predicates inside CTEs

Examples:

```sql
SELECT COUNT(*)
FROM myTable
WHERE (airTime, actualElapsedTime) > (200, 230)
```

```sql
SELECT airlineId, carrier, airTime
FROM myTable
WHERE (airlineId, carrier, airTime) > (20000, 'AA', 120)
ORDER BY airlineId, carrier, airTime
LIMIT 10
```

```sql
WITH filtered AS (
  SELECT airlineId, carrier, airTime
  FROM myTable
  WHERE airlineId > 19000
)
SELECT COUNT(*)
FROM filtered
WHERE (airlineId, carrier) > (20000, 'AA')
```

## Unsupported contexts

Row expressions are rejected outside comparison predicates. In particular, they are not supported in:

* `SELECT` lists
* `GROUP BY`
* `ORDER BY`
* function arguments

Examples that Pinot rejects:

```sql
SELECT (airTime, actualElapsedTime) FROM myTable
```

```sql
SELECT COUNT(*) FROM myTable GROUP BY (airlineId, carrier)
```

```sql
SELECT airlineId, carrier FROM myTable ORDER BY (airlineId, carrier)
```

## Semantics

Row comparisons are lexicographic, not element-wise. For example:

```sql
WHERE (a, b, c) > (x, y, z)
```

is equivalent to:

```sql
WHERE a > x
   OR (a = x AND b > y)
   OR (a = x AND b = y AND c > z)
```

Likewise:

```sql
WHERE (a, b, c) = (x, y, z)
```

is equivalent to:

```sql
WHERE a = x
  AND b = y
  AND c = z
```
