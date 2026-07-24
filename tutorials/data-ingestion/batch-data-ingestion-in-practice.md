# Batch Data Ingestion In Practice

In practice, we need to run Pinot data ingestion as a pipeline or a scheduled job.

Assuming pinot-distribution is already built, inside examples directory, you could find several sample table layouts.

## Table Layout

Usually each table deserves its own directory, like _airlineStats_.

Inside the table directory, _**rawdata**_ is created to put all the input data.

Typically, for data events with timestamp, we partition those data and store them into a daily folder. E.g. a typically layout would follow this pattern: `rawdata/%yyyy%/%mm%/%dd%/[daily_input_files]`.

```
/var/pinot/airlineStats/rawdata/2014/01/01/airlineStats_data_2014-01-01.avro
/var/pinot/airlineStats/rawdata/2014/01/02/airlineStats_data_2014-01-02.avro
/var/pinot/airlineStats/rawdata/2014/01/03/airlineStats_data_2014-01-03.avro
/var/pinot/airlineStats/rawdata/2014/01/04/airlineStats_data_2014-01-04.avro
/var/pinot/airlineStats/rawdata/2014/01/05/airlineStats_data_2014-01-05.avro
/var/pinot/airlineStats/rawdata/2014/01/06/airlineStats_data_2014-01-06.avro
/var/pinot/airlineStats/rawdata/2014/01/07/airlineStats_data_2014-01-07.avro
/var/pinot/airlineStats/rawdata/2014/01/08/airlineStats_data_2014-01-08.avro
/var/pinot/airlineStats/rawdata/2014/01/09/airlineStats_data_2014-01-09.avro
/var/pinot/airlineStats/rawdata/2014/01/10/airlineStats_data_2014-01-10.avro
/var/pinot/airlineStats/rawdata/2014/01/11/airlineStats_data_2014-01-11.avro
/var/pinot/airlineStats/rawdata/2014/01/12/airlineStats_data_2014-01-12.avro
/var/pinot/airlineStats/rawdata/2014/01/13/airlineStats_data_2014-01-13.avro
/var/pinot/airlineStats/rawdata/2014/01/14/airlineStats_data_2014-01-14.avro
/var/pinot/airlineStats/rawdata/2014/01/15/airlineStats_data_2014-01-15.avro
/var/pinot/airlineStats/rawdata/2014/01/16/airlineStats_data_2014-01-16.avro
/var/pinot/airlineStats/rawdata/2014/01/17/airlineStats_data_2014-01-17.avro
/var/pinot/airlineStats/rawdata/2014/01/18/airlineStats_data_2014-01-18.avro
/var/pinot/airlineStats/rawdata/2014/01/19/airlineStats_data_2014-01-19.avro
/var/pinot/airlineStats/rawdata/2014/01/20/airlineStats_data_2014-01-20.avro
/var/pinot/airlineStats/rawdata/2014/01/21/airlineStats_data_2014-01-21.avro
/var/pinot/airlineStats/rawdata/2014/01/22/airlineStats_data_2014-01-22.avro
/var/pinot/airlineStats/rawdata/2014/01/23/airlineStats_data_2014-01-23.avro
/var/pinot/airlineStats/rawdata/2014/01/24/airlineStats_data_2014-01-24.avro
/var/pinot/airlineStats/rawdata/2014/01/25/airlineStats_data_2014-01-25.avro
/var/pinot/airlineStats/rawdata/2014/01/26/airlineStats_data_2014-01-26.avro
/var/pinot/airlineStats/rawdata/2014/01/27/airlineStats_data_2014-01-27.avro
/var/pinot/airlineStats/rawdata/2014/01/28/airlineStats_data_2014-01-28.avro
/var/pinot/airlineStats/rawdata/2014/01/29/airlineStats_data_2014-01-29.avro
/var/pinot/airlineStats/rawdata/2014/01/30/airlineStats_data_2014-01-30.avro
/var/pinot/airlineStats/rawdata/2014/01/31/airlineStats_data_2014-01-31.avro
```

## Configuring batch ingestion job

Create a batch ingestion job spec file to describe how to ingest the data.

Below is an example (also located at `examples/batch/airlineStats/ingestionJobSpec.yaml`)

