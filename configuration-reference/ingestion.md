# Ingestion

The ingestion configuration ('ingestionConfig') is a section of the [table configuration](table.md) that specifies how to ingest streaming data into Pinot.

## `ingestionConfig`

<table data-header-hidden><thead><tr><th width="231"></th><th></th></tr></thead><tbody><tr><td><strong>Config key</strong></td><td><strong>Description</strong></td></tr><tr><td><code>streamConfigMaps</code> </td><td>See the <a href="ingestion.md#streamconfigmaps">streamConfigMaps</a> section for details. </td></tr><tr><td><code>continueOnError</code></td><td>Set to <code>true</code> to skip any row indexing error and move on to the next row. Otherwise, an error evaluating a transform or filter function may block ingestion (real-time or offline), and result in data loss or corruption. Consider your use case to determine if it's preferable to set this option to <code>false</code>, and fail the ingestion if an error occurs to maintain data integrity.</td></tr><tr><td><code>rowTimeValueCheck</code></td><td>Set to <code>true</code> to validate the time column values ingested during segment upload. Validates each row of data in a segment matches the specified time format, and falls within a valid time range (1971-2071). If the value doesn't meet both criteria, Pinot replaces the value with null. This option ensures that the time values are strictly increasing and that there are no duplicates or gaps in the data.</td></tr><tr><td><code>segmentTimeValueCheck</code></td><td>Set to <code>true</code> to validate the time range of the segment falls between 1971 and 2071. This option ensures data segments stored in the system are correct and consistent.</td></tr></tbody></table>

## `streamConfigMaps`

| **Config key**                                        | **Description**                                                                                                                                                                                                                             | **Supported values**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `streamType`                                          | The streaming platform to ingest data from                                                                                                                                                                                                  | `kafka`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `stream.[streamType].consumer.type`                   | Whether to use per partition low-level consumer or high-level stream consumer                                                                                                                                                               | <p>- <code>lowLevel</code>: Consume data from each partition with offset management. </p><p>- <code>highLevel</code>: Consume data without control over the partitions.</p>                                                                                                                                                                                                                                                                                                                                                                                                           |
| `stream.[streamType].topic.name`                      | Topic or data source to ingest data from                                                                                                                                                                                                    | String                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `stream.[streamType].broker.list`                     | List of brokers                                                                                                                                                                                                                             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `stream.[streamType].decoder.class.name`              | Name of class to parse the data. The class should implement the `org.apache.pinot.spi.stream.StreamMessageDecoder` interface.                                                                                                               | String. Available options: - `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.KafkaAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` - `org.apache.pinot.plugin.inputformat.csv.CSVMessageDecoder` - `org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder` - `org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder` |
| `stream.[streamType].consumer.factory.class.name`     | Name of factory class to provide the appropriate implementation of low-level and high-level consumer, as well as the metadata                                                                                                               | String. Available options: - `org.apache.pinot.plugin.stream.kafka09.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory` - `org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory` - `org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory`                                                                                                                                                                                                                                                                                          |
| `stream.[streamType].consumer.prop.auto.offset.reset` | Determines the offset from which to start the ingestion                                                                                                                                                                                     | - `smallest` - `largest` - timestamp in milliseconds                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `stream.[streamType].decoder.prop.format`             | Specifies the data format to ingest via a stream. The value of this property should match the format of the data in the stream.                                                                                                             | - `JSON`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `realtime.segment.flush.threshold.time`               | Maximum elapsed time after which a consuming segment persist. Note that this time should be smaller than the Kafka retention period configured for the corresponding topic.                                                                 | String, such `1d` or `4h30m`. Default is `6h` (six hours).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `realtime.segment.flush.threshold.rows`               | The maximum number of rows to consume before persisting the consuming segment. If this value is set to 0, the configuration looks to `realtime.segment.flush.threshold.segment.size` below. See note below this table for more information. | Default is 5,000,000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `realtime.segment.flush.threshold.segment.size`       | Size the completed segments should be. This value is used when `realtime.segment.flush.threshold.rows` is set to 0.                                                                                                                         | String, such as `150M` or `1.1G`., etc. Default is `200M` (200 megabytes). You can also specify additional configurations for the consumer directly into `streamConfigMaps`. For example, for Kafka streams, add any of the configs described in [Kafka configuration page](https://kafka.apache.org/documentation/#consumerconfigs) to pass them directly to the Kafka consumer.                                                                                                                                                                                                     |

{% hint style="info" %}
The number of rows per segment is computed using the following formula: `realtime.segment.flush.threshold.rows /partitionsConsumedByServer` For example, if you set `realtime.segment.flush.threshold.rows=1000` and each server consumes 10 partitions, the rows per segment is `1000/10 = 100`.
{% endhint %}

### Example table config with `ingestionConfig`

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
