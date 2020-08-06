---
description: >-
  This guide shows you how to ingest a stream of records from an Apache Kafka
  topic into a Pinot table.
---

# Apache Kafka

### Introduction

In this guide, you'll learn how to import data into Pinot using Apache Kafka for real-time stream ingestion. Pinot has out-of-the-box real-time ingestion support for Kafka. 

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

### Creating Schema Configuration

We will publish the data in the same format as mentioned in the [Stream ingestion](./) docs. So you can use the same schema mentioned under [Create Schema Configuration](./#create-schema-configuration).

### Creating a table configuration

The real-time table configuration for the `transcript` table described in the schema from the previous step. 

For Kafka, we use streamType as `kafka` . Currently only JSON format is supported but you can easily write your own decoder by extending the `StreamMessageDecoder` interface. You can then access your decoder class by putting the jar file in `plugins` directory

The `lowLevel` consumer reads data per partition whereas the `highLevel` consumer  utilises Kafka high level consumer to read data from the whole stream. It doesn't have the control over which partition to read at a particular momemt. 

For Kafka versions below 2.X, use `org.apache.pinot.plugin.stream.kafka09.KafkaConsumerFactory` 

For Kafka version 2.X and above, use   
`org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory`

You can set the offset to -

* `smallest` to start consumer from the earliest offset
* `largest` to start consumer from the latest offset
* `timestamp in milliseconds` to start the consumer from the offset after the timestamp.

The resulting configuration should look as follows -

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

### Upload schema and table

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

We will publish data in the following format to Kafka. Let us save the data in a file named as `transcript.json`.

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

Push sample JSON into the `transcript-topic` Kafka topic, using the Kafka console producer. This will add 12 records to the topic described in the `transcript.json` file.

```css
bin/kafka-console-producer.sh \
    --broker-list localhost:9876 \
    --topic transcript-topic < transcript.json
```

### Ingesting streaming data

As soon as data flows into the stream, the Pinot table will consume it and it will be ready for querying. Head over to the [Query Console ](http://localhost:9000/query)to checkout the real-time data.

```sql
SELECT * FROM transcript
```

