---
description: Query-level switches that shape execution, diagnostics, and resource use.
---

# Query Options

Query options are per-query switches that let you choose the execution engine, control runtime limits, and adjust diagnostics.

## The options that matter most

- `useMultistageEngine` selects the multi-stage engine for queries that need advanced SQL features.
- `timeoutMs` bounds how long Pinot should spend on the query.
- `clientQueryId` gives the query a stable identifier for tracking and cancellation.
- `explainPlanVerbose` asks Pinot for richer plan output.
- `maxExecutionThreads` limits concurrency for expensive queries.

```sql
SET useMultistageEngine = true;
SET timeoutMs = 5000;
SET clientQueryId = 'query-2026-03-24-001';
SELECT city, COUNT(*)
FROM stores
GROUP BY city
LIMIT 10;
```

## When to reach for options

Use query options when you want to change behavior without changing table configuration.

Typical cases include:

- lowering timeout for a user-facing request
- forcing multi-stage execution for a query that needs joins
- attaching a custom query ID for logs and cancellation
- widening or narrowing execution resources for a single query

## Where the deeper knobs live

Some query behavior is controlled by dedicated pages rather than a raw option list:

- use [Query quotas](query-quotas.md) for rate limiting
- use [Query cancellation](query-cancellation.md) when a query must be stopped
- use [Cursor pagination](query-using-cursors.md) when the result set is too large

## What this page covered

This page covered the main query-level switches, why you would set them, and which dedicated pages handle related controls.

## Next step

If you need to track or stop a query, read [Query cancellation](query-cancellation.md). If you need to shape result delivery, read [Cursor pagination](query-using-cursors.md).

## Related pages

- [Querying Pinot](../querying-pinot.md)
- [SQL syntax](../sql-syntax.md)
- [Query quotas](query-quotas.md)
- [Correlation IDs](query-correlation-id.md)
