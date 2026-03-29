---
description: Dense reference for Pinot configuration surfaces.
---

# Configuration Reference

This section reorganizes the configuration surface into the core objects operators reach for most often: cluster, schema, table, ingestion, job specs, metrics, and plugin settings. Cluster configuration is flattened directly into this section, while the other detailed source pages still live in the existing `configuration-reference/` tree.

## Reference Map

| Area | Use it for | Reference page |
| --- | --- | --- |
| Cluster | Cluster-wide knobs, query protection, and broker behavior | [Cluster](cluster.md) |
| Schema | Column definitions, null handling, and data types | [Schema](../../configuration-reference/schema.md) |
| Table | Offline, real-time, hybrid, routing, query, and indexing config | [Table](../../configuration-reference/table.md) |
| Ingestion | Stream and batch ingestion settings embedded in table config | [Ingestion](../../configuration-reference/ingestion.md) |
| Job spec | Offline ingestion job configuration and templating | [Ingestion Job Spec](../../configuration-reference/job-specification.md) |
| Monitoring metrics | Server, broker, and controller metric configuration | [Monitoring Metrics](../../configuration-reference/monitoring-metrics.md) |
| Dynamic environment | Environment-variable substitution in config payloads | [Dynamic Environment](../../configuration-reference/dynamic-environment.md) |
| Plugin reference | Plugin-family configuration and version guidance | [Plugin Families Reference](../plugin-reference/README.md) |

## What this page covered

- The dense configuration surfaces that belong in reference.
- Where the existing canonical pages live today.
- How to get from this landing page to the detailed config docs.

## Next step

Open the specific config page for the object you are changing, then cross-check any linked table or schema behavior before editing a table config.

## Related pages

- [Table](../../configuration-reference/table.md)
- [Schema](../../configuration-reference/schema.md)
- [Ingestion](../../configuration-reference/ingestion.md)
- [Plugin Families Reference](../plugin-reference/README.md)
- [Legacy Plugin Configuration Landing](../../configuration-reference/plugin-reference/README.md)
