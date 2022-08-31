# Stream ingestion

Apache Pinot lets users consume data from streams and push it directly into the database, in a process known as stream ingestion. Stream Ingestion makes it possible to query data within seconds of publication.

Stream Ingestion provides support for checkpoints for preventing data loss.

Setting up Stream ingestion involves the following steps:

1. Create schema configuration
2. Create table configuration
3. Upload table and schema spec

Let's take a look at each of the steps in more detail.

Let us assume the data to be ingested is in the following format:

```bash
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

### Create Schema Configuration

Schema defines the fields along with their data types. The schema also defines whether fields serve as `dimensions` , `metrics` or `timestamp`. For more details on schema configuration, see [creating a schema](../../getting-started/pushing-your-data-to-pinot.md#creating-a-schema).

For our sample data, the schema configuration looks like this:

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

### Create Table Configuration

The next step is to create a table where all the ingested data will flow and can be queried. Unlike batch ingestion, table configuration for real-time ingestion also triggers the data ingestion job. For a more detailed overview of tables, see the [table](../../components/table.md) reference.

The real-time table configuration consists of the following fields:

* **tableName** - The name of the table where the data should flow
* **tableType** - The internal type for the table. Should always be set to `REALTIME` for realtime ingestion
* **segmentsConfig** -
* **tableIndexConfig** - defines which column to use for indexing along with the type of index. For full configuration, see \[Indexing Configs]. It has the following _**required**_ fields -
  * **loadMode** - specifies how the segments should be loaded. Should be`heap` or `mmap`. Here's the difference between both the configs
    * _mmap_: Segments are loaded onto memory-mapped files. This is the default mode.
    * _heap_: Segments are loaded into direct memory. Note, 'heap' here is a legacy misnomer, and it does not imply JVM heap. This mode should only be used when we want faster performance than memory-mapped files, and are also sure that we will never run into OOM.
  * **streamConfig** - specifies the data source along with the necessary configs to start consuming the real-time data. The streamConfig can be thought of as the equivalent to the job spec for batch ingestion. The following options are supported:

| Config key                                           | Description                                                                                                                                                                                                                                                                                                                                    | Supported values                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| streamType                                           | The streaming platform from which to consume the data                                                                                                                                                                                                                                                                                          | `kafka`                                                                                                                                                                                                                                                                                                                                                                                                                         |
| stream.\[streamType].consumer.type                   | Whether to use per partition low-level consumer or high-level stream consumer                                                                                                                                                                                                                                                                  | <ul><li><code>lowLevel</code> - Consume data from each partition with offset management</li><li><code>highLevel</code> - Consume data without control over the partitions</li></ul>                                                                                                                                                                                                                                             |
| stream.\[streamType].topic.name                      | The datasource (e.g. topic, data stream) from which to consume the data                                                                                                                                                                                                                                                                        | String                                                                                                                                                                                                                                                                                                                                                                                                                          |
| stream.\[streamType].decoder.class.name              | Name of the class to be used for parsing the data. The class should implement `org.apache.pinot.spi.stream.StreamMessageDecoder` interface                                                                                                                                                                                                     | <p>String. Available options:</p><ul><li><code>org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder</code></li><li><code>org.apache.pinot.plugin.inputformat.avro.KafkaAvroMessageDecoder</code></li><li><code>org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder</code></li><li><code>org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder</code></li></ul> |
| stream.\[streamType].consumer.factory.class.name     | Name of the factory class to be used to provide the appropriate implementation of low level and high level consumer as well as the metadata                                                                                                                                                                                                    | <p>String. Available options:</p><ul><li>org.apache.pinot.plugin.<code>stream.kafka09.KafkaConsumerFactory</code></li><li><code>org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory</code></li><li><code>org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory</code></li><li><code>org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory</code></li></ul>                                                |
| stream.\[streamType].consumer.prop.auto.offset.reset | Determines the offset from which to start the ingestion                                                                                                                                                                                                                                                                                        | <ul><li><code>smallest</code></li><li><code>largest</code> or</li><li>timestamp in milliseconds</li></ul>                                                                                                                                                                                                                                                                                                                       |
| topic.consumption.rate.limit                         | <p>Determines the upper bound for consumption rate for the whole topic.<br>Having a consumption rate limiter is beneficial in case the stream message rate has a bursty pattern which leads to long GC pauses on the Pinot servers. The rate limiter can also be considered as a safeguard against excessive ingestion of realtime tables.</p> | Double. The values should be greater than zero.                                                                                                                                                                                                                                                                                                                                                                                 |

The following flush threshold settings are also supported:

| Config key                                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Supported values |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| realtime.segment.flush.threshold.time         | Time threshold that will keep the realtime segment open for before we complete the segment. Noted that this time should be smaller than the Kafka retention period configured for the corresponding topic.                                                                                                                                                                                                                                                                                                                                                                                                                                |                  |
| realtime.segment.flush.threshold.rows         | <p>Row count flush threshold for realtime segments. This behaves in a similar way for HLC and LLC. For HLC,</p><p>since there is only one consumer per server, this size is used as the size of the consumption buffer and determines after how many rows we flush to disk. For example, if this threshold is set to two million rows,</p><p>then a high level consumer would have a buffer size of two million.</p><p>If this value is set to 0, then the consumers adjust the number of rows consumed by a partition such that the size of the completed segment is the desired size (unless</p><p>threshold.time is reached first)</p> |                  |
| realtime.segment.flush.threshold.segment.size | The desired size of a completed realtime segment. This config is used only if `realtime.segment.flush.threshold.rows` is set to 0.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                  |

You can also specify additional configs for the consumer directly into the streamConfigs.

For our sample data and schema, the table config will look like this:

```json
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
      "realtime.segment.flush.threshold.rows": "50000",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

