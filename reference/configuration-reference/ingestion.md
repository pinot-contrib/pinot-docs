---
description: Ingestion configuration reference.
---

# Ingestion Configuration

This page is the reference hub for ingestion config that lives inside table config: stream config maps, batch ingestion config, validation checks, and row-level transform behavior. The detailed property tables remain in the original ingestion config page.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Stream ingestion | Kafka, Kinesis, Pulsar, decoder, and consumer config | [Ingestion](../../configuration-reference/ingestion.md) |
| Batch ingestion | Offline segment creation cadence and framework settings | [Ingestion](../../configuration-reference/ingestion.md) |
| Validation | Continue-on-error and time-value checks | [Ingestion](../../configuration-reference/ingestion.md) |
| Runtime templates | Table-level ingestion examples and JSON payloads | [Ingestion](../../configuration-reference/ingestion.md) |

## What this page covered

- The ingestion knobs nested in table configuration.
- The split between stream and batch ingestion settings.
- Where to find the canonical property lists and examples.

## Next step

Verify the ingestion mode and source system first, then update the corresponding table config section instead of spreading settings across unrelated files.

## Related pages

- [Configuration Reference](README.md)
- [Table](../../configuration-reference/table.md)
- [Plugin Families Reference](../plugin-reference/README.md)
