---
description: This guide shows you how to ingest a stream of records into a Pinot table.
---

# Stream ingestion

Apache Pinot lets users consume data from streams and push it directly into the database. This process is called stream ingestion. Stream ingestion makes it possible to query data within seconds of publication.

Stream ingestion provides support for checkpoints for preventing data loss.

To set up Stream ingestion, perform the following steps, which are described in more detail in this page:

1. Create schema configuration
2. Create table configuration
3. Create ingestion configuration
4. Upload table and schema spec

Here's an example where we assume the data to be ingested is in the following format:

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

## Create schema configuration

The schema defines the fields along with their data types. The schema also defines whether fields serve as `dimensions` , `metrics`, or `timestamp`. For more details on schema configuration, see [creating a schema](../../getting-started/pushing-your-data-to-pinot.md#creating-a-schema).

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

## Create table configuration

The next step is to create a table where all the ingested data will flow and can be queried. For details about each table component, see the [table](../../components/table/) reference.

## Create ingestion configuration

The ingestion configuration (`ingestionConfig`) specifies how to ingest streaming data into Pinot. First, include a subsection for `streamConfigMaps`. Next, decide whether to skip table errors with `_continueOnError` and whether to validate time values with `rowTimeValueCheck` and `_segmentTimeValueCheck`. See details about these `ingestionConfig` configuration options the **streamConfigMaps** and **Additional ingestion configs** tables below:

### Information about `streamConfigMaps`

| **Config key**                                        | **Description**                                                                                                                                                                     | **Supported values**                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `streamType`                                          | The streaming platform to ingest data from                                                                                                                                          | `kafka`                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `stream.[streamType].consumer.type`                   | Whether to use per partition low-level consumer or high-level stream consumer                                                                                                       | - `lowLevel`: Consume data from each partition with offset management. - `highLevel`: Consume data without control over the partitions.                                                                                                                                                                                                                                                                                                                                           |
| `stream.[streamType].topic.name`                      | Topic or data source to ingest data from                                                                                                                                            | String                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `stream.[streamType].broker.list`                     | List of brokers                                                                                                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `stream.[streamType].decoder.class.name`              | Name of class to parse the data. The class should implement the `org.apache.pinot.spi.stream.StreamMessageDecoder` interface.                                                       | String. Available options: - `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.KafkaAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.csv.CSVMessageDecoder` - `org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder` |
| `stream.[streamType].consumer.factory.class.name`     | Name of factory class to provide the appropriate implementation of low-level and high-level consumer, as well as the metadata                                                       | String. Available options: - `org.apache.pinot.plugin.stream.kafka09.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory` - `org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory`                                                                                                                                                                                      |
| `stream.[streamType].consumer.prop.auto.offset.reset` | Determines the offset from which to start the ingestion                                                                                                                             | - `smallest` - `largest` - timestamp in milliseconds                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `stream.[streamType].decoder.prop.format`             | Specifies the data format to ingest via a stream. The value of this property should match the format of the data in the stream.                                                     | - `JSON`                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `realtime.segment.flush.threshold.time`               | Maximum elapsed time after which a consuming segment persist. Note that this time should be smaller than the Kafka retention period configured for the corresponding topic.         | String, such `1d` or `4h30m`. Default is `6h` (six hours).                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `realtime.segment.flush.threshold.rows`               | The maximum number of rows to consume before persisting the consuming segment. If this value is set to 0, the configuration looks to `realtime.segment.flush.threshold.rows` below. | Default is 5,000,000                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `realtime.segment.flush.threshold.segment.size`       | Desired size of the completed segments. This value is used when `realtime.segment.flush.threshold.rows` is set to 0.                                                                | String, such as `150M` or `1.1G`., etc. Default is `200M` (200 megabytes). You can also specify additional configurations for the consumer directly into `streamConfigMaps`. For example, for Kafka streams, add any of the configs described in [Kafka configuration page](https://kafka.apache.org/documentation/#consumerconfigs) to pass them directly to the Kafka consumer.                                                                                                 |

### Additional ingestion configurations

| Config key               | Description                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_continueOnError`       | Set to `true` to skip any row indexing error and move on to the next row. Otherwise, an error evaluating a transform or filter function may block ingestion (real-time or offline), and result in data loss or corruption. Consider your use case to determine if it's preferable to set this option to `false`, and fail the ingestion if an error occurs to maintain data integrity.                           |
| `rowTimeValueCheck`      | Set to `true` to validate the time column values ingested during segment upload. Validates each row of data in a segment matches the specified time format, and falls within a valid time range (1971-2071). If the value doesn't meet both criteria, Pinot replaces the value with null. This option ensures that the time values are strictly increasing and that there are no duplicates or gaps in the data. |
| `_segmentTimeValueCheck` | Set to `true` to validate the time range of the segment falls between 1971 and 2071. This option ensures data segments stored in the system are correct and consistent                                                                                                                                                                                                                                           |

### Example table config with `ingestionConfig`

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
  },
  "metadata": {
    "customConfigs": {}
  },
  "ingestionConfig": {
    "streamIngestionConfig": {
        "streamConfigMaps": [
          {
            "realtime.segment.flush.threshold.rows": "0",
            "stream.kafka.decoder.prop.format": "JSON",
            "key.serializer": "org.apache.kafka.common.serialization.ByteArraySerializer",
            "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
            "streamType": "kafka",
            "value.serializer": "org.apache.kafka.common.serialization.ByteArraySerializer",
            "stream.kafka.consumer.type": "LOWLEVEL",
            "realtime.segment.flush.threshold.segment.rows": "50000",
            "stream.kafka.broker.list": "localhost:9876",
            "realtime.segment.flush.threshold.time": "3600000",
            "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
            "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
            "stream.kafka.topic.name": "transcript-topic"
          }
        ]
      },
      "transformConfigs": [],
      "continueOnError": true,
      "rowTimeValueCheck": true,
      "segmentTimeValueCheck": false
    },
    "isDimTable": false
  }
}
```

## Upload schema and table config

Now that we have our table and schema configurations, let's upload them to the Pinot cluster. As soon as the configs are uploaded, Pinot will start ingesting available records from the topic.

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

## Tune the stream config

### Throttle stream consumption

There are some scenarios where the message rate in the input stream can come in bursts which can lead to long GC pauses on the Pinot servers or affect the ingestion rate of other real-time tables on the same server. If this happens to you, throttle the consumption rate during stream ingestion to better manage overall performance.

Stream consumption throttling can be tuned using the stream config `topic.consumption.rate.limit` which indicates the upper bound on the message rate for the entire topic.

Here is the sample configuration on how to configure the consumption throttling:

```json
{
  "tableName": "transcript",
  "tableType": "REALTIME",
  ...
  "ingestionConfig": {
    "streamIngestionConfig":,
    "streamConfigMaps": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "lowlevel",
      "stream.kafka.topic.name": "transcript-topic",
      ...
      "topic.consumption.rate.limit": 1000
    }
  },
  ...
```

Some things to keep in mind while tuning this config are:

* Since this configuration applied to the entire topic, internally, this rate is divided by the number of partitions in the topic and applied to each partition's consumer.
* In case of multi-tenant deployment (where you have more than 1 table in the same server instance), you need to make sure that the rate limit on one table doesn't step on/starve the rate limiting of another table. So, when there is more than 1 table on the same server (which is most likely to happen), you may need to re-tune the throttling threshold for all the streaming tables.

Once throttling is enabled for a table, you can verify by searching for a log that looks similar to:

{% code overflow="wrap" %}
```markdown
A consumption rate limiter is set up for topic <topic_name> in table <tableName> with rate limit: <rate_limit> (topic rate limit: <topic_rate_limit>, partition count: <partition_count>)
```
{% endcode %}

In addition, you can monitor the consumption rate utilization with the metric `COSUMPTION_QUOTA_UTILIZATION`.

Note that any configuration change for `topic.consumption.rate.limit` in the stream config will **NOT** take effect immediately. The new configuration will be picked up from the next consuming segment. In order to enforce the new configuration, you need to trigger forceCommit APIs. Refer to [Pause Stream Ingestion](./#pause-stream-ingestion) for more details.

```
$ curl -X POST {controllerHost}/tables/{tableName}/forceCommit
```

## Custom ingestion support

You can also write an ingestion plugin if the platform you are using is not supported out of the box. For a walkthrough, see [Stream Ingestion Plugin](../../../developers/plugin-architecture/write-custom-plugins/write-your-stream.md).

## Pause stream ingestion

There are some scenarios in which you may want to pause the real-time ingestion while your table is available for queries. For example, if there is a problem with the stream ingestion and, while you are troubleshooting the issue, you still want the queries to be executed on the already ingested data. For these scenarios, you can first issue a Pause request to a Controller host. After troubleshooting with the stream is done, you can issue another request to Controller to resume the consumption.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/pauseConsumption
$ curl -X POST {controllerHost}/tables/{tableName}/resumeConsumption
```

When a `Pause` request is issued, the controller instructs the real-time servers hosting your table to commit their consuming segments immediately. However, the commit process may take some time to complete. Note that `Pause` and `Resume` requests are async. An `OK` response means that instructions for pausing or resuming has been successfully sent to the real-time server. If you want to know if the consumption has actually stopped or resumed, issue a pause status request.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/pauseStatus
```

It's worth noting that consuming segments on real-time servers are stored in volatile memory, and their resources are allocated when the consuming segments are first created. These resources cannot be altered if consumption parameters are changed midway through consumption. It may take hours before these changes take effect. Furthermore, if the parameters are changed in an incompatible way (for example, changing the underlying stream with a completely new set of offsets, or changing the stream endpoint from which to consume messages), it will result in the table getting into an error state.

The pause and resume feature is helpful in these instances. When a pause request is issued by the operator, consuming segments are committed without starting new mutable segments. Instead, new mutable segments are started only when the resume request is issued. This mechanism provides the operators as well as developers with more flexibility. It also enables Pinot to be more resilient to the operational and functional constraints imposed by underlying streams.

There is another feature called `Force Commit` which utilizes the primitives of the pause and resume feature. When the operator issues a force commit request, the current mutable segments will be committed and new ones started right away. Operators can now use this feature for all compatible table config parameter changes to take effect immediately.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/forceCommit
```

(v 0.12.0+) Once submitted, the forceCommit API returns a jobId that can be used to get the current progress of the forceCommit operation. A sample response and status API call:

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/forceCommit
{
  "forceCommitJobId": "6757284f-b75b-45ce-91d8-a277bdbc06ae",
  "forceCommitStatus": "SUCCESS",
  "jobMetaZKWriteStatus": "SUCCESS"
}

$ curl -X GET {controllerHost}/tables/forceCommitStatus/6757284f-b75b-45ce-91d8-a277bdbc06ae
{
  "jobId": "6757284f-b75b-45ce-91d8-a277bdbc06ae",
  "segmentsForceCommitted": "[\"airlineStats__0__0__20230119T0700Z\",\"airlineStats__1__0__20230119T0700Z\",\"airlineStats__2__0__20230119T0700Z\"]",
  "submissionTimeMs": "1674111682977",
  "numberOfSegmentsYetToBeCommitted": 0,
  "jobType": "FORCE_COMMIT",
  "segmentsYetToBeCommitted": [],
  "tableName": "airlineStats_REALTIME"
}
```

{% hint style="info" %}
The forceCommit request just triggers a regular commit before the consuming segments reaching the end criteria, so it follows the same mechanism as regular commit. It is one-time shot request, and not retried automatically upon failure. But it is idempotent so one may keep issuing it till success if needed.&#x20;

This API is async, as it doesn't wait for the segment commit to complete. But a status entry is put in ZK to track when the request is issued and the consuming segments included. The consuming segments tracked in the status entry are compared with the latest IdealState to indicate the progress of forceCommit. However, this status is not updated or deleted upon commit success or failure, so that it could become stale. Currently, the most recent 100 status entries are kept in ZK, and the oldest ones only get deleted when the total number is about to exceed 100.
{% endhint %}

For incompatible parameter changes, an option is added to the resume request to handle the case of a completely new set of offsets. Operators can now follow a three-step process: First, issue a pause request. Second, change the consumption parameters. Finally, issue the resume request with the appropriate option. These steps will preserve the old data and allow the new data to be consumed immediately. All through the operation, queries will continue to be served.

```bash
$ curl -X POST {controllerHost}/tables/{tableName}/resumeConsumption?resumeFrom=smallest
$ curl -X POST {controllerHost}/tables/{tableName}/resumeConsumption?resumeFrom=largest
```

## Handle partition changes in streams

If a Pinot table is configured to consume using a [Low Level](./#create-table-configuration) (partition-based) stream type, then it is possible that the partitions of the table change over time. In Kafka, for example, the number of partitions may increase. In Kinesis, the number of partitions may increase _or_ decrease -- some partitions could be merged to create a new one, or existing partitions split to create new ones.

Pinot runs a periodic task called `RealtimeSegmentValidationManager` that monitors such changes and starts consumption on new partitions (or stops consumptions from old ones) as necessary. Since this is a [periodic task](../../components/cluster/controller.md#controller-periodic-tasks) that is run on the controller, it may take some time for Pinot to recognize new partitions and start consuming from them. This may delay the data in new partitions appearing in the results that pinot returns.

If you want to recognize the new partitions sooner, then [manually trigger](../../components/cluster/controller.md#running-the-periodic-task-manually) the periodic task so as to recognize such data immediately.

## Infer ingestion status of real-time tables

Often, it is important to understand the rate of ingestion of data into your real-time table. This is commonly done by looking at the consumption lag of the consumer. The lag itself can be observed in many dimensions. Pinot supports observing consumption lag along the offset dimension and time dimension, whenever applicable (as it depends on the specifics of the connector).

The ingestion status of a connector can be observed by querying either the `/consumingSegmentsInfo` API or the table's `/debug` API, as shown below:

{% code overflow="wrap" lineNumbers="true" %}
```shell
# GET /tables/{tableName}/consumingSegmentsInfo
curl -X GET "http://<controller_url:controller_admin_port>/tables/meetupRsvp/consumingSegmentsInfo" -H "accept: application/json"

# GET /debug/tables/{tableName}
curl -X GET "http://localhost:9000/debug/tables/meetupRsvp?type=REALTIME&verbosity=1" -H "accept: application/json"
```
{% endcode %}

A sample response from a Kafka-based real-time table is shown below. The ingestion status is displayed for each of the CONSUMING segments in the table.

```json
{
  "_segmentToConsumingInfoMap": {
    "meetupRsvp__0__0__20221019T0639Z": [
      {
        "serverName": "Server_192.168.0.103_7000",
        "consumerState": "CONSUMING",
        "lastConsumedTimestamp": 1666161593904,
        "partitionToOffsetMap": { // <<-- Deprecated. See currentOffsetsMap for same info
          "0": "6"
        },
        "partitionOffsetInfo": {
          "currentOffsetsMap": {
            "0": "6" // <-- Current consumer position
          },
          "latestUpstreamOffsetMap": {
            "0": "6"  // <-- Upstream latest position
          },
          "recordsLagMap": {
            "0": "0"  // <-- Lag, in terms of #records behind latest
          },
          "recordsAvailabilityLagMap": {
            "0": "2"  // <-- Lag, in terms of time
          }
        }
      }
    ],
```

| Term                      | Description                                                                                                                                                                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| currentOffsetsMap         | Current consuming offset position per partition                                                                                                                                                                                                                            |
| latestUpstreamOffsetMap   | (Wherever applicable) Latest offset found in the upstream topic partition                                                                                                                                                                                                  |
| recordsLagMap             | (Whenever applicable) Defines how far behind the current record's offset / pointer is from upstream latest record. This is calculated as the difference between the `latestUpstreamOffset` and `currentOffset` for the partition when the lag computation request is made. |
| recordsAvailabilityLagMap | (Whenever applicable) Defines how soon after record ingestion was the record consumed by Pinot. This is calculated as the difference between the time the record was consumed and the time at which the record was ingested upstream.                                      |

## Monitor real-time ingestion

Real-time ingestion includes 3 stages of message processing: Decode, Transform, and Index.

In each of these stages, a failure can happen which may or may not result in an ingestion failure. The following metrics are available to investigation ingestion issues:

1. Decode stage -> an error here is recorded as `INVALID_REALTIME_ROWS_DROPPED`
2. Transform stage -> possible errors here are:
   1. When a message gets dropped due to the [FILTER](../../../developers/advanced/ingestion-level-transformations.md#filtering) transform, it is recorded as `REALTIME_ROWS_FILTERED`
   2. When the transform pipeline sets the `$INCOMPLETE_RECORD_KEY$` key in the message, it is recorded as `INCOMPLETE_REALTIME_ROWS_CONSUMED` , only when `continueOnError` configuration is enabled. If the `continueOnError` is not enabled, the ingestion fails.
3. Index stage -> When there is failure at this stage, the ingestion typically stops and marks the partition as ERROR.

There is yet another metric called `ROWS_WITH_ERROR` which is the sum of all error counts in the 3 stages above.

Furthermore, the metric `REALTIME_CONSUMPTION_EXCEPTIONS` gets incremented whenever there is a transient/permanent stream exception seen during consumption.

These metrics can be used to understand why ingestion failed for a particular table partition before diving into the server logs.
