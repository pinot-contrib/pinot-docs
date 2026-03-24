---
description: Stream ingestion connector reference.
---

# Stream Ingestion Connectors

Pinot ships stream ingestion connectors for Kafka, Kinesis, and Pulsar. This page is the configuration reference for the connector family rather than the authoring guide.

## Built-in Connectors

| Connector | Factory class | Notes |
| --- | --- | --- |
| Kafka 3.x | `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` | Default modern Kafka connector |
| Kinesis | `org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory` | Amazon Kinesis integration |
| Pulsar | `org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory` | Apache Pulsar integration |

## What this page covered

- The built-in stream connector family.
- The key factory class names used in stream config.
- The most relevant connector compatibility concerns.

## Next step

Match the connector family to the stream source you are ingesting, then check the version matrix before upgrading the client or broker side.

## Related pages

- [Plugin Reference](README.md)
- [Stream Connector Version Matrix](stream-connector-matrix.md)
- [Ingestion](../configuration-reference/ingestion.md)
