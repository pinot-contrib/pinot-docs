---
description: Configuration reference entry point for Pinot plugins.
---

# Plugin Configuration Reference

This page points to the configuration surface for Pinot plugin families. The detailed plugin-family tables now live in the new `reference/plugin-reference/` subtree.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Stream ingestion connectors | Kafka, Kinesis, Pulsar config and version compatibility | [Plugin Families Reference](../plugin-reference/README.md) |
| Metrics plugins | JMX metric backends and compound registries | [Plugin Families Reference](../plugin-reference/README.md) |
| Environment provider | Cloud metadata discovery for placement decisions | [Plugin Families Reference](../plugin-reference/README.md) |

## What this page covered

- The plugin families that expose configuration knobs.
- Where the canonical plugin-family pages live today.
- Which plugin pages are most relevant for ingestion and metrics work.

## Next step

Open the plugin family page that matches your integration surface, then verify implementation compatibility before changing a connector version.

## Related pages

- [Configuration Reference](README.md)
- [Plugin Families Reference](../plugin-reference/README.md)
- [Ingestion](../../configuration-reference/ingestion.md)
