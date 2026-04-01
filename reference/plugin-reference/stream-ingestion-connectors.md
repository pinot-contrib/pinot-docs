---
description: Stream ingestion connector reference.
---

# Stream Ingestion Connectors

Pinot ships stream ingestion connectors for Kafka, Kinesis, and Pulsar. This page is the configuration reference for the connector family rather than the authoring guide.

## Built-in Connectors

<table>
  <thead>
    <tr>
      <th>Connector</th>
      <th>Factory class</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Kafka 3.x</td>
      <td>`org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory`</td>
      <td>Default modern Kafka connector</td>
    </tr>
    <tr>
      <td>Kinesis</td>
      <td>`org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory`</td>
      <td>Amazon Kinesis integration</td>
    </tr>
    <tr>
      <td>Pulsar</td>
      <td>`org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory`</td>
      <td>Apache Pulsar integration</td>
    </tr>
  </tbody>
</table>

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
