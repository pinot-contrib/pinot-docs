# Batch Data Ingestion In Practice

In practice, we need to run Pinot data ingestion as a pipeline or a scheduled job.

Assuming pinot-distribution is already built, inside examples directory, you could find several sample table layouts.

### Table Layout

Usually each table deserves its own directory, like _airlineStats_.

Inside the table directory, _**rawdata**_ is created to put all the input data.

Typically, for data events with timestamp, we partition those data and store them into a daily folder. E.g. a typically layout would follow this pattern: `rawdata/%yyyy%/%mm%/%dd%/[daily_input_files]`.

```text
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

### Configuring batch ingestion job

Create a batch ingestion job spec file to describe how to ingest the data.

Below is an example \(also located at `examples/batch/airlineStats/ingestionJobSpec.yaml`\)

```text
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

# includeFileNamePattern: include file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will include all avro files just under the inputDirURI, not sub directories;
#   'glob:**\/*.avro' will include all the avro files under inputDirURI recursively.
includeFileNamePattern: 'glob:**/*.avro'

# excludeFileNamePattern: exclude file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will exclude all avro files just under the inputDirURI, not sub directories;
#   'glob:**\/*.avro' will exclude all the avro files under inputDirURI recursively.
# _excludeFileNamePattern: ''

# outputDirURI: Root directory of output segments, expected to have scheme configured in PinotFS.
outputDirURI: 'examples/batch/airlineStats/segments'

# overwriteOutput: Overwrite output segments if existed.
overwriteOutput: true

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
  #   org.apache.pinot.plugin.inputformat.json.JsonRecordReader
  #   org.apache.pinot.plugin.inputformat.orc.OrcRecordReader
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

# pinotClusterSpecs: defines the Pinot Cluster Access Point.
pinotClusterSpecs:
  - # controllerURI: used to fetch table/schema information and data push.
    # E.g. http://localhost:9000
    controllerURI: 'http://localhost:9000'

# pushJobSpec: defines segment push job related configuration.
pushJobSpec:

  # pushAttempts: number of attempts for push job, default is 1, which means no retry.
  pushAttempts: 2

  # pushRetryIntervalMillis: retry wait Ms, default to 1 second.
  pushRetryIntervalMillis: 1000
