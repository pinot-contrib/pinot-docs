---
description: Match Pinot ingestion to the right input formats and deep-storage filesystems without overcomplicating the table design.
---

# Formats and Filesystems

Pinot supports several source formats and deep-storage choices. Pick these early, because they affect how segments are produced, moved, and recovered.

## Source formats

Use the original format docs when you need the exact supported file types or loader behavior. The main landing page is [Supported Data Formats](pinot-input-formats.md).

## Filesystems and deep storage

Choose the deep-storage backend that matches your operational environment. The detailed filesystem docs still live under [File Systems](file-systems/README.md).

## Keep it simple

Do not mix format decisions with schema design. The schema says what the data means; the filesystem says where segments survive after Pinot produces them.

## What this page covered

This page covered how source formats and deep storage fit into the ingestion design.

## Next step

Read [Transformations and Aggregations](transformations-and-aggregations.md) if data needs cleanup or pre-aggregation before query time.

## Related pages

- [Ingestion](README.md)
- [Batch Ingestion](batch-ingestion.md)
- [Stream Ingestion](stream-ingestion.md)
- [Upsert and Dedup](upsert-dedup.md)
- [Supported Data Formats](pinot-input-formats.md)
- [File Systems](file-systems/README.md)
