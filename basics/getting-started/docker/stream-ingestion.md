---
description: Step-by-step guide for streaming ingestion into Pinot running in Docker
---

# Stream ingestion (Docker)

This guide walks you through setting up real-time stream ingestion into a Pinot cluster running in Docker. Make sure you have completed [Running Pinot in Docker](../docker/) first.

## Set up Kafka

Pinot has out-of-the-box real-time ingestion support for Kafka. Other streams can be plugged in, see [Pluggable Streams](../../../developers/plugin-architecture/write-custom-plugins/write-your-stream.md).

**Start Kafka:**

```bash
docker run \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=manual-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -d bitnami/kafka:latest
```

**Create a Kafka topic:**

```bash
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper manual-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic transcript-topic
```

## Create a schema

If you already pushed a schema during the [Batch ingestion example](batch-ingestion.md), you can reuse it. Otherwise, see [Creating a schema](../../../manage-data/data-import/pinot-stream-ingestion/#create-schema-configuration) to learn how to create one.

## Create a table configuration

{% code title="/tmp/pinot-quick-start/transcript-table-realtime.json" %}
```json
{
  "tableName": "transcript",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "timestampInEpoch",
    "timeType": "MILLISECONDS",
    "schemaName": "transcript",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "transcript-topic",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
      "stream.kafka.broker.list": "kafka:9092",
      "realtime.segment.flush.threshold.rows": "0",
      "realtime.segment.flush.threshold.time": "24h",
      "realtime.segment.flush.threshold.segment.size": "50M",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```
{% endcode %}

## Upload the schema and table configuration

As soon as the real-time table is created, it will begin ingesting from the Kafka topic.

```bash
docker run \
    --network=pinot-demo \
    -v /tmp/pinot-quick-start:/tmp/pinot-quick-start \
    --name pinot-streaming-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
    -tableConfigFile /tmp/pinot-quick-start/transcript-table-realtime.json \
    -controllerHost manual-pinot-controller \
    -controllerPort 9000 \
    -exec
```

## Load sample data into the stream

{% code title="/tmp/pinot-quick-start/rawData/transcript.json" %}
```json
{"studentID":205,"firstName":"Natalie","lastName":"Jones","gender":"Female","subject":"Maths","score":3.8,"timestampInEpoch":1571900400000}
{"studentID":205,"firstName":"Natalie","lastName":"Jones","gender":"Female","subject":"History","score":3.5,"timestampInEpoch":1571900400000}
{"studentID":207,"firstName":"Bob","lastName":"Lewis","gender":"Male","subject":"Maths","score":3.2,"timestampInEpoch":1571900400000}
{"studentID":207,"firstName":"Bob","lastName":"Lewis","gender":"Male","subject":"Chemistry","score":3.6,"timestampInEpoch":1572418800000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Geography","score":3.8,"timestampInEpoch":1572505200000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"English","score":3.5,"timestampInEpoch":1572505200000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Maths","score":3.2,"timestampInEpoch":1572678000000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Physics","score":3.6,"timestampInEpoch":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"Maths","score":3.8,"timestampInEpoch":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"English","score":3.5,"timestampInEpoch":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"History","score":3.2,"timestampInEpoch":1572854400000}
{"studentID":212,"firstName":"Nick","lastName":"Young","gender":"Male","subject":"History","score":3.6,"timestampInEpoch":1572854400000}
```
{% endcode %}

Push the sample JSON into the Kafka topic:

```bash
docker exec -t kafka /opt/kafka/bin/kafka-console-producer.sh \
    --broker-list localhost:9092 \
    --topic transcript-topic < /tmp/pinot-quick-start/rawData/transcript.json
```

## Query your data

As soon as data flows into the stream, Pinot will consume it and make it available for querying. Open the [Query Console](http://localhost:9000/query) to examine the real-time data.
