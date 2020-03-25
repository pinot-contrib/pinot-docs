---
description: This page describes how to connect Kafka to Pinot
---

# Kafka

### Kafka 2.x Plugin

Pinot provides stream plugin support for Kafka 2.x version. Although the version used in this implementation is kafka 2.0.0, it’s possible to compile it with higher kafka lib version, e.g. 2.1.1.

#### How to build and release Pinot package with Kafka 2.x connector

```text
mvn clean package -DskipTests -Pbin-dist -Dkafka.version=2.0
```

#### How to use Kafka 2.x connector

* **Use Kafka Stream\(High\) Level Consumer**

Below is a sample `streamConfigs` used to create a realtime table with Kafka Stream\(High\) level consumer.

Kafka 2.x HLC consumer uses `org.apache.pinot.core.realtime.impl.kafka2.KafkaConsumerFactory` in config `stream.kafka.consumer.factory.class.name`.

```text
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.consumer.type": "highLevel",
  "stream.kafka.topic.name": "meetupRSVPEvents",
  "stream.kafka.decoder.class.name": "org.apache.pinot.core.realtime.impl.kafka.KafkaJSONMessageDecoder",
  "stream.kafka.hlc.zk.connect.string": "localhost:2191/kafka",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.core.realtime.impl.kafka2.KafkaConsumerFactory",
  "stream.kafka.zk.broker.url": "localhost:2191/kafka",
  "stream.kafka.hlc.bootstrap.server": "localhost:19092"
}
```

* **Use Kafka Partition\(Low\) Level Consumer**

Below is a sample table config used to create a realtime table with Kafka Partition\(Low\) level consumer:

```text
{
  "tableName": "meetupRsvp",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "mtime",
    "timeType": "MILLISECONDS",
    "segmentPushType": "APPEND",
    "segmentAssignmentStrategy": "BalanceNumSegmentAssignmentStrategy",
    "schemaName": "meetupRsvp",
    "replication": "1",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "LowLevel",
      "stream.kafka.topic.name": "meetupRSVPEvents",
      "stream.kafka.decoder.class.name": "org.apache.pinot.core.realtime.impl.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.core.realtime.impl.kafka2.KafkaConsumerFactory",
      "stream.kafka.zk.broker.url": "localhost:2191/kafka",
      "stream.kafka.broker.list": "localhost:19092"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

Please note:

1. Config `replicasPerPartition` under `segmentsConfig` is required to specify table replication.
2. Config `stream.kafka.consumer.type` should be specified as `LowLevel` to use partition level consumer. \(The use of `simple` instead of `LowLevel` is deprecated\)
3. Configs `stream.kafka.zk.broker.url` and `stream.kafka.broker.list` are required under `tableIndexConfig.streamConfigs` to provide kafka related information.

#### Upgrade from Kafka 0.9 connector to Kafka 2.x connector

* Update table config for both high level and low level consumer: Update config: `stream.kafka.consumer.factory.class.name` from `org.apache.pinot.core.realtime.impl.kafka.KafkaConsumerFactory` to `org.apache.pinot.core.realtime.impl.kafka2.KafkaConsumerFactory`.
* If using Stream\(High\) level consumer: Please also add config `stream.kafka.hlc.bootstrap.server` into `tableIndexConfig.streamConfigs`. This config should be the URI of Kafka broker lists, e.g. `localhost:9092`.

#### How to use this plugin with higher Kafka version?

This connector is also suitable for Kafka lib version higher than `2.0.0`. In `pinot-connector-kafka-2.0/pom.xml` change the `kafka.lib.version` from `2.0.0` to `2.1.1` will make this Connector working with Kafka `2.1.1`.

