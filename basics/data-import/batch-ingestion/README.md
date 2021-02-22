# Batch Ingestion

Batch ingestion allows users to create a table using data already present in a file system such as S3. This is particularly useful for the cases where the user wants to utilize Pinot's ability to query large data with minimal latency or test out new features using a simple data file.

Ingesting data from a filesystem involves the following steps -

1. Define Schema
2. Define Table Config
3. Upload Schema and Table configs
4. Upload data

Batch Ingestion currently supports the following mechanisms to upload the data -

* Standalone
* [Hadoop](hadoop.md)
* [Spark](spark.md)

Here we'll take a look at the standalone local processing to get you started.

Let's create a table for the following CSV data source.

```text
studentID,firstName,lastName,gender,subject,score,timestampInEpoch
200,Lucy,Smith,Female,Maths,3.8,1570863600000
200,Lucy,Smith,Female,English,3.5,1571036400000
201,Bob,King,Male,Maths,3.2,1571900400000
202,Nick,Young,Male,Physics,3.6,1572418800000
```

### Create Schema Configuration

In our data, the only column on which aggregations can be performed is score. Secondly, timestampInEpoch is the only timestamp column. So, on our schema, we keep score as metric and timestampInEpoch as timestamp column.

```text
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
    "name": "timestampInEpoch",
    "dataType": "LONG",
    "format" : "1:MILLISECONDS:EPOCH",
    "granularity": "1:MILLISECONDS"
  }]
}
```

Here, we have also defined two extra fields - format and granularity. The format specifies the formatting of our timestamp column in the data source. Currently, it is in milliseconds hence we have specified `1:MILLISECONDS:EPOCH`

### **Create Table Configuration**

We define a table`transcript`and map the schema created in the previous step to the table. For batch data, we keep the `tableType` as `OFFLINE`

```text
{
  "tableName": "transcript",
  "segmentsConfig" : {
    "timeColumnName": "timestampInEpoch",
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

### Upload Schema and Table

Now that we have both the configs, we can simply upload them and create a table. To achieve that, just run the command -

```text
bin/pinot-admin.sh AddTable \\
  -tableConfigFile /path/to/table-config.json \\
  -schemaFile /path/to/table-schema.json -exec
```

Check out the table config and schema in the \[Rest API\] to make sure it was successfully uploaded.

### **Upload data**

We now have an empty table in pinot. So as the next step we will upload our CSV file to this table. A table is composed of multiple segments.

The segments are created and uploaded using tasks known as DataIngestionJobs. A job also needs a config of its own. We call this config the JobSpec.

For our CSV file and table, the job spec should look like below.

```text
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
pinotClusterSpecs:
  - controllerURI: '<http://localhost:9000>'
```

You can refer to [Ingestion Job Spec](../../../configuration-reference/job-specification.md) for more details.

Now that we have the job spec for our table `transcript` , we can trigger the job using the following command

```text
bin/pinot-admin.sh LaunchDataIngestionJob \\
    -jobSpecFile /tmp/pinot-quick-start/batch-job-spec.yml
```

Once the job has successfully finished, you can head over to the \[query console\] and start playing with the data.

### Segment Push Job Type

There are 3 ways to upload a Pinot segment:

#### Segment Tar Push

This is the original and default push mechanism.

Tar push requires the segment

The push job will:

1. Upload the entire segment tar file to the Pinot controller. 

Pinot controller will:

1. Save the segment into the controller segment directory\(Local or any PinotFS\). 
2. Extract segment metadata.
3. Add the segment to the table.

#### Segment URI Push

This push mechanism requires the segment Tar file stored on a deep store with a globally accessible segment tar URI.

URI push is light-weight on the client-side, and the controller side requires equivalent work as the Tar push.

The push job will:

1. POST this segment Tar URI to the Pinot controller. 

Pinot controller will:

1. Download segment from the URI and save it to controller segment directory\(Local or any PinotFS\).
2. Extract segment metadata.
3. Add the segment to the table.

#### Segment Metadata Push

This push mechanism also requires the segment Tar file stored on a deep store with a globally accessible segment tar URI.

Metadata push is light-weight on the controller side, there is no deep store download involves from the controller side.

The push job will:

1. Download the segment based on URI.
2. Extract metadata.
3. Upload metadata to the Pinot Controller.

Pinot Controller will:

1. Add the segment to the table based on the metadata.

### Segment Fetchers

When pinot segment files are created in external systems \(Hadoop/spark/etc\), there are several ways to push those data to the Pinot Controller and Server:

1. Push segment to shared NFS and let pinot pull segment files from the location of that NFS. See [Segment URI Push](./#segment-uri-push).
2. Push segment to a Web server and let pinot pull segment files from the Web server with HTTP/HTTPS link. See [Segment URI Push](./#segment-uri-push).
3. Push segment to PinotFS\(HDFS/S3/GCS/ADLS\) and let pinot pull segment files from PinotFS URI. See [Segment URI Push](./#segment-uri-push) and [Segment Metadata Push](./#segment-metadata-push).
4. Push segment to other systems and implement your own segment fetcher to pull data from those systems.

The first three options are supported out of the box within the Pinot package. As long your remote jobs send Pinot controller with the corresponding URI to the files it will pick up the file and allocate it to proper Pinot Servers and brokers. To enable Pinot support for PinotFS, you will need to provide [PinotFS](../pinot-file-system/) configuration and proper Hadoop dependencies.

### Persistence

By default, Pinot does not come with a storage layer, so all the data sent, won't be stored in case of a system crash. In order to persistently store the generated segments, you will need to change controller and server configs to add deep storage. Checkout [File systems](../pinot-file-system/) for all the info and related configs.

### Tuning

#### **Standalone**

Since pinot is written in Java, you can set the following basic java configurations to tune the segment runner job -

* Log4j2 file location with `-Dlog4j2.configurationFile`
* Plugin directory location with `-Dplugins.dir=/opt/pinot/plugins`
* JVM props, like `-Xmx8g -Xms4G`

If you are using the docker, you can set the following under `JAVA_OPTS` variable.

#### Hadoop

You can set `-D mapreduce.map.memory.mb=8192` to set the mapper memory size when submitting the Hadoop job.

#### Spark

You can add config `spark.executor.memory` to tune the memory usage for segment creation when submitting the Spark job.

