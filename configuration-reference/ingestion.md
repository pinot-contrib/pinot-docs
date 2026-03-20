# Ingestion

The ingestion configuration ('ingestionConfig') is a section of the [table configuration](table.md) that specifies how to ingest streaming data into Pinot.

## `ingestionConfig`

<table><thead><tr><th width="231">Config key</th><th>Description</th></tr></thead><tbody><tr><td><code>streamConfigMaps</code></td><td>See the <a href="ingestion.md#streamconfigmaps">streamConfigMaps</a> section for details.</td></tr><tr><td><code>batchIngestionConfig</code></td><td>See the <a href="ingestion.md#batchingestionconfig">batchIngestionConfig</a> section for details.</td></tr><tr><td><code>continueOnError</code></td><td>Set to <code>true</code> to skip any row indexing error and move on to the next row. Otherwise, an error evaluating a transform or filter function may block ingestion (real-time or offline), and result in data loss or corruption. Consider your use case to determine if it's preferable to set this option to <code>false</code>, and fail the ingestion if an error occurs to maintain data integrity.</td></tr><tr><td><code>rowTimeValueCheck</code></td><td>Set to <code>true</code> to validate the time column values ingested during segment upload. Validates each row of data in a segment matches the specified time format, and falls within a valid time range (1971-2071). If the value doesn't meet both criteria, Pinot replaces the value with null. This option ensures that the time values are strictly increasing and that there are no duplicates or gaps in the data.</td></tr><tr><td><code>segmentTimeValueCheck</code></td><td>Set to <code>true</code> to validate the time range of the segment falls between 1971 and 2071. This option ensures data segments stored in the system are correct and consistent.</td></tr></tbody></table>

## `streamConfigMaps`

<table><thead><tr><th>Config key</th><th>Description</th><th>Supported values</th></tr></thead><tbody><tr><td><code>streamType</code></td><td>The streaming platform to ingest data from</td><td><code>kafka</code></td></tr><tr><td><code>stream.[streamType].topic.name</code></td><td>Topic or data source to ingest data from</td><td>String</td></tr><tr><td><code>stream.[streamType].broker.list</code></td><td>List of brokers</td><td></td></tr><tr><td><code>stream.[streamType].decoder.class.name</code></td><td>Name of class to parse the data. The class should implement the <code>org.apache.pinot.spi.stream.StreamMessageDecoder</code> interface.</td><td>String. Available options: - <code>org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder</code> - <code>org.apache.pinot.plugin.inputformat.avro.KafkaAvroMessageDecoder</code> - <code>org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder</code> - <code>org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder</code> - <code>org.apache.pinot.plugin.inputformat.csv.CSVMessageDecoder</code> - <code>org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder</code> - <code>org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder</code></td></tr><tr><td><code>stream.[streamType].consumer.factory.class.name</code></td><td>Name of factory class to provide the appropriate implementation of consumer, as well as the metadata</td><td>String. Available options: - <code>org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory</code> - <code>org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory</code> - <code>org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory</code> - <code>org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory</code></td></tr><tr><td><code>stream.[streamType].consumer.prop.auto.offset.reset</code></td><td>Determines the offset from which to start the ingestion</td><td><code>smallest</code> , <code>largest</code> <br>Period (<code>10d</code>, <code>4h30m</code>, etc)<br>Timestamp (in format <code>yyyy-MM-dd'T'HH:mm:ss.SSSZ</code> eg. <code>2022-08-09T12:31:38.222Z</code>)</td></tr><tr><td><code>stream.[streamType].decoder.prop.format</code></td><td>Specifies the data format to ingest via a stream. The value of this property should match the format of the data in the stream.</td><td>- <code>JSON</code></td></tr><tr><td><code>realtime.segment.flush.threshold.time</code></td><td>Maximum elapsed time after which a consuming segment persist. Note that this time should be smaller than the Kafka retention period configured for the corresponding topic.</td><td>String, such <code>1d</code> or <code>4h30m</code>. Default is <code>6h</code> (six hours).</td></tr><tr><td><code>realtime.segment.flush.threshold.rows</code></td><td>The maximum number of rows to consume before persisting the consuming segment. If this value is set to 0, the configuration looks to <code>realtime.segment.flush.threshold.segment.size</code> below. See note below this table for more information.</td><td>Default is 5,000,000</td></tr><tr><td><code>realtime.segment.flush.threshold.segment.rows</code></td><td>The maximum number of rows to consume before persisting the consuming segment. Added since <code>release-1.2.0</code>. See note below this table for more information.</td><td>Int</td></tr><tr><td><code>realtime.segment.flush.threshold.segment.size</code></td><td>Size the completed segments should be. This value is used when <code>realtime.segment.flush.threshold.rows</code> is set to 0.</td><td>String, such as <code>150M</code> or <code>1.1G</code>., etc. Default is <code>200M</code> (200 megabytes). You can also specify additional configurations for the consumer directly into <code>streamConfigMaps</code>. For example, for Kafka streams, add any of the configs described in <a href="https://kafka.apache.org/documentation/#consumerconfigs">Kafka configuration page</a> to pass them directly to the Kafka consumer.</td></tr><tr><td><pre><code>realtime.segment.flush.threshold.variance.fraction`
</code></pre></td><td><p></p><p>For realtime table with many partitions, the consumers have relatively same size which causes all the segments are committed at roughly same time. This causes the segment build time increases and ingestion delay increases more.</p><p></p><p>The variance fraction allowed for the segment size auto tuning</p></td><td>The valid value is [0.0, 0.5), default is 0.0.</td></tr></tbody></table>



{% hint style="info" %}
The number of rows per segment is computed using the following formula: `realtime.segment.flush.threshold.rows / maxPartitionsConsumedByServer` For example, if you set `realtime.segment.flush.threshold.rows = 1000` and each server consumes 10 partitions, the rows per segment is `1000/10 = 100`.
{% endhint %}

{% hint style="info" %}
Since `release-1.2.0`, we introduced `realtime.segment.flush.threshold.segment.rows`, which is directly used as the number of rows per segment.

Take the above example, if you set `realtime.segment.flush.threshold.segment.rows = 1000` and each server consumes 10 partitions, the rows per segment is `1000`.
{% endhint %}

{% hint style="info" %}
Since [this PR](https://github.com/apache/pinot/pull/13790), `streamConfigMaps` could contain multiple maps pointing to multiple Kafka topics. This would allow creating one single Pinot table with data from multiple stream topics.
{% endhint %}

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
    "loadMode": "MMAP",
  },
  "ingestionConfig": {
    "streamIngestionConfig": {
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

<table><thead><tr><th width="256">Config key</th><th>Description</th><th>Supported values</th></tr></thead><tbody><tr><td>segmentIngestionType<br></td><td><p>Can be either:</p><ul><li><code>APPEND</code> (default): New data segments pushed periodically, to append to the existing data eg. daily or hourly. Time column is mandatory for this push type.</li><li><code>REFRESH</code>: Entire data is replaced every time during a data push. Refresh tables have no retention.</li></ul></td><td><code>APPEND</code> or <code>REFRESH</code></td></tr><tr><td>segmentIngestionFrequency<br></td><td>The cadence at which segments are pushed, such as <code>HOURLY</code> or <code>DAILY</code><br></td><td><code>HOURLY</code> or <code>DAILY</code></td></tr></tbody></table>

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
    "loadMode": "MMAP",
  },
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "HOURLY"
    }
  }
}
```
