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
| `sourceFieldConfigs` | See the [sourceFieldConfigs](ingestion.md#sourcefieldconfigs) section for details. |
| `continueOnError` | Set to `true` to skip any row indexing error and move on to the next row. Otherwise, an error evaluating a transform or filter function may block ingestion (real-time or offline), and result in data loss or corruption. Consider your use case to determine if it's preferable to set this option to `false`, and fail the ingestion if an error occurs to maintain data integrity. |
| `rowTimeValueCheck` | Set to `true` to validate the time column values ingested during segment upload. Validates each row of data in a segment matches the specified time format, and falls within a valid time range (1971-2071). If the value doesn't meet both criteria, Pinot replaces the value with null. This option ensures that the time values are strictly increasing and that there are no duplicates or gaps in the data. |
| `segmentTimeValueCheck` | Set to `true` to validate the time range of the segment falls between 1971 and 2071. This option ensures data segments stored in the system are correct and consistent. |

## `sourceFieldConfigs`

Use `sourceFieldConfigs` to fix the data type of a source field before later ingestion steps consume it. This is useful when the input record carries a value in a type that a downstream enricher or transform does not expect, such as a timestamp arriving as a `String` when a transform expects a `LONG`.

Pinot applies these conversions with a `DataTypeTransformer` in one of two phases:

- `preComplexTypeTransform: true` runs before the complex-type transformer and before pre-complex-type enrichers. Use this when complex-type flattening or pre-complex-type enrichment needs the corrected type.
- `preComplexTypeTransform: false` runs after the complex-type transformer and before post-complex-type enrichers and expression transforms. This is the default.

Each entry in `sourceFieldConfigs` has the following shape:

| Config key | Description | Required |
| --- | --- | --- |
| `name` | Source field name to convert. The field does not need to be a schema column. | Yes |
| `dataType` | Target Pinot data type name, such as `INT`, `LONG`, `STRING`, or `LONG_ARRAY`. | Yes |
| `preComplexTypeTransform` | Selects whether the conversion runs before or after complex-type transformation. Defaults to `false`. | No |

Pinot validates `sourceFieldConfigs` per phase. The same source field can appear once with `preComplexTypeTransform: true` and once with `preComplexTypeTransform: false`, but it cannot appear twice in the same phase.

### Example

```json
"ingestionConfig": {
  "sourceFieldConfigs": [
    {
      "name": "ts",
      "dataType": "LONG"
    },
    {
      "name": "rawId",
      "dataType": "LONG",
      "preComplexTypeTransform": true
    }
  ],
  "transformConfigs": [
    {
      "columnName": "eventDay",
      "transformFunction": "toEpochDays(ts)"
    }
  ]
}
```

In this example, Pinot converts `ts` to `LONG` before `toEpochDays(ts)` runs. It converts `rawId` to `LONG` even earlier, before complex-type transformation and before any pre-complex-type enricher consumes the field.

## `streamConfigMaps`

| Config key | Description | Supported values |
| --- | --- | --- |
| `streamType` | The streaming platform to ingest data from | `kafka` |
| `stream.[streamType].topic.name` | Topic or data source to ingest data from | String |
| `stream.[streamType].broker.list` | List of brokers |  |
| `stream.[streamType].decoder.class.name` | Name of class to parse the data. The class should implement the `org.apache.pinot.spi.stream.StreamMessageDecoder` interface. | String. Available options: - `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.KafkaAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.csv.CSVMessageDecoder` - `org.apache.pinot.plugin.inputformat.bson.BSONMessageDecoder` - `org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder` - `org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder` |
| `stream.[streamType].consumer.factory.class.name` | Name of factory class to provide the appropriate implementation of consumer, as well as the metadata | String. Available options: - `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory` - `org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory` |
| `stream.[streamType].consumer.prop.auto.offset.reset` | Determines the offset from which to start the ingestion | `smallest` , `largest` Period (`10d`, `4h30m`, etc) Timestamp (in format `yyyy-MM-dd'T'HH:mm:ss.SSSZ` eg. `2022-08-09T12:31:38.222Z`) |
| `stream.[streamType].decoder.prop.format` | Specifies the data format to ingest via a stream. The value of this property should match the format of the data in the stream. | - `JSON` |
| `stream.[streamType].decoder.prop.jsonFormat` | Applies only to `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder`. Selects the JSON stream payload encoding. When unset, the decoder preserves its historical UTF-8 text JSON behavior. `AUTO` is opt-in, and CBOR is auto-detected only when the payload carries the CBOR self-describe tag. | `TEXT`, `POSTGRES_JSONB`, `SQLITE_JSONB`, `SMILE`, `CBOR`, `AUTO` |
| `realtime.segment.flush.threshold.time` | Maximum elapsed time after which a consuming segment persist. Note that this time should be smaller than the Kafka retention period configured for the corresponding topic. | String, such `1d` or `4h30m`. Default is `6h` (six hours). |
| `realtime.segment.flush.threshold.rows` | The maximum number of rows to consume before persisting the consuming segment. If this value is set to 0, the configuration looks to `realtime.segment.flush.threshold.segment.size` below. See note below this table for more information. | Default is 5,000,000 |
| `realtime.segment.flush.threshold.segment.rows` | The maximum number of rows to consume before persisting the consuming segment. Added since `release-1.2.0`. See note below this table for more information. | Int |
| `realtime.segment.flush.threshold.segment.size` | Size the completed segments should be. This value is used when `realtime.segment.flush.threshold.rows` is set to 0. | String, such as `150M` or `1.1G`., etc. Default is `200M` (200 megabytes). You can also specify additional configurations for the consumer directly into `streamConfigMaps`. For example, for Kafka streams, add any of the configs described in [Kafka configuration page](https://kafka.apache.org/documentation/#consumerconfigs) to pass them directly to the Kafka consumer. |
| ``realtime.segment.flush.threshold.variance.fraction` `` | For realtime table with many partitions, the consumers have relatively same size which causes all the segments are committed at roughly same time. This causes the segment build time increases and ingestion delay increases more. The variance fraction allowed for the segment size auto tuning | The valid value is [0.0, 0.5), default is 0.0. |
| `partition.consumption.rate.limit` | Per-partition stream consumption rate limit. Pinot uses this value directly for each consuming partition. When both this key and `topic.consumption.rate.limit` are set, Pinot uses the partition-level limit. Non-positive values disable throttling. | Positive number. Default is `-1` (disabled). |
| `topic.consumption.rate.limit` | Topic-wide stream consumption rate limit. When `partition.consumption.rate.limit` is not set, Pinot divides this value by the current partition count to derive each partition's effective limit. Non-positive values disable throttling. | Positive number. Default is `-1` (disabled). |
| `realtime.segment.offsetAutoReset.enable` | When `true`, Pinot can skip a lagging realtime partition forward during segment commit instead of starting the next segment at the previous segment's `nextOffset`. Pinot only resets when at least one positive threshold below is configured. | Boolean. Default is `false`. |
| `realtime.segment.offsetAutoReset.offsetThreshold` | If positive, Pinot resets the next segment to the latest stream offset when `latestOffset - nextOffset` exceeds this many offsets at commit time. | Integer. Default is `-1` (disabled). |
| `realtime.segment.offsetAutoReset.timeThresholdSeconds` | If positive, Pinot resets the next segment to the latest stream offset when the next offset is older than this many seconds at commit time. Pinot compares the next offset against the stream position at `now - threshold`. | Long. Default is `-1` (disabled). |
| `stopOnDecodeError` | When set to `true`, consumption stops with an error if a decode error occurs. When set to `false` (default), decode errors are logged and the problematic row is silently dropped. | Boolean. Default is `false`. |

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

{% hint style="info" %}
For BSON streams, set `stream.[streamType].decoder.class.name` to `org.apache.pinot.plugin.inputformat.bson.BSONMessageDecoder`. Each stream message must contain a single BSON document; BSON does not use `stream.[streamType].decoder.prop.format`.
{% endhint %}

{% hint style="info" %}
`stream.[streamType].decoder.prop.jsonFormat` is a stream-only setting. Batch ingestion with `org.apache.pinot.plugin.inputformat.json.JSONRecordReader` still reads text JSON files.
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
