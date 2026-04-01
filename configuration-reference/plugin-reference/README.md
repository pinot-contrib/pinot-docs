---
description: >-
  Configuration and usage reference for every plugin family in Apache Pinot.
---

# Plugin Reference

Apache Pinot has a plug-and-play architecture organized into **ten plugin families**. Each family targets a specific extensibility need — from reading data in different formats to exporting metrics to your monitoring stack.

This section covers the **configuration** side of each plugin family: which implementations ship with Pinot, what config keys they accept, and how to enable them. If you want to **write your own plugin**, see the [Plugin Architecture](../../developers/plugin-architecture/README.md) section in the Developer Guide.

## Plugin Families at a Glance

<table>
  <thead>
    <tr>
      <th>Plugin Family</th>
      <th>What It Does</th>
      <th>Config Reference</th>
      <th>Authoring Guide</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Stream Ingestion**</td>
      <td>Consume data from real-time streaming platforms (Kafka, Kinesis, Pulsar)</td>
      <td>[Stream Ingestion Connectors](stream-ingestion-connectors.md) · [Version Matrix](stream-connector-matrix.md)</td>
      <td>[Stream Ingestion Plugin](../../developers/plugin-architecture/write-custom-plugins/write-your-stream.md)</td>
    </tr>
    <tr>
      <td>**Input Format**</td>
      <td>Read records from files or streams during ingestion (Avro, JSON, Parquet, ORC, CSV, …)</td>
      <td>[Input Formats](../../manage-data/data-import/pinot-input-formats.md)</td>
      <td>[Input Format Plugin](../../developers/plugin-architecture/write-custom-plugins/record-reader.md)</td>
    </tr>
    <tr>
      <td>**Filesystem**</td>
      <td>Store and fetch segments from pluggable storage backends (S3, GCS, HDFS, ADLS)</td>
      <td>[Filesystem Plugins](../../manage-data/data-import/pinot-file-system/)</td>
      <td>[Filesystem Plugin](../../developers/plugin-architecture/write-custom-plugins/pluggable-storage.md)</td>
    </tr>
    <tr>
      <td>**Batch Ingestion**</td>
      <td>Run data ingestion jobs on different execution frameworks (Standalone, Hadoop, Spark)</td>
      <td>[Batch Ingestion](../../manage-data/data-import/batch-ingestion/)</td>
      <td>—</td>
    </tr>
    <tr>
      <td>**Metrics**</td>
      <td>Collect and expose internal JMX metrics via Dropwizard, Yammer, or a compound backend</td>
      <td>[Metrics Plugins](metrics-plugins.md)</td>
      <td>[Metrics Plugin](../../developers/plugin-architecture/write-custom-plugins/metrics-plugin.md)</td>
    </tr>
    <tr>
      <td>**Segment Writer**</td>
      <td>Programmatically build Pinot segments without a full batch ingestion job</td>
      <td>—</td>
      <td>[Segment Writer Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-writer-plugin.md)</td>
    </tr>
    <tr>
      <td>**Segment Uploader**</td>
      <td>Upload completed segment tar files to the Pinot cluster</td>
      <td>—</td>
      <td>[Segment Uploader Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-uploader-plugin.md)</td>
    </tr>
    <tr>
      <td>**Minion Tasks**</td>
      <td>Run background processing tasks on Pinot Minion nodes (merge, purge, compaction, …)</td>
      <td>[Minion](../../basics/components/cluster/minion.md) · [Merge/Rollup Task](../../operators/operating-pinot/minion-merge-rollup-task.md)</td>
      <td>[Minion Task Plugin](../../developers/plugin-architecture/write-custom-plugins/minion-task-plugin.md)</td>
    </tr>
    <tr>
      <td>**Environment**</td>
      <td>Discover cloud-specific instance metadata for failure-domain–aware placement</td>
      <td>[Environment Provider](environment-provider.md)</td>
      <td>—</td>
    </tr>
    <tr>
      <td>**Time Series Language**</td>
      <td>Support custom time series query languages (M3QL, PromQL)</td>
      <td>—</td>
      <td>[Time Series Language Plugin](../../developers/plugin-architecture/write-custom-plugins/time-series-language-plugin.md)</td>
    </tr>
  </tbody>
</table>

---

## Stream Ingestion Connectors

Pinot ships connectors for Apache Kafka (3.x and 4.x), Amazon Kinesis, and Apache Pulsar. Each connector supplies a `StreamConsumerFactory` implementation.

{% content-ref url="stream-ingestion-connectors.md" %}
[stream-ingestion-connectors.md](stream-ingestion-connectors.md)
{% endcontent-ref %}

