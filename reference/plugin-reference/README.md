---
description: Dense reference for Pinot plugin families.
---

# Plugin Families Reference

This section is the reference map for Pinot's built-in plugin families. The detailed family pages live here so the configuration tree can stay dense and the authoring guides can stay elsewhere.

## Plugin Families

| Family | Use it for | Page |
| --- | --- | --- |
| Stream ingestion connectors | Kafka, Kinesis, and Pulsar consumer factories | [Stream Ingestion Connectors](stream-ingestion-connectors.md) |
| Stream connector version matrix | Compatibility between broker, connector, and Kafka major versions | [Stream Connector Version Matrix](stream-connector-matrix.md) |
| Metrics plugins | JMX metric backends and registry fan-out | [Metrics Plugins](metrics-plugins.md) |
| Environment provider | Cloud metadata discovery for instance placement | [Environment Provider](environment-provider.md) |

## What this page covered

- The plugin families that belong in the configuration reference.
- The detailed pages that live under this subtree.
- The areas where version compatibility matters most.

## Next step

Open the plugin-family page for the integration you are changing, then verify supported versions before changing deployment settings.

## Related pages

- [Configuration Reference](../configuration-reference/README.md)
- [Stream Ingestion Connectors](stream-ingestion-connectors.md)
- [Metrics Plugins](metrics-plugins.md)
