---
description: >-
  Decode Avro, JSON, and Protobuf messages from Kafka using Confluent Schema Registry.
---

# Confluent Schema Registry Decoders

Pinot supports decoding Kafka messages serialized with [Confluent Schema Registry](https://docs.confluent.io/platform/current/schema-registry/index.html) for Avro, JSON Schema, and Protocol Buffers formats. These decoders automatically fetch and cache schemas from the registry, ensuring data is deserialized according to the registered schema.

## Available Decoders

| Format | Decoder Class | Plugin |
|--------|--------------|--------|
| **Avro** | `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` | `pinot-confluent-avro` |
| **JSON Schema** | `org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder` | `pinot-confluent-json` |
| **Protocol Buffers** | `org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder` | `pinot-confluent-protobuf` |

## Common Configuration

All Confluent Schema Registry decoders share the same configuration properties:

| Property | Required | Default | Description |
|----------|----------|---------|-------------|
| `schema.registry.rest.url` | Yes | — | Confluent Schema Registry REST endpoint URL |
| `cached.schema.map.capacity` | No | 1000 | Maximum number of schemas to cache locally |

### SSL/TLS Configuration

To connect to a Schema Registry endpoint over SSL/TLS, add properties with the `schema.registry.` prefix:

| Property | Description |
|----------|-------------|
| `schema.registry.ssl.truststore.location` | Path to truststore file |
| `schema.registry.ssl.truststore.password` | Truststore password |
| `schema.registry.ssl.keystore.location` | Path to keystore file |
| `schema.registry.ssl.keystore.password` | Keystore password |
| `schema.registry.ssl.key.password` | Private key password |

## Confluent Avro Decoder

Decodes Avro-serialized Kafka messages with schema managed by Confluent Schema Registry.

```json
{
  "streamConfigs": {
    "streamType": "kafka",
    "stream.kafka.topic.name": "my-avro-topic",
    "stream.kafka.broker.list": "kafka:9092",
    "stream.kafka.consumer.type": "lowlevel",
    "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
    "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder",
    "stream.kafka.decoder.prop.schema.registry.rest.url": "http://schema-registry:8081"
  }
}
```

## Confluent JSON Schema Decoder

Decodes JSON messages serialized with Confluent's JSON Schema serializer. Messages include a schema ID header that the decoder uses to fetch the JSON Schema from the registry for validation.

```json
{
  "streamConfigs": {
    "streamType": "kafka",
    "stream.kafka.topic.name": "my-json-topic",
    "stream.kafka.broker.list": "kafka:9092",
    "stream.kafka.consumer.type": "lowlevel",
    "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
    "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder",
    "stream.kafka.decoder.prop.schema.registry.rest.url": "http://schema-registry:8081"
  }
}
```

{% hint style="info" %}
The JSON Schema decoder validates incoming messages against the schema registered in Schema Registry. Messages that don't match the magic byte format (non-Confluent messages) are silently dropped.
{% endhint %}

## Confluent Protobuf Decoder

Decodes Protocol Buffer messages serialized with Confluent's Protobuf serializer. The decoder fetches the `.proto` schema definition from the registry and deserializes the binary payload.

```json
{
  "streamConfigs": {
    "streamType": "kafka",
    "stream.kafka.topic.name": "my-protobuf-topic",
    "stream.kafka.broker.list": "kafka:9092",
    "stream.kafka.consumer.type": "lowlevel",
    "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
    "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder",
    "stream.kafka.decoder.prop.schema.registry.rest.url": "http://schema-registry:8081"
  }
}
```

## SSL/TLS Example

To connect to a secured Schema Registry:

```json
{
  "streamConfigs": {
    "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder",
    "stream.kafka.decoder.prop.schema.registry.rest.url": "https://schema-registry:8082",
    "stream.kafka.decoder.prop.schema.registry.ssl.truststore.location": "/path/to/truststore.jks",
    "stream.kafka.decoder.prop.schema.registry.ssl.truststore.password": "changeit",
    "stream.kafka.decoder.prop.schema.registry.ssl.keystore.location": "/path/to/keystore.jks",
    "stream.kafka.decoder.prop.schema.registry.ssl.keystore.password": "changeit"
  }
}
```

## How Schema Resolution Works

1. Each Confluent-serialized message starts with a magic byte (`0x00`) followed by a 4-byte schema ID
2. The decoder extracts the schema ID from the message header
3. The schema is fetched from Schema Registry and cached locally (up to `cached.schema.map.capacity`)
4. The message payload is deserialized using the resolved schema
5. Fields are extracted into Pinot's `GenericRow` format for ingestion

Messages without the Confluent magic byte prefix are silently dropped and logged as errors.

## See Also

- [Ingest from Apache Kafka](import-from-apache-kafka.md) — General Kafka ingestion guide
- [Stream Ingestion Connectors](../../../configuration-reference/plugin-reference/stream-ingestion-connectors.md) — Full connector configuration reference
- [Supported Data Formats](../pinot-input-formats.md) — All supported input formats
