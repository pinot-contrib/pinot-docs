---
description: Dense reference for Pinot configuration surfaces.
---

# Configuration Reference

This section reorganizes the configuration surface into the core objects operators reach for most often: cluster, schema, table, ingestion, job specs, metrics, dynamic environment handling, and plugin settings. Cluster and schema configuration are flattened directly into this section, and the pages here are the primary reference entry points, while some legacy material still remains in the older `configuration-reference/` tree.

## Reference Map

| Area | Use it for | Reference page |
| --- | --- | --- |
| Cluster | Cluster-wide knobs, query protection, and broker behavior | [Cluster](cluster.md) |
| Schema | Column definitions, null handling, data types, and MAP field support | [Schema](schema.md) |
| Table | Offline, real-time, hybrid, routing, query, and indexing config | [Table](table.md) |
| Ingestion | Stream and batch ingestion settings embedded in table config | [Ingestion](ingestion.md) |
| Job spec | Offline ingestion job configuration and templating | [Ingestion Job Spec](job-specification.md) |
| Monitoring metrics | Server, broker, and controller metric configuration | [Monitoring Metrics](monitoring-metrics.md) |
| Dynamic environment | Environment-variable substitution in config payloads | [Dynamic Environment](dynamic-environment.md) |
| Plugin reference | Plugin-family configuration and version guidance | [Plugin Configuration Reference](plugin-reference.md) |

## What this page covers

- The dense configuration surfaces that belong in reference.
- The flat reference pages for the most commonly used Pinot config topics.
- How to get from this landing page to the detailed config docs.

## Next step

Open the specific config page for the object you are changing, then cross-check any linked table or schema behavior before editing a table config.

## Related pages

- [Table](table.md)
- [Schema](schema.md)
- [Ingestion](ingestion.md)
- [Plugin Configuration Reference](plugin-reference.md)
- [Legacy Plugin Configuration Landing](../plugin-reference/README.md)
