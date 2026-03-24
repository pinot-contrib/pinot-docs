---
description: Table configuration reference.
---

# Table Configuration

The detailed table config page stays in the original location. This page is the reference entry point for the pieces operators edit most often: table identity, routing, query controls, ingestion settings, indexing, tenants, and upsert or dedup.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Table identity | OFFLINE, REALTIME, and hybrid table structure | [Table](../../configuration-reference/table.md) |
| Routing | Broker-to-server routing and pruning behavior | [Table](../../configuration-reference/table.md) |
| Query settings | Query timeout, resource limits, and engine toggles | [Table](../../configuration-reference/table.md) |
| Ingestion | Batch and streaming ingestion config nested in table config | [Ingestion](../../configuration-reference/ingestion.md) |
| Indexing | Per-column index configuration and deprecated forms | [Table](../../configuration-reference/table.md) |
| Upsert and dedup | Real-time correctness controls for mutable streams | [Table](../../configuration-reference/table.md) |

## What this page covered

- The table config areas that most directly affect ingestion and query behavior.
- The canonical table-config reference page.
- The relationship between table config and the rest of the reference tree.

## Next step

Check the table config page and the related ingestion or indexing page before editing a production table definition.

## Related pages

- [Configuration Reference](README.md)
- [Schema](../../configuration-reference/schema.md)
- [Ingestion](../../configuration-reference/ingestion.md)
- [Indexing](../../basics/indexing/README.md)
