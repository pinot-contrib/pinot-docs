---
description: >-
  Choose the right Apache Kafka connector version for your Pinot deployment.
---

# Kafka Connector Versions

Apache Pinot provides multiple Kafka connector versions to match different Kafka broker deployments. Choose the connector that matches your Kafka cluster version.

## Available Connectors

| Connector Plugin | Kafka Client Version | Notes |
|---|---|---|
| `pinot-kafka-3.0` | 3.9.x | Recommended for Kafka 3.x clusters. Requires Scala dependency. |
| `pinot-kafka-4.0` | 4.1.x | Recommended for Kafka 4.x clusters (KRaft mode). Pure Java — no Scala dependency. |

{% hint style="warning" %}
The `pinot-kafka-2.0` (kafka20) plugin has been removed. If your table config references `org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory`, you must migrate to either `kafka30` or `kafka40`.
{% endhint %}

## Kafka 4.0 Connector

The Kafka 4.0 connector (`pinot-kafka-4.0`) supports Apache Kafka 4.x brokers running in **KRaft mode** (ZooKeeper-free). It uses pure Java Kafka clients with no Scala dependency, resulting in a smaller deployment footprint.

### When to use Kafka 4.0

- Your Kafka cluster runs Kafka 4.0+ with KRaft mode
- You want to eliminate the Scala transitive dependency
- You are deploying new Pinot clusters against modern Kafka infrastructure

### Configuration

The Kafka 4.0 connector uses the same configuration properties as the Kafka 3.0 connector. The only difference is the `stream.kafka.consumer.factory.class.name`:

```json
{
  "streamConfigs": {
    "streamType": "kafka",
    "stream.kafka.topic.name": "your-topic",
    "stream.kafka.broker.list": "kafka:9092",
    "stream.kafka.consumer.type": "lowlevel",
    "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory",
    "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
    "realtime.segment.flush.threshold.rows": "0",
    "realtime.segment.flush.threshold.time": "24h",
    "realtime.segment.flush.threshold.segment.size": "100M"
  }
}
```

### Migration from Kafka 3.0

To migrate from the Kafka 3.0 connector to Kafka 4.0:

1. Update the consumer factory class name in your table configuration:

| From | To |
|---|---|
| `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` | `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` |

2. Ensure the `pinot-kafka-4.0` plugin JAR is available in your Pinot plugin directory.

3. All other `stream.kafka.*` configuration properties remain the same.

{% hint style="info" %}
The Kafka 4.0 connector is fully compatible with all existing Kafka consumer configuration properties including SSL/TLS, SASL authentication, isolation levels, and Schema Registry integration. See the [main Kafka ingestion guide](import-from-apache-kafka.md) for detailed configuration examples.
{% endhint %}

## Kafka 3.0 Connector

The Kafka 3.0 connector (`pinot-kafka-3.0`) supports Apache Kafka 3.x brokers. This is the most widely deployed connector version.

### Configuration

```json
{
  "streamConfigs": {
    "streamType": "kafka",
    "stream.kafka.topic.name": "your-topic",
    "stream.kafka.broker.list": "kafka:9092",
    "stream.kafka.consumer.type": "lowlevel",
    "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
    "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder"
  }
}
```

## Common Configuration Properties

All Kafka connector versions share the same configuration properties. See [Ingest streaming data from Apache Kafka](import-from-apache-kafka.md) for the complete configuration reference, including:

- SSL/TLS setup
- SASL authentication
- Schema Registry integration (Avro, JSON Schema, Protobuf)
- Consumer tuning properties
- Isolation levels (`read_committed` / `read_uncommitted`)

## Passing Native Kafka Consumer Properties

You can pass any native Kafka consumer configuration property using the `stream.kafka.consumer.prop.` prefix:

```json
{
  "streamConfigs": {
    "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
    "stream.kafka.consumer.prop.max.poll.records": "500",
    "stream.kafka.consumer.prop.fetch.min.bytes": "100000",
    "stream.kafka.consumer.prop.session.timeout.ms": "30000"
  }
}
```
