---
description: The Docker instructions on this page are still WIP
---

# Stream ingestion example

This example assumes you have set up your cluster using [Pinot in Docker](https://docs.pinot.apache.org/basics/getting-started/advanced-pinot-setup).

## Data Stream

First, we need to set up a stream. Pinot has out-of-the-box real-time ingestion support for Kafka. Other streams can be plugged in for use, see [Pluggable Streams](../../developers/plugin-architecture/write-custom-plugins/write-your-stream.md).

Let's set up a demo Kafka cluster locally, and create a sample topic `transcript-topic`.

{% tabs %}
{% tab title="Docker" %}
**Start Kafka**

```
docker run \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=manual-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -d bitnami/kafka:latest
```

**Create a Kafka Topic**

```
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper manual-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic transcript-topic
```
{% endtab %}

{% tab title="Using launcher scripts" %}
**Start Kafka**

Start Kafka cluster on port `9876` using the same Zookeeper from the quick-start examples.

```
bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2123/kafka -port 9876
```

**Create a Kafka topic**

Download the latest [Kafka](https://kafka.apache.org/quickstart#quickstart\_download). Create a topic.

```css
bin/kafka-topics.sh --create --bootstrap-server localhost:9876 --replication-factor 1 --partitions 1 --topic transcript-topic
```
{% endtab %}
{% endtabs %}

## Creating a schema

If you followed [Batch upload sample data](pushing-your-data-to-pinot.md), you have already pushed a schema for your sample table. If not, see [Creating a schema](../data-import/pinot-stream-ingestion/#create-schema-configuration) to learn how to create a schema for your sample data.

## Creating a table configuration

If you followed [Batch upload sample data](pushing-your-data-to-pinot.md), you pushed an offline table and schema. To create a real-time table configuration for the sample use this table configuration for the transcript table. For a more detailed overview about table, see [Table](../components/table/).

{% code title="/tmp/pinot-quick-start/transcript-table-realtime.json" %}
```javascript
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
      "stream.kafka.consumer.type": "lowlevel",
      "stream.kafka.topic.name": "transcript-topic",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
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

## Uploading your schema and table configuration

Next, upload the table and schema to the cluster. As soon as the real-time table is created, it will begin ingesting from the Kafka topic.

{% tabs %}
{% tab title="Docker" %}
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
{% endtab %}

{% tab title="Launcher Script" %}
```
bin/pinot-admin.sh AddTable \
    -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
    -tableConfigFile /tmp/pinot-quick-start/transcript-table-realtime.json \
    -exec
```
{% endtab %}
{% endtabs %}

## Loading sample data into stream

Use the following sample JSON file for transcript table data in the following step.

{% code title="/tmp/pinot-quick-start/rawData/transcript.json" %}
```css
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

Push the sample JSON file into the Kafka topic, using the Kafka script from the Kafka download.

```css
bin/kafka-console-producer.sh \
    --broker-list localhost:9876 \
    --topic transcript-topic < /tmp/pinot-quick-start/rawData/transcript.json
```

## Ingesting streaming data

As soon as data flows into the stream, the Pinot table will consume it and it will be ready for querying. Browse to the [Query Console ](http://localhost:9000/query) running in your Pinot instance (we use `localhost` in this link as an example) to examine the real-time data.

![](../../.gitbook/assets/Pinot\_query\_transcript\_table.png)
