---
description: A narrative guide to Pinot SQL syntax and the main constructs you use most often.
---

# SQL Syntax

Pinot uses the Apache Calcite SQL parser with the `MYSQL_ANSI` dialect. This page is the practical overview: it explains the syntax patterns most people use every day and points to the deeper reference when you need the full operator list.

## Core rules

- Use single quotes for string literals.
- Use double quotes for identifiers when a column name is reserved or contains special characters.
- `SET` statements apply query options before the query runs.
- `EXPLAIN PLAN FOR` shows how Pinot will execute a query without returning data.

```sql
SET useMultistageEngine = true;
SELECT "date", city, COUNT(*)
FROM orders
WHERE status = 'shipped'
GROUP BY "date", city
ORDER BY "date" DESC
LIMIT 20;
```

## Common query shapes

Pinot supports the usual `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, and `LIMIT` patterns.

Typical query shapes include:

- filtering a table and returning a small result set
- grouping and aggregating by one or more dimensions
- using `ORDER BY` to rank rows before a `LIMIT`
- using `CASE WHEN` and scalar functions in select lists

## Engine-aware syntax

Some SQL features depend on the engine:

- single-stage execution is best for simple analytic queries
- multi-stage execution is required for joins, subqueries, and several advanced distributed patterns
- `EXPLAIN PLAN FOR` is the best way to see how Pinot interprets a statement

If you are working on a query and do not know whether a feature is supported, check the engine-specific guidance before you assume the syntax is invalid.

## Where the details live

This page intentionally stays light. For the full statement-by-statement reference, use the detailed [SQL syntax and operators reference](sql-reference.md). For query controls and diagnostics, use the pages under `query-execution-controls/`.

## What this page covered

This page covered the main Pinot SQL rules, the most common statement patterns, and the difference between narrative guidance and the full SQL reference.

## Next step

Read [Querying Pinot](querying-pinot.md) for the broader query workflow, or jump to [Query options](query-execution-controls/query-options.md) if you want to control runtime behavior.

## Related pages

- [Querying Pinot](querying-pinot.md)
- [Query options](query-execution-controls/query-options.md)
- [Explain plan](query-execution-controls/explain-plan.md)