{% content-ref url="stream-connector-matrix.md" %}
[stream-connector-matrix.md](stream-connector-matrix.md)
{% endcontent-ref %}

## Input Format

Input format plugins read data from files or streams during ingestion. Batch ingestion uses `RecordReader` implementations; real-time ingestion uses `StreamMessageDecoder` implementations. Pinot ships with readers for Avro, CSV, JSON, ORC, Parquet, Thrift, Protobuf, Arrow, CLP-Log, and Confluent Schema Registry variants.

{% content-ref url="../../manage-data/data-import/pinot-input-formats.md" %}
[pinot-input-formats.md](../../manage-data/data-import/pinot-input-formats.md)
{% endcontent-ref %}

## Filesystem

Filesystem plugins provide a `PinotFS` storage abstraction so that segments can live on different backends — S3, GCS, HDFS, or ADLS.

{% content-ref url="../../manage-data/data-import/pinot-file-system/" %}
[pinot-file-system](../../manage-data/data-import/pinot-file-system/)
{% endcontent-ref %}

## Batch Ingestion

Batch ingestion plugins run ingestion jobs on different execution frameworks: Standalone, Hadoop, and Spark 3.

{% content-ref url="../../manage-data/data-import/batch-ingestion/" %}
[batch-ingestion](../../manage-data/data-import/batch-ingestion/)
{% endcontent-ref %}

## Metrics

Metrics plugins control which metrics library Pinot uses for internal JMX metrics. Pinot ships with Yammer (default), Dropwizard, and a Compound implementation that fans out to multiple registries.

{% content-ref url="metrics-plugins.md" %}
[metrics-plugins.md](metrics-plugins.md)
{% endcontent-ref %}

## Segment Writer

The Segment Writer plugin provides an API for programmatically collecting `GenericRow` records and building Pinot segments without going through a full batch ingestion job. The built-in file-based implementation buffers rows as Avro records on local disk.

{% content-ref url="../../developers/plugin-architecture/write-custom-plugins/segment-writer-plugin.md" %}
[segment-writer-plugin.md](../../developers/plugin-architecture/write-custom-plugins/segment-writer-plugin.md)
{% endcontent-ref %}

## Segment Uploader

The Segment Uploader plugin handles uploading completed segment tar files to the Pinot cluster. The default implementation supports all push modes configured via `batchConfigMaps` in the table config.

{% content-ref url="../../developers/plugin-architecture/write-custom-plugins/segment-uploader-plugin.md" %}
[segment-uploader-plugin.md](../../developers/plugin-architecture/write-custom-plugins/segment-uploader-plugin.md)
{% endcontent-ref %}

## Minion Tasks

Minion task plugins define background processing tasks that run on Pinot Minion nodes. Built-in tasks include MergeRollup, Purge, RealtimeToOfflineSegments, SegmentGenerationAndPush, UpsertCompaction, UpsertCompactMerge, and RefreshSegment.

{% content-ref url="../../basics/components/cluster/minion.md" %}
[minion.md](../../basics/components/cluster/minion.md)
{% endcontent-ref %}

{% content-ref url="../../operators/operating-pinot/minion-merge-rollup-task.md" %}
[minion-merge-rollup-task.md](../../operators/operating-pinot/minion-merge-rollup-task.md)
{% endcontent-ref %}

## Environment Provider

Environment plugins allow Pinot to discover cloud-specific instance metadata at startup for failure-domain–aware data placement. The Azure provider is the only built-in implementation.

{% content-ref url="environment-provider.md" %}
[environment-provider.md](environment-provider.md)
{% endcontent-ref %}

## Time Series Language

Time series language plugins let Pinot support custom time series query languages like M3QL and PromQL.

{% content-ref url="../../developers/plugin-architecture/write-custom-plugins/time-series-language-plugin.md" %}
[time-series-language-plugin.md](../../developers/plugin-architecture/write-custom-plugins/time-series-language-plugin.md)
{% endcontent-ref %}

---

## Developing Custom Plugins

Plugins implement interfaces from [pinot-spi](https://github.com/apache/pinot/tree/master/pinot-spi/src/main/java/org/apache/pinot/spi). See the developer guide for the full plugin authoring workflow:

{% content-ref url="../../developers/plugin-architecture/write-custom-plugins/" %}
[write-custom-plugins](../../developers/plugin-architecture/write-custom-plugins/)
{% endcontent-ref %}

## Legacy compatibility pages

- [STDDEV_POP](stddev_pop.md)
- [STDDEV_SAMP](stddev_samp.md)
- [VAR_POP](var_pop.md)
- [VAR_SAMP](var_samp.md)
