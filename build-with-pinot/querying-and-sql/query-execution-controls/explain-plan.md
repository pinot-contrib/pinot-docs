---
description: How to inspect Pinot's execution plan for a query.
---

# Explain Plan

Use `EXPLAIN PLAN FOR` when you want to understand how Pinot will execute a query before or while tuning it.

## What it tells you

Explain plan output helps you see:

- which operators Pinot will run
- whether an index is being used
- where filters, projections, and aggregations happen
- how a query is shaped in single-stage or multi-stage execution

```sql
EXPLAIN PLAN FOR
SELECT city, COUNT(*)
FROM stores
GROUP BY city;
```

## Single-stage and multi-stage

Single-stage explain plans are best for understanding the operator flow behind straightforward queries.

Multi-stage explain plans are better when you need to inspect joins, subqueries, or the distributed execution shape.

## How to use it

Start with explain plan when a query is:

- slower than expected
- not using the index you expected
- returning a shape that is hard to reason about

Then pair the plan with query options or index guidance if you need a fix.

## What this page covered

This page covered what explain plan shows, when to use it, and how the single-stage and multi-stage engines differ.

## Next step

If you need a deeper execution-shape discussion, read [SQL syntax](../sql-syntax.md) and then revisit query options or quotas if the issue is runtime control rather than syntax.

## Related pages

- [Query options](query-options.md)
- [Querying Pinot](../querying-pinot.md)
- [SQL syntax](../sql-syntax.md)
