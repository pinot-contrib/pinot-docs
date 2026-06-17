---
description: >-
  Apache Flink connector for writing data directly into Apache Pinot tables,
  supporting offline, realtime, and upsert table types.
---

# Flink Connector

The Pinot Flink Connector provides a `PinotSink` that plugs into any Flink streaming or batch job to generate Pinot segments in-process and upload them directly to the cluster. It supports offline tables, realtime tables, and full-upsert tables.

## Requirements

* **Flink 2.2.0 or later** – The connector requires Flink 2.x and supports Java 21.
* **Java 11+** – Prior versions: Java 8 support ended with Flink 1.x.

> **Note:** If you're using Flink 1.x, use Pinot version 1.5.0 or earlier. Pinot 1.6.0+ requires Flink 2.x.

## Use Cases

* **Offline table backfill** -- Populate or refresh an offline table from a data lake, database export, or any Flink-readable source.
* **Upsert table bootstrapping** -- Seed a realtime upsert table with historical data while preserving correct partition assignment and comparison-column ordering.
* **ETL and enrichment pipelines** -- Embed Pinot writes inside a larger Flink DAG that joins, filters, or enriches data before loading.

## When to Use Flink vs. Other Ingestion Methods

| Capability | Flink Connector | Spark Batch Ingestion | Standalone `LaunchDataIngestionJob` |
| --- | --- | --- | --- |
| Processing framework | Apache Flink (streaming or batch) | Apache Spark | None (standalone Java process) |
| Upsert table backfill | Yes -- generates correctly partitioned uploaded-realtime segments | Not natively supported | Not natively supported |
| Custom transformation logic | Full Flink API (joins, windows, aggregations) | Full Spark API | Limited to ingestion config transforms |
| Cluster dependency | Requires a Flink cluster or local Flink environment | Requires a Spark cluster | Runs as a single JVM process |
| Typical data sources | Kafka, data lake files, JDBC, any Flink source | HDFS, S3, GCS, any Spark source | Local/remote files (CSV, JSON, Avro, Parquet, ORC, Thrift) |
| Best for | Teams already running Flink; upsert backfill scenarios | Teams already running Spark; large-scale batch loads | Simple one-off or scheduled loads without a processing framework |

## Maven Dependency

```xml
<dependency>
  <groupId>org.apache.pinot</groupId>
  <artifactId>pinot-flink-connector</artifactId>
  <version>${pinot.version}</version>
</dependency>
```

Replace `${pinot.version}` with your Pinot release version. Check [Apache Pinot releases](https://pinot.apache.org/download/) for the latest stable version.

The artifact is published to the Apache Maven repository and transitively includes the Pinot admin client,
segment writer, and Flink 2.x core dependencies.

## Quick Example

```java
StreamExecutionEnvironment execEnv = StreamExecutionEnvironment.getExecutionEnvironment();
execEnv.setParallelism(2);

DataStream<Row> srcRows = execEnv.fromData(...);

String controllerUrl = "http://localhost:9000";
URI controllerUri = URI.create(controllerUrl);
String controllerAddress = controllerUri.getAuthority();
String controllerPath = controllerUri.getPath();
if (controllerPath != null && !controllerPath.isEmpty() && !"/".equals(controllerPath)) {
  controllerAddress += controllerPath.endsWith("/") ? controllerPath.substring(0, controllerPath.length() - 1)
      : controllerPath;
}
Properties properties = new Properties();
properties.setProperty(PinotAdminTransport.ADMIN_TRANSPORT_SCHEME, controllerUri.getScheme());

try (PinotAdminClient adminClient = new PinotAdminClient(controllerAddress, properties)) {
  Schema schema = adminClient.getSchemaClient().getSchemaObject("myTable");
  TableConfig tableConfig =
      adminClient.getTableClient().getTableConfigObjectForType("myTable", TableType.OFFLINE);

  srcRows.sinkTo(new PinotSink<>(
      new FlinkRowGenericRowConverter(typeInfo),
      tableConfig,
      schema,
      controllerUrl));
}
execEnv.execute();
```

## Full Configuration Reference

For complete configuration details, including upsert partitioning requirements, segment flush control, segment naming, and realtime table support, see the [Flink batch ingestion reference](../ingestion/batch-ingestion/flink.md).

## Migration from Flink 1.x

> **Deprecated:** The legacy `PinotSinkFunction` (based on Flink 1.x `SinkFunction` API) is deprecated and no longer functional with Flink 2.x. Update your code to use `PinotSink` and the `sinkTo()` API.

### Old API (Flink 1.x – no longer supported)
```java
// This code no longer works on Flink 2.x
srcRows.addSink(new PinotSinkFunction<>(...));
```

### New API (Flink 2.x)
```java
// Use this for Flink 2.2.0 and later
srcRows.sinkTo(new PinotSink<>(...));
```

For help migrating, refer to the updated [Flink batch ingestion examples](../ingestion/batch-ingestion/flink.md).

## Additional Resources

* [Design proposal](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=177045634) -- Original motivation and architecture
* [Source code](https://github.com/apache/pinot/tree/master/pinot-connectors/pinot-flink-connector) -- Connector implementation on GitHub
* [FlinkQuickStart.java](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-flink-connector/src/main/java/org/apache/pinot/connector/flink/FlinkQuickStart.java) -- Runnable example
