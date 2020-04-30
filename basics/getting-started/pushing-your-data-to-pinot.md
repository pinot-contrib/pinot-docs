---
description: Step-by-step guide on pushing your own data into the Pinot cluster
---

# Batch upload sample data

So far, we setup our cluster, ran some queries, explored the admin endpoints. Now, it's time to get our own data into Pinot

### Preparing your data

Let's gather our data files and put it in `pinot-quick-start/rawdata`. 

```bash
mkdir -p /tmp/pinot-quick-start/rawdata
```

Supported file formats are CVS, JSON, AVRO, PARQUET, THRIFT, ORC. If you don't have sample data, you can use this sample CSV.

{% code title="/tmp/pinot-quick-start/rawdata/transcript.csv" %}
```bash
studentID,firstName,lastName,gender,subject,score,timestamp
200,Lucy,Smith,Female,Maths,3.8,1570863600000
200,Lucy,Smith,Female,English,3.5,1571036400000
201,Bob,King,Male,Maths,3.2,1571900400000
202,Nick,Young,Male,Physics,3.6,1572418800000
```
{% endcode %}

### Creating a schema

Schema is used to define the columns and data types of the Pinot table. A detailed overview of the schema can be found in [Schema](../../reference/components/schema.md).

Briefly, we categorize our columns into 3 types

| Column Type | Description |
| :--- | :--- |
| Dimensions | Typically used in filters and group by, for slicing and dicing into data |
| Metrics | Typically used in aggregations, represents the quantitative data |
| Time | Optional column, represents the timestamp associated with each row |

For example, in our sample table, the `playerID, yearID, teamID, league, playerName` columns are the dimensions, the `playerStint, numberOfgames, numberOfGamesAsBatter, AtBatting, runs, hits, doules, triples, homeRuns, runsBattedIn, stolenBases, caughtStealing, baseOnBalls, strikeouts, intentionalWalks, hitsByPitch, sacrificeHits, sacrificeFlies, groundedIntoDoublePlays, G_old` columns are the metrics and there is no time column.

Once you have identified the dimensions, metrics and time columns, create a schema for your data, using the reference below. 

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
  "timeFieldSpec": {
    "incomingGranularitySpec": {
      "name": "timestamp",
      "dataType": "LONG",
      "timeFormat" : "EPOCH",
      "timeType": "MILLISECONDS"
    }
  }
}
```
{% endcode %}

### Creating a table config

A table config is used to define the config related to the Pinot table. A detailed overview of the table can be found in [Table](../../reference/components/table.md). 

Here's the table config for the sample CSV file. You can use this as a reference to build your own table config. Simply edit the tableName and schemaName.

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

### Uploading your table config and schema

Check the directory structure so far

```bash
$ ls /tmp/pinot-quick-start
rawdata			transcript-schema.json	transcript-table-offline.json

$ ls /tmp/pinot-quick-start/rawdata 
transcript.csv
```

Upload the table config using the following command

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

Check out the table config and schema in the [Rest API](http://localhost:9000/help#!/Table/alterTableStateOrListTableConfig) to make sure it was successfully uploaded.

### Creating a segment

A Pinot table's data is stored as Pinot segments. A detailed overview of the segment can be found in [Segment](../../reference/components/segment.md). 

To generate a segment, we need to first create a job spec yaml file. JobSpec yaml file has all the information regarding data format, input data location and pinot cluster coordinates. You can just copy over this job spec file. If you're using your own data, be sure to 1\) replace `transcript` with your table name 2\) set the right `recordReaderSpec`

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

Use the following command to generate a segment and upload it

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

Sample output

```bash
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

Check that your segment made it to the table using the [Rest API](http://localhost:9000/help#!/Segment/getSegments)

### Querying your data

You're all set! You should see your table in the [Query Console](https://apache-pinot.gitbook.io/apache-pinot-cookbook/getting-started/exploring-pinot#query-console) and be able to run queries against it now.

![select \* from transcript](../../.gitbook/assets/screen-shot-2020-02-28-at-2.44.23-pm.png)

