---
description: Ingestion configuration reference.
---

# Ingestion Configuration

This page keeps the `ingestionConfig` overview and the detailed property tables on a single page.

The ingestion configuration (`ingestionConfig`) is a section of the [table configuration](table.md) that specifies how to ingest streaming data into Pinot.

## `ingestionConfig`

| Config key | Description |
| --- | --- |
| `streamIngestionConfig` | See the [streamIngestionConfig](ingestion.md#streamingestionconfig) section for details. |
| `batchIngestionConfig` | See the [batchIngestionConfig](ingestion.md#batchingestionconfig) section for details. |
| `continueOnError` | Set to `true` to skip any row indexing error and move on to the next row. Otherwise, an error evaluating a transform or filter function may block ingestion (real-time or offline), and result in data loss or corruption. Consider your use case to determine if it's preferable to set this option to `false`, and fail the ingestion if an error occurs to maintain data integrity. |
| `rowTimeValueCheck` | Set to `true` to validate the time column values ingested during segment upload. Validates each row of data in a segment matches the specified time format, and falls within a valid time range (1971-2071). If the value doesn't meet both criteria, Pinot replaces the value with null. This option ensures that the time values are strictly increasing and that there are no duplicates or gaps in the data. |
| `segmentTimeValueCheck` | Set to `true` to validate the time range of the segment falls between 1971 and 2071. This option ensures data segments stored in the system are correct and consistent. |

## `streamConfigMaps`

| Config key | Description | Supported values |
| --- | --- | --- |
| `streamType` | The streaming platform to ingest data from | `kafka` |
| `stream.[streamType].topic.name` | Topic or data source to ingest data from | String |
| `stream.[streamType].broker.list` | List of brokers |  |
| `stream.[streamType].decoder.class.name` | Name of class to parse the data. The class should implement the `org.apache.pinot.spi.stream.StreamMessageDecoder` interface. | String. Available options: - `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.KafkaAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.csv.CSVMessageDecoder` - `org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder` - `org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder` |
| `stream.[streamType].consumer.factory.class.name` | Name of factory class to provide the appropriate implementation of consumer, as well as the metadata | String. Available options: - `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory` - `org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory` |
| `stream.[streamType].consumer.prop.auto.offset.reset` | Determines the offset from which to start the ingestion | `smallest` , `largest` Period (`10d`, `4h30m`, etc) Timestamp (in format `yyyy-MM-dd'T'HH:mm:ss.SSSZ` eg. `2022-08-09T12:31:38.222Z`) |
| `stream.[streamType].decoder.prop.format` | Specifies the data format to ingest via a stream. The value of this property should match the format of the data in the stream. | - `JSON` |
| `realtime.segment.flush.threshold.time` | Maximum elapsed time after which a consuming segment persist. Note that this time should be smaller than the Kafka retention period configured for the corresponding topic. | String, such `1d` or `4h30m`. Default is `6h` (six hours). |
| `realtime.segment.flush.threshold.rows` | The maximum number of rows to consume before persisting the consuming segment. If this value is set to 0, the configuration looks to `realtime.segment.flush.threshold.segment.size` below. See note below this table for more information. | Default is 5,000,000 |
| `realtime.segment.flush.threshold.segment.rows` | The maximum number of rows to consume before persisting the consuming segment. Added since `release-1.2.0`. See note below this table for more information. | Int |
| `realtime.segment.flush.threshold.segment.size` | Size the completed segments should be. This value is used when `realtime.segment.flush.threshold.rows` is set to 0. | String, such as `150M` or `1.1G`., etc. Default is `200M` (200 megabytes). You can also specify additional configurations for the consumer directly into `streamConfigMaps`. For example, for Kafka streams, add any of the configs described in [Kafka configuration page](https://kafka.apache.org/documentation/#consumerconfigs) to pass them directly to the Kafka consumer. |
| ``realtime.segment.flush.threshold.variance.fraction` `` | For realtime table with many partitions, the consumers have relatively same size which causes all the segments are committed at roughly same time. This causes the segment build time increases and ingestion delay increases more. The variance fraction allowed for the segment size auto tuning | The valid value is [0.0, 0.5), default is 0.0. |
| `realtime.segment.offsetAutoReset.enable` | When `true`, Pinot can skip a lagging realtime partition forward during segment commit instead of starting the next segment at the previous segment's `nextOffset`. Pinot only resets when at least one positive threshold below is configured. | Boolean. Default is `false`. |
| `realtime.segment.offsetAutoReset.offsetThreshold` | If positive, Pinot resets the next segment to the latest stream offset when `latestOffset - nextOffset` exceeds this many offsets at commit time. | Integer. Default is `-1` (disabled). |
| `realtime.segment.offsetAutoReset.timeThresholdSeconds` | If positive, Pinot resets the next segment to the latest stream offset when the next offset is older than this many seconds at commit time. Pinot compares the next offset against the stream position at `now - threshold`. | Long. Default is `-1` (disabled). |

{% hint style="info" %}
The number of rows per segment is computed using the following formula: `realtime.segment.flush.threshold.rows / maxPartitionsConsumedByServer` For example, if you set `realtime.segment.flush.threshold.rows = 1000` and each server consumes 10 partitions, the rows per segment is `1000/10 = 100`.
{% endhint %}

{% hint style="info" %}
Since `release-1.2.0`, we introduced `realtime.segment.flush.threshold.segment.rows`, which is directly used as the number of rows per segment.

Take the above example, if you set `realtime.segment.flush.threshold.segment.rows = 1000` and each server consumes 10 partitions, the rows per segment is `1000`.
{% endhint %}

{% hint style="info" %}
`streamConfigMaps` can contain more than one config map. When you configure multiple entries, Pinot requires all of them to use the same `streamType`, requires the segment-flush parameters to match across all entries, requires topic names to be unique, and rejects the configuration for upsert tables or when `pauselessConsumptionEnabled=true`.
{% endhint %}

{% hint style="info" %}
When offset auto reset is enabled, Pinot checks the configured lag thresholds during segment commit. If either threshold is exceeded, the new consuming segment starts from the latest stream offset instead of the previous segment's `nextOffset`. If both thresholds are unset or non-positive, Pinot keeps the original `nextOffset`.
{% endhint %}

## `streamIngestionConfig`

The `streamIngestionConfig` section contains configuration properties for stream ingestion behavior.

| Config key | Description | Default | Supported values |
| --- | --- | --- | --- |
| `streamConfigMaps` | See the [streamConfigMaps](ingestion.md#streamconfigmaps) section for details. | N/A | Array of config maps |
| `dropRecordOnPartitionMismatch` | Set to `true` to drop records whose partition column value does not map to the segment's designated partition during real-time ingestion. Records with null partition column value will raise an `IllegalStateException`. Pinot emits the `REALTIME_PARTITION_MISMATCH` server meter on every partition mismatch, whether the row is dropped or kept. | `false` | Boolean |

### Example table config with `ingestionConfig`

```json
{
  "tableName": "transcript",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "timestamp",
    "timeType": "MILLISECONDS",
    "replication": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP"
  },
  "ingestionConfig": {
    "streamIngestionConfig": {
      "dropRecordOnPartitionMismatch": false,
      "streamConfigMaps": [{
        "stream.kafka.decoder.prop.format": "JSON",
        "key.serializer": "org.apache.kafka.common.serialization.ByteArraySerializer",
        "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
        "streamType": "kafka",
        "value.serializer": "org.apache.kafka.common.serialization.ByteArraySerializer",
        "stream.kafka.broker.list": "localhost:9876",
        "realtime.segment.flush.threshold.segment.rows": "500000",
        "realtime.segment.flush.threshold.time": "3600000",
        "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
        "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
        "stream.kafka.topic.name": "transcript-topic"
      }]
    },
    "transformConfigs": [],
    "continueOnError": true,
    "rowTimeValueCheck": true,
    "segmentTimeValueCheck": false
  }
}
```

## `batchIngestionConfig`

| Config key | Description | Supported values |
| --- | --- | --- |
| segmentIngestionType | Can be either: - `APPEND` (default): New data segments pushed periodically, to append to the existing data eg. daily or hourly. Time column is mandatory for this push type. - `REFRESH`: Entire data is replaced every time during a data push. Refresh tables have no retention. | `APPEND` or `REFRESH` |
| segmentIngestionFrequency | The cadence at which segments are pushed, such as `HOURLY` or `DAILY` | `HOURLY` or `DAILY` |

### Example table config with `batchIngestionConfig`

```json
{
  "tableName": "transcript",
  "tableType": "OFFLINE",
  "segmentsConfig": {
    "timeColumnName": "timestamp",
    "timeType": "MILLISECONDS",
    "replication": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP"
  },
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "HOURLY"
    }
  }
}
```
