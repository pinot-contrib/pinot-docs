---
description: Use ingest-time transformations and aggregations when Pinot should normalize or reduce data before it reaches query time.
---

# Transformations and Aggregations

Ingestion transformations clean up source records before they become Pinot rows. Ingestion aggregations reduce repeated values into fewer rows when a realtime table can safely store the summarized shape instead of the raw event stream.

## Transformations

Use transformations to rename, reshape, extract, filter, or derive fields while ingesting. Keep the logic close to the table so the pipeline stays understandable.

The detailed examples still live in [Ingestion Transformations](ingestion-level-transformations.md).

## Aggregations

Use ingestion aggregation when the use case only needs summarized realtime data. This can reduce storage and improve query performance, but it changes the data you keep, so use it only when raw rows are not needed later.

The detailed examples still live in [Ingestion Aggregations](ingestion-level-aggregations.md).

## What this page covered

This page covered when to transform or aggregate data during ingestion instead of waiting for query time.

## Next step

Read the reference pages if you need the exact ingestion-config fields or table-config JSON.

## Related pages

- [Ingestion](README.md)
- [Batch Ingestion](batch-ingestion.md)
- [Stream Ingestion](stream-ingestion.md)
- [Formats and Filesystems](formats-filesystems.md)
- [Original Ingestion Transformations](ingestion-level-transformations.md)
- [Original Ingestion Aggregations](ingestion-level-aggregations.md)
