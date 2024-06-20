---
description: >-
  This guide shows you how to ingest a stream of records from an Apache Kafka
  topic into a Pinot table.
---

# Ingest streaming data from Apache Kafka

Learn how to ingest data from Kafka, a stream processing platform. You should have a local cluster up and running, following the instructions in [Set up a cluster](../../../operators/operating-pinot/setup-cluster.md).

## Install and Launch Kafka

Let's start by downloading Kafka to our local machine.

{% tabs %}
{% tab title="Docker" %}
To pull down the latest Docker image, run the following command:

```bash
docker pull wurstmeister/kafka:latest
```
{% endtab %}

{% tab title="Launcher Scripts" %}
Download Kafka from [kafka.apache.org/quickstart#quickstart\_download](https://kafka.apache.org/quickstart#quickstart\_download) and then extract it:

```bash
tar -xzf kafka_2.13-3.7.0.tgz
cd kafka_2.13-3.7.0
```
{% endtab %}
{% endtabs %}

Next we'll spin up a Kafka broker:

{% tabs %}
{% tab title="Docker" %}
```bash
docker run --network pinot-demo --name=kafka -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181/kafka -e KAFKA_BROKER_ID=0 -e KAFKA_ADVERTISED_HOST_NAME=kafka wurstmeister/kafka:latest
```

Note: The --network pinot-demo flag is optional and assumes that you have a Docker network named pinot-demo that you want to connect the Kafka container to.
{% endtab %}

{% tab title="Launcher Scripts" %}
On one terminal window run this command:

**Start Zookeeper**

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

And on another window, run this command:

**Start Kafka Broker**

```bash
bin/kafka-server-start.sh config/server.properties
```
{% endtab %}
{% endtabs %}

## Data Source

We're going to generate some JSON messages from the terminal using the following script:

```bash
import datetime
import uuid
import random
import json

while True:
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    print(
        json.dumps({"ts": ts, "uuid": id, "count": count})
    )

```

_datagen.py_

If you run this script (`python datagen.py`), you'll see the following output:

```json
{"ts": 1644586485807, "uuid": "93633f7c01d54453a144", "count": 807}
{"ts": 1644586485836, "uuid": "87ebf97feead4e848a2e", "count": 41}
{"ts": 1644586485866, "uuid": "960d4ffa201a4425bb18", "count": 146}
```

## Ingesting Data into Kafka

Let's now pipe that stream of messages into Kafka, by running the following command:

{% tabs %}
{% tab title="Docker" %}
```bash
python datagen.py | docker exec -i kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic events;
```
{% endtab %}

{% tab title="Launcher Scripts" %}
```bash
python datagen.py | bin/kafka-console-producer.sh --bootstrap-server localhost:9092  --topic events;
```
{% endtab %}
{% endtabs %}

We can check how many messages have been ingested by running the following command:

{% tabs %}
{% tab title="Docker" %}
```bash
docker exec -i kafka kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic events
```
{% endtab %}

{% tab title="Launcher Scripts" %}
```bash
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic events
```
{% endtab %}
{% endtabs %}

**Output**

```
events:0:11940
```

And we can print out the messages themselves by running the following command

{% tabs %}
{% tab title="Docker" %}
```bash
docker exec -i kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events
```
{% endtab %}

{% tab title="Launcher Scripts" %}
```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events
```
{% endtab %}
{% endtabs %}

**Output**

```json
...
{"ts": 1644586485807, "uuid": "93633f7c01d54453a144", "count": 807}
{"ts": 1644586485836, "uuid": "87ebf97feead4e848a2e", "count": 41}
{"ts": 1644586485866, "uuid": "960d4ffa201a4425bb18", "count": 146}
...
```

## Schema

A schema defines what fields are present in the table along with their data types in JSON format.

Create a file called `/tmp/pinot/schema-stream.json` and add the following content to it.

```json
{
  "schemaName": "events",
  "dimensionFieldSpecs": [
    {
      "name": "uuid",
      "dataType": "STRING"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "count",
      "dataType": "INT"
    }
  ],
  "dateTimeFieldSpecs": [{
    "name": "ts",
    "dataType": "TIMESTAMP",
    "format" : "1:MILLISECONDS:EPOCH",
    "granularity": "1:MILLISECONDS"
  }]
}
```

## Table Config

A table is a logical abstraction that represents a collection of related data. It is composed of columns and rows (known as documents in Pinot). The table config defines the table's properties in JSON format.

Create a file called `/tmp/pinot/table-config-stream.json` and add the following content to it.

```json
{
  "tableName": "events",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "ts",
    "schemaName": "events",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "lowlevel",
      "stream.kafka.topic.name": "events",
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

## Create schema and table

Create the table and schema by running the appropriate command below:

{% tabs %}
{% tab title="Docker" %}
```bash
docker run --rm -ti  --network=pinot-demo  -v /tmp/pinot:/tmp/pinot  apachepinot/pinot:1.0.0 AddTable  -schemaFile /tmp/pinot/schema-stream.json  -tableConfigFile /tmp/pinot/table-config-stream.json  -controllerHost pinot-controller  -controllerPort 9000 -exec
```
{% endtab %}

{% tab title="Launcher Scripts" %}
```bash
bin/pinot-admin.sh AddTable -schemaFile /tmp/pinot/schema-stream.json -tableConfigFile /tmp/pinot/table-config-stream.json
```
{% endtab %}
{% endtabs %}

## Querying

Navigate to [localhost:9000/#/query](http://localhost:9000/#/query) and click on the `events` table to run a query that shows the first 10 rows in this table.

![Querying the events table](../../../img/events-kafka-query.png) _Querying the events table_

## Kafka ingestion guidelines

### Kafka versions in Pinot

Pinot supports two versions of the Kafka library: `kafka-0.9` and `kafka-2.x` for low level consumers.

{% hint style="info" %}
Post release 0.10.0, we have started shading kafka packages inside Pinot. If you are using our `latest` tagged docker images or `master` build, you should replace `org.apache.kafka` with `shaded.org.apache.kafka` in your table config.
{% endhint %}

#### Upgrade from Kafka 0.9 connector to Kafka 2.x connector

* Update table config for low level consumer: `stream.kafka.consumer.factory.class.name` from `org.apache.pinot.core.realtime.impl.kafka.KafkaConsumerFactory` to `org.apache.pinot.core.realtime.impl.kafka2.KafkaConsumerFactory`.

{% hint style="info" %}
Pinot does _**not support**_ using high-level Kafka consumers (HLC). Pinot uses low-level consumers to ensure accurate results, supports operational complexity and scalability, and minimizes storage overhead.
{% endhint %}

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

<table><thead><tr><th width="242">Kafka Record</th><th width="259">Pinot Table Column</th><th width="250">Description</th></tr></thead><tbody><tr><td>Record key: any type &#x3C;K></td><td><code>__key</code> : String</td><td>For simplicity of design, we assume that the record key is always a UTF-8 encoded String</td></tr><tr><td>Record Headers: Map&#x3C;String, String></td><td>Each header key is listed as a separate column:<br><code>__header$HeaderKeyName</code> : String</td><td>For simplicity of design, we directly map the string headers from kafka record to pinot table column</td></tr><tr><td>Record metadata - offset : long</td><td><code>__metadata$offset</code> : String</td><td><tr><td>Record metadata - partition : int</td><td><code>__metadata$partition</code> : String</td><td></td></tr><tr><td>Record metadata - recordTimestamp : long</td><td><code>__metadata$recordTimestamp</code> : String</td><td></td></tr></tbody></table>

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
    {
      "name": "__metadata$partition",
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
