# Batch Ingestion

Batch ingestion allows user to create a table using data already present in a file system such as S3. This is particularly useful for the cases where the user wants to utilise Pinot's ability to query large data with minimal latency or test out new features using a simple data file.

Ingesting data from a filesystem involves the following steps -

1. Define Schema
2. Define Table Config
3. Upload Schema and Table configs
4. Upload data

Batch Ingestion currently supports following mechanisms to upload the data -

* Standalone
* [Hadoop](hadoop.md)
* [Spark](spark.md)

Here we'll take a look at the standalone local processing to get you started.

Let's create a table for the following CSV datasource.

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

Here, we have also defined two extra fields - format and granularity. Format specifies the formatting of our timestamp column in the data source. Currently, it is in milliseconds hence we have specified `1:MILLISECONDS:EPOCH`

### **Create Table Configuration**

We define a table named  `transcript`  and map the schema created in the previous step to the table. For batch data, we keep the tableType as `OFFLINE`

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

For any other batch job, you can change the following parameters

1. **tableName** - The name of the table to put the data in
2. **recordReaderSpec** - This should match the format of the input data. e.g. CSV, Avro, ProtoBuf etc.
3. **pinotClusterSpecs** - URL of controller node.
4. **inputDirURI** and **outputDirURI**
5. **includeFileNamePattern** - pattern to match files inside the input directory. supports both [`glob`](https://mincong.io/2019/04/16/glob-expression-understanding/) as well as `regex`
6. **pinotFSSpecs** - In case you are using a distributed file system such as GCS, Azure Blob Storage or S3. You can use multiple schemes under this in case the input and output filesystems are different.

You can refer to Segment Generation Job Configuration for more details.

Now that we have the job spec for our table `transcript` , we can trigger the job using the following command

```text
bin/pinot-admin.sh LaunchDataIngestionJob \\
    -jobSpecFile /tmp/pinot-quick-start/batch-job-spec.yml
```

Once the job has successfully finished, you can head over to the \[query console\] and start playing with the data.

### Segment Fetchers

When pinot segment files are created in external systems \(hadoop/spark/etc\), there are several ways to push those data to pinot Controller and Server:

1. push segment to shared NFS and let pinot pull segment files from the location of that NFS.
2. push segment to a Web server and let pinot pull segment files from the Web server with http/https link.
3. push segment to HDFS and let pinot pull segment files from HDFS with hdfs location URI.
4. push segment to other system and implement your own segment fetcher to pull data from those systems.

The first two options are supported out of the box with pinot package. As long your remote jobs send Pinot controller with the corresponding URI to the files it will pick up the file and allocate it to proper Pinot Servers and brokers. To enable Pinot support for HDFS, you will need to provide Pinot Hadoop configuration and proper Hadoop dependencies.

### Persistance

By default, Pinot does not come with a storage layer, so all the data sent, won't be stored in case of system crash. In order to persistently store the generated segments, you will need to change controller and server configs to add a deep storage. Checkout [File systems](../pinot-file-system/) for all the info and related configs.

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

