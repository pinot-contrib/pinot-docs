---
description: >-
  This guide shows you how to ingest a stream of records from an Apache Kafka
  topic into a Pinot table.
---

# Apache Kafka

In this page, you'll learn how to import data into Pinot using Apache Kafka for real-time stream ingestion. Pinot has out-of-the-box real-time ingestion support for Kafka.

Let's set up a demo Kafka cluster locally, and create a sample topic `transcript-topic`

{% tabs %}
{% tab title="Docker" %}
**Start Kafka**

```bash
docker run \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=pinot-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -p 2181:2181 \
    -d wurstmeister/kafka:latest
```

**Create a Kafka topic**

```bash
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper pinot-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic transcript-topic
```
{% endtab %}

{% tab title="Using launcher scripts" %}
**Start Kafka**

Start Kafka cluster on port `9092` using the same Zookeeper from the [quick-start examples](../../getting-started/running-pinot-in-docker.md).

```
bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2181/kafka -port 9092
```

**Create a Kafka topic**

Download the latest [Kafka](https://kafka.apache.org/quickstart#quickstart\_download). Create a topic.

```css
bin/kafka-topics.sh --create --bootstrap-server kafka:9092 --replication-factor 1 --partitions 1 --topic transcript-topic
```
{% endtab %}
{% endtabs %}

### Create schema configuration

We will publish the data in the same format as mentioned in the [Stream ingestion](./) docs. So you can use the same schema mentioned under [Create Schema Configuration](./#create-schema-configuration).

### Create table configuration

The real-time table configuration for the `transcript` table described in the schema from the previous step.

For Kafka, we use streamType as `kafka` . See [#create-table-configuration](./#create-table-configuration "mention") for available decoder class options. You can also write your own decoder by extending the `StreamMessageDecoder` interface and putting the jar file in `plugins` directory.

The `lowLevel` consumer reads data per partition whereas the `highLevel` consumer utilises Kafka high level consumer to read data from the whole stream. It doesn't have the control over which partition to read at a particular momemt.

For Kafka versions below 2.X, use `org.apache.pinot.plugin.stream.kafka09.KafkaConsumerFactory`

For Kafka version 2.X and above, use\
`org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory`

You can set the offset to -

* `smallest` to start consumer from the earliest offset
* `largest` to start consumer from the latest offset
* `timestamp in format yyyy-MM-dd'T'HH:mm:ss.SSSZ` to start the consumer from the offset after the timestamp.
* `datetime duration or period` to start the consumer from the offset after the period eg., '2d'.

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
      "stream.kafka.broker.list": "kafka:9092",
      "realtime.segment.flush.threshold.time": "3600000",
      "realtime.segment.flush.threshold.rows": "50000",
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

### Add sample data to the Kafka topic

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

Checkin Kafka docker container

```bash
docker exec -ti kafka bash
```

Publish messages to the target topic

```bash
bin/kafka-console-producer.sh \
    --broker-list localhost:9092 \
    --topic transcript-topic < transcript.json
```

### Query the table

As soon as data flows into the stream, the Pinot table will consume it and it will be ready for querying. Head over to the [Query Console ](http://localhost:9000/query)to checkout the real-time data.

```sql
SELECT * FROM transcript
```

## Kafka ingestion guidelines

### Kafka versions in Pinot

Pinot supports 2 major generations of Kafka library - kafka-0.9 and kafka-2.x for both high and low level consumers.

{% hint style="info" %}
Post release 0.10.0, we have started shading kafka packages inside Pinot. If you are using our `latest` tagged docker images or `master` build, you should replace `org.apache.kafka` with `shaded.org.apache.kafka` in your table config.
{% endhint %}

#### Upgrade from Kafka 0.9 connector to Kafka 2.x connector

* Update table config for both high level and low level consumer: Update config: `stream.kafka.consumer.factory.class.name` from `org.apache.pinot.core.realtime.impl.kafka.KafkaConsumerFactory` to `org.apache.pinot.core.realtime.impl.kafka2.KafkaConsumerFactory`.
* If using Stream(High) level consumer, also add config `stream.kafka.hlc.bootstrap.server` into `tableIndexConfig.streamConfigs`. This config should be the URI of Kafka broker lists, e.g. `localhost:9092`.

#### How to consume from a Kafka version > 2.0.0

This connector is also suitable for Kafka lib version higher than `2.0.0`. In [Kafka 2.0 connector pom.xml](https://github.com/apache/pinot/blob/master/pinot-plugins/pinot-stream-ingestion/pinot-kafka-2.0/pom.xml), change the `kafka.lib.version` from `2.0.0` to `2.1.1` will make this Connector working with Kafka `2.1.1`.

### Kafka configurations in Pinot

#### Use Kafka partition (low) level consumer with SSL

Here is an example config which uses SSL based authentication to talk with kafka and schema-registry. Notice there are two sets of SSL options, ones starting with `ssl.` are for kafka consumer and ones with `stream.kafka.decoder.prop.schema.registry.` are for `SchemaRegistryClient` used by `KafkaConfluentSchemaRegistryAvroMessageDecoder`.

```
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
        "stream.kafka.consumer.type": "LowLevel",
        "stream.kafka.topic.name": "transcript-topic",
        "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
        "stream.kafka.zk.broker.url": "pinot-zookeeper:2191/kafka",
        "stream.kafka.broker.list": "localhost:9092",
        "schema.registry.url": "",
        "security.protocol": "SSL",
        "ssl.truststore.location": "",
        "ssl.keystore.location": "",
        "ssl.truststore.password": "",
        "ssl.keystore.password": "",
        "ssl.key.password": "",
        "stream.kafka.decoder.prop.schema.registry.rest.url": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.truststore.location": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.keystore.location": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.truststore.password": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.keystore.password": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.keystore.type": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.truststore.type": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.key.password": "",
        "stream.kafka.decoder.prop.schema.registry.ssl.protocol": ""
      }
    },
    "metadata": {
      "customConfigs": {}
    }
  }
```

#### Consume transactionally-committed messages

The connector with Kafka library 2.0+ supports Kafka transactions. The transaction support is controlled by config `kafka.isolation.level` in Kafka stream config, which can be `read_committed` or `read_uncommitted` (default). Setting it to `read_committed` will ingest transactionally committed messages in Kafka stream only.

For example,

```
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
        "stream.kafka.consumer.type": "LowLevel",
        "stream.kafka.topic.name": "transcript-topic",
        "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
        "stream.kafka.zk.broker.url": "pinot-zookeeper:2191/kafka",
        "stream.kafka.broker.list": "kafka:9092",
        "stream.kafka.isolation.level": "read_committed"
      }
    },
    "metadata": {
      "customConfigs": {}
    }
  }
```

Note that the default value of this config `read_uncommitted` to read all messages. Also, this config supports low-level consumer only.

#### Use Kafka partition (low) level consumer with SASL\_SSL

Here is an example config which uses SASL\_SSL based authentication to talk with kafka and schema-registry. Notice there are two sets of SSL options, some for kafka consumer and ones with `stream.kafka.decoder.prop.schema.registry.` are for `SchemaRegistryClient` used by `KafkaConfluentSchemaRegistryAvroMessageDecoder`.

```
"streamConfigs": {
        "streamType": "kafka",
        "stream.kafka.consumer.type": "lowlevel",
        "stream.kafka.topic.name": "mytopic",
        "stream.kafka.consumer.prop.auto.offset.reset": "largest",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
        "stream.kafka.broker.list": "kafka:9092",
        "stream.kafka.schema.registry.url": "https://xxx",
        "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder",
        "stream.kafka.decoder.prop.schema.registry.rest.url": "https://xxx",
        "stream.kafka.decoder.prop.basic.auth.credentials.source": "USER_INFO",
        "stream.kafka.decoder.prop.schema.registry.basic.auth.user.info": "schema_registry_username:schema_registry_password",
        "sasl.mechanism": "PLAIN" ,
        "security.protocol": "SASL_SSL" ,
        "sasl.jaas.config":"org.apache.kafka.common.security.scram.ScramLoginModule required username=\"kafkausername\" password=\"kafkapassword\";",
        "realtime.segment.flush.threshold.rows": "0",
        "realtime.segment.flush.threshold.time": "24h",
        "realtime.segment.flush.autotune.initialRows": "3000000",
        "realtime.segment.flush.threshold.segment.size": "500M"
      },
```

#### Extract record headers as Pinot table columns

Pinot's Kafka connector supports automatically extracting record headers and metadata into the Pinot table columns. The following table shows the mapping for record header/metadata to Pinot table column names:

<table><thead><tr><th width="242">Kafka Record</th><th width="259">Pinot Table Column</th><th width="250">Description</th></tr></thead><tbody><tr><td>Record key: any type &#x3C;K></td><td><code>__key</code> : String</td><td>For simplicity of design, we assume that the record key is always a UTF-8 encoded String</td></tr><tr><td>Record Headers: Map&#x3C;String, String></td><td>Each header key is listed as a separate column:<br><code>__header$HeaderKeyName</code> : String</td><td>For simplicity of design, we directly map the string headers from kafka record to pinot table column</td></tr><tr><td>Record metadata - offset : long</td><td><code>__metadata$offset</code> : String</td><td></td></tr><tr><td>Record metadata - recordTimestamp : long</td><td><code>__metadata$recordTimestamp</code> : String</td><td></td></tr></tbody></table>

In order to enable the metadata extraction in a Kafka table, you can set the stream config `metadata.populate` to `true`.

In addition to this, if you want to use any of these columns in your table, you have to list them explicitly in your table's schema.

For example, if you want to add only the offset and key as dimension columns in your Pinot table, it can listed in the schema as follows:

```json
  "dimensionFieldSpecs": [
    {
      "name": "__key",
      "dataType": "STRING"
    },
    {
      "name": "__metadata$offset",
      "dataType": "STRING"
    },
    ...
  ],
```

Once the schema is updated, these columns are similar to any other pinot column. You can apply ingestion transforms and / or define indexes on them.

{% hint style="info" %}
Remember to follow the [schema evolution guidelines](../../../users/tutorials/schema-evolution.md) when updating schema of an existing table!
{% endhint %}

#### Tell Pinot where to find an Avro schema

There is a standalone utility to generate the schema from an Avro file. See \[infer the pinot schema from the avro schema and JSON data]\([https://docs.pinot.apache.org/basics/data-import/complex-type#infer-the-pinot-schema-from-the-avro-schema-and-json-data](https://docs.pinot.apache.org/basics/data-import/complex-type#infer-the-pinot-schema-from-the-avro-schema-and-json-data)) for details.

To avoid errors like `The Avro schema must be provided`, designate the location of the schema in your `streamConfigs` section. For example, if your current section contains the following:

```json
...
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.consumer.type": "lowlevel",
  "stream.kafka.topic.name": "",
  "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
  "stream.kafka.broker.list": "",
  "stream.kafka.consumer.prop.auto.offset.reset": "largest"
  ...
}
```

Then add this key: `"stream.kafka.decoder.prop.schema"`followed by a value that denotes the location of your schema.
