---
description: Batch ingestion of data into Apache Pinot using Apache Flink.
---

# Flink

Pinot supports Apache Flink as a processing framework to push segment files to the database.

Pinot distribution contains an Apache Flink [SinkFunction](https://nightlies.apache.org/flink/flink-docs-release-1.12/api/java/org/apache/flink/streaming/api/functions/sink/SinkFunction.html) that can be used as part of the Apache Flink application (Streaming or Batch) to directly write into a designated Pinot database.

## Example

### Flink application

Here is an example code snippet to show how to utilize the [PinotSinkFunction](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-flink-connector/src/main/java/org/apache/pinot/connector/flink/sink/PinotSinkFunction.java) in a Flink streaming application:

```
// some environmental setup
StreamExecutionEnvironment execEnv = StreamExecutionEnvironment.getExecutionEnvironment();
DataStream<Row> srcRows = execEnv.addSource(new FlinkKafkaConsumer<Row>(...));
RowTypeInfo typeInfo = new RowTypeInfo(
  new TypeInformation[]{Types.FLOAT, Types.FLOAT, Types.STRING, Types.STRING},
  new String[]{"lon", "lat", "address", "name"});


// add processing logic for the data stream for example:
DataStream<Row> processedRows = srcRow.keyBy(r -> r.getField(0));
...

// configurations for PinotSinkFunction
Schema pinotSchema = ...
TableConfig pinotTableConfig = ...
processedRows.addSink(new PinotSinkFunction<>(
  new FlinkRowGenericRowConverter(typeInfo), 
  pinotTableConfig,
  pinotSchema);

// execute the program
execEnv.execute();
```

As in the example shown above, the only required information from the Pinot side is the table [schema](../../../configuration-reference/schema.md) and the table [config](../../../configuration-reference/table.md).

For a more detailed executable, refer to the [quick start example](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-flink-connector/src/main/java/org/apache/pinot/connector/flink/FlinkQuickStart.java).

### Table Config

PinotSinkFunction uses mostly the TableConfig object to infer the batch ingestion configuration to start a SegmentWriter and SegmentUploader to communicate with the Pinot cluster.&#x20;

Note that even though in the above example Flink application is running in streaming mode, the data is still batch together and flush/upload to Pinot once the flush threshold is reached. It is not a direct streaming write into Pinot.

Here is an example table config

```
{
  "tableName" : "tbl_OFFLINE",
  "tableType" : "OFFLINE",
  "segmentsConfig" : {
    // ...
  },
  "tenants" : {
    // ...
  },
  "tableIndexConfig" : {
    // ....
  },
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "HOURLY", 
      "batchConfigMaps": [
        {
          "outputDirURI": "file://path/to/flink/segmentwriter/output/dir",
          "overwriteOutput": "false",
          "push.controllerUri": "https://target.pinot.cluster.controller.url"
        }
      ]
    }
  }
}

```

the only required configurations are:

* `"outputDirURI"`: where PinotSinkFunction should write the constructed segment file to
* `"push.controllerUri"`: which Pinot cluster (controller) URL PinotSinkFunction should communicate with.

The rest of the configurations are standard for any Pinot table.



















