# Spark Pinot Connector Write Model

{% hint style="warning" %}
Caution: This feature is experimental and the API may change in future releases.
{% endhint %}

Spark Connector also has experimental support for writing Pinot segments from Spark DataFrames. The current implementation writes OFFLINE segment tar files to the destination path supplied via `.save(path)` (or the equivalent `path` option), and the schema of the DataFrame should match the schema of the Pinot table. The examples below use `append` mode.

```
// create sample data
val data = Seq(
  ("ORD", "Florida", 1000, true, 1722025994),
  ("ORD", "Florida", 1000, false, 1722025994),
  ("ORD", "Florida", 1000, false, 1722025994),
  ("NYC", "New York", 20, true, 1722025994),
)

val airports = spark.createDataFrame(data)
  .toDF("airport", "state", "distance", "active", "ts")
  .repartition(2)

airports.write.format("pinot")
  .mode("append")
  .option("table", "airlineStats")
  .option("segmentNameFormat", "{table}_{startTime}_{endTime}_{partitionId:03}")
  .option("invertedIndexColumns", "airport")
  .option("noDictionaryColumns", "airport,state")
  .option("bloomFilterColumns", "airport")
  .option("rangeIndexColumns", "distance")
  .option("timeColumnName", "ts")
  .option("timeFormat", "EPOCH|SECONDS")
  .option("timeGranularity", "1:SECONDS")
  .save("myPath")
```

`.save("myPath")` provides the required `path` option automatically. The writer reads the options below and uses them to build Pinot segment metadata and indexes before pushing `tar.gz` segment files to the target filesystem.

### Connector Write Parameters

| Configuration | Description | Required | Default Value |
| ------------- | ----------- | -------- | ------------- |
| `table` | Pinot table name used for generated segment metadata and schema translation. | Yes | - |
| `path` | Destination directory for generated segment tar files. Calling `.save("...")` sets this option automatically. The current implementation pushes to local filesystems and HDFS. | Yes | - |
| `segmentNameFormat` | Segment name template. Supports `{table}`, `{partitionId}`, `{startTime}`, and `{endTime}` placeholders, plus zero-padding such as `{partitionId:03}`. `startTime` and `endTime` are populated from the minimum and maximum values of a numeric `timeColumnName`. | No | `<tableName>-{partitionId:03}` |
| `invertedIndexColumns` | Comma-separated list of columns that should use Pinot inverted indexes in generated segments. | No | Empty |
| `noDictionaryColumns` | Comma-separated list of columns that should disable dictionary encoding in generated segments. | No | Empty |
| `bloomFilterColumns` | Comma-separated list of columns that should use Pinot bloom filters in generated segments. | No | Empty |
| `rangeIndexColumns` | Comma-separated list of columns that should use Pinot range indexes in generated segments. | No | Empty |
| `timeColumnName` | Pinot time column name to emit in the generated schema and segment metadata. When set, `timeFormat` and `timeGranularity` must also be set. | No | None |
| `timeFormat` | Pinot date-time format for `timeColumnName`, for example `EPOCH|SECONDS`. | Conditionally required | None |
| `timeGranularity` | Pinot granularity for `timeColumnName`, for example `1:SECONDS`. | Conditionally required | None |

### Validation And Behavior Notes

* `table` and `path` are required. The writer rejects requests that omit either option.
* `segmentNameFormat` cannot be an empty string.
* If `timeColumnName` is set, both `timeFormat` and `timeGranularity` must also be set.
* `tableType` is not part of the current write option contract. The writer builds OFFLINE segments regardless of any `tableType` option passed to Spark.

For more details, refer to the implementation at `org.apache.pinot.connector.spark.v3.datasource.PinotDataWriter` and `org.apache.pinot.connector.spark.common.PinotDataSourceWriteOptions`.