```
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

  # name: execution framework name
  name: 'standalone'

  # segmentGenerationJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentGenerationJobRunner interface.
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'

  # segmentTarPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentTarPushJobRunner interface.
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'

  # segmentUriPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentUriPushJobRunner interface.
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'

# jobType: Pinot ingestion job type.
# Supported job types are:
#   'SegmentCreation'
#   'SegmentTarPush'
#   'SegmentUriPush'
#   'SegmentCreationAndTarPush'
#   'SegmentCreationAndUriPush'
jobType: SegmentCreationAndTarPush

# inputDirURI: Root directory of input data, expected to have scheme configured in PinotFS.
inputDirURI: 'examples/batch/airlineStats/rawdata'

# includeFileNamePattern / excludeFileNamePattern: Java NIO PathMatcher patterns (glob: or regex:).
# See https://docs.pinot.apache.org/configuration-reference/job-specification#file-name-patterns
# Sample usage:
#   'glob:**/*.avro' or 'regex:.*[.]avro' matches Avro paths under inputDirURI (full path).
includeFileNamePattern: 'glob:**/*.avro'

# excludeFileNamePattern: 'glob:**/*.tmp' or 'regex:.*[.]tmp'
# excludeFileNamePattern: ''

# outputDirURI: Root directory of output segments, expected to have scheme configured in PinotFS.
outputDirURI: 'examples/batch/airlineStats/segments'

# overwriteOutput: Overwrite output segments if existed.
overwriteOutput: true

# Create a separated metadata only tar gz file to reduce the data transfer of segment metadata push job.
createMetadataTarGz: true

# Job parallelism for segment creation
segmentCreationJobParallelism: 4

# pinotFSSpecs: defines all related Pinot file systems.
pinotFSSpecs:

  - # scheme: used to identify a PinotFS.
    # E.g. local, hdfs, dbfs, etc
    scheme: file

    # className: Class name used to create the PinotFS instance.
    # E.g.
    #   org.apache.pinot.spi.filesystem.LocalPinotFS is used for local filesystem
    #   org.apache.pinot.plugin.filesystem.AzurePinotFS is used for Azure Data Lake
    #   org.apache.pinot.plugin.filesystem.HadoopPinotFS is used for HDFS
    className: org.apache.pinot.spi.filesystem.LocalPinotFS

# recordReaderSpec: defines all record reader
recordReaderSpec:

  # dataFormat: Record data format, e.g. 'avro', 'parquet', 'orc', 'csv', 'json', 'thrift' etc.
  dataFormat: 'avro'

  # className: Corresponding RecordReader class name.
  # E.g.
  #   org.apache.pinot.plugin.inputformat.avro.AvroRecordReader
  #   org.apache.pinot.plugin.inputformat.csv.CSVRecordReader
  #   org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader
  #   org.apache.pinot.plugin.inputformat.json.JSONRecordReader
  #   org.apache.pinot.plugin.inputformat.orc.ORCRecordReader
  #   org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReader
  className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'

# tableSpec: defines table name and where to fetch corresponding table config and table schema.
tableSpec:

  # tableName: Table name
  tableName: 'airlineStats'

  # schemaURI: defines where to read the table schema, supports PinotFS or HTTP.
  # E.g.
  #   hdfs://path/to/table_schema.json
  #   http://localhost:9000/tables/myTable/schema
  schemaURI: 'http://localhost:9000/tables/airlineStats/schema'

  # tableConfigURI: defines where to reade the table config.
  # Supports using PinotFS or HTTP.
  # E.g.
  #   hdfs://path/to/table_config.json
  #   http://localhost:9000/tables/myTable
  # Note that the API to read Pinot table config directly from pinot controller contains a JSON wrapper.
  # The real table config is the object under the field 'OFFLINE'.
  tableConfigURI: 'http://localhost:9000/tables/airlineStats'

# segmentNameGeneratorSpec: defines how to init a SegmentNameGenerator.
segmentNameGeneratorSpec:

  # type: Current supported type is 'simple' and 'normalizedDate'.
  type: normalizedDate

  # configs: Configs to init SegmentNameGenerator.
  configs:
    segment.name.prefix: 'airlineStats_batch'
    exclude.sequence.id: true

# pinotClusterSpecs: defines the Pinot Cluster Access Point.
pinotClusterSpecs:
  - # controllerURI: used to fetch table/schema information and data push.
    # E.g. http://localhost:9000
    controllerURI: 'http://localhost:9000'

# pushJobSpec: defines segment push job related configuration.
pushJobSpec:

  # Job parallelism for segment push
  pushParallelism: 4

  # pushAttempts: number of attempts for push job, default is 1, which means no retry.
  pushAttempts: 2

  # pushRetryIntervalMillis: retry wait Ms, default to 1 second.
  pushRetryIntervalMillis: 1000
  
  # Applicable for URI and METADATA push types.
  #If true, and if segment was not already in the deep store, move it to deep store.
  copyToDeepStoreForMetadataPush: false
  
  # Prefer using segment metadata tar gz file to push segment if exists.
  preferMetadataTarGz: true
```

