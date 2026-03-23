---
description: Set up real-time streaming ingestion from Kafka and watch data arrive in Pinot.
---

# First stream ingest

{% hint style="info" %}
For Kubernetes-specific streaming ingestion, see [Stream ingestion (Kubernetes)](kubernetes/stream-ingestion.md).
{% endhint %}

## Outcome

By the end of this page you will have a realtime Pinot table consuming data from a Kafka topic, with 12 rows visible in the query console.

## Prerequisites

* Completed [First table and schema](first-table-and-schema.md) -- the `transcript` schema must already exist in the cluster.
* A running Pinot cluster. See the install guides for [Local](install/local.md) or [Docker](install/docker.md).
* For Docker users: set the `PINOT_VERSION` environment variable. See the [Version reference](pinot-versions.md) page.

## Steps

### 1. Understand streaming ingestion

Streaming ingestion lets Pinot consume data from a message queue in real time. As messages arrive in a Kafka topic, Pinot reads them and makes the rows queryable within seconds. The realtime table config specifies the Kafka broker, topic, and decoder so that Pinot knows how to connect and interpret incoming records.

### 2. Start Kafka

{% tabs %}
{% tab title="Local" %}
Start Kafka on port `9876` using the same ZooKeeper from the Pinot quick-start:

```bash
bin/pinot-admin.sh StartKafka -zkAddress=localhost:2123/kafka -port 9876
```
{% endtab %}

{% tab title="Docker" %}
```bash
docker run \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=pinot-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -d bitnami/kafka:3.6
```

{% hint style="info" %}
Replace `pinot-zookeeper` with the actual container name of your ZooKeeper instance if you used a different name during setup.
{% endhint %}
{% endtab %}
{% endtabs %}

### 3. Create a Kafka topic

{% tabs %}
{% tab title="Local" %}
Download [Apache Kafka](https://kafka.apache.org/quickstart#quickstart_download) if you have not already, then create the topic:

```bash
bin/kafka-topics.sh --create --bootstrap-server localhost:9876 \
    --replication-factor 1 --partitions 1 --topic transcript-topic
```
{% endtab %}

{% tab title="Docker" %}
```bash
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper pinot-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic transcript-topic
```
{% endtab %}
{% endtabs %}

### 4. Save the realtime table config

Create the file `/tmp/pinot-quick-start/transcript-table-realtime.json`:

{% tabs %}
{% tab title="Local" %}
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
      "stream.kafka.broker.list": "localhost:9876",
      "realtime.segment.flush.threshold.rows": "0",
      "realtime.segment.flush.threshold.time": "24h",
      "realtime.segment.flush.threshold.segment.size": "50M",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": { "customConfigs": {} }
}
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
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
  "metadata": { "customConfigs": {} }
}
```
{% endcode %}

{% hint style="info" %}
The Docker version uses `kafka:9092` as the broker address because both the Kafka and Pinot containers are on the same `pinot-demo` Docker network.
{% endhint %}
{% endtab %}
{% endtabs %}

### 5. Upload the realtime table config

As soon as the realtime table is created, Pinot begins consuming from the Kafka topic.

{% tabs %}
{% tab title="Local" %}
```bash
bin/pinot-admin.sh AddTable \
    -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
    -tableConfigFile /tmp/pinot-quick-start/transcript-table-realtime.json \
    -exec
```

{% hint style="info" %}
If the `transcript` schema was already uploaded during [First table and schema](first-table-and-schema.md), you can omit the `-schemaFile` flag. Including it is safe -- Pinot will skip re-creating an identical schema.
{% endhint %}
{% endtab %}

{% tab title="Docker" %}
```bash
docker run --rm -ti \
    --network=pinot-demo \
    -v /tmp/pinot-quick-start:/tmp/pinot-quick-start \
    --name pinot-streaming-table-creation \
    apachepinot/pinot:${PINOT_VERSION} AddTable \
    -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
    -tableConfigFile /tmp/pinot-quick-start/transcript-table-realtime.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
```

{% hint style="info" %}
Replace `pinot-controller` with the actual container name of your Pinot controller if you used a different name during setup.
{% endhint %}
{% endtab %}
{% endtabs %}

### 6. Save the sample streaming data

Create the file `/tmp/pinot-quick-start/rawdata/transcript.json`:

{% code title="/tmp/pinot-quick-start/rawdata/transcript.json" %}
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

### 7. Push data into the Kafka topic

{% tabs %}
{% tab title="Local" %}
```bash
bin/kafka-console-producer.sh \
    --broker-list localhost:9876 \
    --topic transcript-topic < /tmp/pinot-quick-start/rawdata/transcript.json
```
{% endtab %}

{% tab title="Docker" %}
```bash
docker exec -t kafka /opt/kafka/bin/kafka-console-producer.sh \
    --broker-list localhost:9092 \
    --topic transcript-topic < /tmp/pinot-quick-start/rawdata/transcript.json
```
{% endtab %}
{% endtabs %}

## Verify

1. Open the [Query Console](http://localhost:9000/query) in your browser.
2. Run the following query:

```sql
SELECT * FROM transcript
```

3. You should see **12 rows** of streaming data. Pinot ingests from Kafka in real time, so the rows appear within seconds of being pushed to the topic.

## Next step

Continue to [First query](first-query.md) to learn how to write analytical queries against your Pinot tables.
