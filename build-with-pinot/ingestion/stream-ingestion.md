---
description: Choose stream ingestion when Pinot should consume events continuously and expose new rows quickly.
---

# Stream Ingestion

Stream ingestion keeps Pinot close to the source of truth. Use it when rows should be queryable soon after they are emitted, and when the system needs a steady flow rather than periodic batch loads.

## Core decisions

Pick the stream connector and partitioning strategy.

Choose how Pinot should flush, commit, and complete segments.

Decide whether the table should remain purely realtime or later become hybrid.

## What matters most

The stream has to support the consumption mode you choose. The table config has to describe the partitioning, replicas, and segment lifecycle clearly enough that the servers can behave predictably under load.

## Learn more

The existing walk-throughs in [Import Data](README.md) and [Data Ingestion Overview](README.md) still contain the detailed mechanics.

## What this page covered

This page covered the stream-ingestion model and the main lifecycle choices behind it.

## Next step

Read [Upsert and Dedup](upsert-dedup.md) if the stream should collapse duplicate keys or keep only the latest row.

## Related pages

- [Ingestion](README.md)
- [Batch Ingestion](batch-ingestion.md)
- [Upsert and Dedup](upsert-dedup.md)
- [Formats and Filesystems](formats-filesystems.md)
- [Original Stream Docs](stream-ingestion/README.md)
