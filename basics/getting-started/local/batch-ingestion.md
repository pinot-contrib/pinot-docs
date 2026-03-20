---
description: Step-by-step guide for batch importing data into a local Pinot installation
---

# Batch ingestion (local)

This guide walks you through importing batch data into a Pinot cluster running locally. Make sure you have completed [Running Pinot locally](../local/) first.

## Prepare your data

Create a directory for your data files:

```bash
mkdir -p /tmp/pinot-quick-start/rawdata
```

Supported file formats are CSV, JSON, AVRO, PARQUET, THRIFT, ORC. If you don't have sample data, you can use this sample CSV.

{% code title="/tmp/pinot-quick-start/rawdata/transcript.csv" %}
```bash
studentID,firstName,lastName,gender,subject,score,timestampInEpoch
200,Lucy,Smith,Female,Maths,3.8,1570863600000
200,Lucy,Smith,Female,English,3.5,1571036400000
201,Bob,King,Male,Maths,3.2,1571900400000
202,Nick,Young,Male,Physics,3.6,1572418800000
```
{% endcode %}

## Create a schema

Schema is used to define the columns and data types of the Pinot table. A detailed overview of the schema can be found in [Schema](../../../configuration-reference/schema.md).

| Column Type | Description                                                              |
| ----------- | ------------------------------------------------------------------------ |
| Dimensions  | Typically used in filters and group by, for slicing and dicing into data |
| Metrics     | Typically used in aggregations, represents the quantitative data         |
| Time        | Optional column, represents the timestamp associated with each row       |

In our example, the `studentID, firstName, lastName, gender, subject` columns are the dimensions, `score` is the metric, and `timestampInEpoch` is the time column.

{% code title="/tmp/pinot-quick-start/transcript-schema.json" %}
```json
{
  "schemaName": "transcript",
  "dimensionFieldSpecs": [
    { "name": "studentID", "dataType": "INT" },
    { "name": "firstName", "dataType": "STRING" },
    { "name": "lastName", "dataType": "STRING" },
    { "name": "gender", "dataType": "STRING" },
    { "name": "subject", "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "score", "dataType": "FLOAT" }
  ],
  "dateTimeFieldSpecs": [{
    "name": "timestampInEpoch",
    "dataType": "LONG",
    "format": "1:MILLISECONDS:EPOCH",
    "granularity": "1:MILLISECONDS"
  }]
}
```
{% endcode %}

## Create a table configuration

{% code title="/tmp/pinot-quick-start/transcript-table-offline.json" %}
```json
{
  "tableName": "transcript",
  "segmentsConfig": {
    "timeColumnName": "timestampInEpoch",
    "timeType": "MILLISECONDS",
    "replication": "1",
    "schemaName": "transcript"
  },
  "tableIndexConfig": {
    "invertedIndexColumns": [],
    "loadMode": "MMAP"
  },
  "tenants": {
    "broker": "DefaultTenant",
    "server": "DefaultTenant"
  },
  "tableType": "OFFLINE",
  "metadata": {}
}
```
{% endcode %}

## Upload the schema and table configuration

```bash
bin/pinot-admin.sh AddTable \
  -tableConfigFile /tmp/pinot-quick-start/transcript-table-offline.json \
  -schemaFile /tmp/pinot-quick-start/transcript-schema.json -exec
```

## Create and push a segment

1. Create a job specification file:

{% code title="/tmp/pinot-quick-start/batch-job-spec.yml" %}
```yaml
executionFrameworkSpec:
  name: 'standalone'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
jobType: SegmentCreationAndTarPush
inputDirURI: '/tmp/pinot-quick-start/rawdata/'
includeFileNamePattern: 'glob:**/*.csv'
outputDirURI: '/tmp/pinot-quick-start/segments/'
overwriteOutput: true
pinotFSSpecs:
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS
recordReaderSpec:
  dataFormat: 'csv'
  className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
  tableName: 'transcript'
  schemaURI: 'http://localhost:9000/tables/transcript/schema'
  tableConfigURI: 'http://localhost:9000/tables/transcript'
pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'
```
{% endcode %}

2. Run the ingestion job:

```bash
bin/pinot-admin.sh LaunchDataIngestionJob \
    -jobSpecFile /tmp/pinot-quick-start/batch-job-spec.yml
```

## Query your data

Open the [Query Console](http://localhost:9000/query) in your browser to run queries against the `transcript` table.
