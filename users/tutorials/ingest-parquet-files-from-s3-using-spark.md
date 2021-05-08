# Ingest Parquet Files from S3 Using Spark

One of the primary advantage of using Pinot is its pluggable architecture. The plugins make it easy to add support for any third-party system which can be an execution framework, a filesystem or input format.

In this tutorial, we will use three such plugins to easily ingest data and push it to our pinot cluster. The plugins we will be using are - 

* `pinot-batch-ingestion-spark`
* `pinot-s3` 
* `pinot-parquet` 

You can check out [Batch Ingestion](../../basics/data-import/batch-ingestion/), [File systems](../../basics/data-import/pinot-file-system/) and [Input formats](../../basics/data-import/pinot-input-formats.md) for all the available plugins.

### Setup

We are using the following tools and frameworks for this tutorial - 

* [Apache Spark](https://spark.apache.org/) 2.2.3 \(Although any spark 2.X should work\)
* [Apache Parquet](https://parquet.apache.org/) 1.8.2
* [Amazon S3](https://aws.amazon.com/s3/)
* [Apache Pinot 0.4.0](https://pinot.apache.org/)

### Input Data

We need to get input data to ingest first. For our demo, we'll just create some small parquet files and upload them to our S3 bucket. The easiest way is to create CSV files and then convert them to parquet. CSV makes it human-readable and thus easier to modify input in case of some failure in our demo.  We will call this file `students.csv`

```text
timestampInEpoch,id,name,age,score
1597044264380,1,david,15,98
1597044264381,2,henry,16,97
1597044264382,3,katie,14,99
1597044264383,4,catelyn,15,96
1597044264384,5,emma,13,93
1597044264390,6,john,15,100
1597044264396,7,isabella,13,89
1597044264399,8,linda,17,91
1597044264502,9,mark,16,67
1597044264670,10,tom,14,78
```

Now, we'll create parquet files from the above CSV file using Spark. Since this is a small program, we will be using Spark shell instead of writing a full fledged Spark code.

```scala
scala> val df = spark.read.format("csv").option("header", true).load("path/to/students.csv")
scala> df.write.option("compression","none").mode("overwrite").parquet("/path/to/batch_input/")
```

The `.parquet` files can now be found in `/path/to/batch_input` directory.  You can now upload this directory to S3 either using their UI or running the command

```scala
aws s3 cp /path/to/batch_input s3://my-bucket/batch-input/ --recursive
```

### Create Schema and Table 

We need to create a table to query the data that will be ingested. All tables in pinot are associated with a schema. You can check out [Table configuration](../../configuration-reference/table.md) and [Schema configuration](../../configuration-reference/schema.md) for more details on creating configurations. 

For our demo, we will have the following schema and table configs

{% code title="student\_schema.json" %}
```javascript
{
    "schemaName": "students",
    "dimensionFieldSpecs": [
        {
            "name": "id",
            "dataType": "INT"
        },
        {
            "name": "name",
            "dataType": "STRING"
        },
        {
            "name": "age",
            "dataType": "INT"
        }
    ],
    "metricFieldSpecs": [
        {
            "name": "score",
            "dataType": "INT"
        }
    ],
    "dateTimeFieldSpecs": [
        {
            "name": "timestampInEpoch",
            "dataType": "LONG",
            "format": "1:MILLISECONDS:EPOCH",
            "granularity": "1:MILLISECONDS"
        }
    ]
}
```
{% endcode %}

{% code title="student\_table.json" %}
```scala
{
    "tableName": "students",
    "segmentsConfig": {
        "timeColumnName": "timestampInEpoch",
        "timeType": "MILLISECONDS",
        "replication": "1",
        "schemaName": "students"
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

We can now upload these configurations to pinot and create an empty table. We will be using `pinot-admin.sh` CLI for these purpose. 

```scala
pinot-admin.sh AddTable -tableConfigFile /path/to/student_table.json -schemaFile /path/to/student_schema.json -controllerHost localhost -controllerPort 9000 -exec
```

You can check out [Command-Line Interface \(CLI\)](../../operators/cli.md) for all the available commands. 

Our table will now be available in the [Pinot data explorer](../../basics/components/exploring-pinot.md)

### Ingest Data

Now that our data is available in S3 as well as we have the Tables in Pinot, we can start the process of ingesting the data.  Data ingestion in Pinot involves the following steps - 

* Read data and generate compressed segment files from input
* Upload the compressed segment files to output location
* Push the location of the segment files to the controller

Once the location is available to the controller, it can notify the servers to download the segment files and populate the tables.

The above steps can be performed using any distributed executor of your choice such as Hadoop, Spark, Flink etc.  For this demo we will be using Apache Spark to execute the steps. 

Pinot provides runners for Spark out of the box. So as a user, you don't need to write a single line of code. You can write runners for any other executor using our provided interfaces.

Firstly, we will create a job spec configuration file for our data ingestion process. 

{% code title="spark\_job\_spec.yaml" %}
```scala
executionFrameworkSpec:
  name: 'spark'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentUriPushJobRunner'
  extraConfigs:
    stagingDir: s3://my-bucket/spark/staging/
jobType: SegmentCreationAndTarPush
inputDirURI: 's3://my-bucket/path/to/batch-input/'
outputDirURI: 's3:///my-bucket/path/to/batch-output/'
overwriteOutput: true
pinotFSSpecs:
  - scheme: s3
    className: org.apache.pinot.plugin.filesystem.S3PinotFS
    configs:    
      region: 'us-west-2'
recordReaderSpec:
  dataFormat: 'parquet'
  className: 'org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader'
tableSpec:
  tableName: 'students'
pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'
pushJobSpec:
  pushParallelism: 2
  pushAttempts: 2
  pushRetryIntervalMillis: 1000
```
{% endcode %}

In the job spec, we have kept execution framework as `spark` and configured the appropriate runners for each of our steps. We also need a temporary `stagingDir` for our spark job. This directory is cleaned up after our job has executed.

We also provide the S3 Filesystem and Parquet reader implementation in the config to use. You can refer [Ingestion Job Spec](../../configuration-reference/job-specification.md) for complete list of configuration.

We can now run our spark job to execute all the steps and populate data in pinot.

```bash
export PINOT_VERSION=0.7.1
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-incubating-${PINOT_VERSION}-bin

spark-submit //
--class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand //
--master local --deploy-mode client //
--conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dplugins.include=pinot-s3,pinot-parquet -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml" //
--conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/plugins/pinot-batch-ingestion/pinot-batch-ingestion-spark/pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar:${PINOT_DISTRIBUTION_DIR}/plugins/pinot-file-system/pinot-s3/pinot-s3-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/plugins/pinot-input-format/pinot-parquet/pinot-parquet-${PINOT_VERSION}-shaded.jar" //
local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar -jobSpecFile /path/to/spark_job_spec.yaml
```

{% hint style="info" %}
In the command , we have included the JARs of all the required plugins in the spark's `driver classpath`. In practice, you only need to do this if you get a `ClassNotFoundException`.
{% endhint %}

Voila! Now our data is successfully ingested. Let's try to query it from Pinot's broker

```bash
bin/pinot-admin.sh PostQuery -brokerHost localhost -brokerPort 8000 -queryType sql -query "SELECT * FROM students LIMIT 10"
```

If everything went right, you should receive the following output

```bash
{
  "resultTable": {
    "dataSchema": {
      "columnNames": [
        "age",
        "id",
        "name",
        "score",
        "timestampInEpoch"
      ],
      "columnDataTypes": [
        "INT",
        "INT",
        "STRING",
        "INT",
        "LONG"
      ]
    },
    "rows": [
      [
        15,
        1,
        "david",
        98,
        1597044264380
      ],
      [
        16,
        2,
        "henry",
        97,
        1597044264381
      ],
      [
        14,
        3,
        "katie",
        99,
        1597044264382
      ],
      [
        15,
        4,
        "catelyn",
        96,
        1597044264383
      ],
      [
        13,
        5,
        "emma",
        93,
        1597044264384
      ],
      [
        15,
        6,
        "john",
        100,
        1597044264390
      ],
      [
        13,
        7,
        "isabella",
        89,
        1597044264396
      ],
      [
        17,
        8,
        "linda",
        91,
        1597044264399
      ],
      [
        16,
        9,
        "mark",
        67,
        1597044264502
      ],
      [
        14,
        10,
        "tom",
        78,
        1597044264670
      ]
    ]
  },
  "exceptions": [],
  "numServersQueried": 1,
  "numServersResponded": 1,
  "numSegmentsQueried": 1,
  "numSegmentsProcessed": 1,
  "numSegmentsMatched": 1,
  "numConsumingSegmentsQueried": 0,
  "numDocsScanned": 10,
  "numEntriesScannedInFilter": 0,
  "numEntriesScannedPostFilter": 50,
  "numGroupsLimitReached": false,
  "totalDocs": 10,
  "timeUsedMs": 11,
  "segmentStatistics": [],
  "traceInfo": {},
  "minConsumingFreshnessTimeMs": 0
}
```



