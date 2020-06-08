---
description: This guide shows you how to import a CSV file of records into Pinot.
---

# Import from CSV

## Introduction

In this guide, you'll learn how to create a job specification for importing data into Pinot using a CSV file.

### Preparing your data

First, let's create sample data to load into Pinot. You can create a temporary directory to put the sample CSV file, which we will reference later in the job specification configuration.

```bash
mkdir -p /tmp/pinot-quick-start/rawdata
```

Copy the following sample CSV file into the directory you created in the previous step.

{% code title="/tmp/pinot-quick-start/rawdata/transcript.csv" %}
```bash
studentID,firstName,lastName,gender,subject,score,timestamp
200,Lucy,Smith,Female,Maths,3.8,1570863600000
200,Lucy,Smith,Female,English,3.5,1571036400000
201,Bob,King,Male,Maths,3.2,1571900400000
202,Nick,Young,Male,Physics,3.6,1572418800000
```
{% endcode %}

## Creating a schema configuration

If you followed the [batch upload sample data](../../getting-started/pushing-your-data-to-pinot.md), you have already created a schema for your sample table. If not, head over to [creating a schema](../../getting-started/pushing-your-data-to-pinot.md#creating-a-schema) on that page, to learn how to create a schema for your sample data. To make it easy, the schema from that page is included here.

{% code title="/tmp/pinot-quick-start/transcript-schema.json" %}
```bash
{
  "schemaName": "transcript",
  "dimensionFieldSpecs": [
    {
      "name": "studentID",
      "dataType": "INT"
    },
    {
      "name": "firstName",
      "dataType": "STRING"
    },
    {
      "name": "lastName",
      "dataType": "STRING"
    },
    {
      "name": "gender",
      "dataType": "STRING"
    },
    {
      "name": "subject",
      "dataType": "STRING"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "score",
      "dataType": "FLOAT"
    }
  ],
  "dateTimeFieldSpecs": [{
    "name": "timestamp",
    "dataType": "LONG",
    "format" : "1:MILLISECONDS:EPOCH",
    "granularity": "1:MILLISECONDS"
  }]
}
```
{% endcode %}

## Creating a table configuration

If you followed [batch upload sample data](../../getting-started/pushing-your-data-to-pinot.md), you learned how to push an offline table and schema. Similar to the offline table config, we will create a real-time table config for this sample. Here's the real-time table configuration for the `transcript` table described in the schema from the previous step. For a more detailed overview about tables, check out the [table](../../components/table.md) reference.

{% code title="/tmp/pinot-quick-start/transcript-table-offline.json" %}
```bash
{
  "tableName": "transcript",
  "segmentsConfig" : {
    "timeColumnName": "timestamp",
    "timeType": "MILLISECONDS",
    "replication" : "1",
    "schemaName" : "transcript"
  },
  "tableIndexConfig" : {
    "invertedIndexColumns" : [],
    "loadMode"  : "MMAP"
  },
  "tenants" : {
    "broker":"DefaultTenant",
    "server":"DefaultTenant"
  },
  "tableType":"OFFLINE",
  "metadata": {}
}
```
{% endcode %}

## Create schema and table

The directory structure for this guide should now look like the following.

```bash
$ ls /tmp/pinot-quick-start
rawdata			transcript-schema.json	transcript-table-offline.json

$ ls /tmp/pinot-quick-start/rawdata 
transcript.csv
```

Upload the schema and table config using the following command. This will create the table that we will batch import records to.

{% tabs %}
{% tab title="Docker" %}
```bash
docker run --rm -ti \
    --network=pinot-demo \
    -v /tmp/pinot-quick-start:/tmp/pinot-quick-start \
    --name pinot-batch-table-creation \
    apachepinot/pinot:latest AddTable \
    -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
    -tableConfigFile /tmp/pinot-quick-start/transcript-table-offline.json \
    -controllerHost pinot-quickstart \
    -controllerPort 9000 -exec
```
{% endtab %}

{% tab title="Launcher Script" %}
```bash
bin/pinot-admin.sh AddTable \
  -tableConfigFile /tmp/pinot-quick-start/transcript-table-offline.json \
  -schemaFile /tmp/pinot-quick-start/transcript-schema.json -exec
```
{% endtab %}
{% endtabs %}

You can check out the table config and schema in the [REST API](http://localhost:9000/help#!/Table/alterTableStateOrListTableConfig) to make sure it was successfully uploaded.

## Creating a segment

Table data is stored in Pinot segments. A detailed overview of the segment can be found in [segment](../../components/segment.md). 

To create a segment, we need to first create a job specification `yaml` file. The job specification yaml file should have all of the information regarding the data format, input file location, and Pinot cluster coordinates. Copy the following `batch-job-spec.yml` file and save it to your directory, which should be `/tmp/pinot-quick-start`.

{% tabs %}
{% tab title="Launcher Script" %}
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
{% endtab %}

{% tab title="Docker" %}
{% code title="/tmp/pinot-quick-start/docker-job-spec.yml" %}
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
  schemaURI: 'http://pinot-quickstart:9000/tables/transcript/schema'
  tableConfigURI: 'http://pinot-quickstart:9000/tables/transcript'
pinotClusterSpecs:
  - controllerURI: 'http://pinot-quickstart:9000'
```
{% endcode %}
{% endtab %}
{% endtabs %}

Use the following command to create the segment and upload the data records from the CSV file.

{% tabs %}
{% tab title="Docker" %}
```text
docker run --rm -ti \
    --network=pinot-demo \
    -v /tmp/pinot-quick-start:/tmp/pinot-quick-start \
    --name pinot-data-ingestion-job \
    apachepinot/pinot:latest LaunchDataIngestionJob \
    -jobSpecFile /tmp/pinot-quick-start/docker-job-spec.yml
```
{% endtab %}

{% tab title="Using launcher scripts" %}
```text
bin/pinot-admin.sh LaunchDataIngestionJob \
    -jobSpecFile /tmp/pinot-quick-start/batch-job-spec.yml
```
{% endtab %}
{% endtabs %}

Sample output:

```text
SegmentGenerationJobSpec: 
!!org.apache.pinot.spi.ingestion.batch.spec.SegmentGenerationJobSpec
excludeFileNamePattern: null
executionFrameworkSpec: {extraConfigs: null, name: standalone, segmentGenerationJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner,
  segmentTarPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner,
  segmentUriPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner}
includeFileNamePattern: glob:**\/*.csv
inputDirURI: /tmp/pinot-quick-start/rawdata/
jobType: SegmentCreationAndTarPush
outputDirURI: /tmp/pinot-quick-start/segments
overwriteOutput: true
pinotClusterSpecs:
- {controllerURI: 'http://localhost:9000'}
pinotFSSpecs:
- {className: org.apache.pinot.spi.filesystem.LocalPinotFS, configs: null, scheme: file}
pushJobSpec: null
recordReaderSpec: {className: org.apache.pinot.plugin.inputformat.csv.CSVRecordReader,
  configClassName: org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig,
  configs: null, dataFormat: csv}
segmentNameGeneratorSpec: null
tableSpec: {schemaURI: 'http://localhost:9000/tables/transcript/schema', tableConfigURI: 'http://localhost:9000/tables/transcript',
  tableName: transcript}

Trying to create instance for class org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner
Initializing PinotFS for scheme file, classname org.apache.pinot.spi.filesystem.LocalPinotFS
Finished building StatsCollector!
Collected stats for 4 documents
Using fixed bytes value dictionary for column: studentID, size: 9
Created dictionary for STRING column: studentID with cardinality: 3, max length in bytes: 3, range: 200 to 202
Using fixed bytes value dictionary for column: firstName, size: 12
Created dictionary for STRING column: firstName with cardinality: 3, max length in bytes: 4, range: Bob to Nick
Using fixed bytes value dictionary for column: lastName, size: 15
Created dictionary for STRING column: lastName with cardinality: 3, max length in bytes: 5, range: King to Young
Created dictionary for FLOAT column: score with cardinality: 4, range: 3.2 to 3.8
Using fixed bytes value dictionary for column: gender, size: 12
Created dictionary for STRING column: gender with cardinality: 2, max length in bytes: 6, range: Female to Male
Using fixed bytes value dictionary for column: subject, size: 21
Created dictionary for STRING column: subject with cardinality: 3, max length in bytes: 7, range: English to Physics
Created dictionary for LONG column: timestamp with cardinality: 4, range: 1570863600000 to 1572418800000
Start building IndexCreator!
Finished records indexing in IndexCreator!
Finished segment seal!
Converting segment: /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0 to v3 format
v3 segment location for segment: transcript_OFFLINE_1570863600000_1572418800000_0 is /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0/v3
Deleting files in v1 segment directory: /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0
Starting building 1 star-trees with configs: [StarTreeV2BuilderConfig[splitOrder=[studentID, firstName],skipStarNodeCreation=[],functionColumnPairs=[org.apache.pinot.core.startree.v2.AggregationFunctionColumnPair@3a48efdc],maxLeafRecords=1]] using OFF_HEAP builder
Starting building star-tree with config: StarTreeV2BuilderConfig[splitOrder=[studentID, firstName],skipStarNodeCreation=[],functionColumnPairs=[org.apache.pinot.core.startree.v2.AggregationFunctionColumnPair@3a48efdc],maxLeafRecords=1]
Generated 3 star-tree records from 4 segment records
Finished constructing star-tree, got 9 tree nodes and 4 records under star-node
Finished creating aggregated documents, got 6 aggregated records
Finished building star-tree in 10ms
Finished building 1 star-trees in 27ms
Computed crc = 3454627653, based on files [/var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0/v3/columns.psf, /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0/v3/index_map, /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0/v3/metadata.properties, /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0/v3/star_tree_index, /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0/v3/star_tree_index_map]
Driver, record read time : 0
Driver, stats collector time : 0
Driver, indexing time : 0
Tarring segment from: /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0 to: /var/folders/3z/qn6k60qs6ps1bb6s2c26gx040000gn/T/pinot-1583443148720/output/transcript_OFFLINE_1570863600000_1572418800000_0.tar.gz
Size for segment: transcript_OFFLINE_1570863600000_1572418800000_0, uncompressed: 6.73KB, compressed: 1.89KB
Trying to create instance for class org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner
Initializing PinotFS for scheme file, classname org.apache.pinot.spi.filesystem.LocalPinotFS
Start pushing segments: [/tmp/pinot-quick-start/segments/transcript_OFFLINE_1570863600000_1572418800000_0.tar.gz]... to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@243c4f91] for table transcript
Pushing segment: transcript_OFFLINE_1570863600000_1572418800000_0 to location: http://localhost:9000 for table transcript
Sending request: http://localhost:9000/v2/segments?tableName=transcript to controller: nehas-mbp.hsd1.ca.comcast.net, version: Unknown
Response for pushing table transcript segment transcript_OFFLINE_1570863600000_1572418800000_0 to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: transcript_OFFLINE_1570863600000_1572418800000_0 of table: transcript"}
```

Check that your segment made it to the table using the [REST API](http://localhost:9000/help#!/Segment/getSegments).

## Query the batch imported data

Now that you've created and uploaded the job specification with the raw data in the CSV file, you can query the results.

```sql
SELECT * FROM transcript
```

