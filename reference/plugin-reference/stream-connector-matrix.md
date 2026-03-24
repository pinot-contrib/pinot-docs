---
description: Stream connector version compatibility matrix.
---

# Stream Connector Version Matrix

Use this page when you are deciding whether a stream connector upgrade is safe with the Pinot version you are running. The important part is compatibility, not the exact artifact name.

## Version Guidance

| Connector family | What to verify |
| --- | --- |
| Kafka | Broker-side connector package and Kafka major version compatibility |
| Kinesis | AWS SDK and Pinot connector version compatibility |
| Pulsar | Connector package and broker runtime compatibility |

## What this page covered

- Why stream connector version matching matters.
- Which connector families need the most compatibility checking.
- Where to go next when you are ready to change a connector version.

## Next step

Confirm the source system version first, then check the connector matrix before you change the table config.

## Related pages

- [Plugin Reference](README.md)
- [Stream Ingestion Connectors](stream-ingestion-connectors.md)
- [Ingestion](../configuration-reference/ingestion.md)
