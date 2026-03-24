---
description: Use upsert or dedup when ingesting rows should collapse to one current record per key instead of preserving every event.
---

# Upsert and Dedup

Upsert and dedup are for tables that ingest repeated keys. Use them when the current value matters more than the raw event history, or when duplicate events should not fan out into duplicate query results.

## Choose the right behavior

Use upsert when newer rows should replace older rows for the same primary key.

Use dedup when repeated records should be filtered out and only the first or unique representation should remain.

## Operational notes

These patterns need a careful schema, a stable primary key, and ingestion flow that understands the table-level metadata Pinot uses to keep the result consistent.

The strongest detail still lives in the original docs under [Upsert and Dedup](../../manage-data/data-import/upsert-and-dedup/README.md).

## What this page covered

This page covered the difference between upsert and dedup and when each is the better fit.

## Next step

Read [Formats and Filesystems](formats-filesystems.md) to decide how Pinot should read source data and store generated segments.

## Related pages

- [Ingestion](README.md)
- [Batch Ingestion](batch-ingestion.md)
- [Stream Ingestion](stream-ingestion.md)
- [Formats and Filesystems](formats-filesystems.md)
- [Original Upsert and Dedup Docs](../../manage-data/data-import/upsert-and-dedup/README.md)
