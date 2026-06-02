# Plugins

Starting from the 0.3.X release, Pinot supports a plug-and-play architecture. This means that starting from version 0.3.0, Pinot can be easily extended to support new tools, like streaming services, storage systems, input formats, and metrics providers.

![](<../../.gitbook/assets/Pinot Dependency Graph.svg>)

Plugins are collected in folders, based on their purpose. Pinot organizes its plugins into **eleven plugin families**, each targeting a specific extensibility need. The table below summarizes every family, its SPI module, and the implementations that ship with Pinot.

## Plugin Families at a Glance

| Plugin Family | SPI Interface / Module | Built-in Implementations |
| --- | --- | --- |
| **Input Format** | `RecordReader` / `StreamMessageDecoder` | Avro, CSV, JSON, ORC, Parquet, Thrift, Protobuf, Arrow, CLP-Log, Confluent Avro, Confluent JSON, Confluent Protobuf |
| **Filesystem** | `PinotFS` | S3, GCS, HDFS, ADLS |
| **Stream Ingestion** | `StreamConsumerFactory` | Kafka 3.0, Kafka 4.0, Kinesis, Pulsar |
| **Batch Ingestion** | `IngestionJobRunner` | Standalone, Hadoop, Spark 3 |
| **Metrics** | `PinotMetricsFactory` | Dropwizard, Yammer, Compound |
| **Segment Writer** | `SegmentWriter` | File-based |
| **Segment Uploader** | `SegmentUploader` | Default |
| **Minion Tasks** | `PinotTaskGenerator` / `PinotTaskExecutor` | MergeRollup, Purge, RealtimeToOfflineSegments, SegmentGenerationAndPush, UpsertCompaction, UpsertCompactMerge, RefreshSegment |
| **Environment** | `PinotEnv` | Azure |
| **Time Series Language** | `TimeSeriesLogicalPlanner` | M3QL |
| **OpChain Converter** | `OpChainConverter` | Default |

---

### Input Format

Input format plugins read data from files or streams during data ingestion. Batch ingestion uses `RecordReader` implementations, while real-time ingestion uses `StreamMessageDecoder` implementations.

{% content-ref url="../../build-with-pinot/ingestion/pinot-input-formats.md" %}
[pinot-input-formats.md](../../build-with-pinot/ingestion/pinot-input-formats.md)
{% endcontent-ref %}

### Filesystem

Filesystem plugins provide a storage abstraction layer so that Pinot segments can be stored on and fetched from different storage backends.

{% content-ref url="../../build-with-pinot/ingestion/file-systems/" %}
[pinot-file-system](../../build-with-pinot/ingestion/file-systems/)
{% endcontent-ref %}

### Stream Ingestion

Stream ingestion plugins allow Pinot to consume data from real-time streaming platforms.

{% content-ref url="../../build-with-pinot/ingestion/stream-ingestion/" %}
[pinot-stream-ingestion](../../build-with-pinot/ingestion/stream-ingestion/)
{% endcontent-ref %}

### Batch Ingestion

Batch ingestion plugins run data ingestion jobs on different execution frameworks.

{% content-ref url="../../build-with-pinot/ingestion/batch-ingestion" %}
[batch-ingestion](../../build-with-pinot/ingestion/batch-ingestion)
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

### Planner rule customizers

The multi-stage query engine also exposes an advanced planner SPI for broker-side Calcite rule customization. Implement `org.apache.pinot.query.planner.spi.RuleSetCustomizer` from `pinot-query-planner-spi` when you need to append, remove, reorder, or replace rules in Pinot's per-phase logical planning pipeline.

Discovery uses Java `ServiceLoader`. Pinot first loads `RuleSetCustomizer` implementations on the broker application classpath, then scans each loaded plugin classloader. A plugin JAR should include the standard Pinot plugin packaging plus a `META-INF/services/org.apache.pinot.query.planner.spi.RuleSetCustomizer` file listing the implementation class.

At rule match time, planner rules can read per-query planner options through the Calcite planner context. Pinot exposes `PlannerContext` from both planner variants, so rule code can unwrap it directly and inspect `getOptions()`:

```java
PlannerContext plannerContext =
    call.getPlanner().getContext().unwrap(PlannerContext.class);
String workerRuntime = plannerContext.getOptions().get("workerRuntime");
```

Use this path for query-scoped planner behavior. Rules that need broker-wide planner defaults can still unwrap `QueryEnvironment.Config` from the same Calcite context.

Initialization is one-time. `PinotRuleSet.defaultInstance()` builds the broker process-wide rule set lazily, and each discovered customizer runs once for every planner `Phase` before Pinot freezes those rule lists for the rest of the process. Load the plugin before broker startup, and restart the broker after adding or changing a planner-rules plugin.

This SPI is more upgrade-sensitive than the stable ingestion, filesystem, and metrics plugin families. Pinot keeps `Phase` append-only for binary compatibility, but new phases can be added and the built-in rule ordering can change between releases. Revalidate customizers on every Pinot upgrade, especially if they depend on a specific built-in rule name or order.

### Materialized view DDL handlers

Controller-managed `CREATE MATERIALIZED VIEW ... AS <query>` also has an advanced extension point. Implement `org.apache.pinot.sql.ddl.compile.MaterializedViewDdlHandler` from `pinot-sql-ddl` when a downstream distribution needs a different materialized-view engine contract than the built-in single-source `MaterializedViewTask` path.

The handler owns three decisions:

- `validateDefinedQuery(...)` decides whether the `AS <query>` shape is valid for the target engine.
- `supportsSchemaInference(...)` decides whether Pinot may infer MV columns from the `SELECT` projection when the DDL omits an explicit column list.
- `applyTaskConfig(...)` routes the MV properties onto the `TableConfigBuilder` and returns the task type stamped onto the table.

Register the handler once at controller startup through `DdlCompiler.setMaterializedViewDdlHandler(...)`. If no handler is registered, Pinot keeps the default behavior: JOINs are rejected, schema inference is allowed for the single-source path, and the MV runs under `MaterializedViewTask`.

If a custom handler stamps a task type other than the built-in `MaterializedViewTask`, it also owns that task type's runtime contract. In practice that means the custom task generator/executor, its validation rules, and any definition-metadata persistence or consistency tracking required by that alternate MV implementation.

For the default OSS materialized-view surface, see [Materialized Views](../../build-with-pinot/querying-and-sql/materialized-views.md).

Custom segment or index extensions that depend on `pinot-segment-spi` are a
separate, more upgrade-sensitive path than the stable plugin families listed
above. Revalidate these extensions on every Pinot upgrade. For example, Pinot
1.6.0 adds two required `IndexType` methods for custom index implementations:
`requiresDictionary(FieldSpec, C)` and
`shouldInvalidateOnDictionaryChange(FieldSpec, C)`. See the
[upgrade notes](../../operate-pinot/upgrade-notes.md) before upgrading custom
segment/index extensions.

{% content-ref url="write-custom-plugins/" %}
[write-custom-plugins](write-custom-plugins/)
{% endcontent-ref %}
