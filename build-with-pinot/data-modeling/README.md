---
description: Build Pinot tables by getting schema, table shape, logical-table, and schema-evolution decisions right before ingestion starts.
---

# Data Modeling

Pinot works best when the table shape is clear before data lands. Start here to understand the structure that every ingestion and query decision depends on: schema design, table composition, logical-table layout, and how schemas evolve without breaking existing pipelines.

If you need dense JSON config or controller endpoints, jump to the [Reference](../../reference/README.md) section instead. This section stays narrative and decision-oriented.

## Start Here

- [Schema and Table Shape](schema.md)
- [Logical Tables](logical-tables.md)
- [Schema Evolution](schema-evolution.md)

## Related Existing Docs

- [Schema](../../basics/components/table/schema.md)
- [Table](../../basics/components/table/README.md)
- [Logical Table](../../basics/components/table/logical-table.md)
- [Schema Evolution Tutorial](../../tutorials/data-ingestion/schema-evolution.md)
- [Schema Reference](../../configuration-reference/schema.md)
- [Table Reference](../../configuration-reference/table.md)

## What this page covered

This landing page defines the scope of Pinot data modeling and points to the core pages that matter first.

## Next step

Read [Schema and Table Shape](schema.md) to lock in the table structure before designing ingestion.

## Related pages

- [Schema and Table Shape](schema.md)
- [Logical Tables](logical-tables.md)
- [Schema Evolution](schema-evolution.md)
