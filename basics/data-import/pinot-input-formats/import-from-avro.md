---
description: This guide shows you how to import records into Pinot using Avro file format.
---

# Import from Avro

## Introduction

In this guide, you'll learn how to create a job specification for importing data into Pinot using an Avro file. This guide does not provide you with the avro file to import, since it is a binary file. The JSON file will be provided, and you will need to generate the Avro file on your machine.

### Preparing your data

First, let's create sample data to load into Pinot. You can create a temporary directory to put the sample Avro file, which we will reference later in the job specification configuration.

```bash
mkdir -p /tmp/pinot-quick-start/rawdata
```

Copy the following sample JSON file into the directory you created in the previous step.

{% code title="/tmp/pinot-quick-start/rawdata/transcript.json" %}
```bash
{"studentID":205,"firstName":"Natalie","lastName":"Jones","gender":"Female","subject":"Maths","score":3.8,"timestamp":1571900400000}
{"studentID":205,"firstName":"Natalie","lastName":"Jones","gender":"Female","subject":"History","score":3.5,"timestamp":1571900400000}
{"studentID":207,"firstName":"Bob","lastName":"Lewis","gender":"Male","subject":"Maths","score":3.2,"timestamp":1571900400000}
{"studentID":207,"firstName":"Bob","lastName":"Lewis","gender":"Male","subject":"Chemistry","score":3.6,"timestamp":1572418800000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Geography","score":3.8,"timestamp":1572505200000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"English","score":3.5,"timestamp":1572505200000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Maths","score":3.2,"timestamp":1572678000000}
{"studentID":209,"firstName":"Jane","lastName":"Doe","gender":"Female","subject":"Physics","score":3.6,"timestamp":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"Maths","score":3.8,"timestamp":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"English","score":3.5,"timestamp":1572678000000}
{"studentID":211,"firstName":"John","lastName":"Doe","gender":"Male","subject":"History","score":3.2,"timestamp":1572854400000}
{"studentID":212,"firstName":"Nick","lastName":"Young","gender":"Male","subject":"History","score":3.6,"timestamp":1572854400000}
```
{% endcode %}

Now you will need to generate an Avro file using this JSON file. Use the following Avro schema file to generate the Avro file from the JSON snippet above.

{% code title="/tmp/pinot-quick-start/rawdata/transcript.avsc" %}
```javascript
{
  "name": "MyClass",
  "type": "record",
  "namespace": "com.acme.avro",
  "fields": [
    {
      "name": "studentID",
      "type": "int"
    },
    {
      "name": "firstName",
      "type": "string"
    },
    {
      "name": "lastName",
      "type": "string"
    },
    {
      "name": "gender",
      "type": "string"
    },
    {
      "name": "subject",
      "type": "string"
    },
    {
      "name": "score",
      "type": "float"
    },
    {
      "name": "timestamp",
      "type": "long"
    }
  ]
}
```
{% endcode %}

Save this file to the directory that you saved the JSON dataset to, and run the following Avro command.

```bash
java -jar avro-tools-1.9.2.jar fromjson --schema-file transcript.avsc transcript.json > transcript.avro
```

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
transcript.json
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
includeFileNamePattern: 'glob:**/*.avro'
outputDirURI: '/tmp/pinot-quick-start/segments/'
overwriteOutput: true
pinotFSSpecs:
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS
recordReaderSpec:
  dataFormat: 'avro'
  className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReaderConfig'
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
includeFileNamePattern: 'glob:**/*.avro'
outputDirURI: '/tmp/pinot-quick-start/segments/'
overwriteOutput: true
pinotFSSpecs:
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS
recordReaderSpec:
  dataFormat: 'avro'
  className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReaderConfig'
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

Use the following command to create the segment and upload the data records from the Avro file.

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

Check that your segment made it to the table using the [REST API](http://localhost:9000/help#!/Segment/getSegments).

## Query the batch imported data

Now that you've created and uploaded the job specification with the raw data in the Avro file, you can query the results.

```sql
SELECT * FROM transcript
```