### Upload schema and table config

Now that we have our table and schema configurations, let's upload them to the Pinot cluster. As soon as the configs are uploaded, pinot will start ingesting available records from the topic.

{% tabs %}
{% tab title="Docker" %}
```
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
    -schemaFile /path/to/transcript-schema.json \
    -tableConfigFile /path/to/transcript-table-realtime.json \
    -exec
```
{% endtab %}
{% endtabs %}

### Custom Ingestion Support

We are working on support for other ingestion platforms, but you can also write your own ingestion plugin if it is not supported out of the box. For a walkthrough, see [Stream Ingestion Plugin](../../../developers/plugin-architecture/write-custom-plugins/write-your-stream.md).

### Pause Stream Ingestion

There are some scenarios in which you may want to pause the realtime ingestion while your table is available for queries. For example if there is a problem with the stream ingestion, while you are troubleshooting the issue, you still want the queries to be executed on the already ingested data. For these scenarios, you can first issue a Pause request to a Controller host. After troubleshooting with the stream is done, you can issue another request to Controller to resume the consumption.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/pauseConsumption
$ curl -X POST {controllerHost}/tables/{tableName}/resumeConsumption
```

When a Pause request is issued, Controller instructs the realtime servers hosting your table to commit their consuming segments immediately. However, the commit process may take some time to complete. Please note that Pause and Resume requests are async. OK response means that instructions for pausing or resuming has been successfully sent to the realtime server. If you want to know if the consumptions actually stopped or resumed, you can issue a pause status request.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/pauseStatus
```

It's worth noting that consuming segments on realtime servers are stored in volatile memory, and their resources are allocated when the consuming segments are first created. These resources cannot be altered if consumption parameters are changed midway through consumption. It may therefore take hours before these changes take effect. Furthermore, if the parameters are changed in an incompatible way (for example, changing the underlying stream with a completely new set of offsets, or changing the stream endpoint from which to consume messages, etc.), it will result in the table getting into an error state.

Pause and resume feature comes to the rescue here. When a Pause request is issued by the operator, consuming segments are committed without starting new mutables ones. Instead, new mutable segments are started only when the Resume request is issued. This mechanism provides the operators as well as developers with more flexibility. It also enables Pinot to be more resilient to the operational and functional constraints imposed by underlying streams.

There is another feature called "Force Commit" which utilizes the primitives of pause and resume feature. When the operator issues a force commit request, the current mutable segments will be committed and new ones started right away. Operators can now use this feature for all compatible table config parameter changes to take effect immediately.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/forceCommit
```

For incompatible parameter changes, an option is added to the resume request to handle the case of a completely new set of offsets. Operators can now follow a three-step process: First, issue a Pause request. Second, change the consumption parameters. Finally, issue the Resume request with the appropriate option. These steps will preserve the old data and allow the new data to be consumed immediately. All through the operation, queries will continue to be served.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/resumeConsumption?resumeFrom=smallest
$ curl -X POST {controllerHost}/tables/{tableName}/resumeConsumption?resumeFrom=largest
```
