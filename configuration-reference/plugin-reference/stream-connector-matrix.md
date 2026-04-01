---
description: >-
  A version and packaging matrix for all stream ingestion connectors shipped
  with Apache Pinot.
---

# Stream Connector Version Matrix

This page provides a quick-reference matrix mapping each stream connector to its Maven module, artifact ID, underlying client library version, and consumer factory class.

## Connector matrix

<table>
  <thead>
    <tr>
      <th>Stream</th>
      <th>Connector Module</th>
      <th>Maven Artifact</th>
      <th>Client Library Version</th>
      <th>Consumer Factory Class</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Apache Kafka 3.x</td>
      <td>`pinot-kafka-3.0`</td>
      <td>`org.apache.pinot:pinot-kafka-3.0`</td>
      <td>kafka-clients 3.9.2</td>
      <td>`org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory`</td>
      <td>Default, included in binary distribution</td>
    </tr>
    <tr>
      <td>Apache Kafka 4.x</td>
      <td>`pinot-kafka-4.0`</td>
      <td>`org.apache.pinot:pinot-kafka-4.0`</td>
      <td>kafka-clients 4.1.1</td>
      <td>`org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory`</td>
      <td>Included in binary distribution</td>
    </tr>
    <tr>
      <td>Amazon Kinesis</td>
      <td>`pinot-kinesis`</td>
      <td>`org.apache.pinot:pinot-kinesis`</td>
      <td>AWS SDK 2.42.16 (`software.amazon.awssdk:kinesis`)</td>
      <td>`org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory`</td>
      <td>Included in binary distribution</td>
    </tr>
    <tr>
      <td>Apache Pulsar</td>
      <td>`pinot-pulsar`</td>
      <td>`org.apache.pinot:pinot-pulsar`</td>
      <td>pulsar-client 4.0.9</td>
      <td>`org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory`</td>
      <td>Optional, enable with `-Dplugins.include=pinot-pulsar`</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
All version numbers above are from the Pinot `master` branch (1.5.0-SNAPSHOT). Released Pinot versions may ship slightly different client library versions. Check the `pom.xml` of the corresponding module in your Pinot release for the exact version.
{% endhint %}

## Compatibility notes

### Kafka 3.x connector (`pinot-kafka-3.0`)

* Compatible with Kafka brokers version 2.x and above.
* Uses the Scala-based Kafka library alongside `kafka-clients`.
* This is the recommended connector for most deployments.

### Kafka 4.x connector (`pinot-kafka-4.0`)

* Requires Kafka brokers version 4.0 or above.
* Uses the pure-Java `kafka-clients` library only (no Scala dependency).
* Designed for KRaft-mode Kafka clusters that have removed ZooKeeper.
* Uses Testcontainers for integration testing instead of the embedded Kafka server.

### Amazon Kinesis connector (`pinot-kinesis`)

* Uses AWS SDK v2 (`software.amazon.awssdk`).
* Supports both key-based and IAM role-based authentication.
* Included in the default Pinot distribution.

### Apache Pulsar connector (`pinot-pulsar`)

* Not included in the default binary distribution. Enable with `-Dplugins.include=pinot-pulsar` at startup, or add the plugin JAR to the `plugins` directory.
* Uses the Apache Pulsar client library.
* Supports token-based, OAuth2, and TLS authentication.

## Removed connectors

<table>
  <thead>
    <tr>
      <th>Former Module</th>
      <th>Removed In</th>
      <th>Migration Path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-kafka-0.9`</td>
      <td>Pre-1.0</td>
      <td>Migrate to `pinot-kafka-3.0`</td>
    </tr>
    <tr>
      <td>`pinot-kafka-2.0`</td>
      <td>Pre-1.0</td>
      <td>Migrate to `pinot-kafka-3.0` (or `pinot-kafka-4.0` for Kafka 4.x brokers)</td>
    </tr>
  </tbody>
</table>

To migrate, update `stream.kafka.consumer.factory.class.name` in your table config from the old class to the new one. No other stream config changes are required.
