---
description: >-
  This guide shows you how to ingest a stream of records from an Apache Kafka
  topic into a Pinot table.
---

# Import from Kafka

## Introduction

In this guide, you'll learn how to import data into Pinot using Apache Kafka for real-time stream ingestion. First, we need to setup a stream. Pinot has out-of-the-box real-time ingestion support for Kafka. Other streams can be plugged in, more details in [Pluggable Streams](../../../developers/developers-and-contributors/extending-pinot/pluggable-streams.md).

Let's setup a demo Kafka cluster locally, and create a sample topic `transcript-topic`

{% tabs %}
{% tab title="Docker" %}
**Start Kafka**

```bash
docker run \
	--network pinot-demo --name=kafka \
	-e KAFKA_ZOOKEEPER_CONNECT=pinot-quickstart:2123/kafka \
	-e KAFKA_BROKER_ID=0 \
	-e KAFKA_ADVERTISED_HOST_NAME=kafka \
	-d wurstmeister/kafka:latest
```

**Create a Kafka Topic**

```bash
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper pinot-quickstart:2123/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic transcript-topic
```
{% endtab %}

{% tab title="Using launcher scripts" %}
**Start Kafka**

Start Kafka cluster on port `9876` using the same Zookeeper from the [quick-start examples](../../getting-started/running-pinot-in-docker.md).

```text
bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2123/kafka -port 9876
```

**Create a Kafka topic**

Download the latest [Kafka](https://kafka.apache.org/quickstart#quickstart_download). Create a topic.

```css
bin/kafka-topics.sh --create --bootstrap-server localhost:9876 --replication-factor 1 --partitions 1 --topic transcript-topic
```
{% endtab %}
{% endtabs %}

## Creating a schema configuration

If you followed the [batch upload sample data](../../getting-started/pushing-your-data-to-pinot.md), you have already created a schema for your sample table. If not, head over to [creating a schema](../../getting-started/pushing-your-data-to-pinot.md#creating-a-schema) on that page, to learn how to create a schema for your sample data. To make it easy, the schema from that page is included here.

{% code title="/tmp/pinot-quick-start/transcript-schema.json" %}
```bash
{
  "schemaName": "transcript",
  "dimensionFieldSpecs": [
    {
      "name": "studentID",
      "dataType": "INT"
    },
    {
      "name": "firstName",
      "dataType": "STRING"
    },
    {
      "name": "lastName",
      "dataType": "STRING"
    },
    {
      "name": "gender",
      "dataType": "STRING"
    },
    {
      "name": "subject",
      "dataType": "STRING"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "score",
      "dataType": "FLOAT"
    }
  ],
  "dateTimeFieldSpecs": [{
    "name": "timestamp",
    "dataType": "LONG",
    "format" : "1:MILLISECONDS:EPOCH",
    "granularity": "1:MILLISECONDS"
  }]
}
```
{% endcode %}

## Creating a table configuration

If you followed [batch upload sample data](../../getting-started/pushing-your-data-to-pinot.md), you learned how to push an offline table and schema. Similar to the offline table config, we will create a real-time table config for this sample. Here's the real-time table configuration for the `transcript` table described in the schema from the previous step. For a more detailed overview about tables, check out the [table](../../components/table.md) reference.

{% code title="/tmp/pinot-quick-start/transcript-table-realtime.json" %}
```css
{
  "tableName": "transcript",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "timestamp",
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
      "stream.kafka.broker.list": "localhost:9876",
      "realtime.segment.flush.threshold.time": "3600000",
      "realtime.segment.flush.threshold.size": "50000",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```
{% endcode %}

## Create schema and table

Now that we have our table and schema configurations, let's upload them to the Pinot cluster. As soon as the real-time table is created, it will begin ingesting available records from the Kafka topic.

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
    -controllerHost pinot-quickstart \
    -controllerPort 9000 \
    -exec
```
{% endtab %}

{% tab title="Launcher Script" %}
```bash
bin/pinot-admin.sh AddTable \
    -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
    -tableConfigFile /tmp/pinot-quick-start/transcript-table-realtime.json \
    -exec
```
{% endtab %}
{% endtabs %}

## Add sample data to the Kafka topic

Here's a JSON file containing sample records we will import into the transcript table we created in the last step. Save the following file as `transcript.json`.

{% code title="transcript.json" %}
```css
{"studentID":205,"firstName":"Natalie","lastName":"Jones","gender":"Female","subject":"Maths","score":3.8,"timestamp":1571900400000}
{"studentID":205,"firstName":"Natalie","lastName":"Jones","gender":"Female","subject":"History","score":3.5,"timestamp":1571900400000}
{"studentID":207,"firstName":"Bob","lastName":"Lewis","gender":"Male","subject":"Maths","score":3.2,"timestamp":1571900400000}
{"studentID":207,"firstName":"Bob","lastName":"Lewis","gender":"Male","subject":"Chemistry","score":3.6,"timestamp":1572418800000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Geography","score":3.8,"timestamp":1572505200000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"English","score":3.5,"timestamp":1572505200000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Maths","score":3.2,"timestamp":1572678000000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Physics","score":3.6,"timestamp":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"Maths","score":3.8,"timestamp":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"English","score":3.5,"timestamp":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"History","score":3.2,"timestamp":1572854400000}
{"studentID":212,"firstName":"Nick","lastName":"Young","gender":"Male","subject":"History","score":3.6,"timestamp":1572854400000}
```
{% endcode %}

Push sample JSON into the `transcript-topic` Kafka topic, using the following command. This will add 12 records to the topic described in the `transcript.json` file.

```css
bin/kafka-console-producer.sh \
    --broker-list localhost:9876 \
    --topic transcript-topic < transcript.json
```

## Ingesting streaming data

As soon as data flows into the stream, the Pinot table will consume it and it will be ready for querying. Head over to the [Query Console ](http://localhost:9000/query)to checkout the real-time data.

```sql
SELECT * FROM transcript
```

