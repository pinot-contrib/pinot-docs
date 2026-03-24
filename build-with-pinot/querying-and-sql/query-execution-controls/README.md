---
description: Query controls, diagnostics, and pagination behavior for Pinot SQL.
---

# Querying & SQL Controls

Use this section when the query already works and you need to control how it runs, how it is tracked, or how results are paginated.

The pages here cover the main runtime controls:

- [Query options](query-options.md)
- [Query quotas](query-quotas.md)
- [Query cancellation](query-cancellation.md)
- [Cursor pagination](query-using-cursors.md)
- [Correlation IDs](query-correlation-id.md)
- [Explain plan](explain-plan.md)
- [Multi-stage explain plan](explain-plan-multi-stage.md)

## How to use this section

Start with query options when you need to change a single query.

Move to quotas when you need to control query rate at the table, database, or application level.

Use cancellation and correlation IDs together when you need to track or stop a running query.

Use cursor pagination when the result set is too large to return in one response.

Use explain plan when you need to understand engine behavior or index usage.

Use the multi-stage explain plan page when the query depends on joins, subqueries, or other advanced SQL features.

## What this page covered

This page summarized the query-control pages and explained when to use each one.

## Next step

Open [Query options](query-options.md) if you need to tune a query, or [Explain plan](explain-plan.md) if you need to debug how Pinot will execute it.

## Related pages

- [Querying Pinot](../querying-pinot.md)
- [SQL syntax](../sql-syntax.md)
- [Query options](query-options.md)
- [Query quotas](query-quotas.md)
