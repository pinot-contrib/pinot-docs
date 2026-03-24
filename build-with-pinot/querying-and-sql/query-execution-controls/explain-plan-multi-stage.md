---
description: Multi-stage explain plan guidance for Pinot SQL.
---

# Explain Plan for Multi-Stage Queries

Multi-stage explain plans are useful when a query uses features such as joins, subqueries, or distributed reshaping that do not exist in the single-stage path.

## What to look for

- logical plan shape
- exchange and distribution boundaries
- join and aggregation placement
- implementation details when you need to see the physical operator chain

If you only need to understand a simple filter or aggregation query, the single-stage explain plan page is usually enough.

## Useful patterns

When debugging multi-stage execution, start by:

1. running `EXPLAIN PLAN FOR`
2. checking whether the plan is logical or implementation-oriented
3. comparing the result with the query options you set

## What this page covered

This page covered what the multi-stage explain plan is useful for and how to approach it when debugging advanced SQL.

## Next step

If you are still deciding between engines, read [SSE vs MSE](../sse-vs-mse.md) in the broader query section.

## Related pages

- [Explain plan](explain-plan.md)
- [Querying Pinot](../querying-pinot.md)
- [SQL syntax](../sql-syntax.md)
