---
description: >-
  This guide shows you how to ingest a stream of records from an Apache Kafka
  topic into a Pinot table.
---

# Ingest streaming data from Apache Kafka

Learn how to ingest data from Kafka, a stream processing platform. You should have a local cluster up and running, following the instructions in [Set up a cluster](../../../operate-pinot/setup-cluster.md).

{% hint style="info" %}
This guide uses the Kafka 3.0 connector (`kafka30`). Pinot also supports a **Kafka 4.0 connector** for KRaft-mode Kafka clusters. See [Kafka Connector Versions](kafka-connector-versions.md) for details on choosing the right connector.
{% endhint %}

## Install and Launch Kafka

Let's start by downloading Kafka to our local machine.

{% tabs %}
{% tab title="Docker" %}
To pull down the latest Docker image, run the following command:

```bash
docker pull apache/kafka:4.0.0
```
{% endtab %}

{% tab title="Launcher Scripts" %}
Download Kafka from [kafka.apache.org/quickstart#quickstart\_download](https://kafka.apache.org/quickstart#quickstart\_download) and then extract it:

```bash
tar -xzf kafka_2.13-4.0.0.tgz
cd kafka_2.13-4.0.0
```
{% endtab %}
{% endtabs %}

Next we'll spin up a Kafka broker. Kafka 4.0 uses KRaft mode by default and does not require ZooKeeper:

{% tabs %}
{% tab title="Docker" %}
```bash
docker run --network pinot-demo --name=kafka \
    -e KAFKA_NODE_ID=1 \
    -e KAFKA_PROCESS_ROLES=broker,controller \
    -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 \
    -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
    -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@kafka:9093 \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    -e CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk \
    apache/kafka:4.0.0
```

Note: The --network pinot-demo flag is optional and assumes that you have a Docker network named pinot-demo that you want to connect the Kafka container to.
{% endtab %}

{% tab title="Launcher Scripts" %}
Kafka 4.0 uses KRaft mode by default. Generate a cluster ID and format the storage directory, then start the broker:

**Start Kafka Broker (KRaft mode)**

```bash
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
bin/kafka-server-start.sh config/server.properties
```
{% endtab %}
{% endtabs %}

## Data Source

We're going to generate some JSON messages from the terminal using the following script:

```python
import datetime
import uuid
import random
import json

while True:
    ts = int(datetime.datetime.now().timestamp()* 1000)
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
docker exec -i kafka /opt/kafka/bin/kafka-get-offsets.sh --bootstrap-server localhost:9092 --topic events
```
{% endtab %}

{% tab title="Launcher Scripts" %}
```bash
bin/kafka-get-offsets.sh --bootstrap-server localhost:9092 --topic events
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
      "stream.kafka.topic.name": "events",
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

<!-- Image missing: events-kafka-query.png --> _Querying the events table_

## Kafka ingestion guidelines

### Kafka connector modules in Pinot

Pinot ships two Kafka connector modules:

* **`pinot-kafka-3.0`** -- Uses Kafka client library 3.x (currently 3.9.2). This is the default connector included in Pinot distributions. Consumer factory class: `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory`.
* **`pinot-kafka-4.0`** -- Uses Kafka client library 4.x (currently 4.1.1). This connector drops the ZooKeeper-based Scala dependency and uses the pure-Java Kafka client, suitable for KRaft-mode Kafka clusters. Consumer factory class: `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory`.

{% hint style="info" %}
The legacy `kafka-0.9` and `kafka-2.x` connector modules have been removed. If you are upgrading from an older Pinot release that used `org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory`, update your table configs to use one of the current connector classes listed above.
{% endhint %}

{% hint style="info" %}
Pinot does _**not support**_ using high-level Kafka consumers (HLC). Pinot uses low-level consumers to ensure accurate results, supports operational complexity and scalability, and minimizes storage overhead.
{% endhint %}

#### Migrating from the kafka-2.x connector

If your existing table configs reference the removed `kafka-2.x` connector, update the `stream.kafka.consumer.factory.class.name` property:

* From: `org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory`
* To (Kafka 3.x): `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory`
* To (Kafka 4.x): `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory`

No other stream config changes are required. The Kafka 3.x connector is compatible with Kafka brokers 2.x and above. The Kafka 4.x connector requires Kafka brokers 4.0 or above.

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
        "stream.kafka.topic.name": "transcript-topic",
        "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
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

#### Use Confluent Schema Registry with JSON encoded messages

If your Kafka messages are JSON-encoded and registered with Confluent Schema Registry, use the `KafkaConfluentSchemaRegistryJsonMessageDecoder`. This decoder uses the Confluent `KafkaJsonSchemaDeserializer` to decode messages whose JSON schemas are managed by the registry.

**When to use this decoder**

* Your Kafka producer serializes messages using the Confluent JSON Schema serializer.
* Your JSON schemas are registered in Confluent Schema Registry.
* You want schema validation and evolution support for JSON messages.

If your messages are Avro-encoded and registered with Schema Registry, use `KafkaConfluentSchemaRegistryAvroMessageDecoder` instead (shown in the SSL example above). If your messages are plain JSON without a schema registry, use `JSONMessageDecoder`.

**Example table config**

```json
{
  "tableName": "events",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "created_at",
    "timeType": "MILLISECONDS",
    "schemaName": "events",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "events",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
      "stream.kafka.broker.list": "localhost:9092",
      "stream.kafka.schema.registry.url": "http://localhost:8081",
      "stream.kafka.decoder.prop.schema.registry.rest.url": "http://localhost:8081",
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

The key configuration properties for this decoder are:

* `stream.kafka.decoder.class.name` -- Set to `org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder`.
* `stream.kafka.decoder.prop.schema.registry.rest.url` -- The URL of the Confluent Schema Registry.

**Authentication**

This decoder supports the same authentication options as the Avro schema registry decoder. You can configure SSL or SASL\_SSL authentication for both the Kafka consumer and the Schema Registry client using the `stream.kafka.decoder.prop.schema.registry.*` properties. See the [SSL example](#use-kafka-partition-low-level-consumer-with-ssl) and [SASL\_SSL example](#use-kafka-partition-low-level-consumer-with-sasl\_ssl) above for details.

For Schema Registry basic authentication, add the following properties:

```
"stream.kafka.decoder.prop.basic.auth.credentials.source": "USER_INFO",
"stream.kafka.decoder.prop.schema.registry.basic.auth.user.info": "<username>:<password>"
```

{% hint style="info" %}
This decoder was added in Pinot 1.4. Make sure your Pinot deployment is running version 1.4 or later.
{% endhint %}

#### Consume transactionally-committed messages

The Kafka 3.x and 4.x connectors support Kafka transactions. The transaction support is controlled by config `kafka.isolation.level` in Kafka stream config, which can be `read_committed` or `read_uncommitted` (default). Setting it to `read_committed` will ingest transactionally committed messages in Kafka stream only.

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
        "stream.kafka.topic.name": "transcript-topic",
        "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
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
        "stream.kafka.topic.name": "mytopic",
        "stream.kafka.consumer.prop.auto.offset.reset": "largest",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
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

| Kafka Record | Pinot Table Column | Description |
| --- | --- | --- |
| Record key: any type <K> | `__key` : String | For simplicity of design, we assume that the record key is always a UTF-8 encoded String |
| Record Headers: Map<String, String> | Each header key is listed as a separate column: `__header$HeaderKeyName` : String | For simplicity of design, we directly map the string headers from kafka record to pinot table column |
| Record metadata - offset : long | `__metadata$offset` : String |  |
| Record metadata - partition : int | `__metadata$partition` : String |  |
| Record metadata - recordTimestamp : long | `__metadata$recordTimestamp` : String |  |

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
Remember to follow the [schema evolution guidelines](../../../tutorials/data-ingestion/schema-evolution.md) when updating schema of an existing table!
{% endhint %}

#### Tell Pinot where to find an Avro schema

There is a standalone utility to generate the schema from an Avro file. See [infer the pinot schema from the avro schema and JSON data](../../../build-with-pinot/ingestion/complex-type#infer-the-pinot-schema-from-the-avro-schema-and-json-data) for details.

To avoid errors like `The Avro schema must be provided`, designate the location of the schema in your `streamConfigs` section. For example, if your current section contains the following:

```json
...
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.topic.name": "",
  "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
  "stream.kafka.broker.list": "",
  "stream.kafka.consumer.prop.auto.offset.reset": "largest"
  ...
}
```

Then add this key: `"stream.kafka.decoder.prop.schema"`followed by a value that denotes the location of your schema.

#### Subset partition ingestion

By default, a Pinot REALTIME table consumes from all partitions of the configured Kafka topic. In some scenarios you may want a table to consume only a subset of the topic's partitions. The `stream.kafka.partition.ids` setting lets you specify exactly which Kafka partitions a table should consume.

**When to use subset partition ingestion**

* **Split-topic ingestion** -- Multiple Pinot tables share the same Kafka topic, and each table is responsible for a different set of partitions. This is useful when the same topic contains logically distinct data partitioned by key, and you want separate tables (or indexes) for each partition group.
* **Multi-table partition assignment** -- You want to distribute the partitions of a high-throughput topic across several Pinot tables for workload isolation, independent scaling, or different retention policies.
* **Selective consumption** -- You only need data from specific partitions of a topic (for example, partitions that correspond to a particular region or tenant).

**Configuration**

Add `stream.kafka.partition.ids` to the `streamConfigMaps` entry in your table config. The value can contain individual zero-based partition IDs, inclusive ranges, or a mix of both in a comma-separated string:

```json
"stream.kafka.partition.ids": "0-3,6,8-9"
```

For example, `"0,2,5"` consumes three explicit partitions, `"0-3"` consumes partitions 0 through 3 inclusive, and `"0-3,6,8-9"` mixes both forms in one value.

When this setting is present, Pinot will consume only from the resolved set of partitions. When it is absent or blank, Pinot consumes from all partitions of the topic (the default behavior).

**Example: splitting a topic across two tables**

Suppose you have a Kafka topic called `events` with two partitions (0 and 1). You can create two Pinot tables, each consuming from one partition:

Table `events_part_0`:

```json
{
  "tableName": "events_part_0",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "ts",
    "schemaName": "events",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP"
  },
  "ingestionConfig": {
    "streamIngestionConfig": {
      "streamConfigMaps": [
        {
          "streamType": "kafka",
          "stream.kafka.topic.name": "events",
          "stream.kafka.partition.ids": "0",
          "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
          "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
          "stream.kafka.broker.list": "kafka:9092",
          "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
          "realtime.segment.flush.threshold.rows": "0",
          "realtime.segment.flush.threshold.time": "24h",
          "realtime.segment.flush.threshold.segment.size": "50M"
        }
      ]
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

Table `events_part_1`:

```json
{
  "tableName": "events_part_1",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "ts",
    "schemaName": "events",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP"
  },
  "ingestionConfig": {
    "streamIngestionConfig": {
      "streamConfigMaps": [
        {
          "streamType": "kafka",
          "stream.kafka.topic.name": "events",
          "stream.kafka.partition.ids": "1",
          "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
          "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
          "stream.kafka.broker.list": "kafka:9092",
          "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
          "realtime.segment.flush.threshold.rows": "0",
          "realtime.segment.flush.threshold.time": "24h",
          "realtime.segment.flush.threshold.segment.size": "50M"
        }
      ]
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

**Validation rules and limitations**

* Partition IDs must be non-negative integers. Range values are inclusive, and the start of a range must be less than or equal to the end.
* Non-integer values (for example, `"abc"`) and malformed ranges (for example, `"5-"`) will cause a validation error.
* Duplicate IDs are silently deduplicated after range expansion. For example, `"0,2,0,5"` is treated as `"0,2,5"`.
* The partition IDs are sorted internally for stable ordering, regardless of the order specified in the config.
* Pinot validates the resolved partition IDs against the Kafka topic metadata before it starts consuming. If a specified partition ID does not exist in the topic, an error is raised.
* The resolved set can contain at most 10,000 unique partition IDs.
* When using subset partition ingestion with multiple tables consuming from the same topic, ensure that the partition assignments do not overlap if you want each record to be consumed by exactly one table. Pinot does not enforce non-overlapping partition assignments across tables.
* Whitespace around partition IDs, commas, and range bounds is trimmed (for example, `" 0 - 3 , 5 "` is valid).

#### Use Protocol Buffers (Protobuf) format

Pinot supports decoding Protocol Buffer messages from Kafka using several decoder options depending on your setup.

**ProtoBufMessageDecoder (descriptor file based)**

Use `ProtoBufMessageDecoder` when you have a pre-compiled `.desc` (descriptor) file for your Protobuf schema. This decoder uses dynamic message parsing and does not require compiled Java classes.

Required stream config properties:

| Property | Description |
|---|---|
| `stream.kafka.decoder.prop.descriptorFile` | Path or URI to the `.desc` descriptor file. Supports local file paths, HDFS, and other Pinot-supported file systems. |
| `stream.kafka.decoder.prop.protoClassName` | (Optional) Fully qualified Protobuf message name within the descriptor. If omitted, the first message type in the descriptor is used. |

Example `streamConfigs`:

```json
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.topic.name": "my-protobuf-topic",
  "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
  "stream.kafka.broker.list": "kafka:9092",
  "stream.kafka.decoder.prop.descriptorFile": "/path/to/my_message.desc",
  "stream.kafka.decoder.prop.protoClassName": "mypackage.MyMessage"
}
```

**ProtoBufCodeGenMessageDecoder (compiled JAR based)**

Use `ProtoBufCodeGenMessageDecoder` when you have a compiled JAR containing your generated Protobuf Java classes. This decoder uses runtime code generation for improved decoding performance.

Required stream config properties:

| Property | Description |
|---|---|
| `stream.kafka.decoder.prop.jarFile` | Path or URI to the JAR file containing compiled Protobuf classes. |
| `stream.kafka.decoder.prop.protoClassName` | Fully qualified Java class name of the Protobuf message (required). |

Example `streamConfigs`:

```json
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.topic.name": "my-protobuf-topic",
  "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.protobuf.ProtoBufCodeGenMessageDecoder",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
  "stream.kafka.broker.list": "kafka:9092",
  "stream.kafka.decoder.prop.jarFile": "/path/to/my-protobuf-classes.jar",
  "stream.kafka.decoder.prop.protoClassName": "com.example.proto.MyMessage"
}
```

**KafkaConfluentSchemaRegistryProtoBufMessageDecoder (Confluent Schema Registry)**

Use `KafkaConfluentSchemaRegistryProtoBufMessageDecoder` when your Protobuf schemas are managed by Confluent Schema Registry. This decoder automatically resolves schemas from the registry at runtime.

Required stream config properties:

| Property | Description |
|---|---|
| `stream.kafka.decoder.prop.schema.registry.rest.url` | URL of the Confluent Schema Registry. |

Optional properties:

| Property | Description |
|---|---|
| `stream.kafka.decoder.prop.cached.schema.map.capacity` | Maximum number of cached schemas. Default: `1000`. |
| `stream.kafka.decoder.prop.schema.registry.*` | SSL and authentication options for connecting to Schema Registry (same pattern as the Avro Confluent decoder). |

Example `streamConfigs`:

```json
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.topic.name": "my-protobuf-topic",
  "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
  "stream.kafka.broker.list": "kafka:9092",
  "stream.kafka.decoder.prop.schema.registry.rest.url": "http://schema-registry:8081"
}
```

#### Use Apache Arrow format

Pinot supports decoding Apache Arrow IPC streaming format messages from Kafka using `ArrowMessageDecoder`. This is useful when upstream systems produce data serialized in Arrow format.

Optional stream config properties:

| Property | Description |
|---|---|
| `stream.kafka.decoder.prop.arrow.allocator.limit` | Maximum memory (in bytes) for the Arrow allocator. Default: `268435456` (256 MB). |
| `stream.kafka.decoder.prop.extractRawTimeValues` | Keep Arrow `Date`, `Time`, and `Timestamp` values as raw integers instead of Pinot's default converted values. Default: `false`. |

Example `streamConfigs`:

```json
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.topic.name": "my-arrow-topic",
  "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.arrow.ArrowMessageDecoder",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
  "stream.kafka.broker.list": "kafka:9092",
  "stream.kafka.decoder.prop.arrow.allocator.limit": "536870912",
  "stream.kafka.decoder.prop.extractRawTimeValues": "true"
}
```

{% hint style="info" %}
The Arrow decoder expects each Kafka message to contain a complete Arrow IPC stream (schema + record batch). Ensure your producer serializes Arrow data in the IPC streaming format.
{% endhint %}

When `stream.kafka.decoder.prop.extractRawTimeValues` is `false` (the default), Pinot converts Arrow `Date`, `Time`, and `Timestamp` values during extraction. Set it to `true` to keep raw integers instead: `Date` stays as days since epoch, while `Time` and `Timestamp` stay in the schema's declared Arrow unit.

Each Arrow Kafka message can yield zero, one, or many Pinot rows. Empty batches are ignored, single-row batches ingest as one Pinot row, and multi-row batches fan out into multiple Pinot rows.

## Consuming a Subset of Kafka Partitions

By default, a Pinot realtime table consumes all partitions of a Kafka topic. You can restrict ingestion to a specific subset of partitions using the `stream.kafka.partition.ids` property. This is useful when:

- Splitting a single Kafka topic across multiple Pinot tables for independent scaling
- Multi-tenant scenarios where different tables own different partition ranges

### Configuration

Add `stream.kafka.partition.ids` to your `streamConfigs` with a comma-separated string of partition IDs, inclusive ranges, or both:

```json
"streamConfigs": {
  "streamType": "kafka",
  "stream.kafka.topic.name": "myTopic",
  "stream.kafka.broker.list": "localhost:9092",
  "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
  "stream.kafka.partition.ids": "0-3,6,8-9"
}
```

For example, `"0,2,5"` selects individual partitions, `"0-3"` selects an inclusive range, and `"0-3,6,8-9"` mixes both forms in one value.

### Notes

- Partition IDs must be non-negative integers. Ranges are inclusive and must have `start <= end`.
- Pinot validates the resolved partition IDs against the Kafka topic metadata before it starts consuming.
- Duplicate IDs in the list are automatically deduplicated.
- The resolved set can contain at most 10,000 unique partition IDs.
- The total partition count reported to the broker reflects the full Kafka topic size, ensuring correct query routing across tables sharing the same topic.
- When splitting a topic between two tables, configure one with even-numbered IDs and another with odd-numbered IDs (for example, `"0,2"` and `"1,3"` for a 4-partition topic).
