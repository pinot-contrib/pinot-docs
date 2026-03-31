---
description: Batch ingestion of data into Apache Pinot using Apache Flink.
---

# Flink

Apache Pinot supports using Apache Flink as a processing framework to generate and upload segments. The Pinot distribution includes a [PinotSinkFunction](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-flink-connector/src/main/java/org/apache/pinot/connector/flink/sink/PinotSinkFunction.java) that can be integrated into Flink applications (streaming or batch) to directly write data as segments into Pinot tables.

The `PinotSinkFunction` supports offline tables, realtime tables, and upsert tables (full upsert only). Data is buffered in memory and flushed as segments when the configured threshold is reached, then uploaded to the Pinot cluster.

## Maven Dependency

To use the Pinot Flink Connector in your Flink job, add the following dependency to your `pom.xml`:

```xml
<dependency>
  <groupId>org.apache.pinot</groupId>
  <artifactId>pinot-flink-connector</artifactId>
  <version>1.5.0-SNAPSHOT</version>
</dependency>
```

Replace `1.5.0-SNAPSHOT` with the Pinot version you're using. For the latest stable version, check the [Apache Pinot releases](https://pinot.apache.org/download/).

**Note**: The connector transitively includes dependencies for:
- `pinot-controller` - For controller client APIs
- `pinot-segment-writer-file-based` - For segment generation
- `flink-streaming-java` and `flink-java` - Flink core dependencies

## Offline Table Ingestion

### Quick Start Example

```java
// Set up Flink environment and data source
StreamExecutionEnvironment execEnv = StreamExecutionEnvironment.getExecutionEnvironment();
execEnv.setParallelism(2);

// Configure row type
RowTypeInfo typeInfo = new RowTypeInfo(
    new TypeInformation[]{Types.FLOAT, Types.FLOAT, Types.STRING, Types.STRING},
    new String[]{"lon", "lat", "address", "name"});

DataStream<Row> srcRows = execEnv.addSource(new FlinkKafkaConsumer<Row>(...));

// Create a ControllerRequestClient to fetch Pinot schema and table config
HttpClient httpClient = HttpClient.getInstance();
ControllerRequestClient client = new ControllerRequestClient(
    ControllerRequestURLBuilder.baseUrl(DEFAULT_CONTROLLER_URL), httpClient);

// Fetch Pinot schema
Schema schema = PinotConnectionUtils.getSchema(client, "starbucksStores");
// Fetch Pinot table config
TableConfig tableConfig = PinotConnectionUtils.getTableConfig(client, "starbucksStores", "OFFLINE");

// Create Flink Pinot Sink
srcRows.addSink(new PinotSinkFunction<>(
    new FlinkRowGenericRowConverter(typeInfo),
    tableConfig,
    schema));
execEnv.execute();
```

### Table Configuration

The `PinotSinkFunction` uses the TableConfig to determine batch ingestion settings for segment generation and upload. Here's an example table configuration:

```json
{
  "tableName": "starbucksStores_OFFLINE",
  "tableType": "OFFLINE",
  "segmentsConfig": {
    // ...
  },
  "tenants": {
    // ...
  },
  "tableIndexConfig": {
    // ...
  },
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "HOURLY",
      "batchConfigMaps": [
        {
          "outputDirURI": "file:///tmp/pinotoutput",
          "overwriteOutput": "false",
          "push.controllerUri": "http://localhost:9000"
        }
      ]
    }
  }
}
```

Required configurations:
* `outputDirURI` - Directory where segments are written before upload
* `push.controllerUri` - Pinot controller URL for segment upload

For a complete executable example, refer to [FlinkQuickStart.java](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-flink-connector/src/main/java/org/apache/pinot/connector/flink/FlinkQuickStart.java).

## Realtime Table Ingestion

### Non-Upsert Realtime Tables

For standard realtime tables without upsert, use the same approach as offline tables, but specify `REALTIME` as the table type:

```java
// Same setup as offline table example above...

// Fetch table config for realtime table
TableConfig tableConfig = PinotConnectionUtils.getTableConfig(client, "myTable", "REALTIME");

// Same sink configuration
srcRows.addSink(new PinotSinkFunction<>(
    new FlinkRowGenericRowConverter(typeInfo),
    tableConfig,
    schema));
execEnv.execute();
```

### Upsert Tables

#### Full Upsert Tables

Flink connector supports backfilling full upsert tables where each record contains all columns. The uploaded segments will correctly participate in upsert semantics based on the comparison column value.

