---
description: Configuration reference entry point for Pinot plugins.
---

# Plugin Configuration Reference

This page keeps the plugin-family overview and the detailed configuration sections on a single page.

Apache Pinot has a plug-and-play architecture organized into ten plugin families. Each family targets a specific extensibility need, from reading data in different formats to exporting metrics to your monitoring stack.

This section covers the configuration side of each plugin family: which implementations ship with Pinot, what config keys they accept, and how to enable them. If you want to write your own plugin, see the [Plugin Architecture](../../developers/plugin-architecture/README.md) section in the Developer Guide.

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
      <td>[Stream Ingestion Connectors](#stream-ingestion-connectors) / [Version Matrix](#stream-connector-version-matrix)</td>
      <td>[Stream Ingestion Plugin](../../developers/plugin-architecture/write-custom-plugins/write-your-stream.md)</td>
    </tr>
    <tr>
      <td>**Input Format**</td>
      <td>Read records from files or streams during ingestion (Avro, JSON, Parquet, ORC, CSV, ...)</td>
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
      <td>-</td>
    </tr>
    <tr>
      <td>**Metrics**</td>
      <td>Collect and expose internal JMX metrics via Dropwizard, Yammer, or a compound backend</td>
      <td>[Metrics Plugins](#metrics-plugins)</td>
      <td>[Metrics Plugin](../../developers/plugin-architecture/write-custom-plugins/metrics-plugin.md)</td>
    </tr>
    <tr>
      <td>**Segment Writer**</td>
      <td>Programmatically build Pinot segments without a full batch ingestion job</td>
      <td>-</td>
      <td>[Segment Writer Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-writer-plugin.md)</td>
    </tr>
    <tr>
      <td>**Segment Uploader**</td>
      <td>Upload completed segment tar files to the Pinot cluster</td>
      <td>-</td>
      <td>[Segment Uploader Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-uploader-plugin.md)</td>
    </tr>
    <tr>
      <td>**Minion Tasks**</td>
      <td>Run background processing tasks on Pinot Minion nodes (merge, purge, compaction, ...)</td>
      <td>[Minion](../../basics/components/cluster/minion.md) / [Merge/Rollup Task](../../operators/operating-pinot/minion-merge-rollup-task.md)</td>
      <td>[Minion Task Plugin](../../developers/plugin-architecture/write-custom-plugins/minion-task-plugin.md)</td>
    </tr>
    <tr>
      <td>**Environment**</td>
      <td>Discover cloud-specific instance metadata for failure-domain-aware placement</td>
      <td>[Environment Provider](#environment-provider-plugins)</td>
      <td>-</td>
    </tr>
    <tr>
      <td>**Time Series Language**</td>
      <td>Support custom time series query languages (M3QL, PromQL)</td>
      <td>-</td>
      <td>[Time Series Language Plugin](../../developers/plugin-architecture/write-custom-plugins/time-series-language-plugin.md)</td>
    </tr>
  </tbody>
</table>

## Stream Ingestion Connectors

### Applicable to all stream connectors

<table><thead><tr><th width="281">Configuration</th><th>Description</th></tr></thead><tbody><tr><td>stream.&#x3C;stream_type>.consumer.factory.class.name</td><td>Factory class to be used for the stream consumer</td></tr><tr><td>stream.&#x3C;stream_type>.consumer.prop.auto.offset.reset</td><td>Offset or position in the source stream from which to start consuming data<br><strong>Valid values:</strong> <br><strong><code>smallest</code></strong> - Start consuming from the earliest data in the stream<br><strong><code>largest</code></strong> - Start consuming from the latest data in the stream<br><strong><code>timestamp</code></strong> - Start consuming from the offset after a timestamp , which is specified in the format <code>yyyy-MM-dd'T'HH:mm:ss.SSSZ</code><br><strong><code>datetime</code> -</strong> Start consuming from the offset after the specified period or duration from current time. Eg: <code>2d</code> <br><strong>Default Value:</strong> <code>largest</code> </td></tr><tr><td>stream.&#x3C;stream_type>.topic.name</td><td>Name of the source stream to consume </td></tr><tr><td>stream.&#x3C;stream_type>.fetch.timeout.millis</td><td>Indicates the timeout (in milliseconds) to use for each fetch call to the consumer. If the timeout expires before data becomes available, the consumer will return an empty batch.<br><strong>Default Value:</strong> <code>5_000</code></td></tr><tr><td>stream.&#x3C;stream_type>.connection.timeout.millis</td><td>Indicates the timeout (in milliseconds) used to create the connection to the upstream (Timeout for the initial connection to the upstream)<br><strong>Default Value:</strong> <code>30_000</code></td></tr><tr><td>stream.&#x3C;stream_type>.idle.timeout.millis</td><td>If the stream remains idle (ie. without any data) for the specified time, the client connection is reset and a new consumer instance is created.  <br><strong>Default Value:</strong> <code>180_000</code></td></tr><tr><td>stream.&#x3C;stream_type>.decoder.class.name</td><td>Indicates the name of the decoder class that should be used to decoder the stream payload</td></tr><tr><td>stream.&#x3C;stream_type>.decoder.prop</td><td>Prefix used for any decoder specific property </td></tr><tr><td>topic.consumption.rate.limit</td><td>Indicates the upper bound on the message rate for the entire topic. Use <code>-1</code> to ignore this config. <br><strong>Default Value:</strong> <code>-1</code><br>See <a href="../../manage-data/data-import/pinot-stream-ingestion/README.md">Stream Ingestion</a> for more details.</td></tr><tr><td>stream.&#x3C;stream_type>.metadata.populate</td><td>When set to <code>true</code>, the supported consumer may extract the key, user headers and record metadata from the incoming payload. <br>Currently, this is supported in Kafka connector only.</td></tr><tr><td>realtime.segment.flush.threshold.time</td><td>Time based flush threshold for realtime segments. Used to decides when a realtime segment is ready to be committed / closed / flushed to disk.<br><br>Warning: This time should be smaller than the retention period configured for the corresponding topic</td></tr><tr><td>realtime.segment.flush.threshold.size</td><td>The size a completed realtime segment should be. <br><br>Note: This config is used only if <code>realtime.segment.flush.threshold.rows</code> is set to 0.</td></tr><tr><td>realtime.segment.flush.threshold.rows</td><td><p>Row count based flush threshold for realtime segments. <p>If this value is set to 0, then the consumers adjust the number of rows consumed by a partition so the completed segment is the correct size (unless</p><p>threshold.time is reached first)</p></td></tr><tr><td>realtime.segment.flush.autotune.initialRows</td><td>Initial number of rows to use for <code>SegmentSizeBasedFlushThresholdUpdater</code> . This threshold updater is used by the controller to compute the new segment's flush threshold based on the previous segment's size. <br>Warning: This flush threshold updater is used only when <code>realtime.segment.flush.threshold.rows</code> is set to <code>&#x3C;=0</code> . Otherwise, the <code>DefaultFlushThresholdUpdater</code> is used. </td></tr><tr><td>realtime.segment.commit.timeoutSeconds</td><td>Time threshold that controller will wait for the segment to be built by the server</td></tr></tbody></table>

### Kafka 3.x / 4.x

Pinot ships two Kafka connector modules: `pinot-kafka-3.0` (Kafka client 3.9.2, default) and `pinot-kafka-4.0` (Kafka client 4.1.1, for KRaft-mode clusters). The legacy `kafka-0.9` and `kafka-2.x` modules have been removed.

<table><thead><tr><th width="285">Config</th><th>Description</th></tr></thead><tbody><tr><td>stream.kafka.consumer.factory.class.name</td><td><strong>Allowed Values:</strong><br>- <code>org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory</code> (Kafka 3.x, default)<br>- <code>org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory</code> (Kafka 4.x)</td></tr><tr><td>stream.kafka.topic.name</td><td>(Required) Name of the kafka topic to be ingested</td></tr><tr><td>stream.kafka.broker.list</td><td>(Required) Connection string for the kafka broker</td></tr><tr><td>stream.kafka.partition.ids</td><td>Optional comma-separated list of Kafka partition IDs to consume (e.g. <code>"0,2,5"</code>). When set, only the specified partitions are consumed by this table. When absent or blank, all topic partitions are consumed (the default behavior).<br><br>Partition IDs must be non-negative integers. Duplicates are silently removed. The IDs are validated against the actual topic metadata at table creation time.<br><br>See <a href="../../manage-data/data-import/pinot-stream-ingestion/import-from-apache-kafka.md#subset-partition-ingestion">Subset Partition Ingestion</a> for details and examples.</td></tr><tr><td>stream.kafka.buffer.size</td><td><strong>Default Value:</strong> <code>512000</code></td></tr><tr><td>stream.kafka.socket.timeout</td><td><strong>Default Value:</strong> <code>10000</code></td></tr><tr><td>stream.kafka.fetcher.size</td><td><strong>Default Value:</strong> <code>100000</code></td></tr><tr><td>stream.kafka.isolation.level</td><td><strong>Allowed Value:</strong> <code>read_committed</code> <strong>,</strong> <code>read_uncommitted</code><br><strong>Default:</strong> <code>read_uncommitted</code><br><br><strong>Note:</strong> This must be set to <code>read_committed</code> when using transactions in Kafka.</td></tr></tbody></table>

### Supported Decoder Classes

<table>
  <thead>
    <tr>
      <th>Decoder Class</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder`</td>
      <td>Decodes plain JSON messages without a schema registry.</td>
    </tr>
    <tr>
      <td>`org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder`</td>
      <td>Decodes Avro messages using a schema provided via `stream.kafka.decoder.prop.schema`.</td>
    </tr>
    <tr>
      <td>`org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder`</td>
      <td>Decodes Avro messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`.</td>
    </tr>
    <tr>
      <td>`org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder`</td>
      <td>Decodes JSON messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`. Added in Pinot 1.4.</td>
    </tr>
    <tr>
      <td>`org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder`</td>
      <td>Decodes Protocol Buffer messages.</td>
    </tr>
  </tbody>
</table>

### Kinesis

<table><thead><tr><th width="293">Config</th><th>Description</th></tr></thead><tbody><tr><td>stream.kinesis.consumer.factory.class.name</td><td><strong>Allowed Value:</strong> org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory</td></tr><tr><td>stream.kinesis.topic.name</td><td>(Required) Name of the Kinesis data stream to consume</td></tr><tr><td>region</td><td>(Required) The AWS region where the configured Kinesis data stream resides</td></tr><tr><td>maxRecordsToFetch</td><td>Maximum records to fetch during a single GetRecord request<br><strong>Default:</strong> <code>20</code></td></tr><tr><td>shardIteratorType</td><td>Similar to Kafka's offset reset property - indicates the point in the AWS Kinesis data stream from where the consumption should begin<br><strong>Allowed Values:</strong> <code>TRIM_HORIZON</code> , <code>LATEST</code></td></tr></tbody></table>

### Key-based Authentication Properties

<table><thead><tr><th width="301">Config</th><th>Description</th></tr></thead><tbody><tr><td>accessKey</td><td>(Required) AWS Access key used to access the AWS Kinesis Data stream</td></tr><tr><td>secretKey</td><td>(Required) AWS Secret key used to access the AWS Kinesis Data stream</td></tr></tbody></table>

### IAM Role-based Authentication Properties

<table><thead><tr><th width="301">Config</th><th>Description</th></tr></thead><tbody><tr><td><p></p><p>iamRoleBasedAccessEnabled</p></td><td>Set to <code>true</code> when using IAM role-based authentication for connecting to the AWS Kinesis Data Stream<br><strong>Default:</strong> <code>false</code></td></tr><tr><td>roleArn</td><td><strong>(Required)</strong> ARN of cross-account IAM role</td></tr><tr><td>roleSessionName</td><td>Unique identifier for a session when the client assumes the IAM role<br><strong>Default:</strong> <code>pinot-kinesis-&#x3C;UUID></code></td></tr><tr><td>externalId</td><td>Unique identifier used to manage trust between AWS accounts and prevent the confused deputy problem. More details <a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html">here</a></td></tr><tr><td>sessionDurationSeconds</td><td>Duration of the role session in seconds<br><strong>Default:</strong> <code>900</code></td></tr><tr><td>asyncSessionUpdateEnabled</td><td>Flag to determine with the session update should be enabled<br><strong>Default:</strong> <code>true</code></td></tr></tbody></table>

## Stream Connector Version Matrix

This matrix maps each stream connector to its Maven module, artifact ID, client library version, and consumer factory class.

<table>
  <thead>
    <tr>
      <th>Stream</th>
      <th>Connector Module</th>
      <th>Maven Artifact</th>
      <th>Client Library Version</th>
      <th>Consumer Factory Class</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Apache Kafka 3.x</td>
      <td>`pinot-kafka-3.0`</td>
      <td>`org.apache.pinot:pinot-kafka-3.0`</td>
      <td>kafka-clients 3.9.2</td>
      <td>`org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory`</td>
      <td>Default, included in binary distribution</td>
    </tr>
    <tr>
      <td>Apache Kafka 4.x</td>
      <td>`pinot-kafka-4.0`</td>
      <td>`org.apache.pinot:pinot-kafka-4.0`</td>
      <td>kafka-clients 4.1.1</td>
      <td>`org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory`</td>
      <td>Included in binary distribution</td>
    </tr>
    <tr>
      <td>Amazon Kinesis</td>
      <td>`pinot-kinesis`</td>
      <td>`org.apache.pinot:pinot-kinesis`</td>
      <td>AWS SDK 2.42.16 (`software.amazon.awssdk:kinesis`)</td>
      <td>`org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory`</td>
      <td>Included in binary distribution</td>
    </tr>
    <tr>
      <td>Apache Pulsar</td>
      <td>`pinot-pulsar`</td>
      <td>`org.apache.pinot:pinot-pulsar`</td>
      <td>pulsar-client 4.0.9</td>
      <td>`org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory`</td>
      <td>Optional, enable with `-Dplugins.include=pinot-pulsar`</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
All version numbers above are from the Pinot `master` branch (1.5.0-SNAPSHOT). Released Pinot versions may ship slightly different client library versions. Check the `pom.xml` of the corresponding module in your Pinot release for the exact version.
{% endhint %}

### Compatibility notes

#### Kafka 3.x connector (`pinot-kafka-3.0`)

* Compatible with Kafka brokers version 2.x and above.
* Uses the Scala-based Kafka library alongside `kafka-clients`.
* This is the recommended connector for most deployments.

#### Kafka 4.x connector (`pinot-kafka-4.0`)

* Requires Kafka brokers version 4.0 or above.
* Uses the pure-Java `kafka-clients` library only (no Scala dependency).
* Designed for KRaft-mode Kafka clusters that have removed ZooKeeper.
* Uses Testcontainers for integration testing instead of the embedded Kafka server.

#### Amazon Kinesis connector (`pinot-kinesis`)

* Uses AWS SDK v2 (`software.amazon.awssdk`).
* Supports both key-based and IAM role-based authentication.
* Included in the default Pinot distribution.

#### Apache Pulsar connector (`pinot-pulsar`)

* Not included in the default binary distribution. Enable with `-Dplugins.include=pinot-pulsar` at startup, or add the plugin JAR to the `plugins` directory.
* Uses the Apache Pulsar client library.
* Supports token-based, OAuth2, and TLS authentication.

### Removed connectors

<table>
  <thead>
    <tr>
      <th>Former Module</th>
      <th>Removed In</th>
      <th>Migration Path</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot-kafka-0.9`</td>
      <td>Pre-1.0</td>
      <td>Migrate to `pinot-kafka-3.0`</td>
    </tr>
    <tr>
      <td>`pinot-kafka-2.0`</td>
      <td>Pre-1.0</td>
      <td>Migrate to `pinot-kafka-3.0` (or `pinot-kafka-4.0` for Kafka 4.x brokers)</td>
    </tr>
  </tbody>
</table>

To migrate, update `stream.kafka.consumer.factory.class.name` in your table config from the old class to the new one. No other stream config changes are required.

## Metrics Plugins

Apache Pinot uses a pluggable metrics factory to support multiple metrics backends. Each Pinot component (Server, Broker, Controller, Minion) can be independently configured with a metrics implementation.

### Available Implementations

<table>
  <thead>
    <tr>
      <th>Plugin</th>
      <th>Class Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Yammer** (default)</td>
      <td>`org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory`</td>
      <td>Lightweight, default metrics implementation</td>
    </tr>
    <tr>
      <td>**Dropwizard**</td>
      <td>`org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory`</td>
      <td>Full Dropwizard Metrics integration with sliding time window reservoirs</td>
    </tr>
    <tr>
      <td>**Compound**</td>
      <td>`org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory`</td>
      <td>Registers metrics in multiple backends simultaneously</td>
    </tr>
  </tbody>
</table>

### Configuration

Configure the metrics factory for any component using:

```properties
pinot.<component>.metrics.factory.className=<factory-class-name>
```

Where `<component>` is one of: `server`, `broker`, `controller`, `minion`.

### Yammer Metrics (Default)

The default metrics backend. No additional configuration required.

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory
```

### Dropwizard Metrics

Provides full Dropwizard Metrics library integration with sliding 15-minute time window reservoirs, detailed histograms and timers, and JMX reporting.

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory
```

**Additional properties:**

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot.<component>.metrics.dropwizard.domain`</td>
      <td>`org.apache.pinot.common.metrics`</td>
      <td>JMX domain name for metrics</td>
    </tr>
  </tbody>
</table>

**Example:**

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory
pinot.server.metrics.dropwizard.domain=my.company.pinot.metrics
```

### Compound Metrics (Multi-Backend)

The Compound metrics plugin registers metrics in multiple backends simultaneously. This is useful for comparing metric implementations or reporting to multiple monitoring systems.

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory
```

**Additional properties:**

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinot.<component>.metrics.compound.algorithm`</td>
      <td>`CLASSPATH`</td>
      <td>Discovery algorithm: `CLASSPATH`, `SERVICE_LOADER`, or `LIST`</td>
    </tr>
    <tr>
      <td>`pinot.<component>.metrics.compound.ignored`</td>
      <td>(empty)</td>
      <td>Comma-separated list of factory class names to exclude</td>
    </tr>
    <tr>
      <td>`pinot.<component>.metrics.compound.list`</td>
      <td>(empty)</td>
      <td>Comma-separated list of factory class names to include (only with `algorithm=LIST`)</td>
    </tr>
  </tbody>
</table>

**Example: Use both Yammer and Dropwizard:**

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory
pinot.server.metrics.compound.algorithm=LIST
pinot.server.metrics.compound.list=org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory,org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory
```

**Example: Classpath discovery excluding Yammer:**

```properties
pinot.server.metrics.factory.className=org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory
pinot.server.metrics.compound.algorithm=CLASSPATH
pinot.server.metrics.compound.ignored=org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory
```

{% hint style="warning" %}
When using Compound metrics, ensure JMX MBean names don't conflict between registries. Conflicting MBean names may cause unpredictable metric values.
{% endhint %}

### Metric Types

Pinot exposes the following metric primitives through all backends:

<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Description</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Counter**</td>
      <td>Discrete event counts</td>
      <td>Total queries processed</td>
    </tr>
    <tr>
      <td>**Meter**</td>
      <td>Event rates</td>
      <td>Queries per second</td>
    </tr>
    <tr>
      <td>**Timer**</td>
      <td>Latency and throughput</td>
      <td>Query execution time</td>
    </tr>
    <tr>
      <td>**Histogram**</td>
      <td>Value distributions</td>
      <td>Query result sizes</td>
    </tr>
    <tr>
      <td>**Gauge**</td>
      <td>Point-in-time values</td>
      <td>Segment count, heap usage</td>
    </tr>
  </tbody>
</table>

### JMX Reporting

All metrics implementations include a JMX reporter enabled by default. The `JmxReporterMetricsRegistryRegistrationListener` is automatically registered when the metrics system initializes.

To configure additional metrics reporting (for example, Prometheus or Grafana), see [Monitor Pinot Using Prometheus and Grafana](../../tutorials/operations/monitor-pinot-using-prometheus-and-grafana.md).

## Environment Provider Plugins

Environment Provider plugins allow Pinot to discover cloud-specific instance metadata at startup. This metadata is used to configure failure domains, availability zones, and other cloud-specific settings that improve data placement and fault tolerance.

### Available Implementations

<table>
  <thead>
    <tr>
      <th>Plugin</th>
      <th>Class Name</th>
      <th>Cloud Provider</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Azure**</td>
      <td>`org.apache.pinot.plugin.provider.AzureEnvironmentProvider`</td>
      <td>Microsoft Azure</td>
    </tr>
  </tbody>
</table>

### Azure Environment Provider

The Azure Environment Provider queries the [Azure Instance Metadata Service (IMDS)](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service) to retrieve the platform fault domain for the current VM. This information is used by Pinot's Helix-based cluster management to distribute instances across Azure failure domains for improved fault tolerance.

#### Configuration

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`maxRetry`</td>
      <td>Integer</td>
      <td>Yes</td>
      <td>Maximum number of HTTP retries (must be > 0)</td>
    </tr>
    <tr>
      <td>`imdsEndpoint`</td>
      <td>String</td>
      <td>Yes</td>
      <td>Azure IMDS endpoint URL</td>
    </tr>
    <tr>
      <td>`connectionTimeoutMillis`</td>
      <td>Integer</td>
      <td>Yes</td>
      <td>HTTP connection timeout in milliseconds</td>
    </tr>
    <tr>
      <td>`requestTimeoutMillis`</td>
      <td>Integer</td>
      <td>Yes</td>
      <td>HTTP request/response timeout in milliseconds</td>
    </tr>
  </tbody>
</table>

#### Example Configuration

```properties
pinot.server.environment.provider.className=org.apache.pinot.plugin.provider.AzureEnvironmentProvider
pinot.server.environment.provider.maxRetry=3
pinot.server.environment.provider.imdsEndpoint=http://169.254.169.254/metadata/instance?api-version=2020-09-01
pinot.server.environment.provider.connectionTimeoutMillis=5000
pinot.server.environment.provider.requestTimeoutMillis=5000
```

#### How It Works

1. At startup, the provider sends an HTTP GET request to the Azure IMDS endpoint
2. The IMDS response contains VM metadata including the `compute.platformFaultDomain` field
3. The failure domain value is returned and used by Helix to configure the instance
4. This enables Pinot to distribute replicas across fault domains, improving availability during Azure infrastructure failures

{% hint style="info" %}
The Azure IMDS endpoint (`169.254.169.254`) is only accessible from within an Azure VM. This plugin should only be enabled when running Pinot on Azure infrastructure.
{% endhint %}

## Developing Custom Plugins

To create a custom environment provider, implement the `PinotEnvironmentProvider` interface:

```java
public interface PinotEnvironmentProvider {
    void init(PinotConfiguration pinotConfiguration);
    String getFailureDomain();
}
```

For the general plugin authoring workflow, see [write-custom-plugins](../../developers/plugin-architecture/write-custom-plugins/).

## Legacy compatibility pages

- [STDDEV_POP](../../configuration-reference/plugin-reference/stddev_pop.md)
- [STDDEV_SAMP](../../configuration-reference/plugin-reference/stddev_samp.md)
- [VAR_POP](../../configuration-reference/plugin-reference/var_pop.md)
- [VAR_SAMP](../../configuration-reference/plugin-reference/var_samp.md)
