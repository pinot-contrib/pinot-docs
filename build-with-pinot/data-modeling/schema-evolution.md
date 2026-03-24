---
description: Evolve Pinot schemas safely by adding columns, reloading segments, and deciding when a new table is the cleaner path.
---

# Schema Evolution

Pinot schema evolution is intentionally narrow. The safe path is to add columns, reload the affected segments, and backfill only when the table type and data flow support it. If the change is more invasive than that, create a new table instead of forcing the old one to stretch.

## What is safe

Additive schema changes are the normal path. New columns can be introduced without rewriting the whole table, as long as the ingestion flow and segment reload behavior are understood.

## What is not safe

Renaming a column, dropping a column, or changing a column type is not a small schema tweak. Treat those as table redesign work.

## Typical flow

1. Add the new column to the schema.
2. Update the table config or ingestion config if the new field needs transforms.
3. Reload the affected segments.
4. Backfill historical data if the use case needs it.

## Reference material

The detailed walkthrough still lives in [Schema Evolution tutorial](../../tutorials/data-ingestion/schema-evolution.md).

## What this page covered

This page covered the additive schema-evolution path and the cases where a new table is safer.

## Next step

Read the ingestion pages to see how schema design affects batch and stream pipelines.

## Related pages

- [Data Modeling](README.md)
- [Schema and Table Shape](schema.md)
- [Logical Tables](logical-tables.md)
- [Original Schema Evolution Tutorial](../../tutorials/data-ingestion/schema-evolution.md)