## Executing the job

Below command will create example table into Pinot cluster.

```
bin/pinot-admin.sh AddTable  -schemaFile examples/batch/airlineStats/airlineStats_schema.json -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -exec
```

Below command will kick off the ingestion job to generate Pinot segments and push them into the cluster.

```
bin/pinot-admin.sh LaunchDataIngestionJob -jobSpecFile examples/batch/airlineStats/ingestionJobSpec.yaml
```

After job finished, segments are stored in `examples/batch/airlineStats/segments` following same layout of input directory layout.

```
/var/pinot/airlineStats/segments/2014/01/01/airlineStats_batch_2014-01-01_2014-01-01.tar.gz
/var/pinot/airlineStats/segments/2014/01/02/airlineStats_batch_2014-01-02_2014-01-02.tar.gz
/var/pinot/airlineStats/segments/2014/01/03/airlineStats_batch_2014-01-03_2014-01-03.tar.gz
/var/pinot/airlineStats/segments/2014/01/04/airlineStats_batch_2014-01-04_2014-01-04.tar.gz
/var/pinot/airlineStats/segments/2014/01/05/airlineStats_batch_2014-01-05_2014-01-05.tar.gz
/var/pinot/airlineStats/segments/2014/01/06/airlineStats_batch_2014-01-06_2014-01-06.tar.gz
/var/pinot/airlineStats/segments/2014/01/07/airlineStats_batch_2014-01-07_2014-01-07.tar.gz
/var/pinot/airlineStats/segments/2014/01/08/airlineStats_batch_2014-01-08_2014-01-08.tar.gz
/var/pinot/airlineStats/segments/2014/01/09/airlineStats_batch_2014-01-09_2014-01-09.tar.gz
/var/pinot/airlineStats/segments/2014/01/10/airlineStats_batch_2014-01-10_2014-01-10.tar.gz
/var/pinot/airlineStats/segments/2014/01/11/airlineStats_batch_2014-01-11_2014-01-11.tar.gz
/var/pinot/airlineStats/segments/2014/01/12/airlineStats_batch_2014-01-12_2014-01-12.tar.gz
/var/pinot/airlineStats/segments/2014/01/13/airlineStats_batch_2014-01-13_2014-01-13.tar.gz
/var/pinot/airlineStats/segments/2014/01/14/airlineStats_batch_2014-01-14_2014-01-14.tar.gz
/var/pinot/airlineStats/segments/2014/01/15/airlineStats_batch_2014-01-15_2014-01-15.tar.gz
/var/pinot/airlineStats/segments/2014/01/16/airlineStats_batch_2014-01-16_2014-01-16.tar.gz
/var/pinot/airlineStats/segments/2014/01/17/airlineStats_batch_2014-01-17_2014-01-17.tar.gz
/var/pinot/airlineStats/segments/2014/01/18/airlineStats_batch_2014-01-18_2014-01-18.tar.gz
/var/pinot/airlineStats/segments/2014/01/19/airlineStats_batch_2014-01-19_2014-01-19.tar.gz
/var/pinot/airlineStats/segments/2014/01/20/airlineStats_batch_2014-01-20_2014-01-20.tar.gz
/var/pinot/airlineStats/segments/2014/01/21/airlineStats_batch_2014-01-21_2014-01-21.tar.gz
/var/pinot/airlineStats/segments/2014/01/22/airlineStats_batch_2014-01-22_2014-01-22.tar.gz
/var/pinot/airlineStats/segments/2014/01/23/airlineStats_batch_2014-01-23_2014-01-23.tar.gz
/var/pinot/airlineStats/segments/2014/01/24/airlineStats_batch_2014-01-24_2014-01-24.tar.gz
/var/pinot/airlineStats/segments/2014/01/25/airlineStats_batch_2014-01-25_2014-01-25.tar.gz
/var/pinot/airlineStats/segments/2014/01/26/airlineStats_batch_2014-01-26_2014-01-26.tar.gz
/var/pinot/airlineStats/segments/2014/01/27/airlineStats_batch_2014-01-27_2014-01-27.tar.gz
/var/pinot/airlineStats/segments/2014/01/28/airlineStats_batch_2014-01-28_2014-01-28.tar.gz
/var/pinot/airlineStats/segments/2014/01/29/airlineStats_batch_2014-01-29_2014-01-29.tar.gz
/var/pinot/airlineStats/segments/2014/01/30/airlineStats_batch_2014-01-30_2014-01-30.tar.gz
/var/pinot/airlineStats/segments/2014/01/31/airlineStats_batch_2014-01-31_2014-01-31.tar.gz
```