```

### Executing the job

Below command will create example table into Pinot cluster.

```text
bin/pinot-admin.sh AddTable  -schemaFile examples/batch/airlineStats/airlineStats_schema.json -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -exec
```

Below command will kick off the ingestion job to generate Pinot segments and push them into the cluster.

```text
bin/pinot-ingestion-job.sh examples/batch/airlineStats/ingestionJobSpec.yaml
```

After job finished, segments are stored in `examples/batch/airlineStats/segments` following same layout of input directory layout.

```text
/var/pinot/airlineStats/segments/2014/01/01/airlineStats_OFFLINE_16071_16071_21.tar.gz
/var/pinot/airlineStats/segments/2014/01/02/airlineStats_OFFLINE_16072_16072_3.tar.gz
/var/pinot/airlineStats/segments/2014/01/03/airlineStats_OFFLINE_16073_16073_0.tar.gz
/var/pinot/airlineStats/segments/2014/01/04/airlineStats_OFFLINE_16074_16074_1.tar.gz
/var/pinot/airlineStats/segments/2014/01/05/airlineStats_OFFLINE_16075_16075_2.tar.gz
/var/pinot/airlineStats/segments/2014/01/06/airlineStats_OFFLINE_16076_16076_22.tar.gz
/var/pinot/airlineStats/segments/2014/01/07/airlineStats_OFFLINE_16077_16077_16.tar.gz
/var/pinot/airlineStats/segments/2014/01/08/airlineStats_OFFLINE_16078_16078_20.tar.gz
/var/pinot/airlineStats/segments/2014/01/09/airlineStats_OFFLINE_16079_16079_17.tar.gz
/var/pinot/airlineStats/segments/2014/01/10/airlineStats_OFFLINE_16080_16080_12.tar.gz
/var/pinot/airlineStats/segments/2014/01/11/airlineStats_OFFLINE_16081_16081_7.tar.gz
/var/pinot/airlineStats/segments/2014/01/12/airlineStats_OFFLINE_16082_16082_26.tar.gz
/var/pinot/airlineStats/segments/2014/01/13/airlineStats_OFFLINE_16083_16083_27.tar.gz
/var/pinot/airlineStats/segments/2014/01/14/airlineStats_OFFLINE_16084_16084_28.tar.gz
/var/pinot/airlineStats/segments/2014/01/15/airlineStats_OFFLINE_16085_16085_25.tar.gz
/var/pinot/airlineStats/segments/2014/01/16/airlineStats_OFFLINE_16086_16086_9.tar.gz
/var/pinot/airlineStats/segments/2014/01/17/airlineStats_OFFLINE_16087_16087_11.tar.gz
/var/pinot/airlineStats/segments/2014/01/18/airlineStats_OFFLINE_16088_16088_5.tar.gz
/var/pinot/airlineStats/segments/2014/01/19/airlineStats_OFFLINE_16089_16089_13.tar.gz
/var/pinot/airlineStats/segments/2014/01/20/airlineStats_OFFLINE_16090_16090_4.tar.gz
/var/pinot/airlineStats/segments/2014/01/21/airlineStats_OFFLINE_16091_16091_15.tar.gz
/var/pinot/airlineStats/segments/2014/01/22/airlineStats_OFFLINE_16092_16092_29.tar.gz
/var/pinot/airlineStats/segments/2014/01/23/airlineStats_OFFLINE_16093_16093_24.tar.gz
/var/pinot/airlineStats/segments/2014/01/24/airlineStats_OFFLINE_16094_16094_23.tar.gz
/var/pinot/airlineStats/segments/2014/01/25/airlineStats_OFFLINE_16095_16095_30.tar.gz
/var/pinot/airlineStats/segments/2014/01/26/airlineStats_OFFLINE_16096_16096_14.tar.gz
/var/pinot/airlineStats/segments/2014/01/27/airlineStats_OFFLINE_16097_16097_6.tar.gz
/var/pinot/airlineStats/segments/2014/01/28/airlineStats_OFFLINE_16098_16098_10.tar.gz
/var/pinot/airlineStats/segments/2014/01/29/airlineStats_OFFLINE_16099_16099_8.tar.gz
/var/pinot/airlineStats/segments/2014/01/30/airlineStats_OFFLINE_16100_16100_19.tar.gz
/var/pinot/airlineStats/segments/2014/01/31/airlineStats_OFFLINE_16101_16101_18.tar.gz
```

### Executing the job using Spark

Below example is running in a spark local mode. You can download spark distribution and start it by running:

```text
wget https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
tar xvf spark-2.4.5-bin-hadoop2.7.tgz
cd spark-2.4.5-bin-hadoop2.7
./bin/spark-shell --master 'local[2]'
```

Build latest Pinot Distribution following this [Wiki](https://docs.pinot.apache.org/getting-started/running-pinot-locally#build-from-source-or-download-the-distribution).

Below command shows how to use spark-submit command to submit a spark job using `pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar`.

Sample Spark ingestion job spec yaml, \(also located at `examples/batch/airlineStats/sparkIngestionJobSpec.yaml`\):

```text
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

  # name: execution framework name
  name: 'spark'

  # segmentGenerationJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentGenerationJobRunner interface.
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentGenerationJobRunner'

  # segmentTarPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentTarPushJobRunner interface.
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentTarPushJobRunner'

  # segmentUriPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentUriPushJobRunner interface.
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentUriPushJobRunner'

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
jobType: SegmentCreationAndTarPush

# inputDirURI: Root directory of input data, expected to have scheme configured in PinotFS.
inputDirURI: 'examples/batch/airlineStats/rawdata'

# includeFileNamePattern: include file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will include all avro files just under the inputDirURI, not sub directories;
#   'glob:**\/*.avro' will include all the avro files under inputDirURI recursively.
includeFileNamePattern: 'glob:**/*.avro'

# excludeFileNamePattern: exclude file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will exclude all avro files just under the inputDirURI, not sub directories;
#   'glob:**\/*.avro' will exclude all the avro files under inputDirURI recursively.
# excludeFileNamePattern: ''

# outputDirURI: Root directory of output segments, expected to have scheme configured in PinotFS.
outputDirURI: 'examples/batch/airlineStats/segments'

# overwriteOutput: Overwrite output segments if existed.
overwriteOutput: true

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
    className: org.apache.pinot.plugin.filesystem.HadoopPinotFS

