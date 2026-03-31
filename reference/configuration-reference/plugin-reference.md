---
description: Configuration reference entry point for Pinot plugins.
---

# Plugin Configuration Reference

This page keeps the plugin-family overview and the detailed configuration sections on a single page.

Apache Pinot has a plug-and-play architecture organized into ten plugin families. Each family targets a specific extensibility need, from reading data in different formats to exporting metrics to your monitoring stack.

This section covers the configuration side of each plugin family: which implementations ship with Pinot, what config keys they accept, and how to enable them. If you want to write your own plugin, see the [Plugin Architecture](../../developers/plugin-architecture/README.md) section in the Developer Guide.

## Plugin Families at a Glance

| Plugin Family | What It Does | Config Reference | Authoring Guide |
| --- | --- | --- | --- |
| **Stream Ingestion** | Consume data from real-time streaming platforms (Kafka, Kinesis, Pulsar) | [Stream Ingestion Connectors](#stream-ingestion-connectors) / [Version Matrix](#stream-connector-version-matrix) | [Stream Ingestion Plugin](../../developers/plugin-architecture/write-custom-plugins/write-your-stream.md) |
| **Input Format** | Read records from files or streams during ingestion (Avro, JSON, Parquet, ORC, CSV, ...) | [Input Formats](../../build-with-pinot/ingestion/pinot-input-formats.md) | [Input Format Plugin](../../developers/plugin-architecture/write-custom-plugins/record-reader.md) |
| **Filesystem** | Store and fetch segments from pluggable storage backends (S3, GCS, HDFS, ADLS) | [Filesystem Plugins](../../manage-data/data-import/pinot-file-system/) | [Filesystem Plugin](../../developers/plugin-architecture/write-custom-plugins/pluggable-storage.md) |
| **Batch Ingestion** | Run data ingestion jobs on different execution frameworks (Standalone, Hadoop, Spark) | [Batch Ingestion](../../build-with-pinot/ingestion/batch-ingestion) | - |
| **Metrics** | Collect and expose internal JMX metrics via Dropwizard, Yammer, or a compound backend | [Metrics Plugins](#metrics-plugins) | [Metrics Plugin](../../developers/plugin-architecture/write-custom-plugins/metrics-plugin.md) |
| **Segment Writer** | Programmatically build Pinot segments without a full batch ingestion job | - | [Segment Writer Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-writer-plugin.md) |
| **Segment Uploader** | Upload completed segment tar files to the Pinot cluster | - | [Segment Uploader Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-uploader-plugin.md) |
| **Minion Tasks** | Run background processing tasks on Pinot Minion nodes (merge, purge, compaction, ...) | [Minion](../../basics/components/cluster/minion.md) / [Merge/Rollup Task](../../operators/operating-pinot/minion-merge-rollup-task.md) | [Minion Task Plugin](../../developers/plugin-architecture/write-custom-plugins/minion-task-plugin.md) |
| **Environment** | Discover cloud-specific instance metadata for failure-domain-aware placement | [Environment Provider](#environment-provider-plugins) | - |
| **Time Series Language** | Support custom time series query languages (M3QL, PromQL) | - | [Time Series Language Plugin](../../developers/plugin-architecture/write-custom-plugins/time-series-language-plugin.md) |

## Stream Ingestion Connectors

### Applicable to all stream connectors

<table><thead><tr><th width="281">Configuration</th><th>Description</th></tr></thead><tbody><tr><td>stream.&#x3C;stream_type>.consumer.factory.class.name</td><td>Factory class to be used for the stream consumer</td></tr><tr><td>stream.&#x3C;stream_type>.consumer.prop.auto.offset.reset</td><td>Offset or position in the source stream from which to start consuming data<br><strong>Valid values:</strong> <br><strong><code>smallest</code></strong> - Start consuming from the earliest data in the stream<br><strong><code>largest</code></strong> - Start consuming from the latest data in the stream<br><strong><code>timestamp</code></strong> - Start consuming from the offset after a timestamp , which is specified in the format <code>yyyy-MM-dd'T'HH:mm:ss.SSSZ</code><br><strong><code>datetime</code> -</strong> Start consuming from the offset after the specified period or duration from current time. Eg: <code>2d</code> <br><strong>Default Value:</strong> <code>largest</code> </td></tr><tr><td>stream.&#x3C;stream_type>.topic.name</td><td>Name of the source stream to consume </td></tr><tr><td>stream.&#x3C;stream_type>.fetch.timeout.millis</td><td>Indicates the timeout (in milliseconds) to use for each fetch call to the consumer. If the timeout expires before data becomes available, the consumer will return an empty batch.<br><strong>Default Value:</strong> <code>5_000</code></td></tr><tr><td>stream.&#x3C;stream_type>.connection.timeout.millis</td><td>Indicates the timeout (in milliseconds) used to create the connection to the upstream (Timeout for the initial connection to the upstream)<br><strong>Default Value:</strong> <code>30_000</code></td></tr><tr><td>stream.&#x3C;stream_type>.idle.timeout.millis</td><td>If the stream remains idle (ie. without any data) for the specified time, the client connection is reset and a new consumer instance is created.  <br><strong>Default Value:</strong> <code>180_000</code></td></tr><tr><td>stream.&#x3C;stream_type>.decoder.class.name</td><td>Indicates the name of the decoder class that should be used to decoder the stream payload</td></tr><tr><td>stream.&#x3C;stream_type>.decoder.prop</td><td>Prefix used for any decoder specific property </td></tr><tr><td>topic.consumption.rate.limit</td><td>Indicates the upper bound on the message rate for the entire topic. Use <code>-1</code> to ignore this config. <br><strong>Default Value:</strong> <code>-1</code><br>See <a href="../../build-with-pinot/ingestion/stream-ingestion/README.md">Stream Ingestion</a> for more details.</td></tr><tr><td>stream.&#x3C;stream_type>.metadata.populate</td><td>When set to <code>true</code>, the supported consumer may extract the key, user headers and record metadata from the incoming payload. <br>Currently, this is supported in Kafka connector only.</td></tr><tr><td>realtime.segment.flush.threshold.time</td><td>Time based flush threshold for realtime segments. Used to decides when a realtime segment is ready to be committed / closed / flushed to disk.<br><br>Warning: This time should be smaller than the retention period configured for the corresponding topic</td></tr><tr><td>realtime.segment.flush.threshold.size</td><td>The size a completed realtime segment should be. <br><br>Note: This config is used only if <code>realtime.segment.flush.threshold.rows</code> is set to 0.</td></tr><tr><td>realtime.segment.flush.threshold.rows</td><td><p>Row count based flush threshold for realtime segments. <p>If this value is set to 0, then the consumers adjust the number of rows consumed by a partition so the completed segment is the correct size (unless</p><p>threshold.time is reached first)</p></td></tr><tr><td>realtime.segment.flush.autotune.initialRows</td><td>Initial number of rows to use for <code>SegmentSizeBasedFlushThresholdUpdater</code> . This threshold updater is used by the controller to compute the new segment's flush threshold based on the previous segment's size. <br>Warning: This flush threshold updater is used only when <code>realtime.segment.flush.threshold.rows</code> is set to <code>&#x3C;=0</code> . Otherwise, the <code>DefaultFlushThresholdUpdater</code> is used. </td></tr><tr><td>realtime.segment.commit.timeoutSeconds</td><td>Time threshold that controller will wait for the segment to be built by the server</td></tr></tbody></table>

### Kafka 3.x / 4.x

Pinot ships two Kafka connector modules: `pinot-kafka-3.0` (Kafka client 3.9.2, default) and `pinot-kafka-4.0` (Kafka client 4.1.1, for KRaft-mode clusters). The legacy `kafka-0.9` and `kafka-2.x` modules have been removed.

<table><thead><tr><th width="285">Config</th><th>Description</th></tr></thead><tbody><tr><td>stream.kafka.consumer.factory.class.name</td><td><strong>Allowed Values:</strong><br>- <code>org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory</code> (Kafka 3.x, default)<br>- <code>org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory</code> (Kafka 4.x)</td></tr><tr><td>stream.kafka.topic.name</td><td>(Required) Name of the kafka topic to be ingested</td></tr><tr><td>stream.kafka.broker.list</td><td>(Required) Connection string for the kafka broker</td></tr><tr><td>stream.kafka.partition.ids</td><td>Optional comma-separated list of Kafka partition IDs to consume (e.g. <code>"0,2,5"</code>). When set, only the specified partitions are consumed by this table. When absent or blank, all topic partitions are consumed (the default behavior).<br><br>Partition IDs must be non-negative integers. Duplicates are silently removed. The IDs are validated against the actual topic metadata at table creation time.<br><br>See <a href="../../build-with-pinot/ingestion/stream-ingestion/import-from-apache-kafka.md#subset-partition-ingestion">Subset Partition Ingestion</a> for details and examples.</td></tr><tr><td>stream.kafka.buffer.size</td><td><strong>Default Value:</strong> <code>512000</code></td></tr><tr><td>stream.kafka.socket.timeout</td><td><strong>Default Value:</strong> <code>10000</code></td></tr><tr><td>stream.kafka.fetcher.size</td><td><strong>Default Value:</strong> <code>100000</code></td></tr><tr><td>stream.kafka.isolation.level</td><td><strong>Allowed Value:</strong> <code>read_committed</code> <strong>,</strong> <code>read_uncommitted</code><br><strong>Default:</strong> <code>read_uncommitted</code><br><br><strong>Note:</strong> This must be set to <code>read_committed</code> when using transactions in Kafka.</td></tr></tbody></table>

### Supported Decoder Classes

| Decoder Class | Description |
| --- | --- |
| `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder` | Decodes plain JSON messages without a schema registry. |
| `org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder` | Decodes Avro messages using a schema provided via `stream.kafka.decoder.prop.schema`. |
| `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` | Decodes Avro messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`. |
| `org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder` | Decodes JSON messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`. Added in Pinot 1.4. |
| `org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder` | Decodes Protocol Buffer messages. |

### Kinesis

<table><thead><tr><th width="293">Config</th><th>Description</th></tr></thead><tbody><tr><td>stream.kinesis.consumer.factory.class.name</td><td><strong>Allowed Value:</strong> org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory</td></tr><tr><td>stream.kinesis.topic.name</td><td>(Required) Name of the Kinesis data stream to consume</td></tr><tr><td>region</td><td>(Required) The AWS region where the configured Kinesis data stream resides</td></tr><tr><td>maxRecordsToFetch</td><td>Maximum records to fetch during a single GetRecord request<br><strong>Default:</strong> <code>20</code></td></tr><tr><td>shardIteratorType</td><td>Similar to Kafka's offset reset property - indicates the point in the AWS Kinesis data stream from where the consumption should begin<br><strong>Allowed Values:</strong> <code>TRIM_HORIZON</code> , <code>LATEST</code></td></tr></tbody></table>

### Key-based Authentication Properties

<table><thead><tr><th width="301">Config</th><th>Description</th></tr></thead><tbody><tr><td>accessKey</td><td>(Required) AWS Access key used to access the AWS Kinesis Data stream</td></tr><tr><td>secretKey</td><td>(Required) AWS Secret key used to access the AWS Kinesis Data stream</td></tr></tbody></table>

### IAM Role-based Authentication Properties

<table><thead><tr><th width="301">Config</th><th>Description</th></tr></thead><tbody><tr><td><p></p><p>iamRoleBasedAccessEnabled</p></td><td>Set to <code>true</code> when using IAM role-based authentication for connecting to the AWS Kinesis Data Stream<br><strong>Default:</strong> <code>false</code></td></tr><tr><td>roleArn</td><td><strong>(Required)</strong> ARN of cross-account IAM role</td></tr><tr><td>roleSessionName</td><td>Unique identifier for a session when the client assumes the IAM role<br><strong>Default:</strong> <code>pinot-kinesis-&#x3C;UUID></code></td></tr><tr><td>externalId</td><td>Unique identifier used to manage trust between AWS accounts and prevent the confused deputy problem. More details <a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html">here</a></td></tr><tr><td>sessionDurationSeconds</td><td>Duration of the role session in seconds<br><strong>Default:</strong> <code>900</code></td></tr><tr><td>asyncSessionUpdateEnabled</td><td>Flag to determine with the session update should be enabled<br><strong>Default:</strong> <code>true</code></td></tr></tbody></table>

## Stream Connector Version Matrix

This matrix maps each stream connector to its Maven module, artifact ID, client library version, and consumer factory class.

| Stream | Connector Module | Maven Artifact | Client Library Version | Consumer Factory Class | Status |
| --- | --- | --- | --- | --- | --- |
| Apache Kafka 3.x | `pinot-kafka-3.0` | `org.apache.pinot:pinot-kafka-3.0` | kafka-clients 3.9.2 | `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` | Default, included in binary distribution |
| Apache Kafka 4.x | `pinot-kafka-4.0` | `org.apache.pinot:pinot-kafka-4.0` | kafka-clients 4.1.1 | `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` | Included in binary distribution |
| Amazon Kinesis | `pinot-kinesis` | `org.apache.pinot:pinot-kinesis` | AWS SDK 2.42.16 (`software.amazon.awssdk:kinesis`) | `org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory` | Included in binary distribution |
| Apache Pulsar | `pinot-pulsar` | `org.apache.pinot:pinot-pulsar` | pulsar-client 4.0.9 | `org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory` | Optional, enable with `-Dplugins.include=pinot-pulsar` |

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

| Former Module | Removed In | Migration Path |
| --- | --- | --- |
| `pinot-kafka-0.9` | Pre-1.0 | Migrate to `pinot-kafka-3.0` |
| `pinot-kafka-2.0` | Pre-1.0 | Migrate to `pinot-kafka-3.0` (or `pinot-kafka-4.0` for Kafka 4.x brokers) |

To migrate, update `stream.kafka.consumer.factory.class.name` in your table config from the old class to the new one. No other stream config changes are required.

## Metrics Plugins

Apache Pinot uses a pluggable metrics factory to support multiple metrics backends. Each Pinot component (Server, Broker, Controller, Minion) can be independently configured with a metrics implementation.

### Available Implementations

| Plugin | Class Name | Description |
|--------|-----------|-------------|
| **Yammer** (default) | `org.apache.pinot.plugin.metrics.yammer.YammerMetricsFactory` | Lightweight, default metrics implementation |
| **Dropwizard** | `org.apache.pinot.plugin.metrics.dropwizard.DropwizardMetricsFactory` | Full Dropwizard Metrics integration with sliding time window reservoirs |
| **Compound** | `org.apache.pinot.plugin.metrics.compound.CompoundPinotMetricsFactory` | Registers metrics in multiple backends simultaneously |

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

| Property | Default | Description |
|----------|---------|-------------|
| `pinot.<component>.metrics.dropwizard.domain` | `org.apache.pinot.common.metrics` | JMX domain name for metrics |

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

| Property | Default | Description |
|----------|---------|-------------|
| `pinot.<component>.metrics.compound.algorithm` | `CLASSPATH` | Discovery algorithm: `CLASSPATH`, `SERVICE_LOADER`, or `LIST` |
| `pinot.<component>.metrics.compound.ignored` | (empty) | Comma-separated list of factory class names to exclude |
| `pinot.<component>.metrics.compound.list` | (empty) | Comma-separated list of factory class names to include (only with `algorithm=LIST`) |

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

| Type | Description | Example |
|------|-------------|---------|
| **Counter** | Discrete event counts | Total queries processed |
| **Meter** | Event rates | Queries per second |
| **Timer** | Latency and throughput | Query execution time |
| **Histogram** | Value distributions | Query result sizes |
| **Gauge** | Point-in-time values | Segment count, heap usage |

### JMX Reporting

All metrics implementations include a JMX reporter enabled by default. The `JmxReporterMetricsRegistryRegistrationListener` is automatically registered when the metrics system initializes.

To configure additional metrics reporting (for example, Prometheus or Grafana), see [Monitor Pinot Using Prometheus and Grafana](../../operate-pinot/monitor-pinot-using-prometheus-and-grafana.md).

## Environment Provider Plugins

Environment Provider plugins allow Pinot to discover cloud-specific instance metadata at startup. This metadata is used to configure failure domains, availability zones, and other cloud-specific settings that improve data placement and fault tolerance.

### Available Implementations

| Plugin | Class Name | Cloud Provider |
|--------|-----------|---------------|
| **Azure** | `org.apache.pinot.plugin.provider.AzureEnvironmentProvider` | Microsoft Azure |

### Azure Environment Provider

The Azure Environment Provider queries the [Azure Instance Metadata Service (IMDS)](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service) to retrieve the platform fault domain for the current VM. This information is used by Pinot's Helix-based cluster management to distribute instances across Azure failure domains for improved fault tolerance.

#### Configuration

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `maxRetry` | Integer | Yes | Maximum number of HTTP retries (must be > 0) |
| `imdsEndpoint` | String | Yes | Azure IMDS endpoint URL |
| `connectionTimeoutMillis` | Integer | Yes | HTTP connection timeout in milliseconds |
| `requestTimeoutMillis` | Integer | Yes | HTTP request/response timeout in milliseconds |

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

- [STDDEV_POP](../../functions/statistical/stddevpop.md)
- [STDDEV_SAMP](../../functions/statistical/stddevsamp.md)
- [VAR_POP](../../functions/statistical/varpop.md)
- [VAR_SAMP](../../functions/statistical/varsamp.md)
