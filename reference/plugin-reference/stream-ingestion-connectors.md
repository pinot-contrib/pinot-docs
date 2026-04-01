---
description: >-
  This documents lists all the configurations for each of the supported stream
  ingestion connectors.
---

# Stream Ingestion Connectors

## Applicable to all Stream Connectors

| Configuration | Description |
| --- | --- |
| stream.<stream_type>.consumer.factory.class.name | Factory class to be used for the stream consumer |
| stream.<stream_type>.consumer.prop.auto.offset.reset | Offset or position in the source stream from which to start consuming data **Valid values:** **`smallest`** - Start consuming from the earliest data in the stream **`largest`** - Start consuming from the latest data in the stream **`timestamp`** - Start consuming from the offset after a timestamp , which is specified in the format `yyyy-MM-dd'T'HH:mm:ss.SSSZ` **`datetime` -** Start consuming from the offset after the specified period or duration from current time. Eg: `2d` **Default Value:** `largest` |
| stream.<stream_type>.topic.name | Name of the source stream to consume |
| stream.<stream_type>.fetch.timeout.millis | Indicates the timeout (in milliseconds) to use for each fetch call to the consumer. If the timeout expires before data becomes available, the consumer will return an empty batch. **Default Value:** `5_000` |
| stream.<stream_type>.connection.timeout.millis | Indicates the timeout (in milliseconds) used to create the connection to the upstream (Timeout for the initial connection to the upstream) **Default Value:** `30_000` |
| stream.<stream_type>.idle.timeout.millis | If the stream remains idle (ie. without any data) for the specified time, the client connection is reset and a new consumer instance is created. **Default Value:** `180_000` |
| stream.<stream_type>.decoder.class.name | Indicates the name of the decoder class that should be used to decoder the stream payload |
| stream.<stream_type>.decoder.prop | Prefix used for any decoder specific property |
| topic.consumption.rate.limit | Indicates the upper bound on the message rate for the entire topic. Use `-1` to ignore this config. **Default Value:** `-1` See [here](../../build-with-pinot/ingestion/stream-ingestion/README.md#throttling-stream-consumption) for more details. |
| stream.<stream_type>.metadata.populate | When set to `true`, the supported consumer may extract the key, user headers and record metadata from the incoming payload. Currently, this is supported in Kafka connector only. |
| realtime.segment.flush.threshold.time | Time based flush threshold for realtime segments. Used to decides when a realtime segment is ready to be committed / closed / flushed to disk. ⚠ This time should be smaller than the retention period configured for the corresponding topic |
| realtime.segment.flush.threshold.size | The size a completed realtime segment should be. ℹThis config is used only if `realtime.segment.flush.threshold.rows` is set to 0. |
| realtime.segment.flush.threshold.rows | Row count based flush threshold for realtime segments. If this value is set to 0, then the consumers adjust the number of rows consumed by a partition so the completed segment is the correct size (unless threshold.time is reached first) |
| realtime.segment.flush.autotune.initialRows | Initial number of rows to use for `SegmentSizeBasedFlushThresholdUpdater` . This threshold updater is used by the controller to compute the new segment's flush threshold based on the previous segment's size. ⚠ This flush threshold updater is used only when `realtime.segment.flush.threshold.rows` is set to `<=0` . Otherwise, the `DefaultFlushThresholdUpdater` is used. |
| realtime.segment.commit.timeoutSeconds | Time threshold that controller will wait for the segment to be built by the server |

## Kafka Partition-Level Connector&#x20;

### Kafka 3.x / 4.x

Pinot ships two Kafka connector modules: `pinot-kafka-3.0` (Kafka client 3.9.2, default) and `pinot-kafka-4.0` (Kafka client 4.1.1, for KRaft-mode clusters). The legacy `kafka-0.9` and `kafka-2.x` modules have been removed.


| Config | Description |
| --- | --- |
| stream.kafka.consumer.factory.class.name | **Allowed Values:** - `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` (Kafka 3.x, default) - `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` (Kafka 4.x) |
| stream.kafka.topic.name | (Required) Name of the kafka topic to be ingested |
| stream.kafka.broker.list | (Required) Connection string for the kafka broker |
| stream.kafka.partition.ids | Optional comma-separated list of Kafka partition IDs to consume (e.g. `"0,2,5"`). When set, only the specified partitions are consumed by this table. When absent or blank, all topic partitions are consumed (the default behavior). Partition IDs must be non-negative integers. Duplicates are silently removed. The IDs are validated against the actual topic metadata at table creation time. See [Subset Partition Ingestion](../../build-with-pinot/ingestion/stream-ingestion/import-from-apache-kafka.md#subset-partition-ingestion) for details and examples. |
| stream.kafka.buffer.size | **Default Value:** `512000` |
| stream.kafka.socket.timeout | **Default Value:** `10000` |
| stream.kafka.fetcher.size | **Default Value:** `100000` |
| stream.kafka.isolation.level | **Allowed Value:** `read_committed` **,** `read_uncommitted` **Default:** `read_uncommitted` **Note:** This must be set to `read_committed` when using transactions in Kafka. |

### Supported Decoder Classes

| Decoder Class | Description |
| --- | --- |
| `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder` | Decodes plain JSON messages without a schema registry. |
| `org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder` | Decodes Avro messages using a schema provided via `stream.kafka.decoder.prop.schema`. |
| `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` | Decodes Avro messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`. |
| `org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder` | Decodes JSON messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`. Added in Pinot 1.4. |
| `org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder` | Decodes Protocol Buffer messages. |

## Kinesis Partition-level Connector

| Config | Description |
| --- | --- |
| stream.kinesis.consumer.factory.class.name | **Allowed Value:** org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory |
| stream.kinesis.topic.name | (Required) Name of the Kinesis data stream to consume |
| region | (Required) The AWS region where the configured Kinesis data stream resides |
| maxRecordsToFetch | Maximum records to fetch during a single GetRecord request **Default:** `20` |
| shardIteratorType | Similar to Kafka's offset reset property - indicates the point in the AWS Kinesis data stream from where the consumption should begin **Allowed Values:** `TRIM_HORIZON` , `LATEST` |

### Key-based Authentication Properties

| Config | Description |
| --- | --- |
| accessKey | (Required) AWS Access key used to access the AWS Kinesis Data stream |
| secretKey | (Required) AWS Secret key used to access the AWS Kinesis Data stream |

### IAM Role-based Authentication Properties

| Config | Description |
| --- | --- |
| iamRoleBasedAccessEnabled | Set to `true` when using IAM role-based authentication for connecting to the AWS Kinesis Data Stream **Default:** `false` |
| roleArn | **(Required)** ARN of cross-account IAM role |
| roleSessionName | Unique identifier for a session when the client assumes the IAM role **Default:** `pinot-kinesis-<UUID>` |
| externalId | Unique identifier used to manage trust between AWS accounts and prevent the confused deputy problem. More details [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html) |
| sessionDurationSeconds | Duration of the role session in seconds **Default:** `900` |
| asyncSessionUpdateEnabled | Flag to determine with the session update should be enabled **Default:** `true` |

