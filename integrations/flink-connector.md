---
description: >-
  Apache Flink connector for writing data directly into Apache Pinot tables,
  supporting offline, realtime, and upsert table types.
---

# Flink Connector

The Pinot Flink Connector provides a `PinotSinkFunction` that plugs into any Flink streaming or batch job to generate Pinot segments in-process and upload them directly to the cluster. It supports offline tables, realtime tables, and full-upsert tables.

## Use Cases

* **Offline table backfill** -- Populate or refresh an offline table from a data lake, database export, or any Flink-readable source.
* **Upsert table bootstrapping** -- Seed a realtime upsert table with historical data while preserving correct partition assignment and comparison-column ordering.
* **ETL and enrichment pipelines** -- Embed Pinot writes inside a larger Flink DAG that joins, filters, or enriches data before loading.

## When to Use Flink vs. Other Ingestion Methods

<table>
  <thead>
    <tr>
      <th>Capability</th>
      <th>Flink Connector</th>
      <th>Spark Batch Ingestion</th>
      <th>Standalone `LaunchDataIngestionJob`</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Processing framework</td>
      <td>Apache Flink (streaming or batch)</td>
      <td>Apache Spark</td>
      <td>None (standalone Java process)</td>
    </tr>
    <tr>
      <td>Upsert table backfill</td>
      <td>Yes -- generates correctly partitioned uploaded-realtime segments</td>
      <td>Not natively supported</td>
      <td>Not natively supported</td>
    </tr>
    <tr>
      <td>Custom transformation logic</td>
      <td>Full Flink API (joins, windows, aggregations)</td>
      <td>Full Spark API</td>
      <td>Limited to ingestion config transforms</td>
    </tr>
    <tr>
      <td>Cluster dependency</td>
      <td>Requires a Flink cluster or local Flink environment</td>
      <td>Requires a Spark cluster</td>
      <td>Runs as a single JVM process</td>
    </tr>
    <tr>
      <td>Typical data sources</td>
      <td>Kafka, data lake files, JDBC, any Flink source</td>
      <td>HDFS, S3, GCS, any Spark source</td>
      <td>Local/remote files (CSV, JSON, Avro, Parquet, ORC, Thrift)</td>
    </tr>
    <tr>
      <td>Best for</td>
      <td>Teams already running Flink; upsert backfill scenarios</td>
      <td>Teams already running Spark; large-scale batch loads</td>
      <td>Simple one-off or scheduled loads without a processing framework</td>
    </tr>
  </tbody>
</table>

## Maven Dependency

```xml
<dependency>
  <groupId>org.apache.pinot</groupId>
  <artifactId>pinot-flink-connector</artifactId>
  <version>${pinot.version}</version>
</dependency>
```

Replace `${pinot.version}` with your Pinot release version. Check [Apache Pinot releases](https://pinot.apache.org/download/) for the latest stable version.

The artifact is published to the Apache Maven repository and transitively includes the Pinot controller client, segment writer, and Flink core dependencies.

## Quick Example

```java
StreamExecutionEnvironment execEnv = StreamExecutionEnvironment.getExecutionEnvironment();
execEnv.setParallelism(2);

DataStream<Row> srcRows = execEnv.addSource(new FlinkKafkaConsumer<Row>(...));

HttpClient httpClient = HttpClient.getInstance();
ControllerRequestClient client = new ControllerRequestClient(
    ControllerRequestURLBuilder.baseUrl("http://localhost:9000"), httpClient);

Schema schema = PinotConnectionUtils.getSchema(client, "myTable");
TableConfig tableConfig = PinotConnectionUtils.getTableConfig(client, "myTable", "OFFLINE");

srcRows.addSink(new PinotSinkFunction<>(
    new FlinkRowGenericRowConverter(typeInfo),
    tableConfig,
    schema));
execEnv.execute();
```

## Full Configuration Reference

For complete configuration details, including upsert partitioning requirements, segment flush control, segment naming, and realtime table support, see the [Flink batch ingestion reference](../manage-data/data-import/batch-ingestion/flink.md).

## Additional Resources

* [Design proposal](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=177045634) -- Original motivation and architecture
* [Source code](https://github.com/apache/pinot/tree/master/pinot-connectors/pinot-flink-connector) -- Connector implementation on GitHub
* [FlinkQuickStart.java](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-flink-connector/src/main/java/org/apache/pinot/connector/flink/FlinkQuickStart.java) -- Runnable example