# recordReaderSpec: defines all record reader
recordReaderSpec:

  # dataFormat: Record data format, e.g. 'avro', 'parquet', 'orc', 'csv', 'json', 'thrift' etc.
  dataFormat: 'avro'

  # className: Corresponding RecordReader class name.
  # E.g.
  #   org.apache.pinot.plugin.inputformat.avro.AvroRecordReader
  #   org.apache.pinot.plugin.inputformat.csv.CSVRecordReader
  #   org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader
  #   org.apache.pinot.plugin.inputformat.json.JsonRecordReader
  #   org.apache.pinot.plugin.inputformat.orc.OrcRecordReader
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

  # pushParallelism: push job parallelism, default is 1.
  pushParallelism: 2

  # pushAttempts: number of attempts for push job, default is 1, which means no retry.
  pushAttempts: 2

  # pushRetryIntervalMillis: retry wait Ms, default to 1 second.
  pushRetryIntervalMillis: 1000

```

Please ensure parameter `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

```text
export PINOT_VERSION=0.4.0-SNAPSHOT
export PINOT_DISTRIBUTION_DIR=${PINOT_ROOT_DIR}/pinot-distribution/target/apache-pinot-incubating-${PINOT_VERSION}-bin/apache-pinot-incubating-${PINOT_VERSION}-bin
./bin/spark-submit \
  --class org.apache.pinot.spi.ingestion.batch.IngestionJobLauncher \
  --master "local[2]" \
  --deploy-mode client \
  --conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml" \
  --conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" \
  local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar \
  ${PINOT_DISTRIBUTION_DIR}/examples/batch/airlineStats/sparkIngestionJobSpec.yaml
```

### Executing the job using Hadoop

Below command shows how to use Hadoop jar command to run a Hadoop job using `pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar`.

Sample Hadoop ingestion job spec yaml\(also located at `examples/batch/airlineStats/hadoopIngestionJobSpec.yaml`\):

```text
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

  # name: execution framework name
  name: 'hadoop'

  # segmentGenerationJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentGenerationJobRunner interface.
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentGenerationJobRunner'

  # segmentTarPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentTarPushJobRunner interface.
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentTarPushJobRunner'

  # segmentUriPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentUriPushJobRunner interface.
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentUriPushJobRunner'

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
jobType: SegmentCreationAndTarPush

# inputDirURI: Root directory of input data, expected to have scheme configured in PinotFS.
inputDirURI: 'examples/batch/airlineStats/rawdata'

# includeFileNamePattern: include file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will include all avro files just under the inputDirURI, not sub directories;
#   'glob:**\/*.avro' will include all the avro files under inputDirURI recursively.
includeFileNamePattern: 'glob:**/*.avro'

# excludeFileNamePattern: exclude file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will exclude all avro files just under the inputDirURI, not sub directories;
#   'glob:**\/*.avro' will exclude all the avro files under inputDirURI recursively.
# _excludeFileNamePattern: ''

# outputDirURI: Root directory of output segments, expected to have scheme configured in PinotFS.
outputDirURI: 'examples/batch/airlineStats/segments'

# overwriteOutput: Overwrite output segments if existed.
overwriteOutput: true

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
    className: org.apache.pinot.plugin.filesystem.HadoopPinotFS

# recordReaderSpec: defines all record reader
recordReaderSpec:

  # dataFormat: Record data format, e.g. 'avro', 'parquet', 'orc', 'csv', 'json', 'thrift' etc.
  dataFormat: 'avro'

  # className: Corresponding RecordReader class name.
  # E.g.
  #   org.apache.pinot.plugin.inputformat.avro.AvroRecordReader
  #   org.apache.pinot.plugin.inputformat.csv.CSVRecordReader
  #   org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader
  #   org.apache.pinot.plugin.inputformat.json.JsonRecordReader
  #   org.apache.pinot.plugin.inputformat.orc.OrcRecordReader
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

  # pushParallelism: push job parallelism, default is 1.
  pushParallelism: 2

  # pushAttempts: number of attempts for push job, default is 1, which means no retry.
  pushAttempts: 2

  # pushRetryIntervalMillis: retry wait Ms, default to 1 second.
  pushRetryIntervalMillis: 1000

```

Please ensure parameter `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

```text
export PINOT_VERSION=0.4.0-SNAPSHOT
export PINOT_DISTRIBUTION_DIR=${PINOT_ROOT_DIR}/pinot-distribution/target/apache-pinot-incubating-${PINOT_VERSION}-bin/apache-pinot-incubating-${PINOT_VERSION}-bin
export HADOOP_CLIENT_OPTS="-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml"
hadoop jar  \
        ${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar \
        org.apache.pinot.spi.ingestion.batch.IngestionJobLauncher \
        ${PINOT_DISTRIBUTION_DIR}/examples/batch/airlineStats/hadoopIngestionJobSpec.yaml
```

