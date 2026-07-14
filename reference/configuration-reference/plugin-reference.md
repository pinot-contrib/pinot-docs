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
| **Filesystem** | Store and fetch segments from pluggable storage backends (S3, GCS, HDFS, ADLS) | [Filesystem Plugins](../../build-with-pinot/ingestion/file-systems/) | [Filesystem Plugin](../../developers/plugin-architecture/write-custom-plugins/pluggable-storage.md) |
| **Batch Ingestion** | Run data ingestion jobs on different execution frameworks (Standalone, Hadoop, Spark) | [Batch Ingestion](../../build-with-pinot/ingestion/batch-ingestion) | - |
| **Metrics** | Collect and expose internal JMX metrics via Dropwizard, Yammer, or a compound backend | [Metrics Plugins](#metrics-plugins) | [Metrics Plugin](../../developers/plugin-architecture/write-custom-plugins/metrics-plugin.md) |
| **Segment Writer** | Programmatically build Pinot segments without a full batch ingestion job | - | [Segment Writer Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-writer-plugin.md) |
| **Segment Uploader** | Upload completed segment tar files to the Pinot cluster | - | [Segment Uploader Plugin](../../developers/plugin-architecture/write-custom-plugins/segment-uploader-plugin.md) |
| **Minion Tasks** | Run background processing tasks on Pinot Minion nodes (merge, purge, compaction, ...) | [Minion](../../basics/components/cluster/minion.md) / [Merge/Rollup Task](../../operate-pinot/minion-merge-rollup-task.md) | [Minion Task Plugin](../../developers/plugin-architecture/write-custom-plugins/minion-task-plugin.md) |
| **Environment** | Discover cloud-specific instance metadata for failure-domain-aware placement | [Environment Provider](#environment-provider-plugins) | - |
| **Time Series Language** | Support custom time series query languages (M3QL, PromQL) | - | [Time Series Language Plugin](../../developers/plugin-architecture/write-custom-plugins/time-series-language-plugin.md) |

## Stream Ingestion Connectors

### Applicable to all stream connectors

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
| topic.consumption.rate.limit | Indicates the upper bound on the message rate for the entire topic. Use `-1` to ignore this config. **Default Value:** `-1` See [Stream Ingestion](../../build-with-pinot/ingestion/stream-ingestion/README.md) for more details. |
| stream.<stream_type>.metadata.populate | When set to `true`, the supported consumer may extract the key, user headers and record metadata from the incoming payload. Currently, this is supported in Kafka connector only. |
| realtime.segment.flush.threshold.time | Time based flush threshold for realtime segments. Used to decides when a realtime segment is ready to be committed / closed / flushed to disk. Warning: This time should be smaller than the retention period configured for the corresponding topic |
| realtime.segment.flush.threshold.size | The size a completed realtime segment should be. Note: This config is used only if `realtime.segment.flush.threshold.rows` is set to 0. |
| realtime.segment.flush.threshold.rows | Row count based flush threshold for realtime segments. If this value is set to 0, then the consumers adjust the number of rows consumed by a partition so the completed segment is the correct size (unless threshold.time is reached first) |
| realtime.segment.flush.autotune.initialRows | Initial number of rows to use for `SegmentSizeBasedFlushThresholdUpdater` . This threshold updater is used by the controller to compute the new segment's flush threshold based on the previous segment's size. Warning: This flush threshold updater is used only when `realtime.segment.flush.threshold.rows` is set to `<=0` . Otherwise, the `DefaultFlushThresholdUpdater` is used. |
| realtime.segment.commit.timeoutSeconds | Time threshold that controller will wait for the segment to be built by the server |
| realtime.segment.pauseless.download.timeoutSeconds | For pauseless consumption, the time in seconds that a replica waits for a committed segment to become downloadable from deep store or a peer server before timing out. Default: `600` seconds. Pinot prefers this key over the older `segmentDownloadTimeoutMinutes` setting. |

### Kafka 3.x / 4.x

Pinot ships two Kafka connector modules: `pinot-kafka-3.0` (Kafka client 3.9.2, default) and `pinot-kafka-4.0` (Kafka client 4.1.1, for KRaft-mode clusters). The legacy `kafka-0.9` and `kafka-2.x` modules have been removed.

| Config | Description |
| --- | --- |
| stream.kafka.consumer.factory.class.name | **Allowed Values:** - `org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory` (Kafka 3.x, default) - `org.apache.pinot.plugin.stream.kafka40.KafkaConsumerFactory` (Kafka 4.x) |
| stream.kafka.topic.name | (Required) Name of the kafka topic to be ingested |
| stream.kafka.broker.list | (Required) Connection string for the kafka broker |
| stream.kafka.partition.ids | Optional comma-separated string of Kafka partition IDs and/or inclusive ranges to consume (for example, `"0,2,5"`, `"0-3"`, or `"0-3,6,8-9"`). When set, only the resolved partitions are consumed by this table. When absent or blank, all topic partitions are consumed (the default behavior). Partition IDs must be non-negative integers, ranges are inclusive, duplicates are silently removed, and the resolved set is capped at 10,000 unique partition IDs. Pinot validates the resolved IDs against the topic metadata before it starts consuming. See [Subset Partition Ingestion](../../build-with-pinot/ingestion/stream-ingestion/import-from-apache-kafka.md#subset-partition-ingestion) for details and examples. |
| stream.kafka.buffer.size | **Default Value:** `512000` |
| stream.kafka.socket.timeout | **Default Value:** `10000` |
| stream.kafka.fetcher.size | **Default Value:** `100000` |
| stream.kafka.isolation.level | **Allowed Value:** `read_committed` **,** `read_uncommitted` **Default:** `read_uncommitted` **Note:** This must be set to `read_committed` when using transactions in Kafka. |

### Supported Decoder Classes

| Decoder Class | Description |
| --- | --- |
| `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder` | Decodes stream JSON messages without a schema registry. Defaults to UTF-8 text JSON and also supports `stream.<type>.decoder.prop.jsonFormat` values `TEXT`, `POSTGRES_JSONB`, `SQLITE_JSONB`, `SMILE`, `CBOR`, and opt-in `AUTO`. |
| `org.apache.pinot.plugin.inputformat.avro.SimpleAvroMessageDecoder` | Decodes Avro messages using a schema provided via `stream.kafka.decoder.prop.schema`. |
| `org.apache.pinot.plugin.inputformat.avro.confluent.KafkaConfluentSchemaRegistryAvroMessageDecoder` | Decodes Avro messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`. |
| `org.apache.pinot.plugin.inputformat.json.confluent.KafkaConfluentSchemaRegistryJsonMessageDecoder` | Decodes JSON messages whose schemas are registered in Confluent Schema Registry. Requires `stream.kafka.decoder.prop.schema.registry.rest.url`. Added in Pinot 1.4. |
| `org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder` | Decodes Protocol Buffer messages. |

### Kinesis

| Config | Description |
| --- | --- |
| stream.kinesis.consumer.factory.class.name | **Allowed Value:** org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory |
| stream.kinesis.topic.name | (Required) Name of the Kinesis data stream to consume |
| region | (Required) The AWS region where the configured Kinesis data stream resides |
| maxRecordsToFetch | Maximum records to fetch during a single `GetRecords` request **Default:** `10000` |
| requests_per_second_limit | Maximum Kinesis read requests per second Pinot will attempt per shard. Accepts fractional values such as `0.25` so several consumers can share one shard budget. Pinot applies this limit to both `GetRecords` and `GetShardIterator` reads and backs off/retries on throttling until the fetch timeout. **Default:** `1.0` |
| shardIteratorType | AWS shard iterator type Pinot uses when it opens a shard iterator. Pinot passes this value through to the Kinesis client. **Default:** `LATEST` |

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
