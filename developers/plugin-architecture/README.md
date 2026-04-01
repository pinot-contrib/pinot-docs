# Plugins

Starting from the 0.3.X release, Pinot supports a plug-and-play architecture. This means that starting from version 0.3.0, Pinot can be easily extended to support new tools, like streaming services, storage systems, input formats, and metrics providers.

![](<../../.gitbook/assets/Pinot Dependency Graph.svg>)

Plugins are collected in folders, based on their purpose. Pinot organizes its plugins into **eleven plugin families**, each targeting a specific extensibility need. The table below summarizes every family, its SPI module, and the implementations that ship with Pinot.

## Plugin Families at a Glance

<table>
  <thead>
    <tr>
      <th>Plugin Family</th>
      <th>SPI Interface / Module</th>
      <th>Built-in Implementations</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Input Format**</td>
      <td>`RecordReader` / `StreamMessageDecoder`</td>
      <td>Avro, CSV, JSON, ORC, Parquet, Thrift, Protobuf, Arrow, CLP-Log, Confluent Avro, Confluent JSON, Confluent Protobuf</td>
    </tr>
    <tr>
      <td>**Filesystem**</td>
      <td>`PinotFS`</td>
      <td>S3, GCS, HDFS, ADLS</td>
    </tr>
    <tr>
      <td>**Stream Ingestion**</td>
      <td>`StreamConsumerFactory`</td>
      <td>Kafka 3.0, Kafka 4.0, Kinesis, Pulsar</td>
    </tr>
    <tr>
      <td>**Batch Ingestion**</td>
      <td>`IngestionJobRunner`</td>
      <td>Standalone, Hadoop, Spark 3</td>
    </tr>
    <tr>
      <td>**Metrics**</td>
      <td>`PinotMetricsFactory`</td>
      <td>Dropwizard, Yammer, Compound</td>
    </tr>
    <tr>
      <td>**Segment Writer**</td>
      <td>`SegmentWriter`</td>
      <td>File-based</td>
    </tr>
    <tr>
      <td>**Segment Uploader**</td>
      <td>`SegmentUploader`</td>
      <td>Default</td>
    </tr>
    <tr>
      <td>**Minion Tasks**</td>
      <td>`PinotTaskGenerator` / `PinotTaskExecutor`</td>
      <td>MergeRollup, Purge, RealtimeToOfflineSegments, SegmentGenerationAndPush, UpsertCompaction, UpsertCompactMerge, RefreshSegment</td>
    </tr>
    <tr>
      <td>**Environment**</td>
      <td>`PinotEnv`</td>
      <td>Azure</td>
    </tr>
    <tr>
      <td>**Time Series Language**</td>
      <td>`TimeSeriesLogicalPlanner`</td>
      <td>M3QL</td>
    </tr>
    <tr>
      <td>**OpChain Converter**</td>
      <td>`OpChainConverter`</td>
      <td>Default</td>
    </tr>
  </tbody>
</table>

---

### Input Format

Input format plugins read data from files or streams during data ingestion. Batch ingestion uses `RecordReader` implementations, while real-time ingestion uses `StreamMessageDecoder` implementations.

{% content-ref url="../../manage-data/data-import/pinot-input-formats.md" %}
[pinot-input-formats.md](../../manage-data/data-import/pinot-input-formats.md)
{% endcontent-ref %}

### Filesystem

Filesystem plugins provide a storage abstraction layer so that Pinot segments can be stored on and fetched from different storage backends.

{% content-ref url="../../manage-data/data-import/pinot-file-system/" %}
[pinot-file-system](../../manage-data/data-import/pinot-file-system/)
{% endcontent-ref %}

### Stream Ingestion

Stream ingestion plugins allow Pinot to consume data from real-time streaming platforms.

{% content-ref url="../../manage-data/data-import/pinot-stream-ingestion/" %}
[pinot-stream-ingestion](../../manage-data/data-import/pinot-stream-ingestion/)
{% endcontent-ref %}

### Batch Ingestion

Batch ingestion plugins run data ingestion jobs on different execution frameworks.

{% content-ref url="../../manage-data/data-import/batch-ingestion/" %}
[batch-ingestion](../../manage-data/data-import/batch-ingestion/)
{% endcontent-ref %}

### Metrics

Metrics plugins control which metrics library Pinot uses to collect and expose internal metrics via JMX. Pinot ships with Dropwizard (default), Yammer, and a Compound implementation that can fan out to multiple registries simultaneously.

{% content-ref url="write-custom-plugins/metrics-plugin.md" %}
[metrics-plugin.md](write-custom-plugins/metrics-plugin.md)
{% endcontent-ref %}

### Segment Writer

The Segment Writer plugin provides an API for programmatically collecting `GenericRow` records and building Pinot segments without going through a full batch ingestion job. The built-in file-based implementation buffers rows as Avro records on local disk.

{% content-ref url="write-custom-plugins/segment-writer-plugin.md" %}
[segment-writer-plugin.md](write-custom-plugins/segment-writer-plugin.md)
{% endcontent-ref %}

### Segment Uploader

The Segment Uploader plugin handles uploading completed segment tar files to the Pinot cluster. The default implementation supports all push modes configured via `batchConfigMaps` in the table config.

{% content-ref url="write-custom-plugins/segment-uploader-plugin.md" %}
[segment-uploader-plugin.md](write-custom-plugins/segment-uploader-plugin.md)
{% endcontent-ref %}

### Minion Tasks

Minion task plugins define background processing tasks that run on Pinot Minion nodes. Built-in tasks include segment merge/rollup, purge, real-time to offline conversion, upsert compaction, and more.

{% content-ref url="../../basics/components/cluster/minion.md" %}
[minion.md](../../basics/components/cluster/minion.md)
{% endcontent-ref %}

### Environment

Environment plugins allow Pinot to integrate with cloud-specific features and configurations. The Azure environment plugin provides Azure-specific functionality.

### Time Series Language

Time series language plugins allow Pinot to support custom time series query languages like PromQL or M3QL.

{% content-ref url="write-custom-plugins/time-series-language-plugin.md" %}
[time-series-language-plugin.md](write-custom-plugins/time-series-language-plugin.md)
{% endcontent-ref %}

### OpChain Converter

OpChain Converter plugins provide custom implementations for converting logical query plans into executable OpChain objects in the multi-stage query engine. This enables alternative execution backends and plan-to-execution strategies.

{% content-ref url="write-custom-plugins/opchain-converter-plugin.md" %}
[opchain-converter-plugin.md](write-custom-plugins/opchain-converter-plugin.md)
{% endcontent-ref %}

---

## Developing Plugins

Plugins can be developed with no restriction. There are some standards that have to be followed, though. The plugin has to implement the interfaces from [pinot-spi](https://github.com/apache/pinot/tree/master/pinot-spi/src/main/java/org/apache/pinot/spi).

{% content-ref url="write-custom-plugins/" %}
[write-custom-plugins](write-custom-plugins/)
{% endcontent-ref %}
