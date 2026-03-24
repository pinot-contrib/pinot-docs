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
- [Query quotas](query-execution-controls/query-quotas.md)
- [Query cancellation](query-execution-controls/query-cancellation.md)
- [Cursor pagination](query-execution-controls/query-using-cursors.md)
- [Correlation IDs](query-execution-controls/query-correlation-id.md)
- [Explain plan](query-execution-controls/explain-plan.md)
- [Multi-stage explain plan](query-execution-controls/explain-plan-multi-stage.md)
- [SSE vs MSE](sse-vs-mse.md)

## When to use which engine

Single-stage execution is the default path for straightforward filtering, aggregation, and top-K style queries.

Use multi-stage execution when you need features that are not available in single-stage mode, such as:

- joins
- subqueries
- window functions
- more complex distributed query shapes

If you are unsure, start with the single-stage engine and switch only when the query requires it.

## What this page covered

This page introduced Pinot query flow, the default SQL entry point, and the main follow-up topics for query tuning and debugging.

## Next step

Read [SQL syntax](sql-syntax.md) for the query language itself, then move to [Query options](query-execution-controls/query-options.md) or [Explain plan](query-execution-controls/explain-plan.md) when you need control or diagnostics.

## Related pages

- [Querying & SQL controls](query-execution-controls/README.md)
- [SQL syntax](sql-syntax.md)
- [Explain plan](query-execution-controls/explain-plan.md)
- [Multi-stage explain plan](query-execution-controls/explain-plan-multi-stage.md)
- [SSE vs MSE](sse-vs-mse.md)
