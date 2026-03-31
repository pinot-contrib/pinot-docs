---
description: Plan Pinot ingestion around batch, stream, upsert, dedup, formats, filesystems, and transformation choices.
---

# Ingestion

Ingestion is where Pinot tables become real. Start here to choose the right path for batch or stream data, then refine the design with upsert, dedup, file format, filesystem, transform, and aggregation decisions.

The detailed controller and table-config material belongs in [Reference](../../reference/README.md). This section stays focused on data flow and operational choices.

## Start Here

- [Batch Ingestion](batch-ingestion.md) - for data that arrives in files or lands in a warehouse-style batch flow.
- [Stream Ingestion](stream-ingestion.md) - for Kafka-style or other event streams that should be queryable quickly.
- [Upsert and Dedup](upsert-dedup.md) - for tables that need one canonical row per key instead of raw event history.
- [Formats and Filesystems](formats-filesystems.md) - for source formats, file systems, and deep-storage choices.
- [Transformations and Aggregations](transformations-and-aggregations.md) - for ingest-time cleanup and pre-aggregation decisions.

## Related Existing Docs

- [Import Data](../../manage-data/data-import/README.md)
- [Data Ingestion Overview](../../developers/advanced/data-ingestion.md)
- [Ingestion Transformations](ingestion-level-transformations.md)
- [Ingestion Aggregations](ingestion-level-aggregations.md)
- [Supported Data Formats](pinot-input-formats.md)
- [File Systems](file-systems/README.md)

## What this page covered

This landing page defines the ingestion subtree and points to the main decision pages.

## Next step

Read [Batch Ingestion](batch-ingestion.md) if your source data arrives in files or prebuilt segments.

## Related pages

- [Batch Ingestion](batch-ingestion.md)
- [Stream Ingestion](stream-ingestion.md)
- [Upsert and Dedup](upsert-dedup.md)
- [Formats and Filesystems](formats-filesystems.md)
- [Transformations and Aggregations](transformations-and-aggregations.md)
