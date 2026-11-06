---
description: >-
  Apache Pinot ships a single Kafka connector, pinot-kafka-4.0, which is the
  default for stream ingestion.
---

# Kafka Connector Versions

{% hint style="info" %}
Starting in Pinot 1.7.0, `pinot-kafka-4.0` is the only Kafka connector and the default for tables that omit the consumer factory. The `pinot-kafka-3.0` connector was removed and consolidated into `pinot-kafka-4.0`. Existing table configs that reference the older connectors keep working: the old factory and plugin names resolve directly to Kafka 4 (see [Backward compatibility](#backward-compatibility-of-older-connector-names)).
{% endhint %}

Apache Pinot provides a single Kafka connector, `pinot-kafka-4.0`, built on the pure-Java Kafka 4 client. It supports both ZooKeeper-based and KRaft-mode Kafka clusters.

## Available Connectors

| Connector Plugin | Kafka Client Version | Notes |
|---|---|---|
| `pinot-kafka-4.0` | 4.x | The only Kafka connector and the default when the consumer factory is unset. Pure Java — no Scala dependency. |

The Kafka 4 client requires Kafka brokers version 2.1 or newer. Upgrading the Pinot plugin does **not** require Kafka 4 brokers or a broker-side ZooKeeper-to-KRaft migration. Review [Kafka's client upgrade guide](https://kafka.apache.org/42/getting-started/upgrade/) for other removed Kafka 3 client configuration/API support.

{% hint style="warning" %}
The `pinot-kafka-2.0` (kafka20) and `pinot-kafka-3.0` (kafka30) plugins have been removed. You do not need to change existing table configs — their old factory and plugin names resolve to Kafka 4 (see [Backward compatibility](#backward-compatibility-of-older-connector-names)) — but custom deployments must package the `pinot-kafka-4.0` plugin, as the aliases do not retain the Kafka 2 or Kafka 3 client or its protocol support.
{% endhint %}

## Kafka 4.0 Connector

The Kafka 4.0 connector (`pinot-kafka-4.0`) uses pure Java Kafka clients with no Scala dependency, resulting in a smaller deployment footprint. It supports Apache Kafka brokers 2.1 and newer, including Kafka 4.x brokers running in **KRaft mode** (ZooKeeper-free).

### Configuration

Leave `stream.kafka.consumer.factory.class.name` unset to use the Kafka 4 default, or set it explicitly:

```json
{
  "streamConfigs": {
    "streamType": "kafka",
    "stream.kafka.topic.name": "your-topic",
    "stream.kafka.broker.list": "kafka:9092",
    "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory",
    "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
    "realtime.segment.flush.threshold.rows": "0",
    "realtime.segment.flush.threshold.time": "24h",
    "realtime.segment.flush.threshold.segment.size": "100M"
  }
}
```

{% hint style="info" %}
The Kafka 4.0 connector is fully compatible with all existing Kafka consumer configuration properties including SSL/TLS, SASL authentication, isolation levels, and Schema Registry integration. See the [main Kafka ingestion guide](import-from-apache-kafka.md) for detailed configuration examples.
{% endhint %}

## Backward compatibility of older connector names

You do **not** need to change existing table configs. Every historical Kafka factory and plugin name resolves directly to the Kafka 4 implementation (aliases are not chained):

| Older name in your config | Resolves to |
|---|---|
| `org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory` | `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` |
| `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` | `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` |
| `org.apache.pinot.core.realtime.impl.kafka2.KafkaConsumerFactory` | `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` |
| `org.apache.pinot.core.realtime.impl.kafka3.KafkaConsumerFactory` | `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` |
| `plugins.include` / plugin-qualified names `pinot-kafka-2.0`, `pinot-kafka-3.0` | `pinot-kafka-4.0` |

Stored table configs remain unchanged, and existing offsets and `stream.kafka.*` keys continue to work. The removed `org.apache.kafka.common.security.oauthbearer.secured.OAuthBearerLoginCallbackHandler` class name (including its Pinot-shaded form) also resolves to the current OAuth login callback.

The Kafka 4 client reads a few removed Kafka 3 settings and translates them transparently:

- `auto.include.jmx.reporter` is translated to `metric.reporters`, preserving the Kafka 3 behavior. `true` (or omitting the flag) adds the built-in JMX reporter alongside any custom reporters when absent; `false` disables only automatic inclusion while preserving every explicitly configured reporter, including JMX.

{% hint style="warning" %}
Kafka 4 defaults the `org.apache.kafka.sasl.oauthbearer.allowed.urls` JVM property to an empty allowlist. Before upgrading OAuth-based sources, allow their trusted token endpoint and any configured JWKS URL with this JVM property (see [Kafka system properties](https://kafka.apache.org/42/configuration/system-properties/)). The callback-class alias does not bypass this security requirement.
{% endhint %}

### Rolling upgrade and rollback

During a rolling upgrade, keep existing factory names in table configs so each component uses its own default. Avoid writing explicit Kafka 4 factory names until every component that consumes table configs has the Kafka 4 plugin. Validate partition discovery, ingestion from saved offsets, and restart/replay on representative sources before completing rollout. Before rolling back to an image without the Kafka 4 plugin, restore the legacy factory names in any table configs changed after the upgrade.

## Common Configuration Properties

The Kafka connector configuration properties are documented in [Ingest streaming data from Apache Kafka](import-from-apache-kafka.md), including:

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