**Requirements:**
1. **Partitioning**: Data must be partitioned using the same strategy as the upstream stream (e.g., Kafka)
2. **Parallelism**: Flink job parallelism must match the number of upstream stream/table partitions
3. **Comparison Column**: The values of the comparison column  must have ordering consistent with the upstream stream. This ensures that Pinot can correctly resolve which record is the latest for a given key. See [Pinot upsert comparison column docs](../upsert-and-dedup/upsert.md#comparison-column) for important considerations.

**Example:**

```java
// Set up Flink environment
StreamExecutionEnvironment execEnv = StreamExecutionEnvironment.getExecutionEnvironment();
execEnv.setParallelism(2); // MUST match number of partitions in stream/table

// Configure row type matching your upsert table schema
RowTypeInfo typeInfo = new RowTypeInfo(
    new TypeInformation[]{Types.INT, Types.STRING, Types.STRING, Types.FLOAT, Types.LONG, Types.BOOLEAN},
    new String[]{"playerId", "name", "game", "score", "timestampInEpoch", "deleted"});

DataStream<Row> srcRows = execEnv.addSource(new FlinkKafkaConsumer<Row>(...));

// Fetch schema and table config (same as offline table example)
// HttpClient httpClient = HttpClient.getInstance();
// ControllerRequestClient client = ...
Schema schema = PinotConnectionUtils.getSchema(client, "myUpsertTable");
TableConfig tableConfig = PinotConnectionUtils.getTableConfig(client, "myUpsertTable", "REALTIME");

// IMPORTANT: Partition data by primary key using the SAME logic as the stream
srcRows.partitionCustom(
    (Partitioner<Integer>) (key, partitions) -> key % partitions,
    r -> (Integer) r.getField("playerId"))  // Primary key field
  .addSink(new PinotSinkFunction<>(
      new FlinkRowGenericRowConverter(typeInfo),
      tableConfig,
      schema));
execEnv.execute();
```

**How Partitioning Works:**

When uploading segments for upsert tables, Pinot uses a special segment naming convention [UploadedRealtimeSegmentName](https://github.com/apache/pinot/blob/7f701245ca71c482ce71456e4e5082bfa82d5e14/pinot-common/src/main/java/org/apache/pinot/common/utils/UploadedRealtimeSegmentName.java) that encodes the partition ID. The format is:
```
{prefix}__{tableName}__{partitionId}__{uploadTimeMs}__{sequenceId}
```

Example: `flink__myTable__0__1724045187__1`

Each Flink subtask generates segments for a specific partition based on its subtask index. The segments are then assigned to the same server instances that handle that partition for stream-consumed segments, ensuring correct upsert behavior across all segments.

**Configuration Options:**

You can customize segment generation using additional constructor parameters:

```java
new PinotSinkFunction<>(
    recordConverter,
    tableConfig,
    schema,
    segmentFlushMaxNumRecords,  // Default: 500,000, number of rows per segment
    executorPoolSize,            // Default: 5, number of threads to use to upload segment
    segmentNamePrefix,           // Default: "flink"
    segmentUploadTimeMs          // Default: current time, upload time value to encode in segment name
)
```

#### Partial Upsert Tables

**WARNING**: Flink-based upload is **not recommended** for partial upsert tables.

In partial upsert tables, uploaded segments contain only a subset of columns or an intermdiate row for a primary key. If the uploaded row is not in its final state and subsequent updates arrive via the stream, the partial upsert merger may produce inconsistent results between replicas. This can lead to data inconsistency that is difficult to detect and resolve.

For partial upsert tables, prefer stream-based ingestion only or ensure uploaded data represents the final state for each primary key.

## Advanced Configuration

### Segment Flush Control

Control when segments are flushed and uploaded:

```java
// Same setup as previous examples...

long segmentFlushMaxNumRecords = 1000000; // Flush after 1M records
int executorPoolSize = 10; // Thread pool size for async uploads

srcRows.addSink(new PinotSinkFunction<>(
    new FlinkRowGenericRowConverter(typeInfo),
    tableConfig,
    schema,
    segmentFlushMaxNumRecords,
    executorPoolSize
));
```

### Segment Naming

Customize segment naming and upload time for better organization:

```java
// Same setup as previous examples...

String segmentNamePrefix = "flink_job_daily";
Long segmentUploadTimeMs = 1724045185000L; // Group segments by upload run time

srcRows.addSink(new PinotSinkFunction<>(
    new FlinkRowGenericRowConverter(typeInfo),
    tableConfig,
    schema,
    DEFAULT_SEGMENT_FLUSH_MAX_NUM_RECORDS,
    DEFAULT_EXECUTOR_POOL_SIZE,
    segmentNamePrefix,
    segmentUploadTimeMs
));
```

## Additional Resources

* [Design Proposal](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=177045634) - Original design motivation
* [PR #13107](https://github.com/apache/pinot/pull/13107) - Externally partitioned segments for upsert tables
* [PR #13837](https://github.com/apache/pinot/pull/13837) - Flink connector enhancements for upsert backfill
* [Table Configuration Reference](../../../reference/configuration-reference/table.md)
* [Schema Configuration Reference](../../../reference/configuration-reference/schema.md)