## Executing the job using Spark

{% hint style="warning" %}
**`pinot-all` is not enough for Spark.** Spark (and Hadoop) batch runners ship under `plugins-external/` and are not packaged inside `pinot-all-*-jar-with-dependencies.jar`. If you only put `pinot-all` on the classpath you will get `ClassNotFoundException` for classes such as `SparkSegmentGenerationJobRunner`. Always add the shaded jar from `plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/` and include `plugins-external` in `plugins.dir`.
{% endhint %}

The example below runs Spark in **local mode** against the sample `airlineStats` data on the **local filesystem** (no S3/HDFS credentials). Download a Spark 3.x distribution and set `SPARK_HOME`, or use a pre-installed Spark.

Build or download a Pinot binary distribution following the [local install guide](../../basics/getting-started/install/local.md#1-download-or-build-apache-pinot).

### Local-FS Spark job spec

Use `LocalPinotFS` for local paths. Spark 3 runner classes live in the `spark3` package. You can start from `examples/batch/airlineStats/sparkIngestionJobSpec.yaml` and align class names / FS as below:

```
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

  # name: execution framework name
  name: 'spark'

  # Spark 3 package: org.apache.pinot.plugin.ingestion.batch.spark3.*
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentUriPushJobRunner'
  segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentMetadataPushJobRunner'

  # extraConfigs: extra configs for execution framework.
  extraConfigs:

    # stagingDir is used in distributed filesystem to host all the segments then move this directory entirely to output directory.
    stagingDir: examples/batch/airlineStats/staging

# jobType: Pinot ingestion job type.
# Supported job types are:
#   'SegmentCreation'
#   'SegmentTarPush'
#   'SegmentUriPush'
#   'SegmentCreationAndTarPush'
#   'SegmentCreationAndUriPush'
#   'SegmentCreationAndMetadataPush'
jobType: SegmentCreationAndTarPush

# inputDirURI: Root directory of input data, expected to have scheme configured in PinotFS.
inputDirURI: 'examples/batch/airlineStats/rawdata'

# includeFileNamePattern / excludeFileNamePattern: Java NIO PathMatcher (glob: or regex:).
# See configuration-reference/job-specification.md#file-name-patterns
includeFileNamePattern: 'glob:**/*.avro'
# excludeFileNamePattern: 'glob:**/*.tmp'

# outputDirURI: Root directory of output segments, expected to have scheme configured in PinotFS.
outputDirURI: 'examples/batch/airlineStats/segments'

# overwriteOutput: Overwrite output segments if existed.
overwriteOutput: true

# pinotFSSpecs: defines all related Pinot file systems.
pinotFSSpecs:

  - # Local filesystem — no cloud or HDFS credentials required for this recipe.
    scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS

# recordReaderSpec: defines all record reader
recordReaderSpec:

  dataFormat: 'avro'
  className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'

# tableSpec: defines table name and where to fetch corresponding table config and table schema.
tableSpec:

  tableName: 'airlineStats'
  schemaURI: 'http://localhost:9000/tables/airlineStats/schema'
  # Note that the API to read Pinot table config directly from pinot controller contains a JSON wrapper.
  # The real table config is the object under the field 'OFFLINE'.
  tableConfigURI: 'http://localhost:9000/tables/airlineStats'

# segmentNameGeneratorSpec: defines how to init a SegmentNameGenerator.
segmentNameGeneratorSpec:

  type: normalizedDate
  configs:
    segment.name.prefix: 'airlineStats_batch'
    exclude.sequence.id: true

# pinotClusterSpecs: defines the Pinot Cluster Access Point.
pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'

# pushJobSpec: defines segment push job related configuration.
pushJobSpec:

  pushParallelism: 2
  pushAttempts: 2
  pushRetryIntervalMillis: 1000
```

### Local-mode spark-submit

Ensure `PINOT_DISTRIBUTION_DIR` points at an unpacked binary distribution (contains `lib/`, `plugins/`, `plugins-external/`, and `examples/`).

{% hint style="info" %}
Required pieces:

* `plugins.dir` — semicolon-separated list including **both** `plugins` (record readers such as Avro) and `plugins-external` (Spark batch runners)
* `spark.driver.extraClassPath` / `spark.executor.extraClassPath` — `pinot-batch-ingestion-spark-3-*-shaded.jar` **and** `pinot-all-*-jar-with-dependencies.jar`
{% endhint %}

```
export PINOT_VERSION=1.5.1 #set to the Pinot version you have installed
export PINOT_DISTRIBUTION_DIR=${PINOT_ROOT_DIR}/build/
cd ${PINOT_DISTRIBUTION_DIR}

SPARK_BATCH_PLUGIN=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/pinot-batch-ingestion-spark-3-${PINOT_VERSION}-shaded.jar
PINOT_ALL_JAR=${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar

${SPARK_HOME}/bin/spark-submit \
  --class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \
  --master "local[2]" \
  --deploy-mode client \
  --conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins;${PINOT_DISTRIBUTION_DIR}/plugins-external -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml" \
  --conf "spark.driver.extraClassPath=${SPARK_BATCH_PLUGIN}:${PINOT_ALL_JAR}" \
  --conf "spark.executor.extraClassPath=${SPARK_BATCH_PLUGIN}:${PINOT_ALL_JAR}" \
  local://${PINOT_ALL_JAR} \
  -jobSpecFile ${PINOT_DISTRIBUTION_DIR}/examples/batch/airlineStats/sparkIngestionJobSpec.yaml
```

{% hint style="warning" %}
**Troubleshooting `ClassNotFoundException`:** confirm the shaded jar under `plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/` exists for your `${PINOT_VERSION}`, is on both driver and executor classpaths, and that `plugins.dir` lists `plugins-external`. See also the [Spark batch ingestion](../../build-with-pinot/ingestion/batch-ingestion/spark.md) page FAQ.
{% endhint %}

## Executing the job using Hadoop

{% hint style="warning" %}
**`pinot-all` is not enough for MapReduce.** The Hadoop batch plugin lives under `plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-hadoop/` and must be on `HADOOP_CLASSPATH`. Include `plugins-external` in `plugins.dir`.
{% endhint %}

Sample Hadoop ingestion job spec (also at `examples/batch/airlineStats/hadoopIngestionJobSpec.yaml`). For a **local filesystem** dry run, prefer `LocalPinotFS` as below (the checked-in sample may use `HadoopPinotFS` for HDFS-oriented pipelines):

```
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

  name: 'hadoop'

  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentUriPushJobRunner'
  segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentMetadataPushJobRunner'

  extraConfigs:
    stagingDir: examples/batch/airlineStats/staging

jobType: SegmentCreationAndTarPush

inputDirURI: 'examples/batch/airlineStats/rawdata'
includeFileNamePattern: 'glob:**/*.avro'
# excludeFileNamePattern: 'glob:**/*.tmp'
outputDirURI: 'examples/batch/airlineStats/segments'
overwriteOutput: true

pinotFSSpecs:
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS

recordReaderSpec:
  dataFormat: 'avro'
  className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'

tableSpec:
  tableName: 'airlineStats'
  schemaURI: 'http://localhost:9000/tables/airlineStats/schema'
  tableConfigURI: 'http://localhost:9000/tables/airlineStats'

segmentNameGeneratorSpec:
  type: normalizedDate
  configs:
    segment.name.prefix: 'airlineStats_batch'
    exclude.sequence.id: true

pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'

pushJobSpec:
  pushParallelism: 2
  pushAttempts: 2
  pushRetryIntervalMillis: 1000
```

Ensure `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

```
export PINOT_VERSION=1.5.1 #set to the Pinot version you have installed
export PINOT_DISTRIBUTION_DIR=${PINOT_ROOT_DIR}/build/

HADOOP_BATCH_PLUGIN=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-hadoop/pinot-batch-ingestion-hadoop-${PINOT_VERSION}-shaded.jar
PINOT_ALL_JAR=${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar

export HADOOP_CLIENT_OPTS="-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins;${PINOT_DISTRIBUTION_DIR}/plugins-external -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml"
export HADOOP_CLASSPATH="${HADOOP_BATCH_PLUGIN}:${PINOT_ALL_JAR}:${HADOOP_CLASSPATH}"

hadoop jar \
        ${PINOT_ALL_JAR} \
        org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \
        -jobSpecFile ${PINOT_DISTRIBUTION_DIR}/examples/batch/airlineStats/hadoopIngestionJobSpec.yaml
```

{% hint style="warning" %}
**Troubleshooting `ClassNotFoundException`:** add `plugins-external` to `plugins.dir` and put `pinot-batch-ingestion-hadoop-*-shaded.jar` on `HADOOP_CLASSPATH`. See [Hadoop batch ingestion](../../build-with-pinot/ingestion/batch-ingestion/hadoop.md).
{% endhint %}

## Executing a backfill ingestion job

When the backfill input directory for a given date may contain fewer files than the original ingestion, `LaunchDataIngestionJob` cannot fully replace the existing segments — see the [Edge case example](../../build-with-pinot/ingestion/batch-ingestion/backfill-data.md#edge-case-example) in the backfill docs. For that case, use `LaunchBackfillIngestionJob`, which reuses the same `ingestionJobSpec.yaml` and replaces the existing segments in a date range via Pinot's segment-lineage machinery.

```
bin/pinot-admin.sh LaunchBackfillIngestionJob \
    -jobSpecFile examples/batch/airlineStats/ingestionJobSpec.yaml \
    -startDate 2014-01-01 \
    -endDate 2014-01-02
```

The `-startDate` (inclusive) and `-endDate` (exclusive) arguments use `yyyy-MM-dd` format and are parsed as UTC day boundaries.

{% hint style="info" %}
For the full step-by-step workflow, supported options (including `-partitionColumn` / `-partitionColumnValue` for partition-scoped backfills), and OFFLINE-only constraints, see [Backfill Data](../../build-with-pinot/ingestion/batch-ingestion/backfill-data.md#complete-backfill-with-launchbackfillingestionjob).
{% endhint %}

## Tuning

You can set Environment Variable: `JAVA_OPTS` to modify:

* Log4j2 file location with `-Dlog4j2.configurationFile`
* Plugin directory location with `-Dplugins.dir=/opt/pinot/plugins` (standalone). For Spark/Hadoop batch jobs, use a semicolon-separated list that also includes `plugins-external`: `-Dplugins.dir=/opt/pinot/plugins;/opt/pinot/plugins-external`
* JVM props, like `-Xmx8g -Xms4G`

Note that you need to config above three all together in `JAVA_OPTS`. If you only config `JAVA_OPTS="-Xmx4g"` then `plugins.dir` is empty usually will cause job failure.

E.g. standalone Docker job:

```
docker run --rm -ti -e JAVA_OPTS="-Xms8G -Dlog4j2.configurationFile=/opt/pinot/conf/pinot-admin-log4j2.xml  -Dplugins.dir=/opt/pinot/plugins" --name pinot-data-ingestion-job apachepinot/pinot:latest LaunchDataIngestionJob -jobSpecFile /path/to/ingestion_job_spec.yaml
```

You can also add your customized `JAVA_OPTS` if necessary.
