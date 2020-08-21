# Batch Data Ingestion Using S3 as Deep Store

{% hint style="info" %}
Below commands are based on pinot distribution binary.
{% endhint %}

## Setup Pinot Cluster

In order to setup Pinot to use S3 as deep store, we need to put extra configs for Controller and Server.

### Start Controller

Below is a sample `controller.conf` file.

{% hint style="info" %}
Please config `controller.data.dir`to your s3 bucket. All the uploaded segments will be stored there. 
{% endhint %}

```bash
controller.data.dir=s3://my.bucket/pinot-data/pinot-s3-example/controller-data
controller.local.temp.dir=/tmp/pinot-tmp-data/
controller.zk.str=localhost:2181
controller.host=127.0.0.1
controller.port=9000
controller.helix.cluster.name=pinot-s3-example
pinot.controller.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.controller.storage.factory.s3.region=us-west-2

pinot.controller.segment.fetcher.protocols=file,http,s3
pinot.controller.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

Then start pinot controller with:

```
bin/pinot-admin.sh StartController -configFileName conf/controller.conf
```

### Start Broker

Broker is a simple one you can just start it with default:

```
bin/pinot-admin.sh StartBroker -zkAddress localhost:2181 -clusterName pinot-s3-example
```

### Start Server

Below is a sample `server.conf` file

```bash
pinot.server.netty.port=8098
pinot.server.adminapi.port=8097
pinot.server.instance.dataDir=/tmp/pinot-tmp/server/index
pinot.server.instance.segmentTarDir=/tmp/pinot-tmp/server/segmentTars


pinot.server.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.server.storage.factory.s3.region=us-west-2
pinot.server.segment.fetcher.protocols=file,http,s3
pinot.server.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

Then start pinot controller with:

```
bin/pinot-admin.sh StartServer -configFileName conf/server.conf -zkAddress localhost:2181 -clusterName pinot-s3-example
```

## Setup Table

In this demo, we just use `airlineStats` table as an example.

Create table with below command:

```text
bin/pinot-admin.sh AddTable  -schemaFile examples/batch/airlineStats/airlineStats_schema.json -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -exec
```

## Set up Ingestion Jobs

### Standalone Job

Below is a sample standalone ingestion job spec with certain notable changes:

* **jobType** is **SegmentCreationAndUriPush**
* **inputDirURI** is set to a s3 location  **s3://my.bucket/batch/airlineStats/rawdata/**
* **outputDirURI** is set to a s3 location  **s3://my.bucket/output/airlineStats/segments**
* Add a new PinotFs under **pinotFSSpecs**

  ```text
  - scheme: s3
    className: org.apache.pinot.plugin.filesystem.S3PinotFS
    configs:
      region: 'us-west-2'
      accessKey: '****************LFVX'
      secretKey: '****************gfhz'
  ```

* For library version &lt; **0.6.0**, please set `segmentUriPrefix` to `[scheme]://[bucket.name]`, e.g. `s3://my.bucket` , from version **0.6.0**, you can put empty string or just ignore `segmentUriPrefix`.

Sample `ingestionJobSpec.yaml`

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
#jobType: SegmentCreationAndUriPush
jobType: SegmentCreationAndUriPush
# inputDirURI: Root directory of input data, expected to have scheme configured in PinotFS.
inputDirURI: 's3://my.bucket/batch/airlineStats/rawdata/'

# includeFileNamePattern: include file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will include all avro files just under the inputDirURI, not sub directories;
#   'glob:**/*.avro' will include all the avro files under inputDirURI recursively.
includeFileNamePattern: 'glob:**/*.avro'

# excludeFileNamePattern: exclude file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will exclude all avro files just under the inputDirURI, not sub directories;
#   'glob:**/*.avro' will exclude all the avro files under inputDirURI recursively.
# _excludeFileNamePattern: ''

# outputDirURI: Root directory of output segments, expected to have scheme configured in PinotFS.
outputDirURI: 's3://my.bucket/examples/output/airlineStats/segments'

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


  - scheme: s3
    className: org.apache.pinot.plugin.filesystem.S3PinotFS
    configs:
      region: 'us-west-2'

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
  
  # For Pinot version < 0.6.0, use [scheme]://[bucket.name] as prefix.
  # E.g. s3://my.bucket
  segmentUriPrefix: 's3://my.bucket'
  segmentUriSuffix: ''
```

Below is a sample job output:

```text
➜ bin/pinot-ingestion-job.sh -jobSpecFile  ~/temp/pinot/pinot-s3-test/ingestionJobSpec.yaml
2020/08/18 16:11:03.521 INFO [IngestionJobLauncher] [main] SegmentGenerationJobSpec:
!!org.apache.pinot.spi.ingestion.batch.spec.SegmentGenerationJobSpec
excludeFileNamePattern: null
executionFrameworkSpec: {extraConfigs: null, name: standalone, segmentGenerationJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner,
  segmentTarPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner,
  segmentUriPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner}
includeFileNamePattern: glob:**/*.avro
inputDirURI: s3://my.bucket/batch/airlineStats/rawdata/
jobType: SegmentUriPush
outputDirURI: s3://my.bucket/examples/output/airlineStats/segments
overwriteOutput: true
pinotClusterSpecs:
- {controllerURI: 'http://localhost:9000'}
pinotFSSpecs:
- {className: org.apache.pinot.spi.filesystem.LocalPinotFS, configs: null, scheme: file}
- className: org.apache.pinot.plugin.filesystem.S3PinotFS
  configs: {region: us-west-2}
  scheme: s3
pushJobSpec: {pushAttempts: 2, pushParallelism: 1, pushRetryIntervalMillis: 1000,
  segmentUriPrefix: '', segmentUriSuffix: ''}
recordReaderSpec: {className: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader,
  configClassName: null, configs: null, dataFormat: avro}
segmentNameGeneratorSpec: null
tableSpec: {schemaURI: 'http://localhost:9000/tables/airlineStats/schema', tableConfigURI: 'http://localhost:9000/tables/airlineStats',
  tableName: airlineStats}

2020/08/18 16:11:03.531 INFO [IngestionJobLauncher] [main] Trying to create instance for class org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner
2020/08/18 16:11:03.654 INFO [PinotFSFactory] [main] Initializing PinotFS for scheme file, classname org.apache.pinot.spi.filesystem.LocalPinotFS
2020/08/18 16:11:03.656 INFO [PinotFSFactory] [main] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/18 16:11:05.520 INFO [SegmentPushUtils] [main] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_OFFLINE_16071_16071_0.tar.gz, s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_OFFLINE_16072_16072_1.tar.gz, s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_OFFLINE_16073_16073_2.tar.gz, s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_OFFLINE_16074_16074_3.tar.gz, s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_OFFLINE_16075_16075_4.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@4e07b95f]
2020/08/18 16:11:05.521 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_OFFLINE_16071_16071_0.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:09.356 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:09.358 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_OFFLINE_16071_16071_0.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16071_16071_0 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:09.359 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_OFFLINE_16072_16072_1.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:09.824 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:09.825 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_OFFLINE_16072_16072_1.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16072_16072_1 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:09.825 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_OFFLINE_16073_16073_2.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:10.500 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:10.501 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_OFFLINE_16073_16073_2.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16073_16073_2 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:10.501 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_OFFLINE_16074_16074_3.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:10.967 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:10.968 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_OFFLINE_16074_16074_3.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16074_16074_3 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:10.969 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_OFFLINE_16075_16075_4.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:11.420 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:11.420 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_OFFLINE_16075_16075_4.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16075_16075_4 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:11.421 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_OFFLINE_16076_16076_5.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:11.872 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:11.873 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_OFFLINE_16076_16076_5.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16076_16076_5 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:11.877 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_OFFLINE_16077_16077_6.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:12.293 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:12.294 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_OFFLINE_16077_16077_6.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16077_16077_6 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:12.295 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_OFFLINE_16078_16078_7.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:12.672 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:12.673 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_OFFLINE_16078_16078_7.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16078_16078_7 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:12.674 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_OFFLINE_16079_16079_8.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:13.048 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:13.050 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_OFFLINE_16079_16079_8.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16079_16079_8 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:13.051 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_OFFLINE_16080_16080_9.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:13.483 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:13.485 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_OFFLINE_16080_16080_9.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16080_16080_9 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:13.486 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_OFFLINE_16081_16081_10.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:14.080 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:14.081 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_OFFLINE_16081_16081_10.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16081_16081_10 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:14.082 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_OFFLINE_16082_16082_11.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:14.477 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:14.477 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_OFFLINE_16082_16082_11.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16082_16082_11 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:14.478 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_OFFLINE_16083_16083_12.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:14.865 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:14.866 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_OFFLINE_16083_16083_12.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16083_16083_12 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:14.867 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_OFFLINE_16084_16084_13.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:15.257 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:15.258 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_OFFLINE_16084_16084_13.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16084_16084_13 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:15.258 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_OFFLINE_16085_16085_14.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:15.917 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:15.919 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_OFFLINE_16085_16085_14.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16085_16085_14 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:15.919 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_OFFLINE_16086_16086_15.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:16.719 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:16.720 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_OFFLINE_16086_16086_15.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16086_16086_15 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:16.720 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_OFFLINE_16087_16087_16.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:17.346 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:17.347 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_OFFLINE_16087_16087_16.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16087_16087_16 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:17.347 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_OFFLINE_16088_16088_17.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:17.815 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:17.816 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_OFFLINE_16088_16088_17.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16088_16088_17 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:17.816 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_OFFLINE_16089_16089_18.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:18.389 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:18.389 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_OFFLINE_16089_16089_18.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16089_16089_18 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:18.390 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_OFFLINE_16090_16090_19.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:18.978 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:18.978 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_OFFLINE_16090_16090_19.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16090_16090_19 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:18.979 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_OFFLINE_16091_16091_20.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:19.586 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:19.587 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_OFFLINE_16091_16091_20.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16091_16091_20 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:19.589 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_OFFLINE_16092_16092_21.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:20.087 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:20.087 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_OFFLINE_16092_16092_21.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16092_16092_21 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:20.088 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_OFFLINE_16093_16093_22.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:20.550 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:20.551 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_OFFLINE_16093_16093_22.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16093_16093_22 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:20.552 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_OFFLINE_16094_16094_23.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:20.978 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:20.979 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_OFFLINE_16094_16094_23.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16094_16094_23 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:20.979 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_OFFLINE_16095_16095_24.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:21.626 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:21.628 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_OFFLINE_16095_16095_24.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16095_16095_24 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:21.628 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_OFFLINE_16096_16096_25.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:22.121 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:22.122 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_OFFLINE_16096_16096_25.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16096_16096_25 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:22.123 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_OFFLINE_16097_16097_26.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:22.679 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:22.679 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_OFFLINE_16097_16097_26.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16097_16097_26 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:22.680 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_OFFLINE_16098_16098_27.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:23.373 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:23.374 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_OFFLINE_16098_16098_27.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16098_16098_27 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:23.375 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_OFFLINE_16099_16099_28.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:23.787 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:23.788 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_OFFLINE_16099_16099_28.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16099_16099_28 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:23.788 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_OFFLINE_16100_16100_29.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:24.298 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:24.299 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_OFFLINE_16100_16100_29.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16100_16100_29 of table: airlineStats_OFFLINE"}
2020/08/18 16:11:24.299 INFO [SegmentPushUtils] [main] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_OFFLINE_16101_16101_30.tar.gz to location: http://localhost:9000 for
2020/08/18 16:11:24.987 INFO [FileUploadDownloadClient] [main] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/18 16:11:24.987 INFO [SegmentPushUtils] [main] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_OFFLINE_16101_16101_30.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16101_16101_30 of table: airlineStats_OFFLINE"}
```

### Spark Job

#### Setup Spark Cluster \(Skip if you already have one\)

Please follow this [page](https://app.gitbook.com/@apache-pinot/s/apache-pinot-cookbook/operators/tutorials/batch-data-ingestion-in-practice#executing-the-job-using-spark) to setup a local spark cluster.

#### Submit Spark Job

Below is a sample Spark Ingestion job

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

# jobType: Pinot ingestion job type.
# Supported job types are:
#   'SegmentCreation'
#   'SegmentTarPush'
#   'SegmentUriPush'
#   'SegmentCreationAndTarPush'
#   'SegmentCreationAndUriPush'
jobType: SegmentCreationAndUriPush

# inputDirURI: Root directory of input data, expected to have scheme configured in PinotFS.
inputDirURI: 's3://my.bucket/batch/airlineStats/rawdata/'

# includeFileNamePattern: include file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will include all avro files just under the inputDirURI, not sub directories;
#   'glob:**/*.avro' will include all the avro files under inputDirURI recursively.
includeFileNamePattern: 'glob:**/*.avro'

# excludeFileNamePattern: exclude file name pattern, supported glob pattern.
# Sample usage:
#   'glob:*.avro' will exclude all avro files just under the inputDirURI, not sub directories;
#   'glob:**/*.avro' will exclude all the avro files under inputDirURI recursively.
# _excludeFileNamePattern: ''

# outputDirURI: Root directory of output segments, expected to have scheme configured in PinotFS.
outputDirURI: 's3://my.bucket/examples/output/airlineStats/segments'

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
    configs:
      'hadoop.conf.path': ''

  - scheme: s3
    className: org.apache.pinot.plugin.filesystem.S3PinotFS
    configs:
      region: 'us-west-2'
      accessKey: '****************LFVX'
      secretKey: '****************gfhz'

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

  # pushParallelism: push job parallelism, default is 1.
  pushParallelism: 2

  # pushAttempts: number of attempts for push job, default is 1, which means no retry.
  pushAttempts: 2

  # pushRetryIntervalMillis: retry wait Ms, default to 1 second.
  pushRetryIntervalMillis: 1000
```

Submit spark job with the ingestion job:

```text
${SPARK_HOME}/bin/spark-submit \
  --class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \
  --master "local[2]" \
  --deploy-mode client \
  --conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml" \
  --conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" \
  local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar \
  -jobSpecFile ${PINOT_DISTRIBUTION_DIR}/examples/sparkIngestionJobSpec.yaml
```

Below is sample spark output:

```text
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/lib/pinot-all-0.5.0-SNAPSHOT-jar-with-dependencies.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/private/tmp/spark-2.4.6-bin-hadoop2.7/jars/slf4j-log4j12-1.7.16.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
2020/08/20 13:29:11.323 WARN [NativeCodeLoader] [main] Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
2020/08/20 13:29:11.401 INFO [SecurityManager] [main] Changing view acls to: xiangfu
2020/08/20 13:29:11.402 INFO [SecurityManager] [main] Changing modify acls to: xiangfu
2020/08/20 13:29:11.402 INFO [SecurityManager] [main] Changing view acls groups to:
2020/08/20 13:29:11.403 INFO [SecurityManager] [main] Changing modify acls groups to:
2020/08/20 13:29:11.404 INFO [SecurityManager] [main] SecurityManager: authentication disabled; ui acls disabled; users  with view permissions: Set(xiangfu); groups with view permissions: Set(); users  with modify permissions: Set(xiangfu); groups with modify permissions: Set()
2020/08/20 13:29:12.297 INFO [IngestionJobLauncher] [main] SegmentGenerationJobSpec:
!!org.apache.pinot.spi.ingestion.batch.spec.SegmentGenerationJobSpec
excludeFileNamePattern: null
executionFrameworkSpec: {extraConfigs: null, name: spark, segmentGenerationJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentGenerationJobRunner,
  segmentTarPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentTarPushJobRunner,
  segmentUriPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentUriPushJobRunner}
includeFileNamePattern: glob:**/*.avro
inputDirURI: s3://my.bucket/batch/airlineStats/rawdata/
jobType: SegmentCreationAndUriPush
outputDirURI: s3://my.bucket/examples/output/airlineStats/segments
overwriteOutput: true
pinotClusterSpecs:
- {controllerURI: 'http://localhost:9000'}
pinotFSSpecs:
- className: org.apache.pinot.plugin.filesystem.HadoopPinotFS
  configs: {hadoop.conf.path: ''}
  scheme: file
- className: org.apache.pinot.plugin.filesystem.S3PinotFS
  configs: {region: us-west-2, accessKey: ****************LFVX, secretKey: ****************gfhz}
  scheme: s3
pushJobSpec: {pushAttempts: 2, pushParallelism: 2, pushRetryIntervalMillis: 1000,
  segmentUriPrefix: null, segmentUriSuffix: null}
recordReaderSpec: {className: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader,
  configClassName: null, configs: null, dataFormat: avro}
segmentNameGeneratorSpec:
  configs: {segment.name.prefix: airlineStats_batch, exclude.sequence.id: 'true'}
  type: normalizedDate
tableSpec: {schemaURI: 'http://localhost:9000/tables/airlineStats/schema', tableConfigURI: 'http://localhost:9000/tables/airlineStats',
  tableName: airlineStats}

2020/08/20 13:29:12.298 INFO [IngestionJobLauncher] [main] Trying to create instance for class org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentGenerationJobRunner
2020/08/20 13:29:12.329 INFO [PinotFSFactory] [main] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:12.344 WARN [HadoopPinotFS] [main] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:12.550 INFO [HadoopPinotFS] [main] successfully initialized HadoopPinotFS
2020/08/20 13:29:12.551 INFO [PinotFSFactory] [main] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:13.281 INFO [S3PinotFS] [main] mkdir s3://my.bucket/examples/output/airlineStats/segments
2020/08/20 13:29:15.650 INFO [SparkContext] [main] Running Spark version 2.4.6
2020/08/20 13:29:15.681 INFO [SparkContext] [main] Submitted application: org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand
2020/08/20 13:29:15.739 INFO [SecurityManager] [main] Changing view acls to: xiangfu
2020/08/20 13:29:15.740 INFO [SecurityManager] [main] Changing modify acls to: xiangfu
2020/08/20 13:29:15.740 INFO [SecurityManager] [main] Changing view acls groups to:
2020/08/20 13:29:15.740 INFO [SecurityManager] [main] Changing modify acls groups to:
2020/08/20 13:29:15.740 INFO [SecurityManager] [main] SecurityManager: authentication disabled; ui acls disabled; users  with view permissions: Set(xiangfu); groups with view permissions: Set(); users  with modify permissions: Set(xiangfu); groups with modify permissions: Set()
2020/08/20 13:29:15.991 INFO [Utils] [main] Successfully started service 'sparkDriver' on port 55913.
2020/08/20 13:29:16.018 INFO [SparkEnv] [main] Registering MapOutputTracker
2020/08/20 13:29:16.045 INFO [SparkEnv] [main] Registering BlockManagerMaster
2020/08/20 13:29:16.049 INFO [BlockManagerMasterEndpoint] [main] Using org.apache.spark.storage.DefaultTopologyMapper for getting topology information
2020/08/20 13:29:16.049 INFO [BlockManagerMasterEndpoint] [main] BlockManagerMasterEndpoint up
2020/08/20 13:29:16.063 INFO [DiskBlockManager] [main] Created local directory at /private/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/blockmgr-12f794ef-e30d-445d-b7fc-b30febc0dd86
2020/08/20 13:29:16.084 INFO [MemoryStore] [main] MemoryStore started with capacity 366.3 MB
2020/08/20 13:29:16.106 INFO [SparkEnv] [main] Registering OutputCommitCoordinator
2020/08/20 13:29:16.199 INFO [log] [main] Logging initialized @6508ms
2020/08/20 13:29:16.281 INFO [Server] [main] jetty-9.3.z-SNAPSHOT, build timestamp: unknown, git hash: unknown
2020/08/20 13:29:16.302 INFO [Server] [main] Started @6612ms
2020/08/20 13:29:16.326 WARN [Utils] [main] Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
2020/08/20 13:29:16.333 INFO [AbstractConnector] [main] Started ServerConnector@be164d8{HTTP/1.1,[http/1.1]}{0.0.0.0:4041}
2020/08/20 13:29:16.334 INFO [Utils] [main] Successfully started service 'SparkUI' on port 4041.
2020/08/20 13:29:16.361 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@28a6e171{/jobs,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.362 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@14b528b6{/jobs/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.363 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@c412556{/jobs/job,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.364 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@450f0235{/jobs/job/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.365 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@78c262ba{/stages,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.366 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@7d2c9361{/stages/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.368 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@329dc214{/stages/stage,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.369 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@7d2c345d{/stages/stage/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.370 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@217dc48e{/stages/pool,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.371 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@5db948c9{/stages/pool/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.372 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@296edc75{/storage,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.373 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@357c9bd9{/storage/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.374 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@7aea704c{/storage/rdd,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.375 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@6d0290d8{/storage/rdd/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.376 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@32507479{/environment,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.377 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@632383b9{/environment/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.378 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@4ae2e781{/executors,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.379 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@339f3a55{/executors/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.380 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@2dd63e3{/executors/threadDump,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.382 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@7d1c164a{/executors/threadDump/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.397 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@209f3887{/static,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.398 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@3a3b10f4{/,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.401 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@49580ca8{/api,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.402 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@29962b2f{/jobs/job/kill,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.404 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@491f8831{/stages/stage/kill,null,AVAILABLE,@Spark}
2020/08/20 13:29:16.407 INFO [SparkUI] [main] Bound SparkUI to 0.0.0.0, and started at http://192.168.1.139:4041
2020/08/20 13:29:16.432 INFO [SparkContext] [main] Added JAR local:///Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/lib/pinot-all-0.5.0-SNAPSHOT-jar-with-dependencies.jar at file:/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/lib/pinot-all-0.5.0-SNAPSHOT-jar-with-dependencies.jar with timestamp 1597955356432
2020/08/20 13:29:16.503 INFO [Executor] [main] Starting executor ID driver on host localhost
2020/08/20 13:29:16.532 INFO [Utils] [main] Successfully started service 'org.apache.spark.network.netty.NettyBlockTransferService' on port 55914.
2020/08/20 13:29:16.533 INFO [NettyBlockTransferService] [main] Server created on 192.168.1.139:55914
2020/08/20 13:29:16.535 INFO [BlockManager] [main] Using org.apache.spark.storage.RandomBlockReplicationPolicy for block replication policy
2020/08/20 13:29:16.571 INFO [BlockManagerMaster] [main] Registering BlockManager BlockManagerId(driver, 192.168.1.139, 55914, None)
2020/08/20 13:29:16.575 INFO [BlockManagerMasterEndpoint] [dispatcher-event-loop-0] Registering block manager 192.168.1.139:55914 with 366.3 MB RAM, BlockManagerId(driver, 192.168.1.139, 55914, None)
2020/08/20 13:29:16.578 INFO [BlockManagerMaster] [main] Registered BlockManager BlockManagerId(driver, 192.168.1.139, 55914, None)
2020/08/20 13:29:16.578 INFO [BlockManager] [main] Initialized BlockManager: BlockManagerId(driver, 192.168.1.139, 55914, None)
2020/08/20 13:29:16.744 INFO [ContextHandler] [main] Started o.s.j.s.ServletContextHandler@49754e74{/metrics/json,null,AVAILABLE,@Spark}
2020/08/20 13:29:22.330 INFO [SparkContext] [main] Added file /Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins.tar.gz at file:/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins.tar.gz with timestamp 1597955362329
2020/08/20 13:29:22.332 INFO [Utils] [main] Copying /Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins.tar.gz to /private/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/spark-8e799266-782b-4069-b12a-4c1012c54954/userFiles-54018773-0e58-42dd-967f-1ed088973783/pinot-plugins.tar.gz
2020/08/20 13:29:22.704 INFO [Utils] [main] Untarring pinot-plugins.tar.gz
2020/08/20 13:29:23.868 INFO [SparkContext] [main] Starting job: foreach at SparkSegmentGenerationJobRunner.java:214
2020/08/20 13:29:24.126 INFO [DAGScheduler] [dag-scheduler-event-loop] Got job 0 (foreach at SparkSegmentGenerationJobRunner.java:214) with 31 output partitions
2020/08/20 13:29:24.127 INFO [DAGScheduler] [dag-scheduler-event-loop] Final stage: ResultStage 0 (foreach at SparkSegmentGenerationJobRunner.java:214)
2020/08/20 13:29:24.127 INFO [DAGScheduler] [dag-scheduler-event-loop] Parents of final stage: List()
2020/08/20 13:29:24.129 INFO [DAGScheduler] [dag-scheduler-event-loop] Missing parents: List()
2020/08/20 13:29:24.134 INFO [DAGScheduler] [dag-scheduler-event-loop] Submitting ResultStage 0 (ParallelCollectionRDD[0] at parallelize at SparkSegmentGenerationJobRunner.java:206), which has no missing parents
2020/08/20 13:29:24.227 INFO [MemoryStore] [dag-scheduler-event-loop] Block broadcast_0 stored as values in memory (estimated size 5.3 KB, free 366.3 MB)
2020/08/20 13:29:24.452 INFO [MemoryStore] [dag-scheduler-event-loop] Block broadcast_0_piece0 stored as bytes in memory (estimated size 2.9 KB, free 366.3 MB)
2020/08/20 13:29:24.455 INFO [BlockManagerInfo] [dispatcher-event-loop-0] Added broadcast_0_piece0 in memory on 192.168.1.139:55914 (size: 2.9 KB, free: 366.3 MB)
2020/08/20 13:29:24.459 INFO [SparkContext] [dag-scheduler-event-loop] Created broadcast 0 from broadcast at DAGScheduler.scala:1163
2020/08/20 13:29:24.478 INFO [DAGScheduler] [dag-scheduler-event-loop] Submitting 31 missing tasks from ResultStage 0 (ParallelCollectionRDD[0] at parallelize at SparkSegmentGenerationJobRunner.java:206) (first 15 tasks are for partitions Vector(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))
2020/08/20 13:29:24.480 INFO [TaskSchedulerImpl] [dag-scheduler-event-loop] Adding task set 0.0 with 31 tasks
2020/08/20 13:29:24.546 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 0.0 in stage 0.0 (TID 0, localhost, executor driver, partition 0, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:24.548 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 1.0 in stage 0.0 (TID 1, localhost, executor driver, partition 1, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:24.560 INFO [Executor] [Executor task launch worker for task 1] Running task 1.0 in stage 0.0 (TID 1)
2020/08/20 13:29:24.560 INFO [Executor] [Executor task launch worker for task 0] Running task 0.0 in stage 0.0 (TID 0)
2020/08/20 13:29:24.565 INFO [Executor] [Executor task launch worker for task 1] Fetching file:/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins.tar.gz with timestamp 1597955362329
2020/08/20 13:29:24.801 INFO [Utils] [Executor task launch worker for task 1] /Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins.tar.gz has been previously copied to /private/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/spark-8e799266-782b-4069-b12a-4c1012c54954/userFiles-54018773-0e58-42dd-967f-1ed088973783/pinot-plugins.tar.gz
2020/08/20 13:29:24.801 INFO [Utils] [Executor task launch worker for task 1] Untarring pinot-plugins.tar.gz
2020/08/20 13:29:25.642 INFO [Executor] [Executor task launch worker for task 1] Fetching file:/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/lib/pinot-all-0.5.0-SNAPSHOT-jar-with-dependencies.jar with timestamp 1597955356432
2020/08/20 13:29:25.643 INFO [Utils] [Executor task launch worker for task 1] Copying /Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/lib/pinot-all-0.5.0-SNAPSHOT-jar-with-dependencies.jar to /private/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/spark-8e799266-782b-4069-b12a-4c1012c54954/userFiles-54018773-0e58-42dd-967f-1ed088973783/pinot-all-0.5.0-SNAPSHOT-jar-with-dependencies.jar
2020/08/20 13:29:26.015 INFO [Executor] [Executor task launch worker for task 1] Adding file:/private/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/spark-8e799266-782b-4069-b12a-4c1012c54954/userFiles-54018773-0e58-42dd-967f-1ed088973783/pinot-all-0.5.0-SNAPSHOT-jar-with-dependencies.jar to class loader
2020/08/20 13:29:26.086 INFO [PinotFSFactory] [Executor task launch worker for task 1] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:26.086 INFO [PinotFSFactory] [Executor task launch worker for task 0] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:26.087 WARN [HadoopPinotFS] [Executor task launch worker for task 1] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:26.087 WARN [HadoopPinotFS] [Executor task launch worker for task 0] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:26.108 INFO [HadoopPinotFS] [Executor task launch worker for task 1] successfully initialized HadoopPinotFS
2020/08/20 13:29:26.108 INFO [HadoopPinotFS] [Executor task launch worker for task 0] successfully initialized HadoopPinotFS
2020/08/20 13:29:26.108 INFO [PinotFSFactory] [Executor task launch worker for task 0] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:26.108 INFO [PinotFSFactory] [Executor task launch worker for task 1] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:27.425 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 1] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-1]
2020/08/20 13:29:27.425 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 1] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-1], plugins includes [null]
2020/08/20 13:29:27.428 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 1] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/02/airlineStats_data_2014-01-02.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/input/airlineStats_data_2014-01-02.avro
2020/08/20 13:29:27.429 INFO [S3PinotFS] [Executor task launch worker for task 1] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/02/airlineStats_data_2014-01-02.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/input/airlineStats_data_2014-01-02.avro
2020/08/20 13:29:27.435 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 0] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-0]
2020/08/20 13:29:27.435 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 0] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-0], plugins includes [null]
2020/08/20 13:29:27.436 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 0] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/01/airlineStats_data_2014-01-01.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/input/airlineStats_data_2014-01-01.avro
2020/08/20 13:29:27.436 INFO [S3PinotFS] [Executor task launch worker for task 0] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/01/airlineStats_data_2014-01-01.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/input/airlineStats_data_2014-01-01.avro
2020/08/20 13:29:28.176 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:28.176 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:28.369 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Finished building StatsCollector!
2020/08/20 13:29:28.369 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Collected stats for 289 documents
2020/08/20 13:29:28.370 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Finished building StatsCollector!
2020/08/20 13:29:28.371 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Collected stats for 403 documents
2020/08/20 13:29:28.404 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: FlightNum with cardinality: 386, range: 14 to 7389
2020/08/20 13:29:28.404 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: FlightNum with cardinality: 281, range: 1 to 7433
2020/08/20 13:29:28.425 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: Origin, size: 252
2020/08/20 13:29:28.425 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: Origin, size: 294
2020/08/20 13:29:28.426 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: Origin with cardinality: 98, max length in bytes: 3, range: ABQ to VPS
2020/08/20 13:29:28.426 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: Origin with cardinality: 84, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:28.428 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:28.428 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:28.431 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: LateAircraftDelay with cardinality: 50, range: -2147483648 to 303
2020/08/20 13:29:28.431 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: LateAircraftDelay with cardinality: 38, range: -2147483648 to 250
2020/08/20 13:29:28.433 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivActualElapsedTime with cardinality: 27, range: -2147483648 to 435
2020/08/20 13:29:28.433 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivActualElapsedTime with cardinality: 87, range: -2147483648 to 1241
2020/08/20 13:29:28.435 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivWheelsOns with cardinality: 43, range: -2147483648 to 2058
2020/08/20 13:29:28.435 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivWheelsOns with cardinality: 127, range: -2147483648 to 2359
2020/08/20 13:29:28.438 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivWheelsOffs with cardinality: 93, range: -2147483648 to 2353
2020/08/20 13:29:28.438 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivWheelsOffs with cardinality: 28, range: -2147483648 to 2139
2020/08/20 13:29:28.441 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: AirTime with cardinality: 136, range: -2147483648 to 362
2020/08/20 13:29:28.441 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: AirTime with cardinality: 151, range: -2147483648 to 366
2020/08/20 13:29:28.443 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:28.443 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:28.445 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivTotalGTimes with cardinality: 27, range: -2147483648 to 107
2020/08/20 13:29:28.445 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivTotalGTimes with cardinality: 68, range: -2147483648 to 119
2020/08/20 13:29:28.446 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:28.446 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:28.447 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:28.447 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:28.448 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DestCityMarketID with cardinality: 81, range: 30136 to 34819
2020/08/20 13:29:28.448 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DestCityMarketID with cardinality: 81, range: 30136 to 35411
2020/08/20 13:29:28.450 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 28, range: -2147483648 to 1591902
2020/08/20 13:29:28.450 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 56, range: -2147483648 to 1540103
2020/08/20 13:29:28.451 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16071 to 16071
2020/08/20 13:29:28.451 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16072 to 16072
2020/08/20 13:29:28.452 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DepTime with cardinality: 321, range: -2147483648 to 2356
2020/08/20 13:29:28.452 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DepTime with cardinality: 248, range: -2147483648 to 2357
2020/08/20 13:29:28.453 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:28.454 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:28.455 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: CRSElapsedTime with cardinality: 175, range: 42 to 570
2020/08/20 13:29:28.456 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: CRSElapsedTime with cardinality: 148, range: 36 to 398
2020/08/20 13:29:28.456 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: DestStateName, size: 588
2020/08/20 13:29:28.457 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: DestStateName, size: 588
2020/08/20 13:29:28.483 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:28.484 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:28.485 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:28.485 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:28.486 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:28.486 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:28.488 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DestAirportID with cardinality: 93, range: 10136 to 15411
2020/08/20 13:29:28.488 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DestAirportID with cardinality: 95, range: 10136 to 15370
2020/08/20 13:29:28.489 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: Distance with cardinality: 296, range: 127 to 4983
2020/08/20 13:29:28.489 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: Distance with cardinality: 244, range: 73 to 3302
2020/08/20 13:29:28.493 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 162
2020/08/20 13:29:28.493 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:28.496 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: ArrTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:28.496 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:28.500 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivArrDelay with cardinality: 93, range: -2147483648 to 1068
2020/08/20 13:29:28.500 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivArrDelay with cardinality: 25, range: -2147483648 to 301
2020/08/20 13:29:28.502 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: SecurityDelay with cardinality: 3, range: -2147483648 to 4
2020/08/20 13:29:28.503 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:28.504 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: LongestAddGTime with cardinality: 2, range: -2147483648 to 128
2020/08/20 13:29:28.505 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: LongestAddGTime with cardinality: 11, range: -2147483648 to 148
2020/08/20 13:29:28.507 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: OriginWac with cardinality: 42, range: 2 to 93
2020/08/20 13:29:28.507 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: OriginWac with cardinality: 47, range: 1 to 93
2020/08/20 13:29:28.509 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: WheelsOff with cardinality: 328, range: -2147483648 to 2357
2020/08/20 13:29:28.509 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: WheelsOff with cardinality: 246, range: -2147483648 to 2316
2020/08/20 13:29:28.511 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DestAirportSeqID with cardinality: 95, range: 1013603 to 1537002
2020/08/20 13:29:28.512 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DestAirportSeqID with cardinality: 93, range: 1013603 to 1541103
2020/08/20 13:29:28.513 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:28.514 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:28.515 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:28.517 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:28.517 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:28.518 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:28.519 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:28.520 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:28.522 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: ActualElapsedTime with cardinality: 145, range: -2147483648 to 397
2020/08/20 13:29:28.522 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: ActualElapsedTime with cardinality: 153, range: -2147483648 to 391
2020/08/20 13:29:28.524 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:28.525 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: OriginStateName, size: 658
2020/08/20 13:29:28.525 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:28.526 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: OriginStateName with cardinality: 47, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:28.527 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: OriginStateName, size: 588
2020/08/20 13:29:28.531 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: OriginStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:28.532 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DepartureDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:28.533 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DepartureDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:28.534 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:28.534 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:28.535 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:28.535 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:28.536 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-02 to 2014-01-02
2020/08/20 13:29:28.537 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-01 to 2014-01-01
2020/08/20 13:29:28.538 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: OriginCityName, size: 3196
2020/08/20 13:29:28.539 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: OriginCityName with cardinality: 94, max length in bytes: 34, range: Albany, NY to Wichita, KS
2020/08/20 13:29:28.539 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: OriginCityName, size: 2240
2020/08/20 13:29:28.539 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: OriginCityName with cardinality: 80, max length in bytes: 28, range: Albuquerque, NM to Wichita, KS
2020/08/20 13:29:28.540 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: OriginStateFips with cardinality: 47, range: 1 to 72
2020/08/20 13:29:28.541 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: OriginStateFips with cardinality: 42, range: 1 to 72
2020/08/20 13:29:28.541 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: OriginState, size: 94
2020/08/20 13:29:28.542 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: OriginState with cardinality: 47, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:28.542 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: OriginState, size: 84
2020/08/20 13:29:28.543 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: OriginState with cardinality: 42, max length in bytes: 2, range: AL to WI
2020/08/20 13:29:28.543 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:28.544 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:28.545 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: WeatherDelay with cardinality: 19, range: -2147483648 to 973
2020/08/20 13:29:28.546 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: WeatherDelay with cardinality: 10, range: -2147483648 to 74
2020/08/20 13:29:28.546 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:28.547 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:28.548 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: WheelsOn with cardinality: 282, range: -2147483648 to 2347
2020/08/20 13:29:28.549 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: WheelsOn with cardinality: 234, range: -2147483648 to 2349
2020/08/20 13:29:28.550 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: OriginAirportID with cardinality: 98, range: 10140 to 15624
2020/08/20 13:29:28.551 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: OriginCityMarketID with cardinality: 82, range: 30140 to 35323
2020/08/20 13:29:28.551 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: OriginAirportID with cardinality: 84, range: 10140 to 15919
2020/08/20 13:29:28.553 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: OriginCityMarketID with cardinality: 71, range: 30140 to 34819
2020/08/20 13:29:28.553 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: NASDelay with cardinality: 47, range: -2147483648 to 145
2020/08/20 13:29:28.554 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: ArrTime with cardinality: 291, range: -2147483648 to 2357
2020/08/20 13:29:28.554 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: NASDelay with cardinality: 34, range: -2147483648 to 226
2020/08/20 13:29:28.556 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:29:28.556 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: ArrTime with cardinality: 234, range: -2147483648 to 2353
2020/08/20 13:29:28.556 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:28.557 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:29:28.557 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:28.572 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:28.573 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:28.574 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:28.575 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 2 to 2
2020/08/20 13:29:28.576 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:28.577 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: RandomAirports, size: 272
2020/08/20 13:29:28.577 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 1 to 1
2020/08/20 13:29:28.578 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: RandomAirports with cardinality: 68, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:28.578 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: RandomAirports, size: 292
2020/08/20 13:29:28.579 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: RandomAirports with cardinality: 73, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:28.579 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: TotalAddGTime with cardinality: 11, range: -2147483648 to 148
2020/08/20 13:29:28.580 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: CRSDepTime with cardinality: 243, range: 422 to 2359
2020/08/20 13:29:28.580 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: TotalAddGTime with cardinality: 2, range: -2147483648 to 128
2020/08/20 13:29:28.581 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 4 to 4
2020/08/20 13:29:28.581 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: CRSDepTime with cardinality: 190, range: 5 to 2300
2020/08/20 13:29:28.583 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:28.583 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 3 to 3
2020/08/20 13:29:28.583 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:28.584 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:28.584 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: Dest, size: 285
2020/08/20 13:29:28.584 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:28.585 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: Dest with cardinality: 95, max length in bytes: 3, range: ABI to TUL
2020/08/20 13:29:28.586 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: Dest, size: 279
2020/08/20 13:29:28.586 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: Dest with cardinality: 93, max length in bytes: 3, range: ABI to TYR
2020/08/20 13:29:28.586 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: FirstDepTime with cardinality: 11, range: -2147483648 to 2356
2020/08/20 13:29:28.587 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: FirstDepTime with cardinality: 2, range: -2147483648 to 1153
2020/08/20 13:29:28.597 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: DivTailNums, size: 588
2020/08/20 13:29:28.597 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: DivTailNums, size: 168
2020/08/20 13:29:28.598 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: DivTailNums with cardinality: 28, max length in bytes: 6, range: N13995 to null
2020/08/20 13:29:28.598 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: DivTailNums with cardinality: 98, max length in bytes: 6, range: N001AA to null
2020/08/20 13:29:28.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DepDelayMinutes with cardinality: 134, range: -2147483648 to 973
2020/08/20 13:29:28.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DepDelayMinutes with cardinality: 80, range: -2147483648 to 293
2020/08/20 13:29:28.601 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DepDelay with cardinality: 91, range: -2147483648 to 293
2020/08/20 13:29:28.601 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DepDelay with cardinality: 147, range: -2147483648 to 973
2020/08/20 13:29:28.603 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: TaxiIn with cardinality: 58, range: -2147483648 to 196
2020/08/20 13:29:28.603 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: TaxiIn with cardinality: 28, range: -2147483648 to 93
2020/08/20 13:29:28.604 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: OriginAirportSeqID with cardinality: 98, range: 1014002 to 1562401
2020/08/20 13:29:28.605 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: OriginAirportSeqID with cardinality: 84, range: 1014002 to 1591902
2020/08/20 13:29:28.606 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 72
2020/08/20 13:29:28.607 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 72
2020/08/20 13:29:28.608 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: ArrDelay with cardinality: 115, range: -2147483648 to 996
2020/08/20 13:29:28.609 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: ArrDelay with cardinality: 97, range: -2147483648 to 384
2020/08/20 13:29:28.610 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:28.611 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:28.612 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivAirportIDs with cardinality: 56, range: -2147483648 to 15401
2020/08/20 13:29:28.612 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivAirportIDs with cardinality: 28, range: -2147483648 to 15919
2020/08/20 13:29:28.613 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: TaxiOut with cardinality: 66, range: -2147483648 to 138
2020/08/20 13:29:28.613 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: TaxiOut with cardinality: 47, range: -2147483648 to 141
2020/08/20 13:29:28.616 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: CarrierDelay with cardinality: 40, range: -2147483648 to 203
2020/08/20 13:29:28.616 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: CarrierDelay with cardinality: 34, range: -2147483648 to 139
2020/08/20 13:29:28.618 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:28.618 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:28.619 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivLongestGTimes with cardinality: 56, range: -2147483648 to 111
2020/08/20 13:29:28.619 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivLongestGTimes with cardinality: 26, range: -2147483648 to 94
2020/08/20 13:29:28.620 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: DivAirports, size: 112
2020/08/20 13:29:28.620 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: DivAirports, size: 224
2020/08/20 13:29:28.620 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: DivAirports with cardinality: 28, max length in bytes: 4, range: ATW to null
2020/08/20 13:29:28.621 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: DivAirports with cardinality: 56, max length in bytes: 4, range: ABQ to null
2020/08/20 13:29:28.622 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: DivDistance with cardinality: 10, range: -2147483648 to 277
2020/08/20 13:29:28.622 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: DivDistance with cardinality: 26, range: -2147483648 to 1166
2020/08/20 13:29:28.623 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:28.623 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:28.624 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: ArrDelayMinutes with cardinality: 70, range: -2147483648 to 384
2020/08/20 13:29:28.625 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: ArrDelayMinutes with cardinality: 91, range: -2147483648 to 996
2020/08/20 13:29:28.629 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for INT column: CRSArrTime with cardinality: 226, range: 1 to 2358
2020/08/20 13:29:28.629 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for INT column: CRSArrTime with cardinality: 281, range: 10 to 2359
2020/08/20 13:29:28.630 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: TailNum, size: 1686
2020/08/20 13:29:28.630 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: TailNum, size: 2298
2020/08/20 13:29:28.631 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: TailNum with cardinality: 281, max length in bytes: 6, range: N104UW to null
2020/08/20 13:29:28.631 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: TailNum with cardinality: 383, max length in bytes: 6, range: N001AA to null
2020/08/20 13:29:28.632 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Using fixed bytes value dictionary for column: DestCityName, size: 2670
2020/08/20 13:29:28.632 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Using fixed bytes value dictionary for column: DestCityName, size: 2730
2020/08/20 13:29:28.632 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 0] Created dictionary for STRING column: DestCityName with cardinality: 89, max length in bytes: 30, range: Abilene, TX to Wichita, KS
2020/08/20 13:29:28.632 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 1] Created dictionary for STRING column: DestCityName with cardinality: 91, max length in bytes: 30, range: Abilene, TX to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:28.634 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Start building IndexCreator!
2020/08/20 13:29:28.634 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Start building IndexCreator!
2020/08/20 13:29:28.701 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Finished records indexing in IndexCreator!
2020/08/20 13:29:28.728 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Finished records indexing in IndexCreator!
2020/08/20 13:29:28.847 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Finished segment seal!
2020/08/20 13:29:28.849 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Finished segment seal!
2020/08/20 13:29:28.853 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 0] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01 to v3 format
2020/08/20 13:29:28.853 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 1] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02 to v3 format
2020/08/20 13:29:29.152 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 1] v3 segment location for segment: airlineStats_batch_2014-01-02_2014-01-02 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02/v3
2020/08/20 13:29:29.153 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 0] v3 segment location for segment: airlineStats_batch_2014-01-01_2014-01-01 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01/v3
2020/08/20 13:29:29.153 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 1] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02
2020/08/20 13:29:29.153 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 0] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01
2020/08/20 13:29:29.203 INFO [CrcUtils] [Executor task launch worker for task 1] Computed crc = 3712507352, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02/v3/metadata.properties]
2020/08/20 13:29:29.203 INFO [CrcUtils] [Executor task launch worker for task 0] Computed crc = 2314135128, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01/v3/metadata.properties]
2020/08/20 13:29:29.204 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Driver, record read time : 49
2020/08/20 13:29:29.204 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Driver, record read time : 35
2020/08/20 13:29:29.204 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Driver, stats collector time : 0
2020/08/20 13:29:29.204 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Driver, stats collector time : 0
2020/08/20 13:29:29.204 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 1] Driver, indexing time : 43
2020/08/20 13:29:29.204 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 0] Driver, indexing time : 31
2020/08/20 13:29:29.204 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 1] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02.tar.gz
2020/08/20 13:29:29.204 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 0] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01.tar.gz
2020/08/20 13:29:29.216 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 0] Size for segment: airlineStats_batch_2014-01-01_2014-01-01, uncompressed: 113.77K, compressed: 33.01K
2020/08/20 13:29:29.216 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 1] Size for segment: airlineStats_batch_2014-01-02_2014-01-02, uncompressed: 129.32K, compressed: 42.29K
2020/08/20 13:29:29.217 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 1] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_batch_2014-01-02_2014-01-02.tar.gz]
2020/08/20 13:29:29.217 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 0] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_batch_2014-01-01_2014-01-01.tar.gz]
2020/08/20 13:29:29.217 INFO [S3PinotFS] [Executor task launch worker for task 1] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-a67ab5f6-1fe6-4462-b840-270e60745ba1/output/airlineStats_batch_2014-01-02_2014-01-02.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_batch_2014-01-02_2014-01-02.tar.gz
2020/08/20 13:29:29.217 INFO [S3PinotFS] [Executor task launch worker for task 0] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-831d148a-5f2b-4299-aa04-41884d6c7dfa/output/airlineStats_batch_2014-01-01_2014-01-01.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_batch_2014-01-01_2014-01-01.tar.gz
2020/08/20 13:29:29.596 INFO [Executor] [Executor task launch worker for task 0] Finished task 0.0 in stage 0.0 (TID 0). 708 bytes result sent to driver
2020/08/20 13:29:29.599 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 2.0 in stage 0.0 (TID 2, localhost, executor driver, partition 2, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:29.599 INFO [Executor] [Executor task launch worker for task 2] Running task 2.0 in stage 0.0 (TID 2)
2020/08/20 13:29:29.606 INFO [TaskSetManager] [task-result-getter-0] Finished task 0.0 in stage 0.0 (TID 0) in 5077 ms on localhost (executor driver) (1/31)
2020/08/20 13:29:29.607 INFO [PinotFSFactory] [Executor task launch worker for task 2] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:29.607 WARN [HadoopPinotFS] [Executor task launch worker for task 2] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:29.634 INFO [HadoopPinotFS] [Executor task launch worker for task 2] successfully initialized HadoopPinotFS
2020/08/20 13:29:29.634 INFO [PinotFSFactory] [Executor task launch worker for task 2] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:29.778 INFO [Executor] [Executor task launch worker for task 1] Finished task 1.0 in stage 0.0 (TID 1). 708 bytes result sent to driver
2020/08/20 13:29:29.779 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 3.0 in stage 0.0 (TID 3, localhost, executor driver, partition 3, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:29.779 INFO [Executor] [Executor task launch worker for task 3] Running task 3.0 in stage 0.0 (TID 3)
2020/08/20 13:29:29.779 INFO [TaskSetManager] [task-result-getter-1] Finished task 1.0 in stage 0.0 (TID 1) in 5231 ms on localhost (executor driver) (2/31)
2020/08/20 13:29:29.785 INFO [PinotFSFactory] [Executor task launch worker for task 3] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:29.786 WARN [HadoopPinotFS] [Executor task launch worker for task 3] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:29.813 INFO [HadoopPinotFS] [Executor task launch worker for task 3] successfully initialized HadoopPinotFS
2020/08/20 13:29:29.813 INFO [PinotFSFactory] [Executor task launch worker for task 3] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:30.964 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 2] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-2]
2020/08/20 13:29:30.964 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 2] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-2], plugins includes [null]
2020/08/20 13:29:30.965 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 2] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/03/airlineStats_data_2014-01-03.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/input/airlineStats_data_2014-01-03.avro
2020/08/20 13:29:30.965 INFO [S3PinotFS] [Executor task launch worker for task 2] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/03/airlineStats_data_2014-01-03.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/input/airlineStats_data_2014-01-03.avro
2020/08/20 13:29:31.127 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 3] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-3]
2020/08/20 13:29:31.127 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 3] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-3], plugins includes [null]
2020/08/20 13:29:31.128 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 3] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/04/airlineStats_data_2014-01-04.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/input/airlineStats_data_2014-01-04.avro
2020/08/20 13:29:31.128 INFO [S3PinotFS] [Executor task launch worker for task 3] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/04/airlineStats_data_2014-01-04.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/input/airlineStats_data_2014-01-04.avro
2020/08/20 13:29:31.281 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:31.343 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Finished building StatsCollector!
2020/08/20 13:29:31.344 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Collected stats for 409 documents
2020/08/20 13:29:31.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: FlightNum with cardinality: 395, range: 6 to 7428
2020/08/20 13:29:31.346 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: Origin, size: 360
2020/08/20 13:29:31.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: Origin with cardinality: 120, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:29:31.348 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:31.349 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: LateAircraftDelay with cardinality: 48, range: -2147483648 to 185
2020/08/20 13:29:31.350 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivActualElapsedTime with cardinality: 47, range: -2147483648 to 891
2020/08/20 13:29:31.351 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivWheelsOns with cardinality: 107, range: -2147483648 to 2341
2020/08/20 13:29:31.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivWheelsOffs with cardinality: 47, range: -2147483648 to 2153
2020/08/20 13:29:31.353 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: AirTime with cardinality: 151, range: -2147483648 to 361
2020/08/20 13:29:31.354 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:31.356 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivTotalGTimes with cardinality: 38, range: -2147483648 to 94
2020/08/20 13:29:31.356 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:31.357 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:31.357 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DestCityMarketID with cardinality: 90, range: 30140 to 35356
2020/08/20 13:29:31.358 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 58, range: -2147483648 to 1584102
2020/08/20 13:29:31.359 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16073 to 16073
2020/08/20 13:29:31.361 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DepTime with cardinality: 302, range: -2147483648 to 2345
2020/08/20 13:29:31.362 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:31.363 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: CRSElapsedTime with cardinality: 180, range: 19 to 399
2020/08/20 13:29:31.364 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: DestStateName, size: 588
2020/08/20 13:29:31.366 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:31.367 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:31.367 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:31.369 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DestAirportID with cardinality: 106, range: 10140 to 15919
2020/08/20 13:29:31.370 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: Distance with cardinality: 297, range: 56 to 2762
2020/08/20 13:29:31.371 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:31.371 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:31.373 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivArrDelay with cardinality: 43, range: -2147483648 to 868
2020/08/20 13:29:31.375 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:31.376 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: LongestAddGTime with cardinality: 4, range: -2147483648 to 58
2020/08/20 13:29:31.377 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: OriginWac with cardinality: 45, range: 1 to 93
2020/08/20 13:29:31.378 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: WheelsOff with cardinality: 309, range: -2147483648 to 2358
2020/08/20 13:29:31.379 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DestAirportSeqID with cardinality: 106, range: 1014002 to 1591902
2020/08/20 13:29:31.379 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:31.380 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:31.381 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:31.381 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:31.382 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: ActualElapsedTime with cardinality: 154, range: -2147483648 to 386
2020/08/20 13:29:31.383 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:31.384 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: OriginStateName, size: 855
2020/08/20 13:29:31.384 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: OriginStateName with cardinality: 45, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:29:31.385 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DepartureDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:31.386 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:31.387 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:31.387 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-03 to 2014-01-03
2020/08/20 13:29:31.388 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: OriginCityName, size: 3480
2020/08/20 13:29:31.388 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: OriginCityName with cardinality: 116, max length in bytes: 30, range: Akron, OH to Yuma, AZ
2020/08/20 13:29:31.389 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: OriginStateFips with cardinality: 45, range: 1 to 78
2020/08/20 13:29:31.390 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: OriginState, size: 90
2020/08/20 13:29:31.390 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: OriginState with cardinality: 45, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:31.393 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:31.394 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: WeatherDelay with cardinality: 18, range: -2147483648 to 237
2020/08/20 13:29:31.395 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:31.396 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: WheelsOn with cardinality: 276, range: -2147483648 to 2400
2020/08/20 13:29:31.397 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: OriginAirportID with cardinality: 120, range: 10140 to 16218
2020/08/20 13:29:31.398 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: OriginCityMarketID with cardinality: 105, range: 30140 to 35249
2020/08/20 13:29:31.399 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: NASDelay with cardinality: 37, range: -2147483648 to 113
2020/08/20 13:29:31.400 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: ArrTime with cardinality: 266, range: -2147483648 to 2355
2020/08/20 13:29:31.401 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:29:31.401 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:31.402 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:31.404 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:31.406 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 3 to 3
2020/08/20 13:29:31.408 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: RandomAirports, size: 316
2020/08/20 13:29:31.408 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: RandomAirports with cardinality: 79, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:31.409 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: TotalAddGTime with cardinality: 4, range: -2147483648 to 58
2020/08/20 13:29:31.410 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: CRSDepTime with cardinality: 250, range: 50 to 2355
2020/08/20 13:29:31.411 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 5 to 5
2020/08/20 13:29:31.412 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:31.413 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:31.414 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: Dest, size: 318
2020/08/20 13:29:31.414 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: Dest with cardinality: 106, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:31.415 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: FirstDepTime with cardinality: 4, range: -2147483648 to 726
2020/08/20 13:29:31.416 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: DivTailNums, size: 300
2020/08/20 13:29:31.416 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: DivTailNums with cardinality: 50, max length in bytes: 6, range: N14940 to null
2020/08/20 13:29:31.417 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DepDelayMinutes with cardinality: 115, range: -2147483648 to 466
2020/08/20 13:29:31.418 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DepDelay with cardinality: 129, range: -2147483648 to 466
2020/08/20 13:29:31.420 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: TaxiIn with cardinality: 39, range: -2147483648 to 113
2020/08/20 13:29:31.421 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: OriginAirportSeqID with cardinality: 120, range: 1014002 to 1621801
2020/08/20 13:29:31.423 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 72
2020/08/20 13:29:31.424 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: ArrDelay with cardinality: 117, range: -2147483648 to 414
2020/08/20 13:29:31.425 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:31.426 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivAirportIDs with cardinality: 58, range: -2147483648 to 15841
2020/08/20 13:29:31.427 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: TaxiOut with cardinality: 46, range: -2147483648 to 78
2020/08/20 13:29:31.428 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: CarrierDelay with cardinality: 46, range: -2147483648 to 414
2020/08/20 13:29:31.429 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:31.430 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivLongestGTimes with cardinality: 30, range: -2147483648 to 70
2020/08/20 13:29:31.430 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: DivAirports, size: 232
2020/08/20 13:29:31.431 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: DivAirports with cardinality: 58, max length in bytes: 4, range: ATL to null
2020/08/20 13:29:31.432 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: DivDistance with cardinality: 45, range: -2147483648 to 1807
2020/08/20 13:29:31.433 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:31.434 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: ArrDelayMinutes with cardinality: 92, range: -2147483648 to 414
2020/08/20 13:29:31.437 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for INT column: CRSArrTime with cardinality: 294, range: 5 to 2359
2020/08/20 13:29:31.439 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: TailNum, size: 2298
2020/08/20 13:29:31.439 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: TailNum with cardinality: 383, max length in bytes: 6, range: N009AA to null
2020/08/20 13:29:31.440 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Using fixed bytes value dictionary for column: DestCityName, size: 3060
2020/08/20 13:29:31.441 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 2] Created dictionary for STRING column: DestCityName with cardinality: 102, max length in bytes: 30, range: Albuquerque, NM to Williston, ND
2020/08/20 13:29:31.442 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Start building IndexCreator!
2020/08/20 13:29:31.499 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Finished records indexing in IndexCreator!
2020/08/20 13:29:31.524 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:31.533 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Finished segment seal!
2020/08/20 13:29:31.533 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 2] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03 to v3 format
2020/08/20 13:29:31.570 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Finished building StatsCollector!
2020/08/20 13:29:31.570 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Collected stats for 307 documents
2020/08/20 13:29:31.574 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: FlightNum with cardinality: 303, range: 4 to 7410
2020/08/20 13:29:31.576 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: Origin, size: 297
2020/08/20 13:29:31.577 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: Origin with cardinality: 99, max length in bytes: 3, range: ALB to TVC
2020/08/20 13:29:31.578 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:31.579 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: LateAircraftDelay with cardinality: 58, range: -2147483648 to 373
2020/08/20 13:29:31.580 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivActualElapsedTime with cardinality: 31, range: -2147483648 to 773
2020/08/20 13:29:31.582 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivWheelsOns with cardinality: 50, range: -2147483648 to 2309
2020/08/20 13:29:31.583 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivWheelsOffs with cardinality: 34, range: -2147483648 to 2315
2020/08/20 13:29:31.584 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: AirTime with cardinality: 151, range: -2147483648 to 397
2020/08/20 13:29:31.586 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:31.587 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivTotalGTimes with cardinality: 40, range: -2147483648 to 123
2020/08/20 13:29:31.588 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:31.588 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:31.589 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DestCityMarketID with cardinality: 82, range: 30070 to 35389
2020/08/20 13:29:31.590 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 27, range: -2147483648 to 1591902
2020/08/20 13:29:31.591 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16074 to 16074
2020/08/20 13:29:31.592 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DepTime with cardinality: 246, range: -2147483648 to 2359
2020/08/20 13:29:31.593 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:31.594 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: CRSElapsedTime with cardinality: 154, range: 39 to 430
2020/08/20 13:29:31.594 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: DestStateName, size: 588
2020/08/20 13:29:31.595 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Washington
2020/08/20 13:29:31.595 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:31.596 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:31.597 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DestAirportID with cardinality: 98, range: 10140 to 15389
2020/08/20 13:29:31.598 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: Distance with cardinality: 247, range: 86 to 3801
2020/08/20 13:29:31.599 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:31.599 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:31.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivArrDelay with cardinality: 30, range: -2147483648 to 681
2020/08/20 13:29:31.601 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:31.604 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: LongestAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:31.606 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: OriginWac with cardinality: 36, range: 1 to 93
2020/08/20 13:29:31.608 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: WheelsOff with cardinality: 257, range: -2147483648 to 2351
2020/08/20 13:29:31.609 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DestAirportSeqID with cardinality: 98, range: 1014002 to 1538902
2020/08/20 13:29:31.610 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:31.610 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:31.611 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:31.613 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:31.614 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: ActualElapsedTime with cardinality: 144, range: -2147483648 to 415
2020/08/20 13:29:31.615 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:31.616 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: OriginStateName, size: 1656
2020/08/20 13:29:31.616 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: OriginStateName with cardinality: 36, max length in bytes: 46, range: Alabama to Wisconsin
2020/08/20 13:29:31.617 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DepartureDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:31.619 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:31.620 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:31.620 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-04 to 2014-01-04
2020/08/20 13:29:31.621 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: OriginCityName, size: 3230
2020/08/20 13:29:31.622 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: OriginCityName with cardinality: 95, max length in bytes: 34, range: Aguadilla, PR to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:31.623 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: OriginStateFips with cardinality: 36, range: 1 to 75
2020/08/20 13:29:31.623 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: OriginState, size: 72
2020/08/20 13:29:31.624 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: OriginState with cardinality: 36, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:31.625 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:31.626 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: WeatherDelay with cardinality: 14, range: -2147483648 to 132
2020/08/20 13:29:31.627 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:31.628 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: WheelsOn with cardinality: 238, range: -2147483648 to 2359
2020/08/20 13:29:31.630 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: OriginAirportID with cardinality: 99, range: 10257 to 15380
2020/08/20 13:29:31.631 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: OriginCityMarketID with cardinality: 85, range: 30189 to 35380
2020/08/20 13:29:31.632 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: NASDelay with cardinality: 30, range: -2147483648 to 133
2020/08/20 13:29:31.633 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: ArrTime with cardinality: 232, range: -2147483648 to 2352
2020/08/20 13:29:31.634 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:29:31.635 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WA
2020/08/20 13:29:31.636 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:31.637 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:31.639 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 4 to 4
2020/08/20 13:29:31.640 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: RandomAirports, size: 312
2020/08/20 13:29:31.641 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: RandomAirports with cardinality: 78, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:31.642 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: TotalAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:31.643 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: CRSDepTime with cardinality: 209, range: 500 to 2335
2020/08/20 13:29:31.644 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 6 to 6
2020/08/20 13:29:31.644 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:31.645 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:31.645 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: Dest, size: 294
2020/08/20 13:29:31.646 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: Dest with cardinality: 98, max length in bytes: 3, range: ABQ to TWF
2020/08/20 13:29:31.646 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: FirstDepTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:31.647 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: DivTailNums, size: 210
2020/08/20 13:29:31.647 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: DivTailNums with cardinality: 35, max length in bytes: 6, range: N008AA to null
2020/08/20 13:29:31.649 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DepDelayMinutes with cardinality: 101, range: -2147483648 to 400
2020/08/20 13:29:31.649 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DepDelay with cardinality: 114, range: -2147483648 to 400
2020/08/20 13:29:31.651 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: TaxiIn with cardinality: 28, range: -2147483648 to 46
2020/08/20 13:29:31.652 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: OriginAirportSeqID with cardinality: 99, range: 1025702 to 1538003
2020/08/20 13:29:31.653 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 53
2020/08/20 13:29:31.654 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: ArrDelay with cardinality: 117, range: -2147483648 to 410
2020/08/20 13:29:31.655 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:31.656 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivAirportIDs with cardinality: 27, range: -2147483648 to 15919
2020/08/20 13:29:31.657 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: TaxiOut with cardinality: 38, range: -2147483648 to 69
2020/08/20 13:29:31.658 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: CarrierDelay with cardinality: 46, range: -2147483648 to 179
2020/08/20 13:29:31.660 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:31.661 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivLongestGTimes with cardinality: 33, range: -2147483648 to 123
2020/08/20 13:29:31.661 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: DivAirports, size: 108
2020/08/20 13:29:31.662 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: DivAirports with cardinality: 27, max length in bytes: 4, range: ABQ to null
2020/08/20 13:29:31.664 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: DivDistance with cardinality: 12, range: -2147483648 to 895
2020/08/20 13:29:31.665 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:31.666 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: ArrDelayMinutes with cardinality: 89, range: -2147483648 to 410
2020/08/20 13:29:31.668 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for INT column: CRSArrTime with cardinality: 249, range: 5 to 2355
2020/08/20 13:29:31.669 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: TailNum, size: 1770
2020/08/20 13:29:31.669 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: TailNum with cardinality: 295, max length in bytes: 6, range: D942DN to null
2020/08/20 13:29:31.672 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Using fixed bytes value dictionary for column: DestCityName, size: 2350
2020/08/20 13:29:31.673 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 3] Created dictionary for STRING column: DestCityName with cardinality: 94, max length in bytes: 25, range: Akron, OH to Washington, DC
2020/08/20 13:29:31.675 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Start building IndexCreator!
2020/08/20 13:29:31.712 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Finished records indexing in IndexCreator!
2020/08/20 13:29:31.743 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 2] v3 segment location for segment: airlineStats_batch_2014-01-03_2014-01-03 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03/v3
2020/08/20 13:29:31.743 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Finished segment seal!
2020/08/20 13:29:31.744 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 2] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03
2020/08/20 13:29:31.744 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 3] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04 to v3 format
2020/08/20 13:29:31.792 INFO [CrcUtils] [Executor task launch worker for task 2] Computed crc = 2613637391, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03/v3/metadata.properties]
2020/08/20 13:29:31.792 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Driver, record read time : 44
2020/08/20 13:29:31.792 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Driver, stats collector time : 0
2020/08/20 13:29:31.792 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 2] Driver, indexing time : 13
2020/08/20 13:29:31.792 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 2] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03.tar.gz
2020/08/20 13:29:31.809 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 2] Size for segment: airlineStats_batch_2014-01-03_2014-01-03, uncompressed: 129.42K, compressed: 42.12K
2020/08/20 13:29:31.809 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 2] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_batch_2014-01-03_2014-01-03.tar.gz]
2020/08/20 13:29:31.809 INFO [S3PinotFS] [Executor task launch worker for task 2] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-02888bd0-8351-4053-a483-20ebf35bcc18/output/airlineStats_batch_2014-01-03_2014-01-03.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_batch_2014-01-03_2014-01-03.tar.gz
2020/08/20 13:29:31.893 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 3] v3 segment location for segment: airlineStats_batch_2014-01-04_2014-01-04 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04/v3
2020/08/20 13:29:31.893 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 3] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04
2020/08/20 13:29:31.930 INFO [CrcUtils] [Executor task launch worker for task 3] Computed crc = 586498794, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04/v3/metadata.properties]
2020/08/20 13:29:31.931 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Driver, record read time : 21
2020/08/20 13:29:31.931 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Driver, stats collector time : 0
2020/08/20 13:29:31.931 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 3] Driver, indexing time : 16
2020/08/20 13:29:31.931 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 3] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04.tar.gz
2020/08/20 13:29:31.944 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 3] Size for segment: airlineStats_batch_2014-01-04_2014-01-04, uncompressed: 117.43K, compressed: 34.7K
2020/08/20 13:29:31.944 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 3] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_batch_2014-01-04_2014-01-04.tar.gz]
2020/08/20 13:29:31.944 INFO [S3PinotFS] [Executor task launch worker for task 3] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-986251b5-f003-48b8-804c-7d47e6bda26e/output/airlineStats_batch_2014-01-04_2014-01-04.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_batch_2014-01-04_2014-01-04.tar.gz
2020/08/20 13:29:32.440 INFO [Executor] [Executor task launch worker for task 3] Finished task 3.0 in stage 0.0 (TID 3). 708 bytes result sent to driver
2020/08/20 13:29:32.441 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 4.0 in stage 0.0 (TID 4, localhost, executor driver, partition 4, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:32.441 INFO [Executor] [Executor task launch worker for task 4] Running task 4.0 in stage 0.0 (TID 4)
2020/08/20 13:29:32.441 INFO [TaskSetManager] [task-result-getter-2] Finished task 3.0 in stage 0.0 (TID 3) in 2663 ms on localhost (executor driver) (3/31)
2020/08/20 13:29:32.444 INFO [PinotFSFactory] [Executor task launch worker for task 4] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:32.444 WARN [HadoopPinotFS] [Executor task launch worker for task 4] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:32.462 INFO [HadoopPinotFS] [Executor task launch worker for task 4] successfully initialized HadoopPinotFS
2020/08/20 13:29:32.463 INFO [PinotFSFactory] [Executor task launch worker for task 4] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:32.860 INFO [Executor] [Executor task launch worker for task 2] Finished task 2.0 in stage 0.0 (TID 2). 708 bytes result sent to driver
2020/08/20 13:29:32.861 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 5.0 in stage 0.0 (TID 5, localhost, executor driver, partition 5, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:32.861 INFO [Executor] [Executor task launch worker for task 5] Running task 5.0 in stage 0.0 (TID 5)
2020/08/20 13:29:32.861 INFO [TaskSetManager] [task-result-getter-3] Finished task 2.0 in stage 0.0 (TID 2) in 3263 ms on localhost (executor driver) (4/31)
2020/08/20 13:29:32.865 INFO [PinotFSFactory] [Executor task launch worker for task 5] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:32.865 WARN [HadoopPinotFS] [Executor task launch worker for task 5] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:32.888 INFO [HadoopPinotFS] [Executor task launch worker for task 5] successfully initialized HadoopPinotFS
2020/08/20 13:29:32.888 INFO [PinotFSFactory] [Executor task launch worker for task 5] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:33.814 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 4] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-4]
2020/08/20 13:29:33.815 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 4] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-4], plugins includes [null]
2020/08/20 13:29:33.815 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 4] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/05/airlineStats_data_2014-01-05.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/input/airlineStats_data_2014-01-05.avro
2020/08/20 13:29:33.816 INFO [S3PinotFS] [Executor task launch worker for task 4] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/05/airlineStats_data_2014-01-05.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/input/airlineStats_data_2014-01-05.avro
2020/08/20 13:29:34.150 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 5] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-5]
2020/08/20 13:29:34.150 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 5] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-5], plugins includes [null]
2020/08/20 13:29:34.151 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 5] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/06/airlineStats_data_2014-01-06.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/input/airlineStats_data_2014-01-06.avro
2020/08/20 13:29:34.151 INFO [S3PinotFS] [Executor task launch worker for task 5] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/06/airlineStats_data_2014-01-06.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/input/airlineStats_data_2014-01-06.avro
2020/08/20 13:29:34.175 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:34.222 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Finished building StatsCollector!
2020/08/20 13:29:34.222 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Collected stats for 422 documents
2020/08/20 13:29:34.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: FlightNum with cardinality: 402, range: 24 to 7389
2020/08/20 13:29:34.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: Origin, size: 321
2020/08/20 13:29:34.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: Origin with cardinality: 107, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:34.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:34.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: LateAircraftDelay with cardinality: 62, range: -2147483648 to 291
2020/08/20 13:29:34.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivActualElapsedTime with cardinality: 58, range: -2147483648 to 1968
2020/08/20 13:29:34.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivWheelsOns with cardinality: 149, range: -2147483648 to 2359
2020/08/20 13:29:34.229 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivWheelsOffs with cardinality: 67, range: -2147483648 to 2349
2020/08/20 13:29:34.230 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: AirTime with cardinality: 140, range: -2147483648 to 362
2020/08/20 13:29:34.231 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:34.250 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivTotalGTimes with cardinality: 57, range: -2147483648 to 139
2020/08/20 13:29:34.251 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:34.251 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:34.252 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DestCityMarketID with cardinality: 86, range: 30136 to 35411
2020/08/20 13:29:34.253 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 58, range: -2147483648 to 1591902
2020/08/20 13:29:34.254 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16075 to 16075
2020/08/20 13:29:34.256 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DepTime with cardinality: 319, range: -2147483648 to 2341
2020/08/20 13:29:34.257 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:34.258 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: CRSElapsedTime with cardinality: 181, range: 36 to 403
2020/08/20 13:29:34.259 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: DestStateName, size: 602
2020/08/20 13:29:34.259 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: DestStateName with cardinality: 43, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:34.260 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:34.310 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:34.311 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DestAirportID with cardinality: 103, range: 10136 to 15919
2020/08/20 13:29:34.312 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: Distance with cardinality: 312, range: 77 to 2845
2020/08/20 13:29:34.313 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:34.313 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:34.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivArrDelay with cardinality: 59, range: -2147483648 to 1651
2020/08/20 13:29:34.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:34.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: LongestAddGTime with cardinality: 4, range: -2147483648 to 42
2020/08/20 13:29:34.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: OriginWac with cardinality: 46, range: 1 to 93
2020/08/20 13:29:34.335 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: WheelsOff with cardinality: 327, range: -2147483648 to 2350
2020/08/20 13:29:34.337 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DestAirportSeqID with cardinality: 103, range: 1013603 to 1591902
2020/08/20 13:29:34.339 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:34.340 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:34.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:34.342 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:34.343 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: ActualElapsedTime with cardinality: 154, range: -2147483648 to 423
2020/08/20 13:29:34.346 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:34.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: OriginStateName, size: 644
2020/08/20 13:29:34.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: OriginStateName with cardinality: 46, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:34.348 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DepartureDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:34.349 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:34.349 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:34.350 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-05 to 2014-01-05
2020/08/20 13:29:34.350 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: OriginCityName, size: 3090
2020/08/20 13:29:34.351 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: OriginCityName with cardinality: 103, max length in bytes: 30, range: Aguadilla, PR to Wilmington, NC
2020/08/20 13:29:34.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: OriginStateFips with cardinality: 46, range: 1 to 72
2020/08/20 13:29:34.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: OriginState, size: 92
2020/08/20 13:29:34.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: OriginState with cardinality: 46, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:34.353 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:34.353 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:34.354 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: WeatherDelay with cardinality: 13, range: -2147483648 to 112
2020/08/20 13:29:34.355 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DestWac with cardinality: 43, range: 1 to 93
2020/08/20 13:29:34.356 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: WheelsOn with cardinality: 257, range: -2147483648 to 2355
2020/08/20 13:29:34.357 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: OriginAirportID with cardinality: 107, range: 10140 to 15919
2020/08/20 13:29:34.358 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: OriginCityMarketID with cardinality: 90, range: 30140 to 35380
2020/08/20 13:29:34.359 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: NASDelay with cardinality: 48, range: -2147483648 to 320
2020/08/20 13:29:34.360 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: ArrTime with cardinality: 262, range: -2147483648 to 2358
2020/08/20 13:29:34.361 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: DestState, size: 86
2020/08/20 13:29:34.361 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: DestState with cardinality: 43, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:34.362 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:34.363 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:34.364 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 5 to 5
2020/08/20 13:29:34.365 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: RandomAirports, size: 308
2020/08/20 13:29:34.365 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: RandomAirports with cardinality: 77, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:34.366 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: TotalAddGTime with cardinality: 4, range: -2147483648 to 42
2020/08/20 13:29:34.368 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: CRSDepTime with cardinality: 243, range: 25 to 2337
2020/08/20 13:29:34.369 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 7 to 7
2020/08/20 13:29:34.369 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:34.370 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:34.372 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: Dest, size: 309
2020/08/20 13:29:34.372 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: Dest with cardinality: 103, max length in bytes: 3, range: ABI to XNA
2020/08/20 13:29:34.378 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Finished building StatsCollector!
2020/08/20 13:29:34.383 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Collected stats for 354 documents
2020/08/20 13:29:34.384 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: FlightNum with cardinality: 339, range: 2 to 6504
2020/08/20 13:29:34.384 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: FirstDepTime with cardinality: 4, range: -2147483648 to 1859
2020/08/20 13:29:34.385 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: Origin, size: 294
2020/08/20 13:29:34.385 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: DivTailNums, size: 396
2020/08/20 13:29:34.385 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: Origin with cardinality: 98, max length in bytes: 3, range: ALB to TYS
2020/08/20 13:29:34.386 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: DivTailNums with cardinality: 66, max length in bytes: 6, range: N163US to null
2020/08/20 13:29:34.386 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:34.387 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DepDelayMinutes with cardinality: 149, range: -2147483648 to 388
2020/08/20 13:29:34.388 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: LateAircraftDelay with cardinality: 58, range: -2147483648 to 249
2020/08/20 13:29:34.388 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DepDelay with cardinality: 160, range: -2147483648 to 388
2020/08/20 13:29:34.389 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivActualElapsedTime with cardinality: 46, range: -2147483648 to 1403
2020/08/20 13:29:34.389 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: TaxiIn with cardinality: 31, range: -2147483648 to 83
2020/08/20 13:29:34.390 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivWheelsOns with cardinality: 68, range: -2147483648 to 2247
2020/08/20 13:29:34.390 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: OriginAirportSeqID with cardinality: 107, range: 1014002 to 1591902
2020/08/20 13:29:34.392 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivWheelsOffs with cardinality: 43, range: -2147483648 to 2339
2020/08/20 13:29:34.392 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DestStateFips with cardinality: 43, range: 1 to 56
2020/08/20 13:29:34.393 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: AirTime with cardinality: 138, range: -2147483648 to 359
2020/08/20 13:29:34.393 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: ArrDelay with cardinality: 124, range: -2147483648 to 340
2020/08/20 13:29:34.394 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:34.395 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:34.396 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivTotalGTimes with cardinality: 34, range: -2147483648 to 97
2020/08/20 13:29:34.396 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivAirportIDs with cardinality: 58, range: -2147483648 to 15919
2020/08/20 13:29:34.397 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:29:34.397 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:29:34.398 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: TaxiOut with cardinality: 53, range: -2147483648 to 113
2020/08/20 13:29:34.400 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: CarrierDelay with cardinality: 49, range: -2147483648 to 310
2020/08/20 13:29:34.400 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DestCityMarketID with cardinality: 84, range: 30140 to 35249
2020/08/20 13:29:34.408 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:34.408 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 40, range: -2147483648 to 1530402
2020/08/20 13:29:34.415 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivLongestGTimes with cardinality: 50, range: -2147483648 to 139
2020/08/20 13:29:34.415 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16076 to 16076
2020/08/20 13:29:34.422 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: DivAirports, size: 232
2020/08/20 13:29:34.423 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DepTime with cardinality: 250, range: -2147483648 to 2321
2020/08/20 13:29:34.423 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: DivAirports with cardinality: 58, max length in bytes: 4, range: AUS to null
2020/08/20 13:29:34.428 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:34.428 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: DivDistance with cardinality: 60, range: -2147483648 to 1592
2020/08/20 13:29:34.436 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: CRSElapsedTime with cardinality: 158, range: 36 to 411
2020/08/20 13:29:34.436 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:34.440 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: DestStateName, size: 574
2020/08/20 13:29:34.441 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: ArrDelayMinutes with cardinality: 103, range: -2147483648 to 340
2020/08/20 13:29:34.441 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: DestStateName with cardinality: 41, max length in bytes: 14, range: Alaska to Wisconsin
2020/08/20 13:29:34.448 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:34.448 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for INT column: CRSArrTime with cardinality: 290, range: 17 to 2359
2020/08/20 13:29:34.449 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:34.452 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: TailNum, size: 2358
2020/08/20 13:29:34.454 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: TailNum with cardinality: 393, max length in bytes: 6, range: N0EGMQ to null
2020/08/20 13:29:34.455 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DestAirportID with cardinality: 100, range: 10140 to 15376
2020/08/20 13:29:34.457 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Using fixed bytes value dictionary for column: DestCityName, size: 2970
2020/08/20 13:29:34.460 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 4] Created dictionary for STRING column: DestCityName with cardinality: 99, max length in bytes: 30, range: Abilene, TX to White Plains, NY
2020/08/20 13:29:34.460 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: Distance with cardinality: 282, range: 67 to 2611
2020/08/20 13:29:34.462 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Start building IndexCreator!
2020/08/20 13:29:34.464 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:34.465 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:34.473 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivArrDelay with cardinality: 42, range: -2147483648 to 1280
2020/08/20 13:29:34.478 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: SecurityDelay with cardinality: 3, range: -2147483648 to 8
2020/08/20 13:29:34.483 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: LongestAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:34.489 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: OriginWac with cardinality: 46, range: 1 to 93
2020/08/20 13:29:34.495 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: WheelsOff with cardinality: 250, range: -2147483648 to 2332
2020/08/20 13:29:34.498 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Finished records indexing in IndexCreator!
2020/08/20 13:29:34.502 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DestAirportSeqID with cardinality: 100, range: 1014002 to 1537602
2020/08/20 13:29:34.507 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:34.509 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:34.516 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:34.522 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:34.529 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: ActualElapsedTime with cardinality: 146, range: -2147483648 to 392
2020/08/20 13:29:34.537 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:34.541 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: OriginStateName, size: 644
2020/08/20 13:29:34.542 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: OriginStateName with cardinality: 46, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:34.552 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DepartureDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:34.557 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:29:34.564 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:34.564 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-06 to 2014-01-06
2020/08/20 13:29:34.565 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: OriginCityName, size: 3196
2020/08/20 13:29:34.566 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: OriginCityName with cardinality: 94, max length in bytes: 34, range: Albany, NY to Williston, ND
2020/08/20 13:29:34.567 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: OriginStateFips with cardinality: 46, range: 1 to 72
2020/08/20 13:29:34.568 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: OriginState, size: 92
2020/08/20 13:29:34.569 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: OriginState with cardinality: 46, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:34.571 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:34.572 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: WeatherDelay with cardinality: 11, range: -2147483648 to 214
2020/08/20 13:29:34.574 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DestWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:34.575 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: WheelsOn with cardinality: 237, range: -2147483648 to 2358
2020/08/20 13:29:34.579 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Finished segment seal!
2020/08/20 13:29:34.580 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 4] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05 to v3 format
2020/08/20 13:29:34.581 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: OriginAirportID with cardinality: 98, range: 10257 to 15412
2020/08/20 13:29:34.582 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: OriginCityMarketID with cardinality: 85, range: 30194 to 35412
2020/08/20 13:29:34.583 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: NASDelay with cardinality: 36, range: -2147483648 to 281
2020/08/20 13:29:34.584 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: ArrTime with cardinality: 236, range: -2147483648 to 2354
2020/08/20 13:29:34.585 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: DestState, size: 82
2020/08/20 13:29:34.586 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: DestState with cardinality: 41, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:34.587 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:29:34.588 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:34.589 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 6 to 6
2020/08/20 13:29:34.590 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: RandomAirports, size: 296
2020/08/20 13:29:34.590 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: RandomAirports with cardinality: 74, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:34.591 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: TotalAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:34.592 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: CRSDepTime with cardinality: 219, range: 55 to 2243
2020/08/20 13:29:34.593 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 1 to 1
2020/08/20 13:29:34.594 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:34.594 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:34.595 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: Dest, size: 300
2020/08/20 13:29:34.595 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: Dest with cardinality: 100, max length in bytes: 3, range: ABQ to TUS
2020/08/20 13:29:34.596 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: FirstDepTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:34.597 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: DivTailNums, size: 282
2020/08/20 13:29:34.597 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: DivTailNums with cardinality: 47, max length in bytes: 6, range: N13929 to null
2020/08/20 13:29:34.598 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DepDelayMinutes with cardinality: 108, range: -2147483648 to 369
2020/08/20 13:29:34.599 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DepDelay with cardinality: 119, range: -2147483648 to 369
2020/08/20 13:29:34.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: TaxiIn with cardinality: 35, range: -2147483648 to 71
2020/08/20 13:29:34.601 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: OriginAirportSeqID with cardinality: 98, range: 1025702 to 1541202
2020/08/20 13:29:34.603 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DestStateFips with cardinality: 41, range: 2 to 72
2020/08/20 13:29:34.604 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: ArrDelay with cardinality: 114, range: -2147483648 to 321
2020/08/20 13:29:34.606 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:34.607 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivAirportIDs with cardinality: 40, range: -2147483648 to 15304
2020/08/20 13:29:34.608 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: TaxiOut with cardinality: 40, range: -2147483648 to 70
2020/08/20 13:29:34.609 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: CarrierDelay with cardinality: 48, range: -2147483648 to 288
2020/08/20 13:29:34.610 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:34.611 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivLongestGTimes with cardinality: 32, range: -2147483648 to 97
2020/08/20 13:29:34.612 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: DivAirports, size: 160
2020/08/20 13:29:34.612 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: DivAirports with cardinality: 40, max length in bytes: 4, range: ACY to null
2020/08/20 13:29:34.613 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: DivDistance with cardinality: 19, range: -2147483648 to 1986
2020/08/20 13:29:34.614 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:34.615 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: ArrDelayMinutes with cardinality: 90, range: -2147483648 to 321
2020/08/20 13:29:34.616 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for INT column: CRSArrTime with cardinality: 259, range: 537 to 2358
2020/08/20 13:29:34.617 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: TailNum, size: 1998
2020/08/20 13:29:34.617 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: TailNum with cardinality: 333, max length in bytes: 6, range: N003AA to null
2020/08/20 13:29:34.618 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Using fixed bytes value dictionary for column: DestCityName, size: 2880
2020/08/20 13:29:34.618 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 5] Created dictionary for STRING column: DestCityName with cardinality: 96, max length in bytes: 30, range: Albuquerque, NM to Wichita, KS
2020/08/20 13:29:34.619 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Start building IndexCreator!
2020/08/20 13:29:34.647 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Finished records indexing in IndexCreator!
2020/08/20 13:29:34.673 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Finished segment seal!
2020/08/20 13:29:34.674 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 5] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06 to v3 format
2020/08/20 13:29:34.713 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 4] v3 segment location for segment: airlineStats_batch_2014-01-05_2014-01-05 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05/v3
2020/08/20 13:29:34.714 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 4] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05
2020/08/20 13:29:34.757 INFO [CrcUtils] [Executor task launch worker for task 4] Computed crc = 3311976800, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05/v3/metadata.properties]
2020/08/20 13:29:34.757 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Driver, record read time : 21
2020/08/20 13:29:34.758 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Driver, stats collector time : 0
2020/08/20 13:29:34.758 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 4] Driver, indexing time : 14
2020/08/20 13:29:34.758 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 4] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05.tar.gz
2020/08/20 13:29:34.770 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 4] Size for segment: airlineStats_batch_2014-01-05_2014-01-05, uncompressed: 130.61K, compressed: 42.98K
2020/08/20 13:29:34.771 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 4] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_batch_2014-01-05_2014-01-05.tar.gz]
2020/08/20 13:29:34.772 INFO [S3PinotFS] [Executor task launch worker for task 4] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-31273c0a-fbd2-4ad1-9091-c6ee77c81630/output/airlineStats_batch_2014-01-05_2014-01-05.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_batch_2014-01-05_2014-01-05.tar.gz
2020/08/20 13:29:34.811 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 5] v3 segment location for segment: airlineStats_batch_2014-01-06_2014-01-06 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06/v3
2020/08/20 13:29:34.812 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 5] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06
2020/08/20 13:29:34.852 INFO [CrcUtils] [Executor task launch worker for task 5] Computed crc = 3545912022, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06/v3/metadata.properties]
2020/08/20 13:29:34.852 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Driver, record read time : 19
2020/08/20 13:29:34.852 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Driver, stats collector time : 0
2020/08/20 13:29:34.852 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 5] Driver, indexing time : 9
2020/08/20 13:29:34.852 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 5] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06.tar.gz
2020/08/20 13:29:34.865 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 5] Size for segment: airlineStats_batch_2014-01-06_2014-01-06, uncompressed: 122.23K, compressed: 37.12K
2020/08/20 13:29:34.865 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 5] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_batch_2014-01-06_2014-01-06.tar.gz]
2020/08/20 13:29:34.865 INFO [S3PinotFS] [Executor task launch worker for task 5] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-7f1a7ca0-ba52-4bea-94b1-becad772c782/output/airlineStats_batch_2014-01-06_2014-01-06.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_batch_2014-01-06_2014-01-06.tar.gz
2020/08/20 13:29:35.072 INFO [Executor] [Executor task launch worker for task 5] Finished task 5.0 in stage 0.0 (TID 5). 751 bytes result sent to driver
2020/08/20 13:29:35.073 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 6.0 in stage 0.0 (TID 6, localhost, executor driver, partition 6, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:35.073 INFO [Executor] [Executor task launch worker for task 6] Running task 6.0 in stage 0.0 (TID 6)
2020/08/20 13:29:35.073 INFO [TaskSetManager] [task-result-getter-0] Finished task 5.0 in stage 0.0 (TID 5) in 2213 ms on localhost (executor driver) (5/31)
2020/08/20 13:29:35.075 INFO [PinotFSFactory] [Executor task launch worker for task 6] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:35.076 WARN [HadoopPinotFS] [Executor task launch worker for task 6] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:35.090 INFO [HadoopPinotFS] [Executor task launch worker for task 6] successfully initialized HadoopPinotFS
2020/08/20 13:29:35.091 INFO [PinotFSFactory] [Executor task launch worker for task 6] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:35.509 INFO [Executor] [Executor task launch worker for task 4] Finished task 4.0 in stage 0.0 (TID 4). 751 bytes result sent to driver
2020/08/20 13:29:35.509 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 7.0 in stage 0.0 (TID 7, localhost, executor driver, partition 7, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:35.510 INFO [Executor] [Executor task launch worker for task 7] Running task 7.0 in stage 0.0 (TID 7)
2020/08/20 13:29:35.510 INFO [TaskSetManager] [task-result-getter-1] Finished task 4.0 in stage 0.0 (TID 4) in 3070 ms on localhost (executor driver) (6/31)
2020/08/20 13:29:35.513 INFO [PinotFSFactory] [Executor task launch worker for task 7] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:35.513 WARN [HadoopPinotFS] [Executor task launch worker for task 7] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:35.531 INFO [HadoopPinotFS] [Executor task launch worker for task 7] successfully initialized HadoopPinotFS
2020/08/20 13:29:35.531 INFO [PinotFSFactory] [Executor task launch worker for task 7] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:36.397 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 6] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-6]
2020/08/20 13:29:36.397 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 6] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-6], plugins includes [null]
2020/08/20 13:29:36.398 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 6] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/07/airlineStats_data_2014-01-07.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/input/airlineStats_data_2014-01-07.avro
2020/08/20 13:29:36.398 INFO [S3PinotFS] [Executor task launch worker for task 6] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/07/airlineStats_data_2014-01-07.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/input/airlineStats_data_2014-01-07.avro
2020/08/20 13:29:36.711 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:36.728 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Finished building StatsCollector!
2020/08/20 13:29:36.728 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Collected stats for 292 documents
2020/08/20 13:29:36.729 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: FlightNum with cardinality: 282, range: 29 to 6533
2020/08/20 13:29:36.730 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: Origin, size: 291
2020/08/20 13:29:36.730 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: Origin with cardinality: 97, max length in bytes: 3, range: ABQ to YAK
2020/08/20 13:29:36.731 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:36.732 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: LateAircraftDelay with cardinality: 43, range: -2147483648 to 157
2020/08/20 13:29:36.732 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivActualElapsedTime with cardinality: 16, range: -2147483648 to 704
2020/08/20 13:29:36.733 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivWheelsOns with cardinality: 35, range: -2147483648 to 2151
2020/08/20 13:29:36.734 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivWheelsOffs with cardinality: 17, range: -2147483648 to 2225
2020/08/20 13:29:36.735 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: AirTime with cardinality: 130, range: -2147483648 to 369
2020/08/20 13:29:36.737 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:36.738 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivTotalGTimes with cardinality: 23, range: -2147483648 to 159
2020/08/20 13:29:36.738 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:36.739 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:36.740 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DestCityMarketID with cardinality: 78, range: 30140 to 35401
2020/08/20 13:29:36.740 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 27, range: -2147483648 to 1501603
2020/08/20 13:29:36.741 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16077 to 16077
2020/08/20 13:29:36.742 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DepTime with cardinality: 229, range: -2147483648 to 2330
2020/08/20 13:29:36.743 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:36.744 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: CRSElapsedTime with cardinality: 127, range: 36 to 406
2020/08/20 13:29:36.744 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: DestStateName, size: 546
2020/08/20 13:29:36.744 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: DestStateName with cardinality: 39, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:36.745 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:36.745 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:36.747 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DestAirportID with cardinality: 93, range: 10140 to 16218
2020/08/20 13:29:36.748 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: Distance with cardinality: 237, range: 67 to 2704
2020/08/20 13:29:36.748 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 162
2020/08/20 13:29:36.748 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: ArrTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:36.750 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivArrDelay with cardinality: 14, range: -2147483648 to 552
2020/08/20 13:29:36.751 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: SecurityDelay with cardinality: 3, range: -2147483648 to 14
2020/08/20 13:29:36.751 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 11
2020/08/20 13:29:36.752 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: OriginWac with cardinality: 36, range: 1 to 93
2020/08/20 13:29:36.753 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: WheelsOff with cardinality: 238, range: -2147483648 to 2338
2020/08/20 13:29:36.754 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DestAirportSeqID with cardinality: 93, range: 1014002 to 1621801
2020/08/20 13:29:36.755 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:36.756 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:36.757 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:36.758 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:36.759 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: ActualElapsedTime with cardinality: 137, range: -2147483648 to 397
2020/08/20 13:29:36.760 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:36.761 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: OriginStateName, size: 504
2020/08/20 13:29:36.761 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: OriginStateName with cardinality: 36, max length in bytes: 14, range: Alaska to Wyoming
2020/08/20 13:29:36.762 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DepartureDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:36.763 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:29:36.764 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:36.764 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-07 to 2014-01-07
2020/08/20 13:29:36.764 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: OriginCityName, size: 2790
2020/08/20 13:29:36.765 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: OriginCityName with cardinality: 93, max length in bytes: 30, range: Albany, NY to Yakutat, AK
2020/08/20 13:29:36.766 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: OriginStateFips with cardinality: 36, range: 2 to 72
2020/08/20 13:29:36.766 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: OriginState, size: 72
2020/08/20 13:29:36.767 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: OriginState with cardinality: 36, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:36.767 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:36.768 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: WeatherDelay with cardinality: 17, range: -2147483648 to 115
2020/08/20 13:29:36.769 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DestWac with cardinality: 39, range: 1 to 93
2020/08/20 13:29:36.771 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: WheelsOn with cardinality: 214, range: -2147483648 to 2349
2020/08/20 13:29:36.772 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: OriginAirportID with cardinality: 97, range: 10140 to 15991
2020/08/20 13:29:36.773 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: OriginCityMarketID with cardinality: 81, range: 30140 to 35991
2020/08/20 13:29:36.774 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: NASDelay with cardinality: 23, range: -2147483648 to 62
2020/08/20 13:29:36.775 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: ArrTime with cardinality: 214, range: -2147483648 to 2350
2020/08/20 13:29:36.776 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: DestState, size: 78
2020/08/20 13:29:36.776 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: DestState with cardinality: 39, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:36.777 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 13, range: -2147483648 to 11
2020/08/20 13:29:36.778 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:36.779 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 7 to 7
2020/08/20 13:29:36.779 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: RandomAirports, size: 296
2020/08/20 13:29:36.780 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: RandomAirports with cardinality: 74, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:36.781 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 11
2020/08/20 13:29:36.781 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: CRSDepTime with cardinality: 212, range: 530 to 2359
2020/08/20 13:29:36.782 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 2 to 2
2020/08/20 13:29:36.783 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:36.783 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:36.784 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: Dest, size: 279
2020/08/20 13:29:36.784 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: Dest with cardinality: 93, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:29:36.785 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 1016
2020/08/20 13:29:36.786 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: DivTailNums, size: 102
2020/08/20 13:29:36.786 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: DivTailNums with cardinality: 17, max length in bytes: 6, range: N16981 to null
2020/08/20 13:29:36.787 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DepDelayMinutes with cardinality: 82, range: -2147483648 to 183
2020/08/20 13:29:36.788 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DepDelay with cardinality: 95, range: -2147483648 to 183
2020/08/20 13:29:36.789 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: TaxiIn with cardinality: 33, range: -2147483648 to 50
2020/08/20 13:29:36.790 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: OriginAirportSeqID with cardinality: 97, range: 1014002 to 1599102
2020/08/20 13:29:36.791 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DestStateFips with cardinality: 39, range: 1 to 72
2020/08/20 13:29:36.792 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: ArrDelay with cardinality: 95, range: -2147483648 to 165
2020/08/20 13:29:36.793 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:36.794 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivAirportIDs with cardinality: 27, range: -2147483648 to 15016
2020/08/20 13:29:36.795 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: TaxiOut with cardinality: 33, range: -2147483648 to 50
2020/08/20 13:29:36.796 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: CarrierDelay with cardinality: 36, range: -2147483648 to 117
2020/08/20 13:29:36.797 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:36.798 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivLongestGTimes with cardinality: 21, range: -2147483648 to 152
2020/08/20 13:29:36.800 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: DivAirports, size: 108
2020/08/20 13:29:36.800 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: DivAirports with cardinality: 27, max length in bytes: 4, range: ATL to null
2020/08/20 13:29:36.801 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: DivDistance with cardinality: 16, range: -2147483648 to 1590
2020/08/20 13:29:36.802 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:36.805 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: ArrDelayMinutes with cardinality: 69, range: -2147483648 to 165
2020/08/20 13:29:36.806 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for INT column: CRSArrTime with cardinality: 227, range: 23 to 2359
2020/08/20 13:29:36.808 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: TailNum, size: 1644
2020/08/20 13:29:36.808 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: TailNum with cardinality: 274, max length in bytes: 6, range: N109UW to null
2020/08/20 13:29:36.809 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Using fixed bytes value dictionary for column: DestCityName, size: 2670
2020/08/20 13:29:36.809 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 6] Created dictionary for STRING column: DestCityName with cardinality: 89, max length in bytes: 30, range: Albuquerque, NM to Yuma, AZ
2020/08/20 13:29:36.810 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Start building IndexCreator!
2020/08/20 13:29:36.825 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 7] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-7]
2020/08/20 13:29:36.825 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 7] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-7], plugins includes [null]
2020/08/20 13:29:36.826 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 7] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/08/airlineStats_data_2014-01-08.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/input/airlineStats_data_2014-01-08.avro
2020/08/20 13:29:36.827 INFO [S3PinotFS] [Executor task launch worker for task 7] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/08/airlineStats_data_2014-01-08.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/input/airlineStats_data_2014-01-08.avro
2020/08/20 13:29:36.830 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Finished records indexing in IndexCreator!
2020/08/20 13:29:36.855 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Finished segment seal!
2020/08/20 13:29:36.855 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 6] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07 to v3 format
2020/08/20 13:29:36.992 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:36.994 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 6] v3 segment location for segment: airlineStats_batch_2014-01-07_2014-01-07 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07/v3
2020/08/20 13:29:36.994 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 6] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07
2020/08/20 13:29:37.016 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Finished building StatsCollector!
2020/08/20 13:29:37.016 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Collected stats for 316 documents
2020/08/20 13:29:37.021 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: FlightNum with cardinality: 309, range: 2 to 6534
2020/08/20 13:29:37.022 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: Origin, size: 294
2020/08/20 13:29:37.022 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: Origin with cardinality: 98, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:29:37.023 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:37.024 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: LateAircraftDelay with cardinality: 41, range: -2147483648 to 167
2020/08/20 13:29:37.026 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivActualElapsedTime with cardinality: 31, range: -2147483648 to 744
2020/08/20 13:29:37.027 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivWheelsOns with cardinality: 47, range: -2147483648 to 2322
2020/08/20 13:29:37.028 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivWheelsOffs with cardinality: 32, range: -2147483648 to 2325
2020/08/20 13:29:37.030 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: AirTime with cardinality: 139, range: -2147483648 to 581
2020/08/20 13:29:37.031 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:37.033 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivTotalGTimes with cardinality: 32, range: -2147483648 to 113
2020/08/20 13:29:37.034 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:37.053 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:37.055 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DestCityMarketID with cardinality: 88, range: 30136 to 35412
2020/08/20 13:29:37.056 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 34, range: -2147483648 to 1599102
2020/08/20 13:29:37.057 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16078 to 16078
2020/08/20 13:29:37.058 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DepTime with cardinality: 263, range: -2147483648 to 2327
2020/08/20 13:29:37.060 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:37.061 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: CRSElapsedTime with cardinality: 156, range: 32 to 599
2020/08/20 13:29:37.062 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: DestStateName, size: 798
2020/08/20 13:29:37.062 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:29:37.063 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:37.063 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:37.064 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DestAirportID with cardinality: 100, range: 10136 to 15412
2020/08/20 13:29:37.066 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: Distance with cardinality: 251, range: 68 to 4502
2020/08/20 13:29:37.067 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:37.067 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:37.068 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivArrDelay with cardinality: 30, range: -2147483648 to 376
2020/08/20 13:29:37.074 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:37.075 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: LongestAddGTime with cardinality: 4, range: -2147483648 to 29
2020/08/20 13:29:37.076 INFO [CrcUtils] [Executor task launch worker for task 6] Computed crc = 2168252107, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07/v3/metadata.properties]
2020/08/20 13:29:37.076 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: OriginWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:37.076 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Driver, record read time : 9
2020/08/20 13:29:37.082 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Driver, stats collector time : 0
2020/08/20 13:29:37.082 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 6] Driver, indexing time : 11
2020/08/20 13:29:37.082 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 6] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07.tar.gz
2020/08/20 13:29:37.182 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: WheelsOff with cardinality: 252, range: -2147483648 to 2344
2020/08/20 13:29:37.183 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DestAirportSeqID with cardinality: 100, range: 1013603 to 1541202
2020/08/20 13:29:37.183 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:37.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:37.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:37.185 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 6] Size for segment: airlineStats_batch_2014-01-07_2014-01-07, uncompressed: 113.53K, compressed: 32.57K
2020/08/20 13:29:37.185 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:37.185 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 6] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_batch_2014-01-07_2014-01-07.tar.gz]
2020/08/20 13:29:37.185 INFO [S3PinotFS] [Executor task launch worker for task 6] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-950d9cf9-2249-4e8c-b38a-3135f7f64bbc/output/airlineStats_batch_2014-01-07_2014-01-07.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_batch_2014-01-07_2014-01-07.tar.gz
2020/08/20 13:29:37.186 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: ActualElapsedTime with cardinality: 160, range: -2147483648 to 603
2020/08/20 13:29:37.187 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:37.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: OriginStateName, size: 574
2020/08/20 13:29:37.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: OriginStateName with cardinality: 41, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:37.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DepartureDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:37.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:29:37.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:37.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-08 to 2014-01-08
2020/08/20 13:29:37.191 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: OriginCityName, size: 2820
2020/08/20 13:29:37.191 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: OriginCityName with cardinality: 94, max length in bytes: 30, range: Akron, OH to Yuma, AZ
2020/08/20 13:29:37.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: OriginStateFips with cardinality: 41, range: 1 to 72
2020/08/20 13:29:37.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: OriginState, size: 82
2020/08/20 13:29:37.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: OriginState with cardinality: 41, max length in bytes: 2, range: AK to WV
2020/08/20 13:29:37.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:37.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: WeatherDelay with cardinality: 10, range: -2147483648 to 92
2020/08/20 13:29:37.195 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:37.196 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: WheelsOn with cardinality: 253, range: -2147483648 to 2348
2020/08/20 13:29:37.196 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: OriginAirportID with cardinality: 98, range: 10140 to 16218
2020/08/20 13:29:37.197 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: OriginCityMarketID with cardinality: 85, range: 30140 to 35380
2020/08/20 13:29:37.198 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: NASDelay with cardinality: 24, range: -2147483648 to 66
2020/08/20 13:29:37.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: ArrTime with cardinality: 252, range: -2147483648 to 2352
2020/08/20 13:29:37.200 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:29:37.200 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:37.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:37.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:37.203 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 8 to 8
2020/08/20 13:29:37.204 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: RandomAirports, size: 304
2020/08/20 13:29:37.204 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: RandomAirports with cardinality: 76, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:37.205 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: TotalAddGTime with cardinality: 4, range: -2147483648 to 29
2020/08/20 13:29:37.211 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: CRSDepTime with cardinality: 208, range: 30 to 2352
2020/08/20 13:29:37.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 3 to 3
2020/08/20 13:29:37.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:37.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:37.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: Dest, size: 300
2020/08/20 13:29:37.214 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: Dest with cardinality: 100, max length in bytes: 3, range: ABI to TYS
2020/08/20 13:29:37.214 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: FirstDepTime with cardinality: 4, range: -2147483648 to 1534
2020/08/20 13:29:37.215 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: DivTailNums, size: 186
2020/08/20 13:29:37.215 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: DivTailNums with cardinality: 31, max length in bytes: 6, range: N14993 to null
2020/08/20 13:29:37.216 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DepDelayMinutes with cardinality: 79, range: -2147483648 to 252
2020/08/20 13:29:37.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DepDelay with cardinality: 92, range: -2147483648 to 252
2020/08/20 13:29:37.218 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: TaxiIn with cardinality: 26, range: -2147483648 to 63
2020/08/20 13:29:37.219 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: OriginAirportSeqID with cardinality: 98, range: 1014002 to 1621801
2020/08/20 13:29:37.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 78
2020/08/20 13:29:37.221 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: ArrDelay with cardinality: 98, range: -2147483648 to 255
2020/08/20 13:29:37.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:37.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivAirportIDs with cardinality: 34, range: -2147483648 to 15991
2020/08/20 13:29:37.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: TaxiOut with cardinality: 40, range: -2147483648 to 47
2020/08/20 13:29:37.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: CarrierDelay with cardinality: 39, range: -2147483648 to 184
2020/08/20 13:29:37.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:37.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivLongestGTimes with cardinality: 27, range: -2147483648 to 107
2020/08/20 13:29:37.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: DivAirports, size: 136
2020/08/20 13:29:37.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: DivAirports with cardinality: 34, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:37.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: DivDistance with cardinality: 9, range: -2147483648 to 1011
2020/08/20 13:29:37.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:37.229 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: ArrDelayMinutes with cardinality: 70, range: -2147483648 to 255
2020/08/20 13:29:37.230 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for INT column: CRSArrTime with cardinality: 250, range: 28 to 2359
2020/08/20 13:29:37.230 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: TailNum, size: 1818
2020/08/20 13:29:37.231 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: TailNum with cardinality: 303, max length in bytes: 6, range: N004AA to null
2020/08/20 13:29:37.231 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Using fixed bytes value dictionary for column: DestCityName, size: 2880
2020/08/20 13:29:37.232 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 7] Created dictionary for STRING column: DestCityName with cardinality: 96, max length in bytes: 30, range: Abilene, TX to Wichita, KS
2020/08/20 13:29:37.233 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Start building IndexCreator!
2020/08/20 13:29:37.256 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Finished records indexing in IndexCreator!
2020/08/20 13:29:37.278 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Finished segment seal!
2020/08/20 13:29:37.279 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 7] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08 to v3 format
2020/08/20 13:29:37.396 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 7] v3 segment location for segment: airlineStats_batch_2014-01-08_2014-01-08 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08/v3
2020/08/20 13:29:37.397 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 7] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08
2020/08/20 13:29:37.429 INFO [CrcUtils] [Executor task launch worker for task 7] Computed crc = 727514219, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08/v3/metadata.properties]
2020/08/20 13:29:37.429 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Driver, record read time : 16
2020/08/20 13:29:37.430 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Driver, stats collector time : 0
2020/08/20 13:29:37.430 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 7] Driver, indexing time : 7
2020/08/20 13:29:37.430 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 7] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08.tar.gz
2020/08/20 13:29:37.443 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 7] Size for segment: airlineStats_batch_2014-01-08_2014-01-08, uncompressed: 117.72K, compressed: 35.03K
2020/08/20 13:29:37.443 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 7] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_batch_2014-01-08_2014-01-08.tar.gz]
2020/08/20 13:29:37.443 INFO [S3PinotFS] [Executor task launch worker for task 7] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1a5575e0-eaff-4d8c-a602-e0db7a3e03b9/output/airlineStats_batch_2014-01-08_2014-01-08.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_batch_2014-01-08_2014-01-08.tar.gz
2020/08/20 13:29:37.636 INFO [Executor] [Executor task launch worker for task 7] Finished task 7.0 in stage 0.0 (TID 7). 708 bytes result sent to driver
2020/08/20 13:29:37.637 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 8.0 in stage 0.0 (TID 8, localhost, executor driver, partition 8, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:37.637 INFO [Executor] [Executor task launch worker for task 8] Running task 8.0 in stage 0.0 (TID 8)
2020/08/20 13:29:37.638 INFO [TaskSetManager] [task-result-getter-2] Finished task 7.0 in stage 0.0 (TID 7) in 2128 ms on localhost (executor driver) (7/31)
2020/08/20 13:29:37.640 INFO [PinotFSFactory] [Executor task launch worker for task 8] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:37.640 WARN [HadoopPinotFS] [Executor task launch worker for task 8] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:37.656 INFO [HadoopPinotFS] [Executor task launch worker for task 8] successfully initialized HadoopPinotFS
2020/08/20 13:29:37.656 INFO [PinotFSFactory] [Executor task launch worker for task 8] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:37.742 INFO [Executor] [Executor task launch worker for task 6] Finished task 6.0 in stage 0.0 (TID 6). 708 bytes result sent to driver
2020/08/20 13:29:37.743 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 9.0 in stage 0.0 (TID 9, localhost, executor driver, partition 9, PROCESS_LOCAL, 7968 bytes)
2020/08/20 13:29:37.743 INFO [Executor] [Executor task launch worker for task 9] Running task 9.0 in stage 0.0 (TID 9)
2020/08/20 13:29:37.743 INFO [TaskSetManager] [task-result-getter-3] Finished task 6.0 in stage 0.0 (TID 6) in 2671 ms on localhost (executor driver) (8/31)
2020/08/20 13:29:37.745 INFO [PinotFSFactory] [Executor task launch worker for task 9] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:37.745 WARN [HadoopPinotFS] [Executor task launch worker for task 9] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:37.761 INFO [HadoopPinotFS] [Executor task launch worker for task 9] successfully initialized HadoopPinotFS
2020/08/20 13:29:37.762 INFO [PinotFSFactory] [Executor task launch worker for task 9] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:38.967 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 8] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-8]
2020/08/20 13:29:38.967 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 8] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-8], plugins includes [null]
2020/08/20 13:29:38.969 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 8] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/09/airlineStats_data_2014-01-09.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/input/airlineStats_data_2014-01-09.avro
2020/08/20 13:29:38.969 INFO [S3PinotFS] [Executor task launch worker for task 8] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/09/airlineStats_data_2014-01-09.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/input/airlineStats_data_2014-01-09.avro
2020/08/20 13:29:39.038 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 9] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-9]
2020/08/20 13:29:39.038 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 9] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-9], plugins includes [null]
2020/08/20 13:29:39.039 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 9] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/10/airlineStats_data_2014-01-10.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/input/airlineStats_data_2014-01-10.avro
2020/08/20 13:29:39.039 INFO [S3PinotFS] [Executor task launch worker for task 9] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/10/airlineStats_data_2014-01-10.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/input/airlineStats_data_2014-01-10.avro
2020/08/20 13:29:39.365 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:39.386 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Finished building StatsCollector!
2020/08/20 13:29:39.386 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Collected stats for 338 documents
2020/08/20 13:29:39.387 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: FlightNum with cardinality: 328, range: 15 to 7426
2020/08/20 13:29:39.388 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: Origin, size: 276
2020/08/20 13:29:39.388 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: Origin with cardinality: 92, max length in bytes: 3, range: AMA to TUS
2020/08/20 13:29:39.389 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:39.390 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: LateAircraftDelay with cardinality: 47, range: -2147483648 to 138
2020/08/20 13:29:39.391 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivActualElapsedTime with cardinality: 32, range: -2147483648 to 1047
2020/08/20 13:29:39.392 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivWheelsOns with cardinality: 81, range: -2147483648 to 2350
2020/08/20 13:29:39.393 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivWheelsOffs with cardinality: 37, range: -2147483648 to 2316
2020/08/20 13:29:39.394 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: AirTime with cardinality: 139, range: -2147483648 to 572
2020/08/20 13:29:39.395 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:39.396 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivTotalGTimes with cardinality: 39, range: -2147483648 to 102
2020/08/20 13:29:39.396 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:39.397 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:39.397 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DestCityMarketID with cardinality: 101, range: 30136 to 35380
2020/08/20 13:29:39.398 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 46, range: -2147483648 to 1541202
2020/08/20 13:29:39.399 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16080 to 16080
2020/08/20 13:29:39.400 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DepTime with cardinality: 286, range: -2147483648 to 2339
2020/08/20 13:29:39.401 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:39.402 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: CRSElapsedTime with cardinality: 145, range: 37 to 599
2020/08/20 13:29:39.404 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: DestStateName, size: 616
2020/08/20 13:29:39.405 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: DestStateName with cardinality: 44, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:39.406 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:39.406 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:39.407 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DestAirportID with cardinality: 117, range: 10136 to 15919
2020/08/20 13:29:39.408 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: Distance with cardinality: 270, range: 67 to 4983
2020/08/20 13:29:39.409 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:39.409 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:39.410 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivArrDelay with cardinality: 29, range: -2147483648 to 1025
2020/08/20 13:29:39.411 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:39.412 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 39
2020/08/20 13:29:39.413 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: OriginWac with cardinality: 39, range: 2 to 93
2020/08/20 13:29:39.414 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: WheelsOff with cardinality: 281, range: -2147483648 to 2355
2020/08/20 13:29:39.415 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DestAirportSeqID with cardinality: 117, range: 1013603 to 1591902
2020/08/20 13:29:39.416 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:39.417 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:39.418 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:39.419 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:39.419 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:39.420 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: ActualElapsedTime with cardinality: 139, range: -2147483648 to 605
2020/08/20 13:29:39.421 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:39.421 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: OriginStateName, size: 546
2020/08/20 13:29:39.422 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: OriginStateName with cardinality: 39, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:39.423 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:39.423 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:39.424 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:39.424 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-10 to 2014-01-10
2020/08/20 13:29:39.425 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: OriginCityName, size: 2640
2020/08/20 13:29:39.425 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: OriginCityName with cardinality: 88, max length in bytes: 30, range: Amarillo, TX to Wilmington, NC
2020/08/20 13:29:39.426 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: OriginStateFips with cardinality: 39, range: 1 to 55
2020/08/20 13:29:39.427 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: OriginState, size: 78
2020/08/20 13:29:39.427 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: OriginState with cardinality: 39, max length in bytes: 2, range: AL to WI
2020/08/20 13:29:39.428 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:39.428 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: WeatherDelay with cardinality: 10, range: -2147483648 to 198
2020/08/20 13:29:39.429 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DestWac with cardinality: 44, range: 1 to 93
2020/08/20 13:29:39.430 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: WheelsOn with cardinality: 247, range: -2147483648 to 2357
2020/08/20 13:29:39.431 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: OriginAirportID with cardinality: 92, range: 10279 to 15376
2020/08/20 13:29:39.432 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: OriginCityMarketID with cardinality: 76, range: 30194 to 35249
2020/08/20 13:29:39.433 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: NASDelay with cardinality: 39, range: -2147483648 to 179
2020/08/20 13:29:39.433 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: ArrTime with cardinality: 248, range: -2147483648 to 2400
2020/08/20 13:29:39.434 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: DestState, size: 88
2020/08/20 13:29:39.434 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: DestState with cardinality: 44, max length in bytes: 2, range: AK to WV
2020/08/20 13:29:39.435 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:39.436 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:39.438 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 10 to 10
2020/08/20 13:29:39.438 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: RandomAirports, size: 300
2020/08/20 13:29:39.439 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: RandomAirports with cardinality: 75, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:39.440 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 39
2020/08/20 13:29:39.440 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: CRSDepTime with cardinality: 217, range: 515 to 2300
2020/08/20 13:29:39.441 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 5 to 5
2020/08/20 13:29:39.442 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Finished building StatsCollector!
2020/08/20 13:29:39.443 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Collected stats for 340 documents
2020/08/20 13:29:39.443 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:39.443 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:39.443 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: FlightNum with cardinality: 332, range: 1 to 7430
2020/08/20 13:29:39.444 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: Dest, size: 351
2020/08/20 13:29:39.444 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: Origin, size: 318
2020/08/20 13:29:39.444 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: Dest with cardinality: 117, max length in bytes: 3, range: ABI to XNA
2020/08/20 13:29:39.444 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: Origin with cardinality: 106, max length in bytes: 3, range: ABE to TUS
2020/08/20 13:29:39.445 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:39.445 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 2145
2020/08/20 13:29:39.446 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: DivTailNums, size: 222
2020/08/20 13:29:39.446 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: LateAircraftDelay with cardinality: 42, range: -2147483648 to 209
2020/08/20 13:29:39.446 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: DivTailNums with cardinality: 37, max length in bytes: 6, range: N130DL to null
2020/08/20 13:29:39.447 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivActualElapsedTime with cardinality: 27, range: -2147483648 to 509
2020/08/20 13:29:39.447 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DepDelayMinutes with cardinality: 92, range: -2147483648 to 470
2020/08/20 13:29:39.448 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivWheelsOns with cardinality: 53, range: -2147483648 to 2339
2020/08/20 13:29:39.448 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DepDelay with cardinality: 103, range: -2147483648 to 470
2020/08/20 13:29:39.449 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: TaxiIn with cardinality: 24, range: -2147483648 to 34
2020/08/20 13:29:39.449 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivWheelsOffs with cardinality: 28, range: -2147483648 to 2354
2020/08/20 13:29:39.450 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: AirTime with cardinality: 144, range: -2147483648 to 480
2020/08/20 13:29:39.450 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: OriginAirportSeqID with cardinality: 92, range: 1027903 to 1537602
2020/08/20 13:29:39.451 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:39.451 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DestStateFips with cardinality: 44, range: 1 to 72
2020/08/20 13:29:39.452 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivTotalGTimes with cardinality: 33, range: -2147483648 to 128
2020/08/20 13:29:39.452 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: ArrDelay with cardinality: 96, range: -2147483648 to 450
2020/08/20 13:29:39.453 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:39.453 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:29:39.453 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:29:39.454 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivAirportIDs with cardinality: 46, range: -2147483648 to 15412
2020/08/20 13:29:39.454 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DestCityMarketID with cardinality: 88, range: 30113 to 35041
2020/08/20 13:29:39.455 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: TaxiOut with cardinality: 52, range: -2147483648 to 88
2020/08/20 13:29:39.455 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 36, range: -2147483648 to 1591902
2020/08/20 13:29:39.456 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: CarrierDelay with cardinality: 28, range: -2147483648 to 450
2020/08/20 13:29:39.456 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16079 to 16079
2020/08/20 13:29:39.457 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:39.457 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DepTime with cardinality: 274, range: -2147483648 to 2255
2020/08/20 13:29:39.458 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:39.458 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivLongestGTimes with cardinality: 34, range: -2147483648 to 102
2020/08/20 13:29:39.459 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: DivAirports, size: 184
2020/08/20 13:29:39.459 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: CRSElapsedTime with cardinality: 144, range: 41 to 505
2020/08/20 13:29:39.459 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: DivAirports with cardinality: 46, max length in bytes: 4, range: ALB to null
2020/08/20 13:29:39.460 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: DestStateName, size: 836
2020/08/20 13:29:39.460 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: DivDistance with cardinality: 28, range: -2147483648 to 1138
2020/08/20 13:29:39.460 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: DestStateName with cardinality: 44, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:29:39.460 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:39.461 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:39.461 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:39.462 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: ArrDelayMinutes with cardinality: 74, range: -2147483648 to 450
2020/08/20 13:29:39.462 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DestAirportID with cardinality: 103, range: 10140 to 15370
2020/08/20 13:29:39.462 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for INT column: CRSArrTime with cardinality: 267, range: 25 to 2359
2020/08/20 13:29:39.462 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: Distance with cardinality: 258, range: 73 to 3904
2020/08/20 13:29:39.463 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: TailNum, size: 1956
2020/08/20 13:29:39.463 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:39.463 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: TailNum with cardinality: 326, max length in bytes: 6, range: N010AA to N994AT
2020/08/20 13:29:39.463 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:39.464 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Using fixed bytes value dictionary for column: DestCityName, size: 3390
2020/08/20 13:29:39.464 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivArrDelay with cardinality: 25, range: -2147483648 to 316
2020/08/20 13:29:39.464 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 9] Created dictionary for STRING column: DestCityName with cardinality: 113, max length in bytes: 30, range: Abilene, TX to White Plains, NY
2020/08/20 13:29:39.465 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:39.465 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Start building IndexCreator!
2020/08/20 13:29:39.466 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: LongestAddGTime with cardinality: 4, range: -2147483648 to 55
2020/08/20 13:29:39.467 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: OriginWac with cardinality: 45, range: 1 to 93
2020/08/20 13:29:39.468 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: WheelsOff with cardinality: 283, range: -2147483648 to 2309
2020/08/20 13:29:39.469 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DestAirportSeqID with cardinality: 103, range: 1014002 to 1537002
2020/08/20 13:29:39.470 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:39.471 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:39.472 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:39.473 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:39.474 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: ActualElapsedTime with cardinality: 152, range: -2147483648 to 508
2020/08/20 13:29:39.475 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:39.476 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: OriginStateName, size: 630
2020/08/20 13:29:39.476 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: OriginStateName with cardinality: 45, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:39.477 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:39.478 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:39.479 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:39.479 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-09 to 2014-01-09
2020/08/20 13:29:39.480 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: OriginCityName, size: 3060
2020/08/20 13:29:39.480 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: OriginCityName with cardinality: 102, max length in bytes: 30, range: Albany, GA to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:39.481 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: OriginStateFips with cardinality: 45, range: 1 to 72
2020/08/20 13:29:39.481 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: OriginState, size: 90
2020/08/20 13:29:39.482 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: OriginState with cardinality: 45, max length in bytes: 2, range: AK to WV
2020/08/20 13:29:39.483 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:39.483 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: WeatherDelay with cardinality: 8, range: -2147483648 to 55
2020/08/20 13:29:39.484 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DestWac with cardinality: 44, range: 1 to 93
2020/08/20 13:29:39.485 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: WheelsOn with cardinality: 268, range: -2147483648 to 2355
2020/08/20 13:29:39.486 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: OriginAirportID with cardinality: 106, range: 10135 to 15376
2020/08/20 13:29:39.487 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: OriginCityMarketID with cardinality: 92, range: 30135 to 35096
2020/08/20 13:29:39.488 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: NASDelay with cardinality: 30, range: -2147483648 to 113
2020/08/20 13:29:39.489 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: ArrTime with cardinality: 260, range: -2147483648 to 2400
2020/08/20 13:29:39.489 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: DestState, size: 88
2020/08/20 13:29:39.490 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: DestState with cardinality: 44, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:39.491 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:39.491 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Finished records indexing in IndexCreator!
2020/08/20 13:29:39.492 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:39.493 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 9 to 9
2020/08/20 13:29:39.493 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: RandomAirports, size: 304
2020/08/20 13:29:39.494 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: RandomAirports with cardinality: 76, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:39.494 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: TotalAddGTime with cardinality: 4, range: -2147483648 to 55
2020/08/20 13:29:39.495 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: CRSDepTime with cardinality: 217, range: 555 to 2235
2020/08/20 13:29:39.496 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 4 to 4
2020/08/20 13:29:39.497 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:39.497 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:39.498 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: Dest, size: 309
2020/08/20 13:29:39.498 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: Dest with cardinality: 103, max length in bytes: 3, range: ABQ to TUL
2020/08/20 13:29:39.499 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: FirstDepTime with cardinality: 4, range: -2147483648 to 1653
2020/08/20 13:29:39.500 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: DivTailNums, size: 174
2020/08/20 13:29:39.500 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: DivTailNums with cardinality: 29, max length in bytes: 6, range: N009AA to null
2020/08/20 13:29:39.501 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DepDelayMinutes with cardinality: 74, range: -2147483648 to 644
2020/08/20 13:29:39.502 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DepDelay with cardinality: 89, range: -2147483648 to 644
2020/08/20 13:29:39.504 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: TaxiIn with cardinality: 21, range: -2147483648 to 24
2020/08/20 13:29:39.506 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: OriginAirportSeqID with cardinality: 106, range: 1013503 to 1537602
2020/08/20 13:29:39.507 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DestStateFips with cardinality: 44, range: 1 to 78
2020/08/20 13:29:39.508 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: ArrDelay with cardinality: 97, range: -2147483648 to 242
2020/08/20 13:29:39.509 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:39.511 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivAirportIDs with cardinality: 36, range: -2147483648 to 15919
2020/08/20 13:29:39.512 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: TaxiOut with cardinality: 39, range: -2147483648 to 87
2020/08/20 13:29:39.513 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: CarrierDelay with cardinality: 34, range: -2147483648 to 235
2020/08/20 13:29:39.515 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:39.515 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Finished segment seal!
2020/08/20 13:29:39.516 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 9] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10 to v3 format
2020/08/20 13:29:39.516 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivLongestGTimes with cardinality: 28, range: -2147483648 to 128
2020/08/20 13:29:39.517 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: DivAirports, size: 144
2020/08/20 13:29:39.517 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: DivAirports with cardinality: 36, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:39.518 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: DivDistance with cardinality: 21, range: -2147483648 to 1121
2020/08/20 13:29:39.519 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:39.520 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: ArrDelayMinutes with cardinality: 70, range: -2147483648 to 242
2020/08/20 13:29:39.520 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for INT column: CRSArrTime with cardinality: 247, range: 528 to 2359
2020/08/20 13:29:39.522 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: TailNum, size: 1962
2020/08/20 13:29:39.522 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: TailNum with cardinality: 327, max length in bytes: 6, range: N003AA to null
2020/08/20 13:29:39.523 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Using fixed bytes value dictionary for column: DestCityName, size: 2970
2020/08/20 13:29:39.523 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 8] Created dictionary for STRING column: DestCityName with cardinality: 99, max length in bytes: 30, range: Albuquerque, NM to Williston, ND
2020/08/20 13:29:39.524 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Start building IndexCreator!
2020/08/20 13:29:39.546 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Finished records indexing in IndexCreator!
2020/08/20 13:29:39.572 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Finished segment seal!
2020/08/20 13:29:39.573 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 8] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09 to v3 format
2020/08/20 13:29:39.654 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 9] v3 segment location for segment: airlineStats_batch_2014-01-10_2014-01-10 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10/v3
2020/08/20 13:29:39.654 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 9] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10
2020/08/20 13:29:39.695 INFO [CrcUtils] [Executor task launch worker for task 9] Computed crc = 1605833174, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10/v3/metadata.properties]
2020/08/20 13:29:39.695 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Driver, record read time : 20
2020/08/20 13:29:39.695 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Driver, stats collector time : 0
2020/08/20 13:29:39.695 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 9] Driver, indexing time : 6
2020/08/20 13:29:39.695 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 9] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10.tar.gz
2020/08/20 13:29:39.708 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 9] Size for segment: airlineStats_batch_2014-01-10_2014-01-10, uncompressed: 120.87K, compressed: 37.03K
2020/08/20 13:29:39.708 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 9] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_batch_2014-01-10_2014-01-10.tar.gz]
2020/08/20 13:29:39.708 INFO [S3PinotFS] [Executor task launch worker for task 9] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-223f3bdc-28e6-47c9-8068-e2630f5b2cff/output/airlineStats_batch_2014-01-10_2014-01-10.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_batch_2014-01-10_2014-01-10.tar.gz
2020/08/20 13:29:39.716 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 8] v3 segment location for segment: airlineStats_batch_2014-01-09_2014-01-09 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09/v3
2020/08/20 13:29:39.716 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 8] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09
2020/08/20 13:29:39.749 INFO [CrcUtils] [Executor task launch worker for task 8] Computed crc = 2077663075, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09/v3/metadata.properties]
2020/08/20 13:29:39.750 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Driver, record read time : 14
2020/08/20 13:29:39.750 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Driver, stats collector time : 0
2020/08/20 13:29:39.750 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 8] Driver, indexing time : 8
2020/08/20 13:29:39.750 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 8] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09.tar.gz
2020/08/20 13:29:39.759 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 8] Size for segment: airlineStats_batch_2014-01-09_2014-01-09, uncompressed: 121.44K, compressed: 36.87K
2020/08/20 13:29:39.759 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 8] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_batch_2014-01-09_2014-01-09.tar.gz]
2020/08/20 13:29:39.759 INFO [S3PinotFS] [Executor task launch worker for task 8] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5f857ebf-a1f7-4885-968a-33905728c249/output/airlineStats_batch_2014-01-09_2014-01-09.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_batch_2014-01-09_2014-01-09.tar.gz
2020/08/20 13:29:40.257 INFO [Executor] [Executor task launch worker for task 9] Finished task 9.0 in stage 0.0 (TID 9). 708 bytes result sent to driver
2020/08/20 13:29:40.258 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 10.0 in stage 0.0 (TID 10, localhost, executor driver, partition 10, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:40.258 INFO [Executor] [Executor task launch worker for task 10] Running task 10.0 in stage 0.0 (TID 10)
2020/08/20 13:29:40.258 INFO [TaskSetManager] [task-result-getter-0] Finished task 9.0 in stage 0.0 (TID 9) in 2515 ms on localhost (executor driver) (9/31)
2020/08/20 13:29:40.260 INFO [PinotFSFactory] [Executor task launch worker for task 10] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:40.260 WARN [HadoopPinotFS] [Executor task launch worker for task 10] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:40.277 INFO [HadoopPinotFS] [Executor task launch worker for task 10] successfully initialized HadoopPinotFS
2020/08/20 13:29:40.277 INFO [PinotFSFactory] [Executor task launch worker for task 10] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:40.456 INFO [Executor] [Executor task launch worker for task 8] Finished task 8.0 in stage 0.0 (TID 8). 708 bytes result sent to driver
2020/08/20 13:29:40.457 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 11.0 in stage 0.0 (TID 11, localhost, executor driver, partition 11, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:40.457 INFO [Executor] [Executor task launch worker for task 11] Running task 11.0 in stage 0.0 (TID 11)
2020/08/20 13:29:40.457 INFO [TaskSetManager] [task-result-getter-1] Finished task 8.0 in stage 0.0 (TID 8) in 2820 ms on localhost (executor driver) (10/31)
2020/08/20 13:29:40.460 INFO [PinotFSFactory] [Executor task launch worker for task 11] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:40.460 WARN [HadoopPinotFS] [Executor task launch worker for task 11] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:40.482 INFO [HadoopPinotFS] [Executor task launch worker for task 11] successfully initialized HadoopPinotFS
2020/08/20 13:29:40.482 INFO [PinotFSFactory] [Executor task launch worker for task 11] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:41.567 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 10] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-10]
2020/08/20 13:29:41.567 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 10] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-10], plugins includes [null]
2020/08/20 13:29:41.568 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 10] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/11/airlineStats_data_2014-01-11.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/input/airlineStats_data_2014-01-11.avro
2020/08/20 13:29:41.568 INFO [S3PinotFS] [Executor task launch worker for task 10] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/11/airlineStats_data_2014-01-11.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/input/airlineStats_data_2014-01-11.avro
2020/08/20 13:29:41.811 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 11] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-11]
2020/08/20 13:29:41.811 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 11] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-11], plugins includes [null]
2020/08/20 13:29:41.811 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 11] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/12/airlineStats_data_2014-01-12.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/input/airlineStats_data_2014-01-12.avro
2020/08/20 13:29:41.811 INFO [S3PinotFS] [Executor task launch worker for task 11] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/12/airlineStats_data_2014-01-12.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/input/airlineStats_data_2014-01-12.avro
2020/08/20 13:29:41.922 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:41.943 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Finished building StatsCollector!
2020/08/20 13:29:41.943 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Collected stats for 269 documents
2020/08/20 13:29:41.944 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: FlightNum with cardinality: 266, range: 9 to 7381
2020/08/20 13:29:41.945 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: Origin, size: 282
2020/08/20 13:29:41.945 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: Origin with cardinality: 94, max length in bytes: 3, range: ACT to YAK
2020/08/20 13:29:41.946 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:41.947 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: LateAircraftDelay with cardinality: 32, range: -2147483648 to 166
2020/08/20 13:29:41.948 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivActualElapsedTime with cardinality: 38, range: -2147483648 to 846
2020/08/20 13:29:41.949 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivWheelsOns with cardinality: 61, range: -2147483648 to 2353
2020/08/20 13:29:41.950 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivWheelsOffs with cardinality: 40, range: -2147483648 to 2138
2020/08/20 13:29:41.951 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: AirTime with cardinality: 132, range: -2147483648 to 378
2020/08/20 13:29:41.952 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:41.953 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivTotalGTimes with cardinality: 37, range: -2147483648 to 118
2020/08/20 13:29:41.954 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:29:41.954 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:29:41.955 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DestCityMarketID with cardinality: 75, range: 30140 to 35550
2020/08/20 13:29:41.956 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 31, range: -2147483648 to 1538902
2020/08/20 13:29:41.957 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16081 to 16081
2020/08/20 13:29:41.958 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DepTime with cardinality: 232, range: -2147483648 to 2256
2020/08/20 13:29:41.958 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:41.959 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: CRSElapsedTime with cardinality: 141, range: 32 to 395
2020/08/20 13:29:41.960 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: DestStateName, size: 703
2020/08/20 13:29:41.960 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: DestStateName with cardinality: 37, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:29:41.961 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:41.961 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:41.962 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DestAirportID with cardinality: 88, range: 10140 to 15919
2020/08/20 13:29:41.963 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: Distance with cardinality: 228, range: 68 to 2845
2020/08/20 13:29:41.963 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:41.963 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:41.964 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivArrDelay with cardinality: 38, range: -2147483648 to 521
2020/08/20 13:29:41.965 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: SecurityDelay with cardinality: 3, range: -2147483648 to 4
2020/08/20 13:29:41.965 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 78
2020/08/20 13:29:41.966 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: OriginWac with cardinality: 37, range: 1 to 93
2020/08/20 13:29:41.967 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: WheelsOff with cardinality: 235, range: -2147483648 to 2318
2020/08/20 13:29:41.968 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DestAirportSeqID with cardinality: 88, range: 1014002 to 1591902
2020/08/20 13:29:41.968 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:41.969 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:41.970 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:41.971 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:41.972 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: ActualElapsedTime with cardinality: 137, range: -2147483648 to 401
2020/08/20 13:29:41.973 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:41.974 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: OriginStateName, size: 518
2020/08/20 13:29:41.974 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: OriginStateName with cardinality: 37, max length in bytes: 14, range: Alabama to Washington
2020/08/20 13:29:41.975 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DepartureDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:29:41.976 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:41.977 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:41.977 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-11 to 2014-01-11
2020/08/20 13:29:41.977 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: OriginCityName, size: 2700
2020/08/20 13:29:41.978 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: OriginCityName with cardinality: 90, max length in bytes: 30, range: Anchorage, AK to Yakutat, AK
2020/08/20 13:29:41.979 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: OriginStateFips with cardinality: 37, range: 1 to 72
2020/08/20 13:29:41.979 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: OriginState, size: 74
2020/08/20 13:29:41.980 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: OriginState with cardinality: 37, max length in bytes: 2, range: AK to WA
2020/08/20 13:29:41.981 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:41.982 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: WeatherDelay with cardinality: 6, range: -2147483648 to 205
2020/08/20 13:29:41.983 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DestWac with cardinality: 37, range: 1 to 93
2020/08/20 13:29:41.984 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: WheelsOn with cardinality: 214, range: -2147483648 to 2354
2020/08/20 13:29:41.984 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: OriginAirportID with cardinality: 94, range: 10155 to 15991
2020/08/20 13:29:41.985 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: OriginCityMarketID with cardinality: 80, range: 30155 to 35991
2020/08/20 13:29:41.986 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: NASDelay with cardinality: 28, range: -2147483648 to 238
2020/08/20 13:29:41.987 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: ArrTime with cardinality: 218, range: -2147483648 to 2358
2020/08/20 13:29:41.988 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: DestState, size: 74
2020/08/20 13:29:41.988 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: DestState with cardinality: 37, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:41.989 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:42.000 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:42.001 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 11 to 11
2020/08/20 13:29:42.002 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: RandomAirports, size: 288
2020/08/20 13:29:42.002 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: RandomAirports with cardinality: 72, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:42.004 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 78
2020/08/20 13:29:42.006 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: CRSDepTime with cardinality: 184, range: 500 to 2255
2020/08/20 13:29:42.007 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 6 to 6
2020/08/20 13:29:42.008 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: CancellationCode, size: 12
2020/08/20 13:29:42.009 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: CancellationCode with cardinality: 3, max length in bytes: 4, range: A to null
2020/08/20 13:29:42.009 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: Dest, size: 264
2020/08/20 13:29:42.010 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: Dest with cardinality: 88, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:42.011 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 944
2020/08/20 13:29:42.011 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: DivTailNums, size: 240
2020/08/20 13:29:42.011 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: DivTailNums with cardinality: 40, max length in bytes: 6, range: N113UW to null
2020/08/20 13:29:42.012 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DepDelayMinutes with cardinality: 62, range: -2147483648 to 265
2020/08/20 13:29:42.013 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DepDelay with cardinality: 75, range: -2147483648 to 265
2020/08/20 13:29:42.014 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: TaxiIn with cardinality: 24, range: -2147483648 to 28
2020/08/20 13:29:42.015 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: OriginAirportSeqID with cardinality: 94, range: 1015502 to 1599102
2020/08/20 13:29:42.016 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DestStateFips with cardinality: 37, range: 1 to 78
2020/08/20 13:29:42.016 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: ArrDelay with cardinality: 84, range: -2147483648 to 250
2020/08/20 13:29:42.017 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:42.018 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivAirportIDs with cardinality: 31, range: -2147483648 to 15389
2020/08/20 13:29:42.019 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: TaxiOut with cardinality: 40, range: -2147483648 to 122
2020/08/20 13:29:42.020 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: CarrierDelay with cardinality: 21, range: -2147483648 to 89
2020/08/20 13:29:42.021 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:42.022 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivLongestGTimes with cardinality: 32, range: -2147483648 to 118
2020/08/20 13:29:42.022 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: DivAirports, size: 124
2020/08/20 13:29:42.023 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: DivAirports with cardinality: 31, max length in bytes: 4, range: AGS to null
2020/08/20 13:29:42.024 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: DivDistance with cardinality: 9, range: -2147483648 to 228
2020/08/20 13:29:42.024 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:42.025 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: ArrDelayMinutes with cardinality: 57, range: -2147483648 to 250
2020/08/20 13:29:42.026 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for INT column: CRSArrTime with cardinality: 216, range: 11 to 2359
2020/08/20 13:29:42.027 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: TailNum, size: 1566
2020/08/20 13:29:42.027 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: TailNum with cardinality: 261, max length in bytes: 6, range: N113UW to null
2020/08/20 13:29:42.028 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Using fixed bytes value dictionary for column: DestCityName, size: 2520
2020/08/20 13:29:42.028 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 10] Created dictionary for STRING column: DestCityName with cardinality: 84, max length in bytes: 30, range: Albuquerque, NM to White Plains, NY
2020/08/20 13:29:42.029 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Start building IndexCreator!
2020/08/20 13:29:42.048 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Finished records indexing in IndexCreator!
2020/08/20 13:29:42.067 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Finished segment seal!
2020/08/20 13:29:42.067 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 10] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11 to v3 format
2020/08/20 13:29:42.168 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:42.187 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Finished building StatsCollector!
2020/08/20 13:29:42.187 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Collected stats for 276 documents
2020/08/20 13:29:42.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: FlightNum with cardinality: 272, range: 6 to 7420
2020/08/20 13:29:42.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: Origin, size: 267
2020/08/20 13:29:42.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: Origin with cardinality: 89, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:29:42.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:42.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: LateAircraftDelay with cardinality: 21, range: -2147483648 to 278
2020/08/20 13:29:42.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivActualElapsedTime with cardinality: 11, range: -2147483648 to 514
2020/08/20 13:29:42.194 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 10] v3 segment location for segment: airlineStats_batch_2014-01-11_2014-01-11 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11/v3
2020/08/20 13:29:42.194 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 10] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11
2020/08/20 13:29:42.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivWheelsOns with cardinality: 28, range: -2147483648 to 2003
2020/08/20 13:29:42.195 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivWheelsOffs with cardinality: 11, range: -2147483648 to 2121
2020/08/20 13:29:42.197 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: AirTime with cardinality: 151, range: -2147483648 to 512
2020/08/20 13:29:42.198 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:42.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivTotalGTimes with cardinality: 20, range: -2147483648 to 69
2020/08/20 13:29:42.200 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:42.200 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:42.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DestCityMarketID with cardinality: 84, range: 30073 to 35412
2020/08/20 13:29:42.202 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 17, range: -2147483648 to 1537002
2020/08/20 13:29:42.203 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16082 to 16082
2020/08/20 13:29:42.206 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DepTime with cardinality: 243, range: -2147483648 to 2343
2020/08/20 13:29:42.207 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:42.208 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: CRSElapsedTime with cardinality: 139, range: 37 to 553
2020/08/20 13:29:42.209 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: DestStateName, size: 779
2020/08/20 13:29:42.209 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: DestStateName with cardinality: 41, max length in bytes: 19, range: Alabama to Wisconsin
2020/08/20 13:29:42.210 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:42.210 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:42.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DestAirportID with cardinality: 97, range: 10140 to 16218
2020/08/20 13:29:42.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: Distance with cardinality: 231, range: 89 to 4243
2020/08/20 13:29:42.214 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:42.214 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:42.215 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivArrDelay with cardinality: 11, range: -2147483648 to 436
2020/08/20 13:29:42.216 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:42.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 23
2020/08/20 13:29:42.219 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: OriginWac with cardinality: 40, range: 1 to 93
2020/08/20 13:29:42.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: WheelsOff with cardinality: 241, range: -2147483648 to 2357
2020/08/20 13:29:42.221 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DestAirportSeqID with cardinality: 97, range: 1014002 to 1621801
2020/08/20 13:29:42.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:42.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:42.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:42.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:42.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: ActualElapsedTime with cardinality: 150, range: -2147483648 to 535
2020/08/20 13:29:42.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:42.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: OriginStateName, size: 560
2020/08/20 13:29:42.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: OriginStateName with cardinality: 40, max length in bytes: 14, range: Alaska to Wyoming
2020/08/20 13:29:42.230 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DepartureDelayGroups with cardinality: 12, range: -2147483648 to 12
2020/08/20 13:29:42.231 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:29:42.232 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:42.232 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-12 to 2014-01-12
2020/08/20 13:29:42.233 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: OriginCityName, size: 2125
2020/08/20 13:29:42.233 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: OriginCityName with cardinality: 85, max length in bytes: 25, range: Albuquerque, NM to Yuma, AZ
2020/08/20 13:29:42.235 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: OriginStateFips with cardinality: 40, range: 2 to 72
2020/08/20 13:29:42.236 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: OriginState, size: 80
2020/08/20 13:29:42.236 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: OriginState with cardinality: 40, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:42.238 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:42.240 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: WeatherDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:42.241 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DestWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:42.242 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: WheelsOn with cardinality: 226, range: -2147483648 to 2359
2020/08/20 13:29:42.243 INFO [CrcUtils] [Executor task launch worker for task 10] Computed crc = 1684503910, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11/v3/metadata.properties]
2020/08/20 13:29:42.243 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Driver, record read time : 13
2020/08/20 13:29:42.243 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Driver, stats collector time : 0
2020/08/20 13:29:42.243 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 10] Driver, indexing time : 6
2020/08/20 13:29:42.243 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 10] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11.tar.gz
2020/08/20 13:29:42.244 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: OriginAirportID with cardinality: 89, range: 10140 to 16218
2020/08/20 13:29:42.245 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: OriginCityMarketID with cardinality: 76, range: 30140 to 35401
2020/08/20 13:29:42.245 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: NASDelay with cardinality: 15, range: -2147483648 to 38
2020/08/20 13:29:42.246 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: ArrTime with cardinality: 224, range: -2147483648 to 2359
2020/08/20 13:29:42.247 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: DestState, size: 82
2020/08/20 13:29:42.247 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: DestState with cardinality: 41, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:42.248 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 10, range: -2147483648 to 12
2020/08/20 13:29:42.249 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:42.250 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 12 to 12
2020/08/20 13:29:42.251 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: RandomAirports, size: 312
2020/08/20 13:29:42.251 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: RandomAirports with cardinality: 78, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:42.252 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 23
2020/08/20 13:29:42.253 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: CRSDepTime with cardinality: 190, range: 546 to 2345
2020/08/20 13:29:42.253 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 10] Size for segment: airlineStats_batch_2014-01-11_2014-01-11, uncompressed: 111.89K, compressed: 32.11K
2020/08/20 13:29:42.253 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 10] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_batch_2014-01-11_2014-01-11.tar.gz]
2020/08/20 13:29:42.253 INFO [S3PinotFS] [Executor task launch worker for task 10] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-3c46ebe1-3147-48ff-9c58-3bc1f00b056d/output/airlineStats_batch_2014-01-11_2014-01-11.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_batch_2014-01-11_2014-01-11.tar.gz
2020/08/20 13:29:42.254 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 7 to 7
2020/08/20 13:29:42.255 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:42.255 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:42.256 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: Dest, size: 291
2020/08/20 13:29:42.256 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: Dest with cardinality: 97, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:29:42.257 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 2146
2020/08/20 13:29:42.258 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: DivTailNums, size: 66
2020/08/20 13:29:42.258 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: DivTailNums with cardinality: 11, max length in bytes: 6, range: N11121 to null
2020/08/20 13:29:42.259 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DepDelayMinutes with cardinality: 50, range: -2147483648 to 334
2020/08/20 13:29:42.260 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DepDelay with cardinality: 65, range: -2147483648 to 334
2020/08/20 13:29:42.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: TaxiIn with cardinality: 23, range: -2147483648 to 35
2020/08/20 13:29:42.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: OriginAirportSeqID with cardinality: 89, range: 1014002 to 1621801
2020/08/20 13:29:42.262 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DestStateFips with cardinality: 41, range: 1 to 78
2020/08/20 13:29:42.263 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: ArrDelay with cardinality: 69, range: -2147483648 to 312
2020/08/20 13:29:42.264 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:42.265 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivAirportIDs with cardinality: 17, range: -2147483648 to 15370
2020/08/20 13:29:42.266 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: TaxiOut with cardinality: 33, range: -2147483648 to 53
2020/08/20 13:29:42.267 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: CarrierDelay with cardinality: 21, range: -2147483648 to 188
2020/08/20 13:29:42.269 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:42.271 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivLongestGTimes with cardinality: 18, range: -2147483648 to 69
2020/08/20 13:29:42.272 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: DivAirports, size: 68
2020/08/20 13:29:42.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: DivAirports with cardinality: 17, max length in bytes: 4, range: CLT to null
2020/08/20 13:29:42.274 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: DivDistance with cardinality: 7, range: -2147483648 to 125
2020/08/20 13:29:42.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:42.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: ArrDelayMinutes with cardinality: 37, range: -2147483648 to 312
2020/08/20 13:29:42.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for INT column: CRSArrTime with cardinality: 222, range: 20 to 2359
2020/08/20 13:29:42.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: TailNum, size: 1620
2020/08/20 13:29:42.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: TailNum with cardinality: 270, max length in bytes: 6, range: N0EGMQ to N997DL
2020/08/20 13:29:42.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Using fixed bytes value dictionary for column: DestCityName, size: 2790
2020/08/20 13:29:42.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 11] Created dictionary for STRING column: DestCityName with cardinality: 93, max length in bytes: 30, range: Albany, NY to Yuma, AZ
2020/08/20 13:29:42.281 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Start building IndexCreator!
2020/08/20 13:29:42.299 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Finished records indexing in IndexCreator!
2020/08/20 13:29:42.325 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Finished segment seal!
2020/08/20 13:29:42.326 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 11] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12 to v3 format
2020/08/20 13:29:42.442 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 11] v3 segment location for segment: airlineStats_batch_2014-01-12_2014-01-12 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12/v3
2020/08/20 13:29:42.442 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 11] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12
2020/08/20 13:29:42.478 INFO [CrcUtils] [Executor task launch worker for task 11] Computed crc = 2855725741, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12/v3/metadata.properties]
2020/08/20 13:29:42.478 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Driver, record read time : 13
2020/08/20 13:29:42.478 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Driver, stats collector time : 0
2020/08/20 13:29:42.479 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 11] Driver, indexing time : 5
2020/08/20 13:29:42.479 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 11] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12.tar.gz
2020/08/20 13:29:42.487 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 11] Size for segment: airlineStats_batch_2014-01-12_2014-01-12, uncompressed: 111.18K, compressed: 31.61K
2020/08/20 13:29:42.487 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 11] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_batch_2014-01-12_2014-01-12.tar.gz]
2020/08/20 13:29:42.487 INFO [S3PinotFS] [Executor task launch worker for task 11] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-d5068dd0-ada9-4625-8c59-ceb80d01ae7f/output/airlineStats_batch_2014-01-12_2014-01-12.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_batch_2014-01-12_2014-01-12.tar.gz
2020/08/20 13:29:42.656 INFO [Executor] [Executor task launch worker for task 11] Finished task 11.0 in stage 0.0 (TID 11). 708 bytes result sent to driver
2020/08/20 13:29:42.657 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 12.0 in stage 0.0 (TID 12, localhost, executor driver, partition 12, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:42.657 INFO [Executor] [Executor task launch worker for task 12] Running task 12.0 in stage 0.0 (TID 12)
2020/08/20 13:29:42.657 INFO [TaskSetManager] [task-result-getter-2] Finished task 11.0 in stage 0.0 (TID 11) in 2201 ms on localhost (executor driver) (11/31)
2020/08/20 13:29:42.659 INFO [PinotFSFactory] [Executor task launch worker for task 12] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:42.659 WARN [HadoopPinotFS] [Executor task launch worker for task 12] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:42.677 INFO [HadoopPinotFS] [Executor task launch worker for task 12] successfully initialized HadoopPinotFS
2020/08/20 13:29:42.677 INFO [PinotFSFactory] [Executor task launch worker for task 12] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:42.897 INFO [Executor] [Executor task launch worker for task 10] Finished task 10.0 in stage 0.0 (TID 10). 708 bytes result sent to driver
2020/08/20 13:29:42.898 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 13.0 in stage 0.0 (TID 13, localhost, executor driver, partition 13, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:42.898 INFO [Executor] [Executor task launch worker for task 13] Running task 13.0 in stage 0.0 (TID 13)
2020/08/20 13:29:42.899 INFO [TaskSetManager] [task-result-getter-3] Finished task 10.0 in stage 0.0 (TID 10) in 2641 ms on localhost (executor driver) (12/31)
2020/08/20 13:29:42.900 INFO [PinotFSFactory] [Executor task launch worker for task 13] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:42.900 WARN [HadoopPinotFS] [Executor task launch worker for task 13] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:42.930 INFO [HadoopPinotFS] [Executor task launch worker for task 13] successfully initialized HadoopPinotFS
2020/08/20 13:29:42.930 INFO [PinotFSFactory] [Executor task launch worker for task 13] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:43.900 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 12] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-12]
2020/08/20 13:29:43.900 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 12] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-12], plugins includes [null]
2020/08/20 13:29:43.901 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 12] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/13/airlineStats_data_2014-01-13.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/input/airlineStats_data_2014-01-13.avro
2020/08/20 13:29:43.901 INFO [S3PinotFS] [Executor task launch worker for task 12] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/13/airlineStats_data_2014-01-13.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/input/airlineStats_data_2014-01-13.avro
2020/08/20 13:29:44.141 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 13] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-13]
2020/08/20 13:29:44.141 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 13] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-13], plugins includes [null]
2020/08/20 13:29:44.142 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 13] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/14/airlineStats_data_2014-01-14.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/input/airlineStats_data_2014-01-14.avro
2020/08/20 13:29:44.142 INFO [S3PinotFS] [Executor task launch worker for task 13] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/14/airlineStats_data_2014-01-14.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/input/airlineStats_data_2014-01-14.avro
2020/08/20 13:29:44.253 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:44.270 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Finished building StatsCollector!
2020/08/20 13:29:44.270 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Collected stats for 296 documents
2020/08/20 13:29:44.272 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: FlightNum with cardinality: 286, range: 5 to 7429
2020/08/20 13:29:44.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: Origin, size: 282
2020/08/20 13:29:44.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: Origin with cardinality: 94, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:29:44.274 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:44.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: LateAircraftDelay with cardinality: 12, range: -2147483648 to 147
2020/08/20 13:29:44.276 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivActualElapsedTime with cardinality: 14, range: -2147483648 to 805
2020/08/20 13:29:44.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivWheelsOns with cardinality: 32, range: -2147483648 to 2217
2020/08/20 13:29:44.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivWheelsOffs with cardinality: 16, range: -2147483648 to 2300
2020/08/20 13:29:44.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: AirTime with cardinality: 157, range: -2147483648 to 347
2020/08/20 13:29:44.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:44.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivTotalGTimes with cardinality: 23, range: -2147483648 to 112
2020/08/20 13:29:44.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:44.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:44.281 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DestCityMarketID with cardinality: 76, range: 30140 to 35841
2020/08/20 13:29:44.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 27, range: -2147483648 to 1538902
2020/08/20 13:29:44.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16083 to 16083
2020/08/20 13:29:44.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DepTime with cardinality: 249, range: -2147483648 to 2339
2020/08/20 13:29:44.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:44.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: CRSElapsedTime with cardinality: 139, range: 29 to 385
2020/08/20 13:29:44.286 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: DestStateName, size: 560
2020/08/20 13:29:44.286 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: DestStateName with cardinality: 40, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:44.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:44.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:44.288 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DestAirportID with cardinality: 91, range: 10140 to 16218
2020/08/20 13:29:44.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: Distance with cardinality: 240, range: 31 to 2611
2020/08/20 13:29:44.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 162
2020/08/20 13:29:44.290 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: ArrTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:44.291 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivArrDelay with cardinality: 14, range: -2147483648 to 735
2020/08/20 13:29:44.292 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:44.292 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: LongestAddGTime with cardinality: 4, range: -2147483648 to 29
2020/08/20 13:29:44.304 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: OriginWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:44.306 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: WheelsOff with cardinality: 256, range: -2147483648 to 2350
2020/08/20 13:29:44.306 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DestAirportSeqID with cardinality: 91, range: 1014002 to 1621801
2020/08/20 13:29:44.307 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:44.307 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:44.308 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:44.309 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:44.310 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: ActualElapsedTime with cardinality: 146, range: -2147483648 to 370
2020/08/20 13:29:44.310 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:44.311 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: OriginStateName, size: 779
2020/08/20 13:29:44.311 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: OriginStateName with cardinality: 41, max length in bytes: 19, range: Alabama to Wisconsin
2020/08/20 13:29:44.312 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:44.313 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:44.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:44.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-13 to 2014-01-13
2020/08/20 13:29:44.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: OriginCityName, size: 2275
2020/08/20 13:29:44.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: OriginCityName with cardinality: 91, max length in bytes: 25, range: Akron, OH to Yuma, AZ
2020/08/20 13:29:44.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: OriginStateFips with cardinality: 41, range: 1 to 78
2020/08/20 13:29:44.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: OriginState, size: 82
2020/08/20 13:29:44.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: OriginState with cardinality: 41, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:44.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:44.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: WeatherDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:44.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DestWac with cardinality: 40, range: 1 to 93
2020/08/20 13:29:44.320 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: WheelsOn with cardinality: 246, range: -2147483648 to 2339
2020/08/20 13:29:44.321 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: OriginAirportID with cardinality: 94, range: 10140 to 16218
2020/08/20 13:29:44.321 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: OriginCityMarketID with cardinality: 79, range: 30140 to 35412
2020/08/20 13:29:44.323 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: NASDelay with cardinality: 7, range: -2147483648 to 36
2020/08/20 13:29:44.323 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: ArrTime with cardinality: 251, range: -2147483648 to 2359
2020/08/20 13:29:44.324 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: DestState, size: 80
2020/08/20 13:29:44.324 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: DestState with cardinality: 40, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:44.325 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:44.326 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:44.326 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 13 to 13
2020/08/20 13:29:44.327 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: RandomAirports, size: 332
2020/08/20 13:29:44.329 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: RandomAirports with cardinality: 83, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:44.329 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: TotalAddGTime with cardinality: 4, range: -2147483648 to 29
2020/08/20 13:29:44.330 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: CRSDepTime with cardinality: 199, range: 540 to 2345
2020/08/20 13:29:44.331 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 1 to 1
2020/08/20 13:29:44.331 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: CancellationCode, size: 12
2020/08/20 13:29:44.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: CancellationCode with cardinality: 3, max length in bytes: 4, range: A to null
2020/08/20 13:29:44.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: Dest, size: 273
2020/08/20 13:29:44.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: Dest with cardinality: 91, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:29:44.333 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: FirstDepTime with cardinality: 4, range: -2147483648 to 1957
2020/08/20 13:29:44.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: DivTailNums, size: 96
2020/08/20 13:29:44.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: DivTailNums with cardinality: 16, max length in bytes: 6, range: N12996 to null
2020/08/20 13:29:44.336 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DepDelayMinutes with cardinality: 43, range: -2147483648 to 276
2020/08/20 13:29:44.337 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DepDelay with cardinality: 57, range: -2147483648 to 276
2020/08/20 13:29:44.338 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: TaxiIn with cardinality: 22, range: -2147483648 to 41
2020/08/20 13:29:44.339 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: OriginAirportSeqID with cardinality: 94, range: 1014002 to 1621801
2020/08/20 13:29:44.340 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DestStateFips with cardinality: 40, range: 1 to 72
2020/08/20 13:29:44.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: ArrDelay with cardinality: 62, range: -2147483648 to 230
2020/08/20 13:29:44.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:44.342 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivAirportIDs with cardinality: 27, range: -2147483648 to 15389
2020/08/20 13:29:44.343 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: TaxiOut with cardinality: 32, range: -2147483648 to 40
2020/08/20 13:29:44.344 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: CarrierDelay with cardinality: 15, range: -2147483648 to 230
2020/08/20 13:29:44.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:44.346 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivLongestGTimes with cardinality: 22, range: -2147483648 to 112
2020/08/20 13:29:44.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: DivAirports, size: 108
2020/08/20 13:29:44.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: DivAirports with cardinality: 27, max length in bytes: 4, range: ABE to null
2020/08/20 13:29:44.348 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: DivDistance with cardinality: 13, range: -2147483648 to 406
2020/08/20 13:29:44.349 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:44.349 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: ArrDelayMinutes with cardinality: 31, range: -2147483648 to 230
2020/08/20 13:29:44.350 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for INT column: CRSArrTime with cardinality: 229, range: 100 to 2349
2020/08/20 13:29:44.351 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: TailNum, size: 1716
2020/08/20 13:29:44.351 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: TailNum with cardinality: 286, max length in bytes: 6, range: N001AA to N991AT
2020/08/20 13:29:44.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Using fixed bytes value dictionary for column: DestCityName, size: 2523
2020/08/20 13:29:44.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 12] Created dictionary for STRING column: DestCityName with cardinality: 87, max length in bytes: 29, range: Akron, OH to Yuma, AZ
2020/08/20 13:29:44.353 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Start building IndexCreator!
2020/08/20 13:29:44.372 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Finished records indexing in IndexCreator!
2020/08/20 13:29:44.391 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Finished segment seal!
2020/08/20 13:29:44.391 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 12] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13 to v3 format
2020/08/20 13:29:44.468 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:44.491 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Finished building StatsCollector!
2020/08/20 13:29:44.491 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Collected stats for 311 documents
2020/08/20 13:29:44.492 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: FlightNum with cardinality: 305, range: 4 to 6466
2020/08/20 13:29:44.492 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: Origin, size: 315
2020/08/20 13:29:44.493 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: Origin with cardinality: 105, max length in bytes: 3, range: AGS to YUM
2020/08/20 13:29:44.494 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:44.495 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: LateAircraftDelay with cardinality: 12, range: -2147483648 to 64
2020/08/20 13:29:44.496 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivActualElapsedTime with cardinality: 15, range: -2147483648 to 996
2020/08/20 13:29:44.496 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivWheelsOns with cardinality: 58, range: -2147483648 to 2357
2020/08/20 13:29:44.497 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivWheelsOffs with cardinality: 17, range: -2147483648 to 2353
2020/08/20 13:29:44.498 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: AirTime with cardinality: 139, range: -2147483648 to 481
2020/08/20 13:29:44.499 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:44.500 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivTotalGTimes with cardinality: 27, range: -2147483648 to 110
2020/08/20 13:29:44.501 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:44.501 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:44.502 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DestCityMarketID with cardinality: 84, range: 30135 to 35380
2020/08/20 13:29:44.504 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 31, range: -2147483648 to 1501603
2020/08/20 13:29:44.506 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16084 to 16084
2020/08/20 13:29:44.507 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DepTime with cardinality: 261, range: -2147483648 to 2310
2020/08/20 13:29:44.508 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:44.508 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: CRSElapsedTime with cardinality: 146, range: 32 to 520
2020/08/20 13:29:44.509 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: DestStateName, size: 546
2020/08/20 13:29:44.509 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: DestStateName with cardinality: 39, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:44.510 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:44.510 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:44.511 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DestAirportID with cardinality: 96, range: 10135 to 15380
2020/08/20 13:29:44.512 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: Distance with cardinality: 257, range: 84 to 3784
2020/08/20 13:29:44.513 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:44.513 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:44.514 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivArrDelay with cardinality: 14, range: -2147483648 to 751
2020/08/20 13:29:44.515 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:44.516 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: LongestAddGTime with cardinality: 2, range: -2147483648 to 31
2020/08/20 13:29:44.517 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: OriginWac with cardinality: 40, range: 1 to 93
2020/08/20 13:29:44.517 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 12] v3 segment location for segment: airlineStats_batch_2014-01-13_2014-01-13 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13/v3
2020/08/20 13:29:44.518 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 12] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13
2020/08/20 13:29:44.518 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: WheelsOff with cardinality: 263, range: -2147483648 to 2327
2020/08/20 13:29:44.519 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DestAirportSeqID with cardinality: 96, range: 1013503 to 1538003
2020/08/20 13:29:44.519 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:44.520 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:44.521 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:44.521 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:44.522 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: ActualElapsedTime with cardinality: 147, range: -2147483648 to 507
2020/08/20 13:29:44.523 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:44.524 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: OriginStateName, size: 760
2020/08/20 13:29:44.525 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: OriginStateName with cardinality: 40, max length in bytes: 19, range: Alabama to Wisconsin
2020/08/20 13:29:44.526 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DepartureDelayGroups with cardinality: 11, range: -2147483648 to 12
2020/08/20 13:29:44.526 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:44.527 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:44.527 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-14 to 2014-01-14
2020/08/20 13:29:44.528 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: OriginCityName, size: 3030
2020/08/20 13:29:44.528 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: OriginCityName with cardinality: 101, max length in bytes: 30, range: Amarillo, TX to Yuma, AZ
2020/08/20 13:29:44.529 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: OriginStateFips with cardinality: 40, range: 1 to 78
2020/08/20 13:29:44.530 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: OriginState, size: 80
2020/08/20 13:29:44.530 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: OriginState with cardinality: 40, max length in bytes: 2, range: AK to WV
2020/08/20 13:29:44.531 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:44.532 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: WeatherDelay with cardinality: 4, range: -2147483648 to 22
2020/08/20 13:29:44.533 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DestWac with cardinality: 39, range: 1 to 93
2020/08/20 13:29:44.534 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: WheelsOn with cardinality: 223, range: -2147483648 to 2343
2020/08/20 13:29:44.535 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: OriginAirportID with cardinality: 105, range: 10208 to 16218
2020/08/20 13:29:44.538 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: OriginCityMarketID with cardinality: 90, range: 30194 to 35411
2020/08/20 13:29:44.539 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: NASDelay with cardinality: 22, range: -2147483648 to 109
2020/08/20 13:29:44.540 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: ArrTime with cardinality: 228, range: -2147483648 to 2357
2020/08/20 13:29:44.541 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: DestState, size: 78
2020/08/20 13:29:44.541 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: DestState with cardinality: 39, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:44.542 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 11, range: -2147483648 to 12
2020/08/20 13:29:44.543 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:44.543 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 14 to 14
2020/08/20 13:29:44.544 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: RandomAirports, size: 292
2020/08/20 13:29:44.544 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: RandomAirports with cardinality: 73, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:44.545 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: TotalAddGTime with cardinality: 2, range: -2147483648 to 31
2020/08/20 13:29:44.546 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: CRSDepTime with cardinality: 215, range: 517 to 2315
2020/08/20 13:29:44.547 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 2 to 2
2020/08/20 13:29:44.548 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:44.548 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:44.549 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: Dest, size: 288
2020/08/20 13:29:44.549 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: Dest with cardinality: 96, max length in bytes: 3, range: ABE to TVC
2020/08/20 13:29:44.550 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: FirstDepTime with cardinality: 2, range: -2147483648 to 639
2020/08/20 13:29:44.551 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: DivTailNums, size: 102
2020/08/20 13:29:44.551 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: DivTailNums with cardinality: 17, max length in bytes: 6, range: N11539 to null
2020/08/20 13:29:44.552 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DepDelayMinutes with cardinality: 45, range: -2147483648 to 286
2020/08/20 13:29:44.553 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DepDelay with cardinality: 62, range: -2147483648 to 286
2020/08/20 13:29:44.554 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: TaxiIn with cardinality: 20, range: -2147483648 to 29
2020/08/20 13:29:44.555 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: OriginAirportSeqID with cardinality: 105, range: 1020803 to 1621801
2020/08/20 13:29:44.556 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DestStateFips with cardinality: 39, range: 1 to 72
2020/08/20 13:29:44.557 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: ArrDelay with cardinality: 74, range: -2147483648 to 199
2020/08/20 13:29:44.558 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:44.559 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivAirportIDs with cardinality: 31, range: -2147483648 to 15016
2020/08/20 13:29:44.559 INFO [CrcUtils] [Executor task launch worker for task 12] Computed crc = 2829010080, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13/v3/metadata.properties]
2020/08/20 13:29:44.560 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Driver, record read time : 11
2020/08/20 13:29:44.560 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Driver, stats collector time : 0
2020/08/20 13:29:44.560 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 12] Driver, indexing time : 6
2020/08/20 13:29:44.560 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 12] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13.tar.gz
2020/08/20 13:29:44.560 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: TaxiOut with cardinality: 41, range: -2147483648 to 79
2020/08/20 13:29:44.561 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: CarrierDelay with cardinality: 15, range: -2147483648 to 199
2020/08/20 13:29:44.562 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:44.563 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivLongestGTimes with cardinality: 21, range: -2147483648 to 110
2020/08/20 13:29:44.563 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: DivAirports, size: 124
2020/08/20 13:29:44.564 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: DivAirports with cardinality: 31, max length in bytes: 4, range: ANC to null
2020/08/20 13:29:44.565 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: DivDistance with cardinality: 27, range: -2147483648 to 937
2020/08/20 13:29:44.566 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:44.567 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: ArrDelayMinutes with cardinality: 40, range: -2147483648 to 199
2020/08/20 13:29:44.567 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for INT column: CRSArrTime with cardinality: 252, range: 5 to 2350
2020/08/20 13:29:44.568 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: TailNum, size: 1788
2020/08/20 13:29:44.568 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: TailNum with cardinality: 298, max length in bytes: 6, range: N107US to null
2020/08/20 13:29:44.570 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Using fixed bytes value dictionary for column: DestCityName, size: 2760
2020/08/20 13:29:44.570 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 12] Size for segment: airlineStats_batch_2014-01-13_2014-01-13, uncompressed: 112.54K, compressed: 32.45K
2020/08/20 13:29:44.570 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 12] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_batch_2014-01-13_2014-01-13.tar.gz]
2020/08/20 13:29:44.570 INFO [S3PinotFS] [Executor task launch worker for task 12] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8765325a-0a34-4cb9-a085-a52adfa8e1ea/output/airlineStats_batch_2014-01-13_2014-01-13.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_batch_2014-01-13_2014-01-13.tar.gz
2020/08/20 13:29:44.570 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 13] Created dictionary for STRING column: DestCityName with cardinality: 92, max length in bytes: 30, range: Abilene, TX to Worcester, MA
2020/08/20 13:29:44.571 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Start building IndexCreator!
2020/08/20 13:29:44.590 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Finished records indexing in IndexCreator!
2020/08/20 13:29:44.611 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Finished segment seal!
2020/08/20 13:29:44.611 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 13] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14 to v3 format
2020/08/20 13:29:44.724 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 13] v3 segment location for segment: airlineStats_batch_2014-01-14_2014-01-14 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14/v3
2020/08/20 13:29:44.724 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 13] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14
2020/08/20 13:29:44.757 INFO [CrcUtils] [Executor task launch worker for task 13] Computed crc = 3795307611, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14/v3/metadata.properties]
2020/08/20 13:29:44.757 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Driver, record read time : 14
2020/08/20 13:29:44.757 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Driver, stats collector time : 0
2020/08/20 13:29:44.757 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 13] Driver, indexing time : 4
2020/08/20 13:29:44.757 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 13] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14.tar.gz
2020/08/20 13:29:44.766 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 13] Size for segment: airlineStats_batch_2014-01-14_2014-01-14, uncompressed: 116K, compressed: 33.97K
2020/08/20 13:29:44.767 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 13] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_batch_2014-01-14_2014-01-14.tar.gz]
2020/08/20 13:29:44.767 INFO [S3PinotFS] [Executor task launch worker for task 13] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c04b3c1a-1ca1-4e5f-a65e-b3a3806f0229/output/airlineStats_batch_2014-01-14_2014-01-14.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_batch_2014-01-14_2014-01-14.tar.gz
2020/08/20 13:29:45.362 INFO [Executor] [Executor task launch worker for task 13] Finished task 13.0 in stage 0.0 (TID 13). 751 bytes result sent to driver
2020/08/20 13:29:45.363 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 14.0 in stage 0.0 (TID 14, localhost, executor driver, partition 14, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:45.364 INFO [TaskSetManager] [task-result-getter-0] Finished task 13.0 in stage 0.0 (TID 13) in 2466 ms on localhost (executor driver) (13/31)
2020/08/20 13:29:45.364 INFO [Executor] [Executor task launch worker for task 14] Running task 14.0 in stage 0.0 (TID 14)
2020/08/20 13:29:45.365 INFO [PinotFSFactory] [Executor task launch worker for task 14] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:45.366 WARN [HadoopPinotFS] [Executor task launch worker for task 14] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:45.384 INFO [HadoopPinotFS] [Executor task launch worker for task 14] successfully initialized HadoopPinotFS
2020/08/20 13:29:45.384 INFO [PinotFSFactory] [Executor task launch worker for task 14] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:45.475 INFO [Executor] [Executor task launch worker for task 12] Finished task 12.0 in stage 0.0 (TID 12). 751 bytes result sent to driver
2020/08/20 13:29:45.476 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 15.0 in stage 0.0 (TID 15, localhost, executor driver, partition 15, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:45.477 INFO [Executor] [Executor task launch worker for task 15] Running task 15.0 in stage 0.0 (TID 15)
2020/08/20 13:29:45.477 INFO [TaskSetManager] [task-result-getter-1] Finished task 12.0 in stage 0.0 (TID 12) in 2820 ms on localhost (executor driver) (14/31)
2020/08/20 13:29:45.479 INFO [PinotFSFactory] [Executor task launch worker for task 15] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:45.479 WARN [HadoopPinotFS] [Executor task launch worker for task 15] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:45.499 INFO [HadoopPinotFS] [Executor task launch worker for task 15] successfully initialized HadoopPinotFS
2020/08/20 13:29:45.499 INFO [PinotFSFactory] [Executor task launch worker for task 15] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:46.717 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 14] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-14]
2020/08/20 13:29:46.717 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 14] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-14], plugins includes [null]
2020/08/20 13:29:46.718 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 14] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/15/airlineStats_data_2014-01-15.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/input/airlineStats_data_2014-01-15.avro
2020/08/20 13:29:46.718 INFO [S3PinotFS] [Executor task launch worker for task 14] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/15/airlineStats_data_2014-01-15.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/input/airlineStats_data_2014-01-15.avro
2020/08/20 13:29:46.803 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 15] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-15]
2020/08/20 13:29:46.804 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 15] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-15], plugins includes [null]
2020/08/20 13:29:46.805 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 15] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/16/airlineStats_data_2014-01-16.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/input/airlineStats_data_2014-01-16.avro
2020/08/20 13:29:46.805 INFO [S3PinotFS] [Executor task launch worker for task 15] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/16/airlineStats_data_2014-01-16.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/input/airlineStats_data_2014-01-16.avro
2020/08/20 13:29:47.058 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:47.078 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Finished building StatsCollector!
2020/08/20 13:29:47.078 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Collected stats for 313 documents
2020/08/20 13:29:47.079 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: FlightNum with cardinality: 304, range: 3 to 7416
2020/08/20 13:29:47.079 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: Origin, size: 291
2020/08/20 13:29:47.080 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: Origin with cardinality: 97, max length in bytes: 3, range: ABR to XNA
2020/08/20 13:29:47.080 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:47.081 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: LateAircraftDelay with cardinality: 17, range: -2147483648 to 221
2020/08/20 13:29:47.082 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivActualElapsedTime with cardinality: 36, range: -2147483648 to 1099
2020/08/20 13:29:47.083 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivWheelsOns with cardinality: 50, range: -2147483648 to 2347
2020/08/20 13:29:47.084 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivWheelsOffs with cardinality: 35, range: -2147483648 to 2322
2020/08/20 13:29:47.085 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: AirTime with cardinality: 151, range: -2147483648 to 437
2020/08/20 13:29:47.086 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:47.087 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivTotalGTimes with cardinality: 33, range: -2147483648 to 145
2020/08/20 13:29:47.088 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:29:47.088 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:29:47.089 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DestCityMarketID with cardinality: 88, range: 30135 to 35412
2020/08/20 13:29:47.090 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 33, range: -2147483648 to 1509602
2020/08/20 13:29:47.091 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16085 to 16085
2020/08/20 13:29:47.092 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DepTime with cardinality: 265, range: -2147483648 to 2216
2020/08/20 13:29:47.093 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:47.093 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: CRSElapsedTime with cardinality: 154, range: 33 to 470
2020/08/20 13:29:47.094 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: DestStateName, size: 1932
2020/08/20 13:29:47.094 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 46, range: Alabama to Wisconsin
2020/08/20 13:29:47.095 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:47.095 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:47.096 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DestAirportID with cardinality: 104, range: 10135 to 15624
2020/08/20 13:29:47.097 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: Distance with cardinality: 250, range: 67 to 3801
2020/08/20 13:29:47.098 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:47.098 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:47.099 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivArrDelay with cardinality: 31, range: -2147483648 to 1024
2020/08/20 13:29:47.100 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:47.101 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 41
2020/08/20 13:29:47.102 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: OriginWac with cardinality: 43, range: 1 to 93
2020/08/20 13:29:47.103 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: WheelsOff with cardinality: 269, range: -2147483648 to 2243
2020/08/20 13:29:47.105 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DestAirportSeqID with cardinality: 104, range: 1013503 to 1562401
2020/08/20 13:29:47.107 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:47.107 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:47.108 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:47.109 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:47.110 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: ActualElapsedTime with cardinality: 153, range: -2147483648 to 461
2020/08/20 13:29:47.111 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:47.111 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: OriginStateName, size: 602
2020/08/20 13:29:47.111 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: OriginStateName with cardinality: 43, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:47.112 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:47.113 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:29:47.114 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:47.114 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-15 to 2014-01-15
2020/08/20 13:29:47.115 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: OriginCityName, size: 2790
2020/08/20 13:29:47.115 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: OriginCityName with cardinality: 93, max length in bytes: 30, range: Aberdeen, SD to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:47.115 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: OriginStateFips with cardinality: 43, range: 1 to 72
2020/08/20 13:29:47.116 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: OriginState, size: 86
2020/08/20 13:29:47.116 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: OriginState with cardinality: 43, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:47.117 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:47.118 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: WeatherDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:47.119 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:47.119 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: WheelsOn with cardinality: 259, range: -2147483648 to 2355
2020/08/20 13:29:47.120 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: OriginAirportID with cardinality: 97, range: 10141 to 15919
2020/08/20 13:29:47.121 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: OriginCityMarketID with cardinality: 82, range: 30070 to 35165
2020/08/20 13:29:47.122 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: NASDelay with cardinality: 19, range: -2147483648 to 66
2020/08/20 13:29:47.123 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: ArrTime with cardinality: 262, range: -2147483648 to 2348
2020/08/20 13:29:47.123 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:29:47.124 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:47.124 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 12, range: -2147483648 to 12
2020/08/20 13:29:47.125 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:47.126 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 15 to 15
2020/08/20 13:29:47.127 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: RandomAirports, size: 312
2020/08/20 13:29:47.127 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: RandomAirports with cardinality: 78, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:47.128 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 41
2020/08/20 13:29:47.129 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: CRSDepTime with cardinality: 206, range: 510 to 2209
2020/08/20 13:29:47.130 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 3 to 3
2020/08/20 13:29:47.131 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:47.131 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:47.131 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: Dest, size: 312
2020/08/20 13:29:47.132 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: Dest with cardinality: 104, max length in bytes: 3, range: ABE to VPS
2020/08/20 13:29:47.133 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 1301
2020/08/20 13:29:47.133 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: DivTailNums, size: 222
2020/08/20 13:29:47.134 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: DivTailNums with cardinality: 37, max length in bytes: 6, range: N11536 to null
2020/08/20 13:29:47.135 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DepDelayMinutes with cardinality: 54, range: -2147483648 to 356
2020/08/20 13:29:47.135 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DepDelay with cardinality: 71, range: -2147483648 to 356
2020/08/20 13:29:47.138 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: TaxiIn with cardinality: 21, range: -2147483648 to 36
2020/08/20 13:29:47.140 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: OriginAirportSeqID with cardinality: 97, range: 1014102 to 1591902
2020/08/20 13:29:47.141 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 75
2020/08/20 13:29:47.142 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: ArrDelay with cardinality: 78, range: -2147483648 to 343
2020/08/20 13:29:47.143 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:47.144 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivAirportIDs with cardinality: 33, range: -2147483648 to 15096
2020/08/20 13:29:47.145 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: TaxiOut with cardinality: 35, range: -2147483648 to 54
2020/08/20 13:29:47.145 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: CarrierDelay with cardinality: 19, range: -2147483648 to 343
2020/08/20 13:29:47.146 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:47.147 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivLongestGTimes with cardinality: 28, range: -2147483648 to 145
2020/08/20 13:29:47.148 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: DivAirports, size: 132
2020/08/20 13:29:47.148 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: DivAirports with cardinality: 33, max length in bytes: 4, range: ALB to null
2020/08/20 13:29:47.149 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: DivDistance with cardinality: 9, range: -2147483648 to 257
2020/08/20 13:29:47.150 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:47.150 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: ArrDelayMinutes with cardinality: 41, range: -2147483648 to 343
2020/08/20 13:29:47.151 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for INT column: CRSArrTime with cardinality: 241, range: 10 to 2359
2020/08/20 13:29:47.153 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: TailNum, size: 1818
2020/08/20 13:29:47.153 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: TailNum with cardinality: 303, max length in bytes: 6, range: N002AA to N995DL
2020/08/20 13:29:47.154 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Using fixed bytes value dictionary for column: DestCityName, size: 3000
2020/08/20 13:29:47.154 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 14] Created dictionary for STRING column: DestCityName with cardinality: 100, max length in bytes: 30, range: Albany, GA to Wichita, KS
2020/08/20 13:29:47.155 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Start building IndexCreator!
2020/08/20 13:29:47.180 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Finished records indexing in IndexCreator!
2020/08/20 13:29:47.194 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:47.204 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Finished segment seal!
2020/08/20 13:29:47.205 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 14] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15 to v3 format
2020/08/20 13:29:47.221 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Finished building StatsCollector!
2020/08/20 13:29:47.221 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Collected stats for 310 documents
2020/08/20 13:29:47.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: FlightNum with cardinality: 299, range: 3 to 7364
2020/08/20 13:29:47.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: Origin, size: 306
2020/08/20 13:29:47.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: Origin with cardinality: 102, max length in bytes: 3, range: ABQ to TYS
2020/08/20 13:29:47.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:47.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: LateAircraftDelay with cardinality: 26, range: -2147483648 to 145
2020/08/20 13:29:47.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivActualElapsedTime with cardinality: 20, range: -2147483648 to 779
2020/08/20 13:29:47.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivWheelsOns with cardinality: 36, range: -2147483648 to 2243
2020/08/20 13:29:47.244 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivWheelsOffs with cardinality: 22, range: -2147483648 to 2234
2020/08/20 13:29:47.245 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: AirTime with cardinality: 155, range: -2147483648 to 474
2020/08/20 13:29:47.246 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:47.247 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivTotalGTimes with cardinality: 27, range: -2147483648 to 65
2020/08/20 13:29:47.248 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:47.249 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:47.250 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DestCityMarketID with cardinality: 78, range: 30107 to 34905
2020/08/20 13:29:47.251 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 26, range: -2147483648 to 1625702
2020/08/20 13:29:47.252 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16086 to 16086
2020/08/20 13:29:47.253 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DepTime with cardinality: 270, range: -2147483648 to 2353
2020/08/20 13:29:47.255 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:47.256 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: CRSElapsedTime with cardinality: 156, range: 37 to 491
2020/08/20 13:29:47.257 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: DestStateName, size: 630
2020/08/20 13:29:47.257 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: DestStateName with cardinality: 45, max length in bytes: 14, range: Alaska to Wyoming
2020/08/20 13:29:47.258 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:47.259 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:47.260 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DestAirportID with cardinality: 92, range: 10135 to 15304
2020/08/20 13:29:47.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: Distance with cardinality: 253, range: 74 to 4243
2020/08/20 13:29:47.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:47.262 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:47.263 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivArrDelay with cardinality: 20, range: -2147483648 to 638
2020/08/20 13:29:47.264 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:47.264 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 38
2020/08/20 13:29:47.265 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: OriginWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:47.266 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: WheelsOff with cardinality: 266, range: -2147483648 to 2342
2020/08/20 13:29:47.267 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DestAirportSeqID with cardinality: 92, range: 1013503 to 1530402
2020/08/20 13:29:47.267 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:47.267 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:47.268 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:47.271 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:47.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: ActualElapsedTime with cardinality: 154, range: -2147483648 to 502
2020/08/20 13:29:47.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:47.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: OriginStateName, size: 588
2020/08/20 13:29:47.276 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: OriginStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:47.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:47.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:47.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:47.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-16 to 2014-01-16
2020/08/20 13:29:47.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: OriginCityName, size: 3332
2020/08/20 13:29:47.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: OriginCityName with cardinality: 98, max length in bytes: 34, range: Aberdeen, SD to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:47.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: OriginStateFips with cardinality: 42, range: 1 to 56
2020/08/20 13:29:47.281 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: OriginState, size: 84
2020/08/20 13:29:47.281 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: OriginState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:47.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:47.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: WeatherDelay with cardinality: 7, range: -2147483648 to 21
2020/08/20 13:29:47.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DestWac with cardinality: 45, range: 1 to 93
2020/08/20 13:29:47.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: WheelsOn with cardinality: 262, range: -2147483648 to 2353
2020/08/20 13:29:47.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: OriginAirportID with cardinality: 102, range: 10140 to 15412
2020/08/20 13:29:47.286 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: OriginCityMarketID with cardinality: 88, range: 30073 to 35412
2020/08/20 13:29:47.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: NASDelay with cardinality: 25, range: -2147483648 to 74
2020/08/20 13:29:47.288 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: ArrTime with cardinality: 249, range: -2147483648 to 2352
2020/08/20 13:29:47.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: DestState, size: 90
2020/08/20 13:29:47.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: DestState with cardinality: 45, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:47.290 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 12, range: -2147483648 to 10
2020/08/20 13:29:47.291 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:47.292 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 16 to 16
2020/08/20 13:29:47.293 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: RandomAirports, size: 316
2020/08/20 13:29:47.293 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: RandomAirports with cardinality: 79, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:47.294 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 38
2020/08/20 13:29:47.295 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: CRSDepTime with cardinality: 208, range: 525 to 2355
2020/08/20 13:29:47.296 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 4 to 4
2020/08/20 13:29:47.297 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:47.297 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:47.298 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: Dest, size: 276
2020/08/20 13:29:47.298 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: Dest with cardinality: 92, max length in bytes: 3, range: ABE to TPA
2020/08/20 13:29:47.299 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 1742
2020/08/20 13:29:47.300 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: DivTailNums, size: 132
2020/08/20 13:29:47.300 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: DivTailNums with cardinality: 22, max length in bytes: 6, range: N14148 to null
2020/08/20 13:29:47.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DepDelayMinutes with cardinality: 56, range: -2147483648 to 187
2020/08/20 13:29:47.302 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DepDelay with cardinality: 70, range: -2147483648 to 187
2020/08/20 13:29:47.303 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: TaxiIn with cardinality: 29, range: -2147483648 to 37
2020/08/20 13:29:47.306 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: OriginAirportSeqID with cardinality: 102, range: 1014002 to 1541202
2020/08/20 13:29:47.307 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DestStateFips with cardinality: 45, range: 2 to 72
2020/08/20 13:29:47.308 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: ArrDelay with cardinality: 83, range: -2147483648 to 159
2020/08/20 13:29:47.309 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:47.310 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivAirportIDs with cardinality: 26, range: -2147483648 to 16257
2020/08/20 13:29:47.311 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: TaxiOut with cardinality: 46, range: -2147483648 to 82
2020/08/20 13:29:47.312 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: CarrierDelay with cardinality: 27, range: -2147483648 to 82
2020/08/20 13:29:47.313 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:47.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivLongestGTimes with cardinality: 22, range: -2147483648 to 42
2020/08/20 13:29:47.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: DivAirports, size: 104
2020/08/20 13:29:47.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: DivAirports with cardinality: 26, max length in bytes: 4, range: ANC to null
2020/08/20 13:29:47.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: DivDistance with cardinality: 10, range: -2147483648 to 483
2020/08/20 13:29:47.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:47.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: ArrDelayMinutes with cardinality: 52, range: -2147483648 to 159
2020/08/20 13:29:47.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for INT column: CRSArrTime with cardinality: 247, range: 12 to 2359
2020/08/20 13:29:47.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: TailNum, size: 1812
2020/08/20 13:29:47.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: TailNum with cardinality: 302, max length in bytes: 6, range: D942DN to N9EAMQ
2020/08/20 13:29:47.320 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Using fixed bytes value dictionary for column: DestCityName, size: 2670
2020/08/20 13:29:47.320 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 15] Created dictionary for STRING column: DestCityName with cardinality: 89, max length in bytes: 30, range: Albuquerque, NM to Wichita, KS
2020/08/20 13:29:47.321 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Start building IndexCreator!
2020/08/20 13:29:47.342 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Finished records indexing in IndexCreator!
2020/08/20 13:29:47.342 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 14] v3 segment location for segment: airlineStats_batch_2014-01-15_2014-01-15 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15/v3
2020/08/20 13:29:47.343 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 14] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15
2020/08/20 13:29:47.362 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Finished segment seal!
2020/08/20 13:29:47.363 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 15] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16 to v3 format
2020/08/20 13:29:47.382 INFO [CrcUtils] [Executor task launch worker for task 14] Computed crc = 225594280, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15/v3/metadata.properties]
2020/08/20 13:29:47.383 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Driver, record read time : 15
2020/08/20 13:29:47.383 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Driver, stats collector time : 0
2020/08/20 13:29:47.383 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 14] Driver, indexing time : 9
2020/08/20 13:29:47.383 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 14] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15.tar.gz
2020/08/20 13:29:47.393 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 14] Size for segment: airlineStats_batch_2014-01-15_2014-01-15, uncompressed: 118.23K, compressed: 35.09K
2020/08/20 13:29:47.393 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 14] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_batch_2014-01-15_2014-01-15.tar.gz]
2020/08/20 13:29:47.393 INFO [S3PinotFS] [Executor task launch worker for task 14] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-abda183c-34b3-4fb2-b02c-5023b1a26aa6/output/airlineStats_batch_2014-01-15_2014-01-15.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_batch_2014-01-15_2014-01-15.tar.gz
2020/08/20 13:29:47.479 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 15] v3 segment location for segment: airlineStats_batch_2014-01-16_2014-01-16 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16/v3
2020/08/20 13:29:47.479 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 15] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16
2020/08/20 13:29:47.514 INFO [CrcUtils] [Executor task launch worker for task 15] Computed crc = 2628540537, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16/v3/metadata.properties]
2020/08/20 13:29:47.514 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Driver, record read time : 16
2020/08/20 13:29:47.514 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Driver, stats collector time : 0
2020/08/20 13:29:47.514 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 15] Driver, indexing time : 5
2020/08/20 13:29:47.514 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 15] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16.tar.gz
2020/08/20 13:29:47.523 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 15] Size for segment: airlineStats_batch_2014-01-16_2014-01-16, uncompressed: 117.15K, compressed: 34.29K
2020/08/20 13:29:47.523 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 15] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_batch_2014-01-16_2014-01-16.tar.gz]
2020/08/20 13:29:47.523 INFO [S3PinotFS] [Executor task launch worker for task 15] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-cc7ba3cd-19eb-4f6f-a4f8-616e6d7924e4/output/airlineStats_batch_2014-01-16_2014-01-16.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_batch_2014-01-16_2014-01-16.tar.gz
2020/08/20 13:29:48.007 INFO [Executor] [Executor task launch worker for task 15] Finished task 15.0 in stage 0.0 (TID 15). 708 bytes result sent to driver
2020/08/20 13:29:48.008 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 16.0 in stage 0.0 (TID 16, localhost, executor driver, partition 16, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:48.008 INFO [Executor] [Executor task launch worker for task 16] Running task 16.0 in stage 0.0 (TID 16)
2020/08/20 13:29:48.008 INFO [TaskSetManager] [task-result-getter-2] Finished task 15.0 in stage 0.0 (TID 15) in 2532 ms on localhost (executor driver) (15/31)
2020/08/20 13:29:48.011 INFO [PinotFSFactory] [Executor task launch worker for task 16] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:48.011 WARN [HadoopPinotFS] [Executor task launch worker for task 16] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:48.027 INFO [HadoopPinotFS] [Executor task launch worker for task 16] successfully initialized HadoopPinotFS
2020/08/20 13:29:48.027 INFO [PinotFSFactory] [Executor task launch worker for task 16] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:48.106 INFO [Executor] [Executor task launch worker for task 14] Finished task 14.0 in stage 0.0 (TID 14). 665 bytes result sent to driver
2020/08/20 13:29:48.107 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 17.0 in stage 0.0 (TID 17, localhost, executor driver, partition 17, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:48.107 INFO [Executor] [Executor task launch worker for task 17] Running task 17.0 in stage 0.0 (TID 17)
2020/08/20 13:29:48.107 INFO [TaskSetManager] [task-result-getter-3] Finished task 14.0 in stage 0.0 (TID 14) in 2744 ms on localhost (executor driver) (16/31)
2020/08/20 13:29:48.109 INFO [PinotFSFactory] [Executor task launch worker for task 17] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:48.109 WARN [HadoopPinotFS] [Executor task launch worker for task 17] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:48.125 INFO [HadoopPinotFS] [Executor task launch worker for task 17] successfully initialized HadoopPinotFS
2020/08/20 13:29:48.125 INFO [PinotFSFactory] [Executor task launch worker for task 17] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:49.258 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 16] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-16]
2020/08/20 13:29:49.258 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 16] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-16], plugins includes [null]
2020/08/20 13:29:49.259 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 16] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/17/airlineStats_data_2014-01-17.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/input/airlineStats_data_2014-01-17.avro
2020/08/20 13:29:49.259 INFO [S3PinotFS] [Executor task launch worker for task 16] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/17/airlineStats_data_2014-01-17.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/input/airlineStats_data_2014-01-17.avro
2020/08/20 13:29:49.382 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 17] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-17]
2020/08/20 13:29:49.382 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 17] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-17], plugins includes [null]
2020/08/20 13:29:49.383 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 17] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/18/airlineStats_data_2014-01-18.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/input/airlineStats_data_2014-01-18.avro
2020/08/20 13:29:49.383 INFO [S3PinotFS] [Executor task launch worker for task 17] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/18/airlineStats_data_2014-01-18.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/input/airlineStats_data_2014-01-18.avro
2020/08/20 13:29:49.568 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:49.586 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Finished building StatsCollector!
2020/08/20 13:29:49.586 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Collected stats for 285 documents
2020/08/20 13:29:49.587 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: FlightNum with cardinality: 276, range: 10 to 6506
2020/08/20 13:29:49.588 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: Origin, size: 291
2020/08/20 13:29:49.588 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: Origin with cardinality: 97, max length in bytes: 3, range: ABQ to TYS
2020/08/20 13:29:49.589 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:49.589 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: LateAircraftDelay with cardinality: 20, range: -2147483648 to 49
2020/08/20 13:29:49.590 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivActualElapsedTime with cardinality: 12, range: -2147483648 to 500
2020/08/20 13:29:49.591 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivWheelsOns with cardinality: 24, range: -2147483648 to 2018
2020/08/20 13:29:49.592 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivWheelsOffs with cardinality: 13, range: -2147483648 to 1915
2020/08/20 13:29:49.592 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: AirTime with cardinality: 139, range: -2147483648 to 348
2020/08/20 13:29:49.593 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:49.594 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivTotalGTimes with cardinality: 20, range: -2147483648 to 46
2020/08/20 13:29:49.594 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:29:49.595 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:29:49.596 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DestCityMarketID with cardinality: 81, range: 30107 to 34783
2020/08/20 13:29:49.596 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 17, range: -2147483648 to 1538902
2020/08/20 13:29:49.597 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16087 to 16087
2020/08/20 13:29:49.598 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DepTime with cardinality: 251, range: -2147483648 to 2254
2020/08/20 13:29:49.599 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:49.599 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: CRSElapsedTime with cardinality: 136, range: 40 to 380
2020/08/20 13:29:49.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: DestStateName, size: 574
2020/08/20 13:29:49.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: DestStateName with cardinality: 41, max length in bytes: 14, range: Alaska to Wisconsin
2020/08/20 13:29:49.601 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: Carrier, size: 26
2020/08/20 13:29:49.601 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: Carrier with cardinality: 13, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:49.602 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DestAirportID with cardinality: 97, range: 10140 to 15919
2020/08/20 13:29:49.604 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: Distance with cardinality: 235, range: 89 to 2585
2020/08/20 13:29:49.605 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:49.605 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:49.606 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivArrDelay with cardinality: 12, range: -2147483648 to 309
2020/08/20 13:29:49.607 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:49.608 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: LongestAddGTime with cardinality: 4, range: -2147483648 to 40
2020/08/20 13:29:49.609 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: OriginWac with cardinality: 44, range: 1 to 93
2020/08/20 13:29:49.609 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: WheelsOff with cardinality: 244, range: -2147483648 to 2310
2020/08/20 13:29:49.610 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DestAirportSeqID with cardinality: 97, range: 1014002 to 1591902
2020/08/20 13:29:49.611 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: UniqueCarrier, size: 26
2020/08/20 13:29:49.611 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: UniqueCarrier with cardinality: 13, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:49.612 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:49.613 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:49.614 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: ActualElapsedTime with cardinality: 146, range: -2147483648 to 369
2020/08/20 13:29:49.615 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: AirlineID with cardinality: 13, range: 19393 to 21171
2020/08/20 13:29:49.615 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: OriginStateName, size: 616
2020/08/20 13:29:49.615 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: OriginStateName with cardinality: 44, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:49.616 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:49.617 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:49.618 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:49.618 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-17 to 2014-01-17
2020/08/20 13:29:49.619 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: OriginCityName, size: 2790
2020/08/20 13:29:49.619 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: OriginCityName with cardinality: 93, max length in bytes: 30, range: Albuquerque, NM to Wichita, KS
2020/08/20 13:29:49.620 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: OriginStateFips with cardinality: 44, range: 1 to 72
2020/08/20 13:29:49.621 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: OriginState, size: 88
2020/08/20 13:29:49.621 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: OriginState with cardinality: 44, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:49.622 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:49.623 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: WeatherDelay with cardinality: 4, range: -2147483648 to 23
2020/08/20 13:29:49.623 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DestWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:49.624 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: WheelsOn with cardinality: 245, range: -2147483648 to 2345
2020/08/20 13:29:49.625 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: OriginAirportID with cardinality: 97, range: 10140 to 15412
2020/08/20 13:29:49.626 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: OriginCityMarketID with cardinality: 82, range: 30073 to 35412
2020/08/20 13:29:49.626 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: NASDelay with cardinality: 18, range: -2147483648 to 157
2020/08/20 13:29:49.627 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: ArrTime with cardinality: 245, range: -2147483648 to 2351
2020/08/20 13:29:49.628 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: DestState, size: 82
2020/08/20 13:29:49.628 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: DestState with cardinality: 41, max length in bytes: 2, range: AK to WV
2020/08/20 13:29:49.629 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:49.630 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:49.631 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 17 to 17
2020/08/20 13:29:49.631 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: RandomAirports, size: 328
2020/08/20 13:29:49.631 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: RandomAirports with cardinality: 82, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:49.632 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: TotalAddGTime with cardinality: 4, range: -2147483648 to 42
2020/08/20 13:29:49.633 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: CRSDepTime with cardinality: 198, range: 35 to 2255
2020/08/20 13:29:49.634 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 5 to 5
2020/08/20 13:29:49.634 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: CancellationCode, size: 12
2020/08/20 13:29:49.634 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: CancellationCode with cardinality: 3, max length in bytes: 4, range: A to null
2020/08/20 13:29:49.635 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: Dest, size: 291
2020/08/20 13:29:49.635 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: Dest with cardinality: 97, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:49.637 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: FirstDepTime with cardinality: 5, range: -2147483648 to 2153
2020/08/20 13:29:49.645 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: DivTailNums, size: 78
2020/08/20 13:29:49.645 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: DivTailNums with cardinality: 13, max length in bytes: 6, range: N13988 to null
2020/08/20 13:29:49.646 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DepDelayMinutes with cardinality: 56, range: -2147483648 to 472
2020/08/20 13:29:49.647 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DepDelay with cardinality: 69, range: -2147483648 to 472
2020/08/20 13:29:49.648 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: TaxiIn with cardinality: 28, range: -2147483648 to 44
2020/08/20 13:29:49.648 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: OriginAirportSeqID with cardinality: 97, range: 1014002 to 1541202
2020/08/20 13:29:49.649 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DestStateFips with cardinality: 41, range: 2 to 55
2020/08/20 13:29:49.650 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: ArrDelay with cardinality: 80, range: -2147483648 to 463
2020/08/20 13:29:49.651 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:49.652 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivAirportIDs with cardinality: 17, range: -2147483648 to 15389
2020/08/20 13:29:49.653 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: TaxiOut with cardinality: 32, range: -2147483648 to 44
2020/08/20 13:29:49.653 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: CarrierDelay with cardinality: 25, range: -2147483648 to 463
2020/08/20 13:29:49.654 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:49.655 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivLongestGTimes with cardinality: 18, range: -2147483648 to 46
2020/08/20 13:29:49.656 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: DivAirports, size: 68
2020/08/20 13:29:49.656 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: DivAirports with cardinality: 17, max length in bytes: 4, range: ANC to null
2020/08/20 13:29:49.657 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: DivDistance with cardinality: 9, range: -2147483648 to 546
2020/08/20 13:29:49.658 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:49.658 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: ArrDelayMinutes with cardinality: 47, range: -2147483648 to 463
2020/08/20 13:29:49.659 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for INT column: CRSArrTime with cardinality: 231, range: 10 to 2355
2020/08/20 13:29:49.660 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: TailNum, size: 1644
2020/08/20 13:29:49.660 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: TailNum with cardinality: 274, max length in bytes: 6, range: N004AA to N997DL
2020/08/20 13:29:49.661 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Using fixed bytes value dictionary for column: DestCityName, size: 2790
2020/08/20 13:29:49.662 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 16] Created dictionary for STRING column: DestCityName with cardinality: 93, max length in bytes: 30, range: Albuquerque, NM to White Plains, NY
2020/08/20 13:29:49.663 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Start building IndexCreator!
2020/08/20 13:29:49.682 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Finished records indexing in IndexCreator!
2020/08/20 13:29:49.702 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Finished segment seal!
2020/08/20 13:29:49.703 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 16] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17 to v3 format
2020/08/20 13:29:49.765 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:49.784 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Finished building StatsCollector!
2020/08/20 13:29:49.784 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Collected stats for 241 documents
2020/08/20 13:29:49.785 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: FlightNum with cardinality: 236, range: 4 to 7423
2020/08/20 13:29:49.785 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: Origin, size: 261
2020/08/20 13:29:49.785 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: Origin with cardinality: 87, max length in bytes: 3, range: ABQ to TUS
2020/08/20 13:29:49.786 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:49.787 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: LateAircraftDelay with cardinality: 9, range: -2147483648 to 192
2020/08/20 13:29:49.788 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivActualElapsedTime with cardinality: 27, range: -2147483648 to 611
2020/08/20 13:29:49.789 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivWheelsOns with cardinality: 36, range: -2147483648 to 2236
2020/08/20 13:29:49.790 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivWheelsOffs with cardinality: 28, range: -2147483648 to 2329
2020/08/20 13:29:49.791 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: AirTime with cardinality: 128, range: -2147483648 to 522
2020/08/20 13:29:49.792 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:49.793 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivTotalGTimes with cardinality: 29, range: -2147483648 to 196
2020/08/20 13:29:49.794 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:29:49.794 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:29:49.795 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DestCityMarketID with cardinality: 79, range: 30073 to 35841
2020/08/20 13:29:49.796 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 22, range: -2147483648 to 1501603
2020/08/20 13:29:49.797 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16088 to 16088
2020/08/20 13:29:49.798 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DepTime with cardinality: 207, range: -2147483648 to 2228
2020/08/20 13:29:49.799 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:49.800 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: CRSElapsedTime with cardinality: 126, range: 35 to 553
2020/08/20 13:29:49.801 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: DestStateName, size: 574
2020/08/20 13:29:49.801 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: DestStateName with cardinality: 41, max length in bytes: 14, range: Alaska to Wisconsin
2020/08/20 13:29:49.802 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:49.802 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:49.803 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DestAirportID with cardinality: 91, range: 10140 to 15919
2020/08/20 13:29:49.804 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: Distance with cardinality: 204, range: 67 to 4817
2020/08/20 13:29:49.806 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 162
2020/08/20 13:29:49.806 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: ArrTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:49.808 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivArrDelay with cardinality: 28, range: -2147483648 to 484
2020/08/20 13:29:49.809 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:49.810 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 63
2020/08/20 13:29:49.811 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: OriginWac with cardinality: 35, range: 1 to 93
2020/08/20 13:29:49.812 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: WheelsOff with cardinality: 206, range: -2147483648 to 2245
2020/08/20 13:29:49.813 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DestAirportSeqID with cardinality: 91, range: 1014002 to 1591902
2020/08/20 13:29:49.813 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:49.814 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:49.815 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:49.816 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:49.817 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: ActualElapsedTime with cardinality: 134, range: -2147483648 to 544
2020/08/20 13:29:49.818 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:49.819 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: OriginStateName, size: 490
2020/08/20 13:29:49.819 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: OriginStateName with cardinality: 35, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:49.820 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:49.821 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:49.822 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:49.823 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-18 to 2014-01-18
2020/08/20 13:29:49.823 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: OriginCityName, size: 2324
2020/08/20 13:29:49.824 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: OriginCityName with cardinality: 83, max length in bytes: 28, range: Albany, NY to Wilmington, NC
2020/08/20 13:29:49.825 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: OriginStateFips with cardinality: 35, range: 1 to 55
2020/08/20 13:29:49.825 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: OriginState, size: 70
2020/08/20 13:29:49.826 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: OriginState with cardinality: 35, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:49.827 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:49.828 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: WeatherDelay with cardinality: 6, range: -2147483648 to 134
2020/08/20 13:29:49.829 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DestWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:49.829 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: WheelsOn with cardinality: 203, range: -2147483648 to 2343
2020/08/20 13:29:49.830 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: OriginAirportID with cardinality: 87, range: 10140 to 15376
2020/08/20 13:29:49.831 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: OriginCityMarketID with cardinality: 70, range: 30140 to 34986
2020/08/20 13:29:49.832 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: NASDelay with cardinality: 15, range: -2147483648 to 79
2020/08/20 13:29:49.833 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 16] v3 segment location for segment: airlineStats_batch_2014-01-17_2014-01-17 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17/v3
2020/08/20 13:29:49.833 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: ArrTime with cardinality: 197, range: -2147483648 to 2348
2020/08/20 13:29:49.834 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 16] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17
2020/08/20 13:29:49.834 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: DestState, size: 82
2020/08/20 13:29:49.834 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: DestState with cardinality: 41, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:49.835 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 11, range: -2147483648 to 12
2020/08/20 13:29:49.837 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:49.839 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 18 to 18
2020/08/20 13:29:49.840 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: RandomAirports, size: 332
2020/08/20 13:29:49.840 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: RandomAirports with cardinality: 83, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:49.841 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 63
2020/08/20 13:29:49.842 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: CRSDepTime with cardinality: 162, range: 540 to 2234
2020/08/20 13:29:49.843 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 6 to 6
2020/08/20 13:29:49.844 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: CancellationCode, size: 12
2020/08/20 13:29:49.844 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: CancellationCode with cardinality: 3, max length in bytes: 4, range: A to null
2020/08/20 13:29:49.845 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: Dest, size: 273
2020/08/20 13:29:49.845 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: Dest with cardinality: 91, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:49.846 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 1745
2020/08/20 13:29:49.847 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: DivTailNums, size: 174
2020/08/20 13:29:49.847 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: DivTailNums with cardinality: 29, max length in bytes: 6, range: N13903 to null
2020/08/20 13:29:49.849 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DepDelayMinutes with cardinality: 48, range: -2147483648 to 271
2020/08/20 13:29:49.850 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DepDelay with cardinality: 64, range: -2147483648 to 271
2020/08/20 13:29:49.851 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: TaxiIn with cardinality: 22, range: -2147483648 to 51
2020/08/20 13:29:49.852 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: OriginAirportSeqID with cardinality: 87, range: 1014002 to 1537602
2020/08/20 13:29:49.853 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DestStateFips with cardinality: 41, range: 2 to 72
2020/08/20 13:29:49.854 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: ArrDelay with cardinality: 73, range: -2147483648 to 197
2020/08/20 13:29:49.855 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:49.856 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivAirportIDs with cardinality: 22, range: -2147483648 to 15016
2020/08/20 13:29:49.857 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: TaxiOut with cardinality: 38, range: -2147483648 to 97
2020/08/20 13:29:49.858 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: CarrierDelay with cardinality: 16, range: -2147483648 to 189
2020/08/20 13:29:49.859 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:49.860 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivLongestGTimes with cardinality: 27, range: -2147483648 to 104
2020/08/20 13:29:49.861 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: DivAirports, size: 88
2020/08/20 13:29:49.862 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: DivAirports with cardinality: 22, max length in bytes: 4, range: BLI to null
2020/08/20 13:29:49.863 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: DivDistance with cardinality: 10, range: -2147483648 to 1521
2020/08/20 13:29:49.864 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:49.866 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: ArrDelayMinutes with cardinality: 40, range: -2147483648 to 197
2020/08/20 13:29:49.867 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for INT column: CRSArrTime with cardinality: 182, range: 36 to 2354
2020/08/20 13:29:49.868 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: TailNum, size: 1398
2020/08/20 13:29:49.868 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: TailNum with cardinality: 233, max length in bytes: 6, range: N11164 to N997AT
2020/08/20 13:29:49.869 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Using fixed bytes value dictionary for column: DestCityName, size: 2610
2020/08/20 13:29:49.869 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 17] Created dictionary for STRING column: DestCityName with cardinality: 87, max length in bytes: 30, range: Aguadilla, PR to Wrangell, AK
2020/08/20 13:29:49.870 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Start building IndexCreator!
2020/08/20 13:29:49.880 INFO [CrcUtils] [Executor task launch worker for task 16] Computed crc = 2969176634, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17/v3/metadata.properties]
2020/08/20 13:29:49.881 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Driver, record read time : 12
2020/08/20 13:29:49.881 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Driver, stats collector time : 0
2020/08/20 13:29:49.881 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 16] Driver, indexing time : 7
2020/08/20 13:29:49.881 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 16] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17.tar.gz
2020/08/20 13:29:49.888 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Finished records indexing in IndexCreator!
2020/08/20 13:29:49.890 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 16] Size for segment: airlineStats_batch_2014-01-17_2014-01-17, uncompressed: 113.48K, compressed: 32.12K
2020/08/20 13:29:49.890 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 16] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_batch_2014-01-17_2014-01-17.tar.gz]
2020/08/20 13:29:49.891 INFO [S3PinotFS] [Executor task launch worker for task 16] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-8ac58d7e-2af1-4ea2-a03b-ea1b4b33ddd4/output/airlineStats_batch_2014-01-17_2014-01-17.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_batch_2014-01-17_2014-01-17.tar.gz
2020/08/20 13:29:49.908 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Finished segment seal!
2020/08/20 13:29:49.909 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 17] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18 to v3 format
2020/08/20 13:29:50.024 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 17] v3 segment location for segment: airlineStats_batch_2014-01-18_2014-01-18 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18/v3
2020/08/20 13:29:50.024 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 17] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18
2020/08/20 13:29:50.058 INFO [CrcUtils] [Executor task launch worker for task 17] Computed crc = 63688276, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18/v3/metadata.properties]
2020/08/20 13:29:50.059 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Driver, record read time : 11
2020/08/20 13:29:50.059 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Driver, stats collector time : 0
2020/08/20 13:29:50.059 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 17] Driver, indexing time : 6
2020/08/20 13:29:50.059 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 17] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18.tar.gz
2020/08/20 13:29:50.068 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 17] Size for segment: airlineStats_batch_2014-01-18_2014-01-18, uncompressed: 108.16K, compressed: 29.62K
2020/08/20 13:29:50.068 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 17] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_batch_2014-01-18_2014-01-18.tar.gz]
2020/08/20 13:29:50.068 INFO [S3PinotFS] [Executor task launch worker for task 17] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-e39e544c-65f2-4f31-bba2-ace62ba8b21c/output/airlineStats_batch_2014-01-18_2014-01-18.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_batch_2014-01-18_2014-01-18.tar.gz
2020/08/20 13:29:50.480 INFO [Executor] [Executor task launch worker for task 17] Finished task 17.0 in stage 0.0 (TID 17). 708 bytes result sent to driver
2020/08/20 13:29:50.481 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 18.0 in stage 0.0 (TID 18, localhost, executor driver, partition 18, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:50.481 INFO [Executor] [Executor task launch worker for task 18] Running task 18.0 in stage 0.0 (TID 18)
2020/08/20 13:29:50.481 INFO [TaskSetManager] [task-result-getter-0] Finished task 17.0 in stage 0.0 (TID 17) in 2374 ms on localhost (executor driver) (17/31)
2020/08/20 13:29:50.483 INFO [PinotFSFactory] [Executor task launch worker for task 18] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:50.483 WARN [HadoopPinotFS] [Executor task launch worker for task 18] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:50.502 INFO [HadoopPinotFS] [Executor task launch worker for task 18] successfully initialized HadoopPinotFS
2020/08/20 13:29:50.502 INFO [PinotFSFactory] [Executor task launch worker for task 18] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:50.550 INFO [Executor] [Executor task launch worker for task 16] Finished task 16.0 in stage 0.0 (TID 16). 708 bytes result sent to driver
2020/08/20 13:29:50.551 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 19.0 in stage 0.0 (TID 19, localhost, executor driver, partition 19, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:50.551 INFO [Executor] [Executor task launch worker for task 19] Running task 19.0 in stage 0.0 (TID 19)
2020/08/20 13:29:50.551 INFO [TaskSetManager] [task-result-getter-1] Finished task 16.0 in stage 0.0 (TID 16) in 2543 ms on localhost (executor driver) (18/31)
2020/08/20 13:29:50.553 INFO [PinotFSFactory] [Executor task launch worker for task 19] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:50.553 WARN [HadoopPinotFS] [Executor task launch worker for task 19] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:50.575 INFO [HadoopPinotFS] [Executor task launch worker for task 19] successfully initialized HadoopPinotFS
2020/08/20 13:29:50.575 INFO [PinotFSFactory] [Executor task launch worker for task 19] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:51.811 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 18] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-18]
2020/08/20 13:29:51.811 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 18] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-18], plugins includes [null]
2020/08/20 13:29:51.812 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 18] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/19/airlineStats_data_2014-01-19.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/input/airlineStats_data_2014-01-19.avro
2020/08/20 13:29:51.812 INFO [S3PinotFS] [Executor task launch worker for task 18] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/19/airlineStats_data_2014-01-19.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/input/airlineStats_data_2014-01-19.avro
2020/08/20 13:29:51.888 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 19] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-19]
2020/08/20 13:29:51.888 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 19] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-19], plugins includes [null]
2020/08/20 13:29:51.889 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 19] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/20/airlineStats_data_2014-01-20.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/input/airlineStats_data_2014-01-20.avro
2020/08/20 13:29:51.889 INFO [S3PinotFS] [Executor task launch worker for task 19] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/20/airlineStats_data_2014-01-20.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/input/airlineStats_data_2014-01-20.avro
2020/08/20 13:29:52.175 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:52.191 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Finished building StatsCollector!
2020/08/20 13:29:52.191 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Collected stats for 270 documents
2020/08/20 13:29:52.191 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: FlightNum with cardinality: 261, range: 23 to 7416
2020/08/20 13:29:52.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: Origin, size: 282
2020/08/20 13:29:52.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: Origin with cardinality: 94, max length in bytes: 3, range: ABI to TUS
2020/08/20 13:29:52.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:52.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: LateAircraftDelay with cardinality: 12, range: -2147483648 to 123
2020/08/20 13:29:52.195 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivActualElapsedTime with cardinality: 7, range: -2147483648 to 410
2020/08/20 13:29:52.196 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivWheelsOns with cardinality: 10, range: -2147483648 to 1813
2020/08/20 13:29:52.197 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivWheelsOffs with cardinality: 8, range: -2147483648 to 1933
2020/08/20 13:29:52.198 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: AirTime with cardinality: 145, range: -2147483648 to 343
2020/08/20 13:29:52.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:52.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivTotalGTimes with cardinality: 11, range: -2147483648 to 28
2020/08/20 13:29:52.200 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:52.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:52.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DestCityMarketID with cardinality: 75, range: 30140 to 35412
2020/08/20 13:29:52.202 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 9, range: -2147483648 to 1448902
2020/08/20 13:29:52.204 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16089 to 16089
2020/08/20 13:29:52.205 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DepTime with cardinality: 236, range: 526 to 2345
2020/08/20 13:29:52.207 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:52.208 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: CRSElapsedTime with cardinality: 133, range: 32 to 390
2020/08/20 13:29:52.208 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: DestStateName, size: 532
2020/08/20 13:29:52.208 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: DestStateName with cardinality: 38, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:52.209 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:52.209 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:52.245 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:52.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DestAirportID with cardinality: 90, range: 10140 to 15919
2020/08/20 13:29:52.262 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: Distance with cardinality: 224, range: 101 to 2556
2020/08/20 13:29:52.262 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:52.263 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:52.264 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivArrDelay with cardinality: 8, range: -2147483648 to 291
2020/08/20 13:29:52.265 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: SecurityDelay with cardinality: 3, range: -2147483648 to 18
2020/08/20 13:29:52.266 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: LongestAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:52.267 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: OriginWac with cardinality: 43, range: 1 to 93
2020/08/20 13:29:52.268 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: WheelsOff with cardinality: 242, range: 545 to 2357
2020/08/20 13:29:52.269 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DestAirportSeqID with cardinality: 90, range: 1014002 to 1591902
2020/08/20 13:29:52.270 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:52.271 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:52.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:52.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:52.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: ActualElapsedTime with cardinality: 156, range: -2147483648 to 366
2020/08/20 13:29:52.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:52.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: OriginStateName, size: 602
2020/08/20 13:29:52.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: OriginStateName with cardinality: 43, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:52.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2 to 12
2020/08/20 13:29:52.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivAirportLandings with cardinality: 2, range: 0 to 1
2020/08/20 13:29:52.283 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Finished building StatsCollector!
2020/08/20 13:29:52.286 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Collected stats for 284 documents
2020/08/20 13:29:52.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:52.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: FlightNum with cardinality: 278, range: 5 to 7390
2020/08/20 13:29:52.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-19 to 2014-01-19
2020/08/20 13:29:52.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: Origin, size: 267
2020/08/20 13:29:52.288 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: OriginCityName, size: 2700
2020/08/20 13:29:52.288 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: Origin with cardinality: 89, max length in bytes: 3, range: ABQ to VPS
2020/08/20 13:29:52.288 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: OriginCityName with cardinality: 90, max length in bytes: 30, range: Abilene, TX to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:52.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:52.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: OriginStateFips with cardinality: 43, range: 1 to 72
2020/08/20 13:29:52.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: LateAircraftDelay with cardinality: 17, range: -2147483648 to 55
2020/08/20 13:29:52.290 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: OriginState, size: 86
2020/08/20 13:29:52.290 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivActualElapsedTime with cardinality: 16, range: -2147483648 to 495
2020/08/20 13:29:52.291 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: OriginState with cardinality: 43, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:52.291 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivWheelsOns with cardinality: 26, range: -2147483648 to 2311
2020/08/20 13:29:52.291 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:52.292 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivWheelsOffs with cardinality: 17, range: -2147483648 to 2355
2020/08/20 13:29:52.292 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: WeatherDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:52.293 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: AirTime with cardinality: 146, range: -2147483648 to 362
2020/08/20 13:29:52.294 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DestWac with cardinality: 38, range: 1 to 93
2020/08/20 13:29:52.294 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:52.300 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: WheelsOn with cardinality: 240, range: -2147483648 to 2346
2020/08/20 13:29:52.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivTotalGTimes with cardinality: 18, range: -2147483648 to 59
2020/08/20 13:29:52.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: OriginAirportID with cardinality: 94, range: 10136 to 15376
2020/08/20 13:29:52.302 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:52.302 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:52.303 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: OriginCityMarketID with cardinality: 79, range: 30107 to 35249
2020/08/20 13:29:52.304 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DestCityMarketID with cardinality: 84, range: 30140 to 35412
2020/08/20 13:29:52.305 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: NASDelay with cardinality: 8, range: -2147483648 to 94
2020/08/20 13:29:52.306 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 22, range: -2147483648 to 1486903
2020/08/20 13:29:52.307 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: ArrTime with cardinality: 235, range: -2147483648 to 2351
2020/08/20 13:29:52.307 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16090 to 16090
2020/08/20 13:29:52.308 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: DestState, size: 76
2020/08/20 13:29:52.308 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DepTime with cardinality: 242, range: -2147483648 to 2327
2020/08/20 13:29:52.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: DestState with cardinality: 38, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:52.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:52.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:52.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: CRSElapsedTime with cardinality: 146, range: 37 to 400
2020/08/20 13:29:52.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:52.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: DestStateName, size: 630
2020/08/20 13:29:52.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: DestStateName with cardinality: 45, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:52.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 19 to 19
2020/08/20 13:29:52.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:52.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: RandomAirports, size: 332
2020/08/20 13:29:52.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:52.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: RandomAirports with cardinality: 83, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:52.320 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DestAirportID with cardinality: 99, range: 10140 to 15919
2020/08/20 13:29:52.321 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: TotalAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:52.321 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: CRSDepTime with cardinality: 190, range: 530 to 2345
2020/08/20 13:29:52.321 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: Distance with cardinality: 232, range: 56 to 2994
2020/08/20 13:29:52.322 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:52.322 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 7 to 7
2020/08/20 13:29:52.323 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:52.323 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: CancellationCode, size: 4
2020/08/20 13:29:52.323 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: CancellationCode with cardinality: 1, max length in bytes: 4, range: null to null
2020/08/20 13:29:52.324 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivArrDelay with cardinality: 17, range: -2147483648 to 609
2020/08/20 13:29:52.324 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: Dest, size: 270
2020/08/20 13:29:52.325 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: Dest with cardinality: 90, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:52.325 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:52.326 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: FirstDepTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:52.326 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: LongestAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:52.326 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: DivTailNums, size: 48
2020/08/20 13:29:52.327 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: DivTailNums with cardinality: 8, max length in bytes: 6, range: N16976 to null
2020/08/20 13:29:52.327 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: OriginWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:52.328 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DepDelayMinutes with cardinality: 35, range: 0 to 456
2020/08/20 13:29:52.328 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: WheelsOff with cardinality: 251, range: -2147483648 to 2348
2020/08/20 13:29:52.329 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DepDelay with cardinality: 51, range: -22 to 456
2020/08/20 13:29:52.329 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DestAirportSeqID with cardinality: 99, range: 1014002 to 1591902
2020/08/20 13:29:52.330 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: TaxiIn with cardinality: 23, range: -2147483648 to 33
2020/08/20 13:29:52.330 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:52.330 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:52.331 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: OriginAirportSeqID with cardinality: 94, range: 1013603 to 1537602
2020/08/20 13:29:52.331 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:52.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DestStateFips with cardinality: 38, range: 1 to 55
2020/08/20 13:29:52.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:52.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: ArrDelay with cardinality: 71, range: -2147483648 to 455
2020/08/20 13:29:52.333 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: ActualElapsedTime with cardinality: 153, range: -2147483648 to 388
2020/08/20 13:29:52.333 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: Cancelled with cardinality: 1, range: 0 to 0
2020/08/20 13:29:52.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:52.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivAirportIDs with cardinality: 9, range: -2147483648 to 14489
2020/08/20 13:29:52.335 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: OriginStateName, size: 588
2020/08/20 13:29:52.335 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: OriginStateName with cardinality: 42, max length in bytes: 14, range: Alaska to Wyoming
2020/08/20 13:29:52.335 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: TaxiOut with cardinality: 32, range: 3 to 38
2020/08/20 13:29:52.337 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DepartureDelayGroups with cardinality: 12, range: -2147483648 to 12
2020/08/20 13:29:52.337 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: CarrierDelay with cardinality: 14, range: -2147483648 to 455
2020/08/20 13:29:52.338 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:29:52.339 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DepDel15 with cardinality: 2, range: 0 to 1
2020/08/20 13:29:52.339 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:52.340 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-20 to 2014-01-20
2020/08/20 13:29:52.340 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivLongestGTimes with cardinality: 9, range: -2147483648 to 22
2020/08/20 13:29:52.340 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: OriginCityName, size: 2550
2020/08/20 13:29:52.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: OriginCityName with cardinality: 85, max length in bytes: 30, range: Albuquerque, NM to Wichita, KS
2020/08/20 13:29:52.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: DivAirports, size: 36
2020/08/20 13:29:52.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: DivAirports with cardinality: 9, max length in bytes: 4, range: BOI to null
2020/08/20 13:29:52.342 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: OriginStateFips with cardinality: 42, range: 2 to 72
2020/08/20 13:29:52.342 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: DivDistance with cardinality: 4, range: -2147483648 to 156
2020/08/20 13:29:52.343 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: OriginState, size: 84
2020/08/20 13:29:52.343 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: OriginState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:52.343 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:52.344 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:52.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: ArrDelayMinutes with cardinality: 34, range: -2147483648 to 455
2020/08/20 13:29:52.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: WeatherDelay with cardinality: 4, range: -2147483648 to 68
2020/08/20 13:29:52.346 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for INT column: CRSArrTime with cardinality: 215, range: 47 to 2357
2020/08/20 13:29:52.346 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DestWac with cardinality: 45, range: 1 to 93
2020/08/20 13:29:52.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: TailNum, size: 1578
2020/08/20 13:29:52.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: WheelsOn with cardinality: 247, range: -2147483648 to 2351
2020/08/20 13:29:52.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: TailNum with cardinality: 263, max length in bytes: 6, range: N005AA to N989AT
2020/08/20 13:29:52.348 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Using fixed bytes value dictionary for column: DestCityName, size: 2580
2020/08/20 13:29:52.348 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: OriginAirportID with cardinality: 89, range: 10140 to 15624
2020/08/20 13:29:52.348 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 18] Created dictionary for STRING column: DestCityName with cardinality: 86, max length in bytes: 30, range: Albany, NY to Wilmington, NC
2020/08/20 13:29:52.349 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Start building IndexCreator!
2020/08/20 13:29:52.349 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: OriginCityMarketID with cardinality: 76, range: 30107 to 35411
2020/08/20 13:29:52.350 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: NASDelay with cardinality: 18, range: -2147483648 to 80
2020/08/20 13:29:52.351 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: ArrTime with cardinality: 245, range: -2147483648 to 2354
2020/08/20 13:29:52.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: DestState, size: 90
2020/08/20 13:29:52.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: DestState with cardinality: 45, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:52.353 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 10, range: -2147483648 to 7
2020/08/20 13:29:52.354 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:52.355 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 20 to 20
2020/08/20 13:29:52.355 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: RandomAirports, size: 272
2020/08/20 13:29:52.355 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: RandomAirports with cardinality: 68, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:52.356 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: TotalAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:52.357 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: CRSDepTime with cardinality: 200, range: 35 to 2330
2020/08/20 13:29:52.358 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 1 to 1
2020/08/20 13:29:52.358 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:52.358 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:52.359 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: Dest, size: 297
2020/08/20 13:29:52.359 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: Dest with cardinality: 99, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:52.360 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: FirstDepTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:29:52.361 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: DivTailNums, size: 102
2020/08/20 13:29:52.361 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: DivTailNums with cardinality: 17, max length in bytes: 6, range: N11181 to null
2020/08/20 13:29:52.362 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DepDelayMinutes with cardinality: 51, range: -2147483648 to 414
2020/08/20 13:29:52.363 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DepDelay with cardinality: 66, range: -2147483648 to 414
2020/08/20 13:29:52.364 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: TaxiIn with cardinality: 22, range: -2147483648 to 96
2020/08/20 13:29:52.365 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: OriginAirportSeqID with cardinality: 89, range: 1014002 to 1562401
2020/08/20 13:29:52.365 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Finished records indexing in IndexCreator!
2020/08/20 13:29:52.366 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DestStateFips with cardinality: 45, range: 1 to 72
2020/08/20 13:29:52.367 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: ArrDelay with cardinality: 70, range: -2147483648 to 115
2020/08/20 13:29:52.368 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:52.369 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivAirportIDs with cardinality: 22, range: -2147483648 to 14869
2020/08/20 13:29:52.371 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: TaxiOut with cardinality: 39, range: -2147483648 to 74
2020/08/20 13:29:52.372 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: CarrierDelay with cardinality: 20, range: -2147483648 to 96
2020/08/20 13:29:52.373 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:52.375 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivLongestGTimes with cardinality: 19, range: -2147483648 to 59
2020/08/20 13:29:52.376 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: DivAirports, size: 88
2020/08/20 13:29:52.376 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: DivAirports with cardinality: 22, max length in bytes: 4, range: AEX to null
2020/08/20 13:29:52.377 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: DivDistance with cardinality: 6, range: -2147483648 to 2556
2020/08/20 13:29:52.378 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:52.379 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: ArrDelayMinutes with cardinality: 39, range: -2147483648 to 115
2020/08/20 13:29:52.380 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for INT column: CRSArrTime with cardinality: 236, range: 55 to 2351
2020/08/20 13:29:52.381 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: TailNum, size: 1656
2020/08/20 13:29:52.381 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: TailNum with cardinality: 276, max length in bytes: 6, range: N11109 to N991DL
2020/08/20 13:29:52.382 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Using fixed bytes value dictionary for column: DestCityName, size: 2850
2020/08/20 13:29:52.382 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 19] Created dictionary for STRING column: DestCityName with cardinality: 95, max length in bytes: 30, range: Albuquerque, NM to Wichita, KS
2020/08/20 13:29:52.383 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Start building IndexCreator!
2020/08/20 13:29:52.389 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Finished segment seal!
2020/08/20 13:29:52.389 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 18] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19 to v3 format
2020/08/20 13:29:52.401 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Finished records indexing in IndexCreator!
2020/08/20 13:29:52.422 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Finished segment seal!
2020/08/20 13:29:52.423 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 19] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20 to v3 format
2020/08/20 13:29:52.519 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 18] v3 segment location for segment: airlineStats_batch_2014-01-19_2014-01-19 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19/v3
2020/08/20 13:29:52.519 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 18] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19
2020/08/20 13:29:52.557 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 19] v3 segment location for segment: airlineStats_batch_2014-01-20_2014-01-20 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20/v3
2020/08/20 13:29:52.558 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 19] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20
2020/08/20 13:29:52.561 INFO [CrcUtils] [Executor task launch worker for task 18] Computed crc = 739722361, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19/v3/metadata.properties]
2020/08/20 13:29:52.562 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Driver, record read time : 9
2020/08/20 13:29:52.562 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Driver, stats collector time : 0
2020/08/20 13:29:52.562 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 18] Driver, indexing time : 7
2020/08/20 13:29:52.562 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 18] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19.tar.gz
2020/08/20 13:29:52.573 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 18] Size for segment: airlineStats_batch_2014-01-19_2014-01-19, uncompressed: 110.02K, compressed: 30.42K
2020/08/20 13:29:52.573 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 18] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_batch_2014-01-19_2014-01-19.tar.gz]
2020/08/20 13:29:52.573 INFO [S3PinotFS] [Executor task launch worker for task 18] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-423c39a0-0ce1-4ed6-bd64-11b52744f8d6/output/airlineStats_batch_2014-01-19_2014-01-19.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_batch_2014-01-19_2014-01-19.tar.gz
2020/08/20 13:29:52.595 INFO [CrcUtils] [Executor task launch worker for task 19] Computed crc = 1605417079, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20/v3/metadata.properties]
2020/08/20 13:29:52.595 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Driver, record read time : 11
2020/08/20 13:29:52.596 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Driver, stats collector time : 0
2020/08/20 13:29:52.596 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 19] Driver, indexing time : 7
2020/08/20 13:29:52.596 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 19] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20.tar.gz
2020/08/20 13:29:52.606 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 19] Size for segment: airlineStats_batch_2014-01-20_2014-01-20, uncompressed: 112.48K, compressed: 31.96K
2020/08/20 13:29:52.606 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 19] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_batch_2014-01-20_2014-01-20.tar.gz]
2020/08/20 13:29:52.606 INFO [S3PinotFS] [Executor task launch worker for task 19] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-6f57209b-2b91-4165-9c52-5bec4f001056/output/airlineStats_batch_2014-01-20_2014-01-20.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_batch_2014-01-20_2014-01-20.tar.gz
2020/08/20 13:29:53.072 INFO [Executor] [Executor task launch worker for task 19] Finished task 19.0 in stage 0.0 (TID 19). 751 bytes result sent to driver
2020/08/20 13:29:53.073 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 20.0 in stage 0.0 (TID 20, localhost, executor driver, partition 20, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:53.074 INFO [Executor] [Executor task launch worker for task 20] Running task 20.0 in stage 0.0 (TID 20)
2020/08/20 13:29:53.074 INFO [TaskSetManager] [task-result-getter-2] Finished task 19.0 in stage 0.0 (TID 19) in 2523 ms on localhost (executor driver) (19/31)
2020/08/20 13:29:53.075 INFO [PinotFSFactory] [Executor task launch worker for task 20] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:53.076 WARN [HadoopPinotFS] [Executor task launch worker for task 20] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:53.091 INFO [HadoopPinotFS] [Executor task launch worker for task 20] successfully initialized HadoopPinotFS
2020/08/20 13:29:53.091 INFO [PinotFSFactory] [Executor task launch worker for task 20] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:53.200 INFO [Executor] [Executor task launch worker for task 18] Finished task 18.0 in stage 0.0 (TID 18). 665 bytes result sent to driver
2020/08/20 13:29:53.201 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 21.0 in stage 0.0 (TID 21, localhost, executor driver, partition 21, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:53.202 INFO [TaskSetManager] [task-result-getter-3] Finished task 18.0 in stage 0.0 (TID 18) in 2722 ms on localhost (executor driver) (20/31)
2020/08/20 13:29:53.202 INFO [Executor] [Executor task launch worker for task 21] Running task 21.0 in stage 0.0 (TID 21)
2020/08/20 13:29:53.206 INFO [PinotFSFactory] [Executor task launch worker for task 21] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:53.207 WARN [HadoopPinotFS] [Executor task launch worker for task 21] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:53.224 INFO [HadoopPinotFS] [Executor task launch worker for task 21] successfully initialized HadoopPinotFS
2020/08/20 13:29:53.225 INFO [PinotFSFactory] [Executor task launch worker for task 21] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:54.642 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 20] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-20]
2020/08/20 13:29:54.642 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 20] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-20], plugins includes [null]
2020/08/20 13:29:54.643 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 20] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/21/airlineStats_data_2014-01-21.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/input/airlineStats_data_2014-01-21.avro
2020/08/20 13:29:54.644 INFO [S3PinotFS] [Executor task launch worker for task 20] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/21/airlineStats_data_2014-01-21.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/input/airlineStats_data_2014-01-21.avro
2020/08/20 13:29:54.768 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 21] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-21]
2020/08/20 13:29:54.768 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 21] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-21], plugins includes [null]
2020/08/20 13:29:54.769 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 21] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/22/airlineStats_data_2014-01-22.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/input/airlineStats_data_2014-01-22.avro
2020/08/20 13:29:54.769 INFO [S3PinotFS] [Executor task launch worker for task 21] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/22/airlineStats_data_2014-01-22.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/input/airlineStats_data_2014-01-22.avro
2020/08/20 13:29:54.960 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:54.979 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Finished building StatsCollector!
2020/08/20 13:29:54.979 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Collected stats for 305 documents
2020/08/20 13:29:54.980 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: FlightNum with cardinality: 301, range: 3 to 7423
2020/08/20 13:29:54.981 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: Origin, size: 270
2020/08/20 13:29:54.981 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: Origin with cardinality: 90, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:29:54.982 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:54.982 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: LateAircraftDelay with cardinality: 22, range: -2147483648 to 78
2020/08/20 13:29:54.983 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivActualElapsedTime with cardinality: 25, range: -2147483648 to 1331
2020/08/20 13:29:54.984 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivWheelsOns with cardinality: 59, range: -2147483648 to 2247
2020/08/20 13:29:54.985 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivWheelsOffs with cardinality: 28, range: -2147483648 to 2326
2020/08/20 13:29:54.986 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: AirTime with cardinality: 131, range: -2147483648 to 416
2020/08/20 13:29:54.987 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:54.989 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivTotalGTimes with cardinality: 39, range: -2147483648 to 182
2020/08/20 13:29:54.990 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:29:54.990 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:29:54.991 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DestCityMarketID with cardinality: 83, range: 30194 to 35389
2020/08/20 13:29:54.992 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 37, range: -2147483648 to 1532302
2020/08/20 13:29:54.993 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16091 to 16091
2020/08/20 13:29:54.994 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DepTime with cardinality: 238, range: -2147483648 to 2250
2020/08/20 13:29:54.995 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:54.997 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: CRSElapsedTime with cardinality: 149, range: 39 to 440
2020/08/20 13:29:54.998 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: DestStateName, size: 588
2020/08/20 13:29:54.998 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:29:54.999 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: Carrier, size: 26
2020/08/20 13:29:54.999 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: Carrier with cardinality: 13, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:55.000 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DestAirportID with cardinality: 96, range: 10299 to 15919
2020/08/20 13:29:55.001 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: Distance with cardinality: 251, range: 67 to 3784
2020/08/20 13:29:55.002 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:55.002 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:55.003 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivArrDelay with cardinality: 26, range: -2147483648 to 979
2020/08/20 13:29:55.004 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:55.006 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: LongestAddGTime with cardinality: 5, range: -2147483648 to 96
2020/08/20 13:29:55.007 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: OriginWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:55.009 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: WheelsOff with cardinality: 241, range: -2147483648 to 2302
2020/08/20 13:29:55.010 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DestAirportSeqID with cardinality: 96, range: 1029904 to 1591902
2020/08/20 13:29:55.010 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: UniqueCarrier, size: 26
2020/08/20 13:29:55.011 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: UniqueCarrier with cardinality: 13, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:55.011 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:55.012 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:55.013 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: ActualElapsedTime with cardinality: 136, range: -2147483648 to 435
2020/08/20 13:29:55.014 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: AirlineID with cardinality: 13, range: 19393 to 21171
2020/08/20 13:29:55.015 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: OriginStateName, size: 798
2020/08/20 13:29:55.015 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: OriginStateName with cardinality: 42, max length in bytes: 19, range: Alabama to Wisconsin
2020/08/20 13:29:55.016 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:55.017 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:55.018 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:55.018 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-21 to 2014-01-21
2020/08/20 13:29:55.019 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: OriginCityName, size: 1978
2020/08/20 13:29:55.019 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: OriginCityName with cardinality: 86, max length in bytes: 23, range: Albuquerque, NM to White Plains, NY
2020/08/20 13:29:55.020 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: OriginStateFips with cardinality: 42, range: 1 to 78
2020/08/20 13:29:55.021 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: OriginState, size: 84
2020/08/20 13:29:55.021 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: OriginState with cardinality: 42, max length in bytes: 2, range: AK to WI
2020/08/20 13:29:55.022 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:55.024 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: WeatherDelay with cardinality: 7, range: -2147483648 to 103
2020/08/20 13:29:55.025 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:29:55.026 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: WheelsOn with cardinality: 218, range: -2147483648 to 2340
2020/08/20 13:29:55.027 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: OriginAirportID with cardinality: 90, range: 10140 to 15919
2020/08/20 13:29:55.028 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: OriginCityMarketID with cardinality: 75, range: 30140 to 34945
2020/08/20 13:29:55.028 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: NASDelay with cardinality: 24, range: -2147483648 to 92
2020/08/20 13:29:55.029 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: ArrTime with cardinality: 222, range: -2147483648 to 2346
2020/08/20 13:29:55.030 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:29:55.031 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WV
2020/08/20 13:29:55.033 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:55.034 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:55.035 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 21 to 21
2020/08/20 13:29:55.035 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: RandomAirports, size: 272
2020/08/20 13:29:55.036 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: RandomAirports with cardinality: 68, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:55.037 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: TotalAddGTime with cardinality: 5, range: -2147483648 to 96
2020/08/20 13:29:55.039 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: CRSDepTime with cardinality: 202, range: 35 to 2240
2020/08/20 13:29:55.041 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 2 to 2
2020/08/20 13:29:55.042 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:55.042 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:55.043 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: Dest, size: 288
2020/08/20 13:29:55.043 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: Dest with cardinality: 96, max length in bytes: 3, range: ANC to XNA
2020/08/20 13:29:55.044 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: FirstDepTime with cardinality: 5, range: -2147483648 to 1119
2020/08/20 13:29:55.045 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: DivTailNums, size: 174
2020/08/20 13:29:55.045 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: DivTailNums with cardinality: 29, max length in bytes: 6, range: N12967 to null
2020/08/20 13:29:55.046 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DepDelayMinutes with cardinality: 62, range: -2147483648 to 290
2020/08/20 13:29:55.047 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DepDelay with cardinality: 79, range: -2147483648 to 290
2020/08/20 13:29:55.048 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: TaxiIn with cardinality: 22, range: -2147483648 to 29
2020/08/20 13:29:55.049 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: OriginAirportSeqID with cardinality: 90, range: 1014002 to 1591902
2020/08/20 13:29:55.050 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 72
2020/08/20 13:29:55.050 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: ArrDelay with cardinality: 76, range: -2147483648 to 332
2020/08/20 13:29:55.051 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:55.052 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivAirportIDs with cardinality: 37, range: -2147483648 to 15323
2020/08/20 13:29:55.053 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: TaxiOut with cardinality: 45, range: -2147483648 to 121
2020/08/20 13:29:55.054 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: CarrierDelay with cardinality: 21, range: -2147483648 to 290
2020/08/20 13:29:55.055 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:55.056 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivLongestGTimes with cardinality: 33, range: -2147483648 to 102
2020/08/20 13:29:55.057 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: DivAirports, size: 148
2020/08/20 13:29:55.057 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: DivAirports with cardinality: 37, max length in bytes: 4, range: ALB to null
2020/08/20 13:29:55.058 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: DivDistance with cardinality: 21, range: -2147483648 to 967
2020/08/20 13:29:55.058 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:55.059 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: ArrDelayMinutes with cardinality: 49, range: -2147483648 to 332
2020/08/20 13:29:55.060 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for INT column: CRSArrTime with cardinality: 238, range: 28 to 2335
2020/08/20 13:29:55.061 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: TailNum, size: 1734
2020/08/20 13:29:55.061 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: TailNum with cardinality: 289, max length in bytes: 6, range: N0EGMQ to null
2020/08/20 13:29:55.062 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Using fixed bytes value dictionary for column: DestCityName, size: 2576
2020/08/20 13:29:55.062 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 20] Created dictionary for STRING column: DestCityName with cardinality: 92, max length in bytes: 28, range: Anchorage, AK to Wichita, KS
2020/08/20 13:29:55.063 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Start building IndexCreator!
2020/08/20 13:29:55.088 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Finished records indexing in IndexCreator!
2020/08/20 13:29:55.097 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:55.113 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Finished segment seal!
2020/08/20 13:29:55.114 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 20] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21 to v3 format
2020/08/20 13:29:55.119 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Finished building StatsCollector!
2020/08/20 13:29:55.119 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Collected stats for 299 documents
2020/08/20 13:29:55.120 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: FlightNum with cardinality: 294, range: 6 to 7381
2020/08/20 13:29:55.121 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: Origin, size: 291
2020/08/20 13:29:55.121 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: Origin with cardinality: 97, max length in bytes: 3, range: ABQ to TYS
2020/08/20 13:29:55.122 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:55.123 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: LateAircraftDelay with cardinality: 28, range: -2147483648 to 255
2020/08/20 13:29:55.124 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivActualElapsedTime with cardinality: 17, range: -2147483648 to 349
2020/08/20 13:29:55.125 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivWheelsOns with cardinality: 31, range: -2147483648 to 2326
2020/08/20 13:29:55.126 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivWheelsOffs with cardinality: 18, range: -2147483648 to 2320
2020/08/20 13:29:55.127 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: AirTime with cardinality: 145, range: -2147483648 to 361
2020/08/20 13:29:55.128 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:55.129 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivTotalGTimes with cardinality: 20, range: -2147483648 to 29
2020/08/20 13:29:55.130 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:55.130 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:55.131 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DestCityMarketID with cardinality: 73, range: 30194 to 34828
2020/08/20 13:29:55.133 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 21, range: -2147483648 to 1486903
2020/08/20 13:29:55.134 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16092 to 16092
2020/08/20 13:29:55.135 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DepTime with cardinality: 245, range: -2147483648 to 2338
2020/08/20 13:29:55.137 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:55.138 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: CRSElapsedTime with cardinality: 142, range: 32 to 395
2020/08/20 13:29:55.139 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: DestStateName, size: 532
2020/08/20 13:29:55.140 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: DestStateName with cardinality: 38, max length in bytes: 14, range: Alaska to Wyoming
2020/08/20 13:29:55.141 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:55.142 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:55.143 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DestAirportID with cardinality: 87, range: 10257 to 15376
2020/08/20 13:29:55.144 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: Distance with cardinality: 234, range: 67 to 2917
2020/08/20 13:29:55.145 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:55.145 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:55.146 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivArrDelay with cardinality: 17, range: -2147483648 to 246
2020/08/20 13:29:55.148 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:55.149 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: LongestAddGTime with cardinality: 2, range: -2147483648 to 26
2020/08/20 13:29:55.150 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: OriginWac with cardinality: 39, range: 1 to 93
2020/08/20 13:29:55.151 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: WheelsOff with cardinality: 248, range: -2147483648 to 2347
2020/08/20 13:29:55.152 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DestAirportSeqID with cardinality: 87, range: 1025702 to 1537602
2020/08/20 13:29:55.153 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:55.154 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:55.155 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:55.156 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:55.157 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: ActualElapsedTime with cardinality: 152, range: -2147483648 to 394
2020/08/20 13:29:55.159 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:55.160 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: OriginStateName, size: 741
2020/08/20 13:29:55.160 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: OriginStateName with cardinality: 39, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:29:55.161 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:55.163 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:55.165 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:55.165 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-22 to 2014-01-22
2020/08/20 13:29:55.168 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: OriginCityName, size: 2790
2020/08/20 13:29:55.169 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: OriginCityName with cardinality: 93, max length in bytes: 30, range: Akron, OH to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:55.173 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: OriginStateFips with cardinality: 39, range: 1 to 78
2020/08/20 13:29:55.175 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: OriginState, size: 78
2020/08/20 13:29:55.176 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: OriginState with cardinality: 39, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:55.178 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:55.179 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: WeatherDelay with cardinality: 8, range: -2147483648 to 71
2020/08/20 13:29:55.181 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DestWac with cardinality: 38, range: 1 to 93
2020/08/20 13:29:55.182 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: WheelsOn with cardinality: 228, range: -2147483648 to 2358
2020/08/20 13:29:55.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: OriginAirportID with cardinality: 97, range: 10140 to 15412
2020/08/20 13:29:55.185 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: OriginCityMarketID with cardinality: 82, range: 30140 to 35412
2020/08/20 13:29:55.186 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: NASDelay with cardinality: 21, range: -2147483648 to 43
2020/08/20 13:29:55.187 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: ArrTime with cardinality: 231, range: -2147483648 to 2347
2020/08/20 13:29:55.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: DestState, size: 76
2020/08/20 13:29:55.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: DestState with cardinality: 38, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:55.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:55.191 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:55.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 22 to 22
2020/08/20 13:29:55.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: RandomAirports, size: 300
2020/08/20 13:29:55.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: RandomAirports with cardinality: 75, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:55.195 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: TotalAddGTime with cardinality: 2, range: -2147483648 to 26
2020/08/20 13:29:55.196 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: CRSDepTime with cardinality: 202, range: 550 to 2345
2020/08/20 13:29:55.198 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 3 to 3
2020/08/20 13:29:55.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:55.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:55.200 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: Dest, size: 261
2020/08/20 13:29:55.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: Dest with cardinality: 87, max length in bytes: 3, range: ALB to TUS
2020/08/20 13:29:55.202 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: FirstDepTime with cardinality: 2, range: -2147483648 to 2009
2020/08/20 13:29:55.203 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: DivTailNums, size: 108
2020/08/20 13:29:55.203 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: DivTailNums with cardinality: 18, max length in bytes: 6, range: N187PQ to null
2020/08/20 13:29:55.205 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DepDelayMinutes with cardinality: 58, range: -2147483648 to 268
2020/08/20 13:29:55.207 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DepDelay with cardinality: 73, range: -2147483648 to 268
2020/08/20 13:29:55.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: TaxiIn with cardinality: 22, range: -2147483648 to 37
2020/08/20 13:29:55.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: OriginAirportSeqID with cardinality: 97, range: 1014002 to 1541202
2020/08/20 13:29:55.214 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DestStateFips with cardinality: 38, range: 2 to 72
2020/08/20 13:29:55.216 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: ArrDelay with cardinality: 79, range: -2147483648 to 255
2020/08/20 13:29:55.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:55.218 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivAirportIDs with cardinality: 21, range: -2147483648 to 14869
2020/08/20 13:29:55.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: TaxiOut with cardinality: 42, range: -2147483648 to 62
2020/08/20 13:29:55.221 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: CarrierDelay with cardinality: 24, range: -2147483648 to 139
2020/08/20 13:29:55.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:55.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivLongestGTimes with cardinality: 17, range: -2147483648 to 26
2020/08/20 13:29:55.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: DivAirports, size: 84
2020/08/20 13:29:55.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: DivAirports with cardinality: 21, max length in bytes: 4, range: ATL to null
2020/08/20 13:29:55.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: DivDistance with cardinality: 10, range: -2147483648 to 829
2020/08/20 13:29:55.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:55.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: ArrDelayMinutes with cardinality: 52, range: -2147483648 to 255
2020/08/20 13:29:55.230 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for INT column: CRSArrTime with cardinality: 230, range: 553 to 2355
2020/08/20 13:29:55.231 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: TailNum, size: 1692
2020/08/20 13:29:55.231 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: TailNum with cardinality: 282, max length in bytes: 6, range: N008AA to null
2020/08/20 13:29:55.233 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Using fixed bytes value dictionary for column: DestCityName, size: 2490
2020/08/20 13:29:55.233 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 21] Created dictionary for STRING column: DestCityName with cardinality: 83, max length in bytes: 30, range: Albany, NY to West Palm Beach/Palm Beach, FL
2020/08/20 13:29:55.234 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Start building IndexCreator!
2020/08/20 13:29:55.265 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Finished records indexing in IndexCreator!
2020/08/20 13:29:55.296 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Finished segment seal!
2020/08/20 13:29:55.297 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 21] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22 to v3 format
2020/08/20 13:29:55.297 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 20] v3 segment location for segment: airlineStats_batch_2014-01-21_2014-01-21 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21/v3
2020/08/20 13:29:55.298 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 20] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21
2020/08/20 13:29:55.352 INFO [CrcUtils] [Executor task launch worker for task 20] Computed crc = 3768493809, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21/v3/metadata.properties]
2020/08/20 13:29:55.354 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Driver, record read time : 17
2020/08/20 13:29:55.354 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Driver, stats collector time : 0
2020/08/20 13:29:55.354 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 20] Driver, indexing time : 7
2020/08/20 13:29:55.354 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 20] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21.tar.gz
2020/08/20 13:29:55.369 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 20] Size for segment: airlineStats_batch_2014-01-21_2014-01-21, uncompressed: 114.67K, compressed: 33.79K
2020/08/20 13:29:55.369 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 20] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_batch_2014-01-21_2014-01-21.tar.gz]
2020/08/20 13:29:55.369 INFO [S3PinotFS] [Executor task launch worker for task 20] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-5e7c2480-c3be-44b4-aeac-aece625c3722/output/airlineStats_batch_2014-01-21_2014-01-21.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_batch_2014-01-21_2014-01-21.tar.gz
2020/08/20 13:29:55.506 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 21] v3 segment location for segment: airlineStats_batch_2014-01-22_2014-01-22 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22/v3
2020/08/20 13:29:55.507 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 21] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22
2020/08/20 13:29:55.568 INFO [CrcUtils] [Executor task launch worker for task 21] Computed crc = 1631232385, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22/v3/metadata.properties]
2020/08/20 13:29:55.569 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Driver, record read time : 17
2020/08/20 13:29:55.569 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Driver, stats collector time : 0
2020/08/20 13:29:55.569 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 21] Driver, indexing time : 14
2020/08/20 13:29:55.569 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 21] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22.tar.gz
2020/08/20 13:29:55.583 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 21] Size for segment: airlineStats_batch_2014-01-22_2014-01-22, uncompressed: 113.13K, compressed: 32.63K
2020/08/20 13:29:55.583 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 21] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_batch_2014-01-22_2014-01-22.tar.gz]
2020/08/20 13:29:55.584 INFO [S3PinotFS] [Executor task launch worker for task 21] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-81949bdc-6d37-4e93-a419-6e86bf516b8f/output/airlineStats_batch_2014-01-22_2014-01-22.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_batch_2014-01-22_2014-01-22.tar.gz
2020/08/20 13:29:55.982 INFO [Executor] [Executor task launch worker for task 21] Finished task 21.0 in stage 0.0 (TID 21). 751 bytes result sent to driver
2020/08/20 13:29:55.983 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 22.0 in stage 0.0 (TID 22, localhost, executor driver, partition 22, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:55.983 INFO [Executor] [Executor task launch worker for task 22] Running task 22.0 in stage 0.0 (TID 22)
2020/08/20 13:29:55.983 INFO [TaskSetManager] [task-result-getter-0] Finished task 21.0 in stage 0.0 (TID 21) in 2782 ms on localhost (executor driver) (21/31)
2020/08/20 13:29:55.986 INFO [PinotFSFactory] [Executor task launch worker for task 22] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:55.986 WARN [HadoopPinotFS] [Executor task launch worker for task 22] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:56.009 INFO [HadoopPinotFS] [Executor task launch worker for task 22] successfully initialized HadoopPinotFS
2020/08/20 13:29:56.010 INFO [PinotFSFactory] [Executor task launch worker for task 22] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:56.079 INFO [Executor] [Executor task launch worker for task 20] Finished task 20.0 in stage 0.0 (TID 20). 708 bytes result sent to driver
2020/08/20 13:29:56.080 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 23.0 in stage 0.0 (TID 23, localhost, executor driver, partition 23, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:56.080 INFO [Executor] [Executor task launch worker for task 23] Running task 23.0 in stage 0.0 (TID 23)
2020/08/20 13:29:56.080 INFO [TaskSetManager] [task-result-getter-1] Finished task 20.0 in stage 0.0 (TID 20) in 3007 ms on localhost (executor driver) (22/31)
2020/08/20 13:29:56.082 INFO [PinotFSFactory] [Executor task launch worker for task 23] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:56.082 WARN [HadoopPinotFS] [Executor task launch worker for task 23] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:56.100 INFO [HadoopPinotFS] [Executor task launch worker for task 23] successfully initialized HadoopPinotFS
2020/08/20 13:29:56.100 INFO [PinotFSFactory] [Executor task launch worker for task 23] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:57.685 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 22] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-22]
2020/08/20 13:29:57.685 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 22] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-22], plugins includes [null]
2020/08/20 13:29:57.686 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 23] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-23]
2020/08/20 13:29:57.686 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 23] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-23], plugins includes [null]
2020/08/20 13:29:57.686 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 22] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/23/airlineStats_data_2014-01-23.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/input/airlineStats_data_2014-01-23.avro
2020/08/20 13:29:57.686 INFO [S3PinotFS] [Executor task launch worker for task 22] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/23/airlineStats_data_2014-01-23.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/input/airlineStats_data_2014-01-23.avro
2020/08/20 13:29:57.687 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 23] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/24/airlineStats_data_2014-01-24.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/input/airlineStats_data_2014-01-24.avro
2020/08/20 13:29:57.687 INFO [S3PinotFS] [Executor task launch worker for task 23] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/24/airlineStats_data_2014-01-24.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/input/airlineStats_data_2014-01-24.avro
2020/08/20 13:29:58.088 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:58.116 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Finished building StatsCollector!
2020/08/20 13:29:58.116 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Collected stats for 317 documents
2020/08/20 13:29:58.117 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: FlightNum with cardinality: 313, range: 2 to 7429
2020/08/20 13:29:58.118 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: Origin, size: 291
2020/08/20 13:29:58.118 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: Origin with cardinality: 97, max length in bytes: 3, range: AMA to YUM
2020/08/20 13:29:58.120 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:58.121 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: LateAircraftDelay with cardinality: 30, range: -2147483648 to 110
2020/08/20 13:29:58.122 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivActualElapsedTime with cardinality: 15, range: -2147483648 to 345
2020/08/20 13:29:58.123 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivWheelsOns with cardinality: 28, range: -2147483648 to 2335
2020/08/20 13:29:58.125 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivWheelsOffs with cardinality: 16, range: -2147483648 to 2334
2020/08/20 13:29:58.126 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: AirTime with cardinality: 159, range: -2147483648 to 342
2020/08/20 13:29:58.127 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:58.128 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivTotalGTimes with cardinality: 20, range: -2147483648 to 78
2020/08/20 13:29:58.129 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:58.129 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:58.131 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DestCityMarketID with cardinality: 83, range: 30070 to 35389
2020/08/20 13:29:58.132 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:29:58.132 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 20, range: -2147483648 to 1486903
2020/08/20 13:29:58.133 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16093 to 16093
2020/08/20 13:29:58.134 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DepTime with cardinality: 268, range: -2147483648 to 2339
2020/08/20 13:29:58.135 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:58.136 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: CRSElapsedTime with cardinality: 156, range: 32 to 390
2020/08/20 13:29:58.137 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: DestStateName, size: 741
2020/08/20 13:29:58.137 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: DestStateName with cardinality: 39, max length in bytes: 19, range: Alaska to Wyoming
2020/08/20 13:29:58.140 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:58.140 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:58.142 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DestAirportID with cardinality: 96, range: 10170 to 15389
2020/08/20 13:29:58.143 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: Distance with cardinality: 249, range: 67 to 2917
2020/08/20 13:29:58.144 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:58.144 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:58.145 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivArrDelay with cardinality: 16, range: -2147483648 to 246
2020/08/20 13:29:58.146 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:58.147 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: LongestAddGTime with cardinality: 2, range: -2147483648 to 45
2020/08/20 13:29:58.148 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: OriginWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:58.149 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: WheelsOff with cardinality: 271, range: -2147483648 to 2348
2020/08/20 13:29:58.149 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DestAirportSeqID with cardinality: 96, range: 1017001 to 1538902
2020/08/20 13:29:58.150 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:58.150 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:58.152 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:58.152 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:58.153 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: ActualElapsedTime with cardinality: 163, range: -2147483648 to 382
2020/08/20 13:29:58.156 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:58.157 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: OriginStateName, size: 574
2020/08/20 13:29:58.157 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: OriginStateName with cardinality: 41, max length in bytes: 14, range: Alaska to Wyoming
2020/08/20 13:29:58.158 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Finished building StatsCollector!
2020/08/20 13:29:58.158 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Collected stats for 343 documents
2020/08/20 13:29:58.158 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:58.159 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: FlightNum with cardinality: 334, range: 1 to 7416
2020/08/20 13:29:58.160 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:29:58.161 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: Origin, size: 297
2020/08/20 13:29:58.161 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:58.161 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: Origin with cardinality: 99, max length in bytes: 3, range: ABQ to YAK
2020/08/20 13:29:58.161 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-23 to 2014-01-23
2020/08/20 13:29:58.162 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:29:58.173 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: OriginCityName, size: 2790
2020/08/20 13:29:58.173 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: LateAircraftDelay with cardinality: 34, range: -2147483648 to 121
2020/08/20 13:29:58.173 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: OriginCityName with cardinality: 93, max length in bytes: 30, range: Aguadilla, PR to Yuma, AZ
2020/08/20 13:29:58.175 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivActualElapsedTime with cardinality: 33, range: -2147483648 to 667
2020/08/20 13:29:58.175 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: OriginStateFips with cardinality: 41, range: 2 to 72
2020/08/20 13:29:58.176 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: OriginState, size: 82
2020/08/20 13:29:58.176 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivWheelsOns with cardinality: 80, range: -2147483648 to 2340
2020/08/20 13:29:58.177 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: OriginState with cardinality: 41, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:58.177 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivWheelsOffs with cardinality: 39, range: -2147483648 to 2358
2020/08/20 13:29:58.177 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:58.179 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: WeatherDelay with cardinality: 9, range: -2147483648 to 71
2020/08/20 13:29:58.179 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: AirTime with cardinality: 145, range: -2147483648 to 418
2020/08/20 13:29:58.180 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:58.180 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DestWac with cardinality: 39, range: 1 to 93
2020/08/20 13:29:58.181 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivTotalGTimes with cardinality: 38, range: -2147483648 to 100
2020/08/20 13:29:58.181 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: WheelsOn with cardinality: 265, range: -2147483648 to 2359
2020/08/20 13:29:58.181 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:29:58.182 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:58.182 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: OriginAirportID with cardinality: 97, range: 10279 to 16218
2020/08/20 13:29:58.183 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DestCityMarketID with cardinality: 87, range: 30140 to 35411
2020/08/20 13:29:58.183 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: OriginCityMarketID with cardinality: 82, range: 30107 to 35412
2020/08/20 13:29:58.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 44, range: -2147483648 to 1537602
2020/08/20 13:29:58.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: NASDelay with cardinality: 28, range: -2147483648 to 46
2020/08/20 13:29:58.185 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16094 to 16094
2020/08/20 13:29:58.185 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: ArrTime with cardinality: 251, range: -2147483648 to 2359
2020/08/20 13:29:58.186 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: DestState, size: 78
2020/08/20 13:29:58.186 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: DestState with cardinality: 39, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:58.186 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DepTime with cardinality: 279, range: -2147483648 to 2325
2020/08/20 13:29:58.187 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:29:58.187 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:29:58.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: CRSElapsedTime with cardinality: 150, range: 31 to 455
2020/08/20 13:29:58.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:58.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 23 to 23
2020/08/20 13:29:58.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: DestStateName, size: 574
2020/08/20 13:29:58.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: DestStateName with cardinality: 41, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:29:58.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: RandomAirports, size: 268
2020/08/20 13:29:58.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:29:58.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: RandomAirports with cardinality: 67, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:58.191 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:58.191 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: TotalAddGTime with cardinality: 2, range: -2147483648 to 45
2020/08/20 13:29:58.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DestAirportID with cardinality: 99, range: 10140 to 15411
2020/08/20 13:29:58.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: Distance with cardinality: 267, range: 67 to 3365
2020/08/20 13:29:58.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: CRSDepTime with cardinality: 207, range: 417 to 2330
2020/08/20 13:29:58.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:29:58.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 4 to 4
2020/08/20 13:29:58.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:29:58.195 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:58.197 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:58.198 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivArrDelay with cardinality: 37, range: -2147483648 to 330
2020/08/20 13:29:58.198 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: Dest, size: 288
2020/08/20 13:29:58.198 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: Dest with cardinality: 96, max length in bytes: 3, range: ADQ to TWF
2020/08/20 13:29:58.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:29:58.199 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: FirstDepTime with cardinality: 2, range: -2147483648 to 814
2020/08/20 13:29:58.200 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: LongestAddGTime with cardinality: 5, range: -2147483648 to 60
2020/08/20 13:29:58.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: DivTailNums, size: 96
2020/08/20 13:29:58.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: DivTailNums with cardinality: 16, max length in bytes: 6, range: N13949 to null
2020/08/20 13:29:58.201 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: OriginWac with cardinality: 44, range: 1 to 93
2020/08/20 13:29:58.202 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DepDelayMinutes with cardinality: 60, range: -2147483648 to 419
2020/08/20 13:29:58.203 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: WheelsOff with cardinality: 283, range: -2147483648 to 2339
2020/08/20 13:29:58.204 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DepDelay with cardinality: 74, range: -2147483648 to 419
2020/08/20 13:29:58.204 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DestAirportSeqID with cardinality: 99, range: 1014002 to 1541103
2020/08/20 13:29:58.206 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: TaxiIn with cardinality: 28, range: -2147483648 to 55
2020/08/20 13:29:58.206 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:29:58.207 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:29:58.208 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: OriginAirportSeqID with cardinality: 97, range: 1027903 to 1621801
2020/08/20 13:29:58.208 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:58.210 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DestStateFips with cardinality: 39, range: 2 to 78
2020/08/20 13:29:58.210 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:29:58.211 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: ArrDelay with cardinality: 88, range: -2147483648 to 418
2020/08/20 13:29:58.211 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: ActualElapsedTime with cardinality: 149, range: -2147483648 to 444
2020/08/20 13:29:58.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:58.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:29:58.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: OriginStateName, size: 616
2020/08/20 13:29:58.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivAirportIDs with cardinality: 20, range: -2147483648 to 14869
2020/08/20 13:29:58.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: OriginStateName with cardinality: 44, max length in bytes: 14, range: Alaska to Wyoming
2020/08/20 13:29:58.215 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:29:58.215 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: TaxiOut with cardinality: 40, range: -2147483648 to 68
2020/08/20 13:29:58.216 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: CarrierDelay with cardinality: 26, range: -2147483648 to 375
2020/08/20 13:29:58.216 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:29:58.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:29:58.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-24 to 2014-01-24
2020/08/20 13:29:58.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:58.218 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: OriginCityName, size: 3230
2020/08/20 13:29:58.219 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: OriginCityName with cardinality: 95, max length in bytes: 34, range: Albuquerque, NM to Yakutat, AK
2020/08/20 13:29:58.219 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivLongestGTimes with cardinality: 16, range: -2147483648 to 78
2020/08/20 13:29:58.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: DivAirports, size: 80
2020/08/20 13:29:58.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: DivAirports with cardinality: 20, max length in bytes: 4, range: ANC to null
2020/08/20 13:29:58.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: OriginStateFips with cardinality: 44, range: 2 to 72
2020/08/20 13:29:58.221 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: DivDistance with cardinality: 6, range: -2147483648 to 261
2020/08/20 13:29:58.221 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: OriginState, size: 88
2020/08/20 13:29:58.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: OriginState with cardinality: 44, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:58.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:58.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:29:58.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: ArrDelayMinutes with cardinality: 60, range: -2147483648 to 418
2020/08/20 13:29:58.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: WeatherDelay with cardinality: 9, range: -2147483648 to 166
2020/08/20 13:29:58.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for INT column: CRSArrTime with cardinality: 253, range: 10 to 2359
2020/08/20 13:29:58.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DestWac with cardinality: 41, range: 1 to 93
2020/08/20 13:29:58.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: TailNum, size: 1812
2020/08/20 13:29:58.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: TailNum with cardinality: 302, max length in bytes: 6, range: D942DN to N993DL
2020/08/20 13:29:58.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: WheelsOn with cardinality: 252, range: -2147483648 to 2344
2020/08/20 13:29:58.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Using fixed bytes value dictionary for column: DestCityName, size: 2760
2020/08/20 13:29:58.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 22] Created dictionary for STRING column: DestCityName with cardinality: 92, max length in bytes: 30, range: Alexandria, LA to Wichita, KS
2020/08/20 13:29:58.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: OriginAirportID with cardinality: 99, range: 10140 to 15991
2020/08/20 13:29:58.229 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Start building IndexCreator!
2020/08/20 13:29:58.229 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: OriginCityMarketID with cardinality: 84, range: 30140 to 35991
2020/08/20 13:29:58.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: NASDelay with cardinality: 19, range: -2147483648 to 82
2020/08/20 13:29:58.274 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: ArrTime with cardinality: 252, range: -2147483648 to 2350
2020/08/20 13:29:58.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: DestState, size: 82
2020/08/20 13:29:58.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: DestState with cardinality: 41, max length in bytes: 2, range: AK to WY
2020/08/20 13:29:58.276 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 11
2020/08/20 13:29:58.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:29:58.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 24 to 24
2020/08/20 13:29:58.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: RandomAirports, size: 328
2020/08/20 13:29:58.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: RandomAirports with cardinality: 82, max length in bytes: 4, range: ABI to null
2020/08/20 13:29:58.281 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: TotalAddGTime with cardinality: 5, range: -2147483648 to 60
2020/08/20 13:29:58.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: CRSDepTime with cardinality: 209, range: 35 to 2330
2020/08/20 13:29:58.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 5 to 5
2020/08/20 13:29:58.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:29:58.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:29:58.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: Dest, size: 297
2020/08/20 13:29:58.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: Dest with cardinality: 99, max length in bytes: 3, range: ABQ to TYR
2020/08/20 13:29:58.286 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: FirstDepTime with cardinality: 5, range: -2147483648 to 2031
2020/08/20 13:29:58.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: DivTailNums, size: 252
2020/08/20 13:29:58.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: DivTailNums with cardinality: 42, max length in bytes: 6, range: N14148 to null
2020/08/20 13:29:58.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DepDelayMinutes with cardinality: 77, range: -2147483648 to 580
2020/08/20 13:29:58.290 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DepDelay with cardinality: 91, range: -2147483648 to 580
2020/08/20 13:29:58.291 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: TaxiIn with cardinality: 25, range: -2147483648 to 41
2020/08/20 13:29:58.292 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: OriginAirportSeqID with cardinality: 99, range: 1014002 to 1599102
2020/08/20 13:29:58.293 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DestStateFips with cardinality: 41, range: 1 to 72
2020/08/20 13:29:58.294 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: ArrDelay with cardinality: 93, range: -2147483648 to 166
2020/08/20 13:29:58.295 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:29:58.295 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Finished records indexing in IndexCreator!
2020/08/20 13:29:58.296 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivAirportIDs with cardinality: 44, range: -2147483648 to 15376
2020/08/20 13:29:58.297 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: TaxiOut with cardinality: 40, range: -2147483648 to 85
2020/08/20 13:29:58.298 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: CarrierDelay with cardinality: 24, range: -2147483648 to 112
2020/08/20 13:29:58.299 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:29:58.309 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivLongestGTimes with cardinality: 32, range: -2147483648 to 74
2020/08/20 13:29:58.310 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: DivAirports, size: 176
2020/08/20 13:29:58.310 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: DivAirports with cardinality: 44, max length in bytes: 4, range: ABQ to null
2020/08/20 13:29:58.311 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: DivDistance with cardinality: 25, range: -2147483648 to 1300
2020/08/20 13:29:58.313 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:29:58.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: ArrDelayMinutes with cardinality: 60, range: -2147483648 to 166
2020/08/20 13:29:58.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for INT column: CRSArrTime with cardinality: 253, range: 550 to 2359
2020/08/20 13:29:58.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: TailNum, size: 1980
2020/08/20 13:29:58.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: TailNum with cardinality: 330, max length in bytes: 6, range: N11165 to N987AT
2020/08/20 13:29:58.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Using fixed bytes value dictionary for column: DestCityName, size: 2850
2020/08/20 13:29:58.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 23] Created dictionary for STRING column: DestCityName with cardinality: 95, max length in bytes: 30, range: Albany, NY to Wilmington, DE
2020/08/20 13:29:58.320 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Finished segment seal!
2020/08/20 13:29:58.322 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 22] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23 to v3 format
2020/08/20 13:29:58.322 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Start building IndexCreator!
2020/08/20 13:29:58.349 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Finished records indexing in IndexCreator!
2020/08/20 13:29:58.373 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Finished segment seal!
2020/08/20 13:29:58.374 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 23] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24 to v3 format
2020/08/20 13:29:58.462 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 22] v3 segment location for segment: airlineStats_batch_2014-01-23_2014-01-23 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23/v3
2020/08/20 13:29:58.463 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 22] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23
2020/08/20 13:29:58.507 INFO [CrcUtils] [Executor task launch worker for task 22] Computed crc = 1584405507, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23/v3/metadata.properties]
2020/08/20 13:29:58.507 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Driver, record read time : 17
2020/08/20 13:29:58.507 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Driver, stats collector time : 0
2020/08/20 13:29:58.508 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 22] Driver, indexing time : 6
2020/08/20 13:29:58.508 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 22] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23.tar.gz
2020/08/20 13:29:58.513 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 23] v3 segment location for segment: airlineStats_batch_2014-01-24_2014-01-24 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24/v3
2020/08/20 13:29:58.513 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 23] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24
2020/08/20 13:29:58.520 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 22] Size for segment: airlineStats_batch_2014-01-23_2014-01-23, uncompressed: 116.25K, compressed: 34.06K
2020/08/20 13:29:58.520 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 22] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_batch_2014-01-23_2014-01-23.tar.gz]
2020/08/20 13:29:58.520 INFO [S3PinotFS] [Executor task launch worker for task 22] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-b588c5ca-1115-438d-9d36-7e856ae2db3b/output/airlineStats_batch_2014-01-23_2014-01-23.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_batch_2014-01-23_2014-01-23.tar.gz
2020/08/20 13:29:58.551 INFO [CrcUtils] [Executor task launch worker for task 23] Computed crc = 3348207036, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24/v3/metadata.properties]
2020/08/20 13:29:58.551 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Driver, record read time : 24
2020/08/20 13:29:58.552 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Driver, stats collector time : 0
2020/08/20 13:29:58.552 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 23] Driver, indexing time : 3
2020/08/20 13:29:58.552 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 23] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24.tar.gz
2020/08/20 13:29:58.562 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 23] Size for segment: airlineStats_batch_2014-01-24_2014-01-24, uncompressed: 120.85K, compressed: 36.67K
2020/08/20 13:29:58.563 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 23] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_batch_2014-01-24_2014-01-24.tar.gz]
2020/08/20 13:29:58.563 INFO [S3PinotFS] [Executor task launch worker for task 23] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-13e438a1-7856-4679-9915-3a0f35f082ea/output/airlineStats_batch_2014-01-24_2014-01-24.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_batch_2014-01-24_2014-01-24.tar.gz
2020/08/20 13:29:59.280 INFO [Executor] [Executor task launch worker for task 23] Finished task 23.0 in stage 0.0 (TID 23). 708 bytes result sent to driver
2020/08/20 13:29:59.281 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 24.0 in stage 0.0 (TID 24, localhost, executor driver, partition 24, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:59.281 INFO [Executor] [Executor task launch worker for task 24] Running task 24.0 in stage 0.0 (TID 24)
2020/08/20 13:29:59.281 INFO [TaskSetManager] [task-result-getter-2] Finished task 23.0 in stage 0.0 (TID 23) in 3202 ms on localhost (executor driver) (23/31)
2020/08/20 13:29:59.283 INFO [PinotFSFactory] [Executor task launch worker for task 24] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:59.283 WARN [HadoopPinotFS] [Executor task launch worker for task 24] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:59.299 INFO [HadoopPinotFS] [Executor task launch worker for task 24] successfully initialized HadoopPinotFS
2020/08/20 13:29:59.299 INFO [PinotFSFactory] [Executor task launch worker for task 24] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:29:59.662 INFO [Executor] [Executor task launch worker for task 22] Finished task 22.0 in stage 0.0 (TID 22). 708 bytes result sent to driver
2020/08/20 13:29:59.663 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 25.0 in stage 0.0 (TID 25, localhost, executor driver, partition 25, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:29:59.664 INFO [Executor] [Executor task launch worker for task 25] Running task 25.0 in stage 0.0 (TID 25)
2020/08/20 13:29:59.664 INFO [TaskSetManager] [task-result-getter-3] Finished task 22.0 in stage 0.0 (TID 22) in 3681 ms on localhost (executor driver) (24/31)
2020/08/20 13:29:59.666 INFO [PinotFSFactory] [Executor task launch worker for task 25] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:29:59.666 WARN [HadoopPinotFS] [Executor task launch worker for task 25] no hadoop conf path is provided, will rely on default config
2020/08/20 13:29:59.684 INFO [HadoopPinotFS] [Executor task launch worker for task 25] successfully initialized HadoopPinotFS
2020/08/20 13:29:59.684 INFO [PinotFSFactory] [Executor task launch worker for task 25] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:30:00.671 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 24] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-24]
2020/08/20 13:30:00.671 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 24] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-24], plugins includes [null]
2020/08/20 13:30:00.673 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 24] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/25/airlineStats_data_2014-01-25.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/input/airlineStats_data_2014-01-25.avro
2020/08/20 13:30:00.673 INFO [S3PinotFS] [Executor task launch worker for task 24] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/25/airlineStats_data_2014-01-25.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/input/airlineStats_data_2014-01-25.avro
2020/08/20 13:30:00.996 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:30:01.013 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Finished building StatsCollector!
2020/08/20 13:30:01.013 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Collected stats for 228 documents
2020/08/20 13:30:01.014 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: FlightNum with cardinality: 222, range: 4 to 7391
2020/08/20 13:30:01.015 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: Origin, size: 264
2020/08/20 13:30:01.015 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: Origin with cardinality: 88, max length in bytes: 3, range: ABQ to YAK
2020/08/20 13:30:01.016 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:30:01.017 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: LateAircraftDelay with cardinality: 16, range: -2147483648 to 75
2020/08/20 13:30:01.018 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivActualElapsedTime with cardinality: 24, range: -2147483648 to 654
2020/08/20 13:30:01.019 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivWheelsOns with cardinality: 37, range: -2147483648 to 2214
2020/08/20 13:30:01.020 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivWheelsOffs with cardinality: 23, range: -2147483648 to 2334
2020/08/20 13:30:01.022 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: AirTime with cardinality: 117, range: -2147483648 to 402
2020/08/20 13:30:01.023 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:01.024 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivTotalGTimes with cardinality: 26, range: -2147483648 to 63
2020/08/20 13:30:01.025 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:30:01.025 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:01.026 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DestCityMarketID with cardinality: 70, range: 30135 to 34922
2020/08/20 13:30:01.027 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 27, range: -2147483648 to 1599102
2020/08/20 13:30:01.028 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16095 to 16095
2020/08/20 13:30:01.029 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DepTime with cardinality: 197, range: -2147483648 to 2245
2020/08/20 13:30:01.030 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:30:01.031 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: CRSElapsedTime with cardinality: 132, range: 32 to 449
2020/08/20 13:30:01.032 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: DestStateName, size: 504
2020/08/20 13:30:01.032 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: DestStateName with cardinality: 36, max length in bytes: 14, range: Alaska to Washington
2020/08/20 13:30:01.033 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:30:01.033 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:01.034 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DestAirportID with cardinality: 79, range: 10135 to 15304
2020/08/20 13:30:01.035 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: Distance with cardinality: 193, range: 31 to 3711
2020/08/20 13:30:01.036 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:30:01.036 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:01.037 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivArrDelay with cardinality: 23, range: -2147483648 to 274
2020/08/20 13:30:01.039 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:30:01.040 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 97
2020/08/20 13:30:01.041 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: OriginWac with cardinality: 39, range: 1 to 93
2020/08/20 13:30:01.042 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: WheelsOff with cardinality: 205, range: -2147483648 to 2253
2020/08/20 13:30:01.043 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DestAirportSeqID with cardinality: 79, range: 1013503 to 1530402
2020/08/20 13:30:01.044 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:30:01.044 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:01.045 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:01.046 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:30:01.046 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 25] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-25]
2020/08/20 13:30:01.046 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 25] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-25], plugins includes [null]
2020/08/20 13:30:01.047 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: ActualElapsedTime with cardinality: 127, range: -2147483648 to 427
2020/08/20 13:30:01.047 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 25] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/26/airlineStats_data_2014-01-26.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/input/airlineStats_data_2014-01-26.avro
2020/08/20 13:30:01.047 INFO [S3PinotFS] [Executor task launch worker for task 25] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/26/airlineStats_data_2014-01-26.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/input/airlineStats_data_2014-01-26.avro
2020/08/20 13:30:01.047 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:30:01.048 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: OriginStateName, size: 546
2020/08/20 13:30:01.048 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: OriginStateName with cardinality: 39, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:30:01.050 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:30:01.051 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:30:01.052 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:30:01.052 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-25 to 2014-01-25
2020/08/20 13:30:01.053 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: OriginCityName, size: 2436
2020/08/20 13:30:01.053 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: OriginCityName with cardinality: 84, max length in bytes: 29, range: Albuquerque, NM to Yakutat, AK
2020/08/20 13:30:01.054 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: OriginStateFips with cardinality: 39, range: 1 to 72
2020/08/20 13:30:01.054 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: OriginState, size: 78
2020/08/20 13:30:01.055 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: OriginState with cardinality: 39, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:01.059 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:30:01.059 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: WeatherDelay with cardinality: 5, range: -2147483648 to 95
2020/08/20 13:30:01.060 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DestWac with cardinality: 36, range: 1 to 93
2020/08/20 13:30:01.061 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: WheelsOn with cardinality: 191, range: -2147483648 to 2346
2020/08/20 13:30:01.062 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: OriginAirportID with cardinality: 88, range: 10140 to 15991
2020/08/20 13:30:01.063 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: OriginCityMarketID with cardinality: 73, range: 30140 to 35991
2020/08/20 13:30:01.063 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: NASDelay with cardinality: 15, range: -2147483648 to 229
2020/08/20 13:30:01.064 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: ArrTime with cardinality: 190, range: -2147483648 to 2350
2020/08/20 13:30:01.065 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: DestState, size: 72
2020/08/20 13:30:01.065 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: DestState with cardinality: 36, max length in bytes: 2, range: AK to WA
2020/08/20 13:30:01.066 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:30:01.067 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:30:01.068 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 25 to 25
2020/08/20 13:30:01.069 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: RandomAirports, size: 296
2020/08/20 13:30:01.069 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: RandomAirports with cardinality: 74, max length in bytes: 4, range: ABI to null
2020/08/20 13:30:01.071 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 97
2020/08/20 13:30:01.072 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: CRSDepTime with cardinality: 166, range: 30 to 2351
2020/08/20 13:30:01.073 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 6 to 6
2020/08/20 13:30:01.074 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:30:01.075 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:30:01.075 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: Dest, size: 237
2020/08/20 13:30:01.075 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: Dest with cardinality: 79, max length in bytes: 3, range: ABE to TPA
2020/08/20 13:30:01.076 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 2110
2020/08/20 13:30:01.077 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: DivTailNums, size: 144
2020/08/20 13:30:01.077 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: DivTailNums with cardinality: 24, max length in bytes: 6, range: N11548 to null
2020/08/20 13:30:01.078 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DepDelayMinutes with cardinality: 54, range: -2147483648 to 340
2020/08/20 13:30:01.078 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DepDelay with cardinality: 70, range: -2147483648 to 340
2020/08/20 13:30:01.079 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: TaxiIn with cardinality: 22, range: -2147483648 to 50
2020/08/20 13:30:01.080 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: OriginAirportSeqID with cardinality: 88, range: 1014002 to 1599102
2020/08/20 13:30:01.081 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DestStateFips with cardinality: 36, range: 2 to 53
2020/08/20 13:30:01.082 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: ArrDelay with cardinality: 72, range: -2147483648 to 229
2020/08/20 13:30:01.083 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:30:01.084 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivAirportIDs with cardinality: 27, range: -2147483648 to 15991
2020/08/20 13:30:01.084 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: TaxiOut with cardinality: 37, range: -2147483648 to 65
2020/08/20 13:30:01.085 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: CarrierDelay with cardinality: 16, range: -2147483648 to 174
2020/08/20 13:30:01.086 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:01.087 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivLongestGTimes with cardinality: 22, range: -2147483648 to 53
2020/08/20 13:30:01.088 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: DivAirports, size: 108
2020/08/20 13:30:01.088 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: DivAirports with cardinality: 27, max length in bytes: 4, range: ABQ to null
2020/08/20 13:30:01.089 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: DivDistance with cardinality: 8, range: -2147483648 to 909
2020/08/20 13:30:01.090 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:30:01.090 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: ArrDelayMinutes with cardinality: 41, range: -2147483648 to 229
2020/08/20 13:30:01.091 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for INT column: CRSArrTime with cardinality: 192, range: 500 to 2359
2020/08/20 13:30:01.092 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: TailNum, size: 1320
2020/08/20 13:30:01.092 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: TailNum with cardinality: 220, max length in bytes: 6, range: N005AA to N986CA
2020/08/20 13:30:01.093 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Using fixed bytes value dictionary for column: DestCityName, size: 2250
2020/08/20 13:30:01.093 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 24] Created dictionary for STRING column: DestCityName with cardinality: 75, max length in bytes: 30, range: Alexandria, LA to Wichita, KS
2020/08/20 13:30:01.094 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Start building IndexCreator!
2020/08/20 13:30:01.111 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Finished records indexing in IndexCreator!
2020/08/20 13:30:01.128 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Finished segment seal!
2020/08/20 13:30:01.129 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 24] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25 to v3 format
2020/08/20 13:30:01.221 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:30:01.245 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Finished building StatsCollector!
2020/08/20 13:30:01.245 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Collected stats for 319 documents
2020/08/20 13:30:01.246 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: FlightNum with cardinality: 306, range: 3 to 7416
2020/08/20 13:30:01.247 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: Origin, size: 288
2020/08/20 13:30:01.247 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: Origin with cardinality: 96, max length in bytes: 3, range: ACV to YAK
2020/08/20 13:30:01.248 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:30:01.249 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: LateAircraftDelay with cardinality: 31, range: -2147483648 to 327
2020/08/20 13:30:01.250 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivActualElapsedTime with cardinality: 21, range: -2147483648 to 854
2020/08/20 13:30:01.251 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivWheelsOns with cardinality: 40, range: -2147483648 to 2328
2020/08/20 13:30:01.252 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivWheelsOffs with cardinality: 20, range: -2147483648 to 2338
2020/08/20 13:30:01.253 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: AirTime with cardinality: 153, range: -2147483648 to 357
2020/08/20 13:30:01.255 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:01.255 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 24] v3 segment location for segment: airlineStats_batch_2014-01-25_2014-01-25 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25/v3
2020/08/20 13:30:01.256 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivTotalGTimes with cardinality: 24, range: -2147483648 to 116
2020/08/20 13:30:01.256 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 24] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25
2020/08/20 13:30:01.257 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:30:01.257 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0600-0659 to 2300-2359
2020/08/20 13:30:01.258 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DestCityMarketID with cardinality: 99, range: 30070 to 35412
2020/08/20 13:30:01.259 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 28, range: -2147483648 to 1599102
2020/08/20 13:30:01.260 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16096 to 16096
2020/08/20 13:30:01.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DepTime with cardinality: 262, range: -2147483648 to 2347
2020/08/20 13:30:01.262 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:30:01.263 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: CRSElapsedTime with cardinality: 160, range: 35 to 520
2020/08/20 13:30:01.264 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: DestStateName, size: 817
2020/08/20 13:30:01.264 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: DestStateName with cardinality: 43, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:30:01.265 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:30:01.265 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:01.266 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DestAirportID with cardinality: 111, range: 10140 to 16218
2020/08/20 13:30:01.267 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: Distance with cardinality: 264, range: 77 to 3784
2020/08/20 13:30:01.268 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:30:01.268 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:01.269 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivArrDelay with cardinality: 21, range: -2147483648 to 864
2020/08/20 13:30:01.271 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: SecurityDelay with cardinality: 3, range: -2147483648 to 10
2020/08/20 13:30:01.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: LongestAddGTime with cardinality: 4, range: -2147483648 to 31
2020/08/20 13:30:01.274 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: OriginWac with cardinality: 44, range: 1 to 93
2020/08/20 13:30:01.276 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: WheelsOff with cardinality: 264, range: -2147483648 to 2359
2020/08/20 13:30:01.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DestAirportSeqID with cardinality: 111, range: 1014002 to 1621801
2020/08/20 13:30:01.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:30:01.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:01.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:01.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:30:01.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: ActualElapsedTime with cardinality: 158, range: -2147483648 to 403
2020/08/20 13:30:01.281 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:30:01.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: OriginStateName, size: 836
2020/08/20 13:30:01.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: OriginStateName with cardinality: 44, max length in bytes: 19, range: Alabama to Wisconsin
2020/08/20 13:30:01.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DepartureDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:30:01.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:30:01.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:30:01.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-26 to 2014-01-26
2020/08/20 13:30:01.286 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: OriginCityName, size: 2760
2020/08/20 13:30:01.287 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: OriginCityName with cardinality: 92, max length in bytes: 30, range: Akron, OH to Yakutat, AK
2020/08/20 13:30:01.288 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: OriginStateFips with cardinality: 44, range: 1 to 78
2020/08/20 13:30:01.288 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: OriginState, size: 88
2020/08/20 13:30:01.289 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: OriginState with cardinality: 44, max length in bytes: 2, range: AK to WI
2020/08/20 13:30:01.290 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:30:01.290 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: WeatherDelay with cardinality: 8, range: -2147483648 to 54
2020/08/20 13:30:01.291 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DestWac with cardinality: 43, range: 1 to 93
2020/08/20 13:30:01.292 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: WheelsOn with cardinality: 244, range: -2147483648 to 2359
2020/08/20 13:30:01.293 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: OriginAirportID with cardinality: 96, range: 10157 to 15991
2020/08/20 13:30:01.294 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: OriginCityMarketID with cardinality: 80, range: 30157 to 35991
2020/08/20 13:30:01.295 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: NASDelay with cardinality: 25, range: -2147483648 to 74
2020/08/20 13:30:01.296 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: ArrTime with cardinality: 248, range: -2147483648 to 2356
2020/08/20 13:30:01.297 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: DestState, size: 86
2020/08/20 13:30:01.297 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: DestState with cardinality: 43, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:01.298 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:30:01.299 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:30:01.300 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 26 to 26
2020/08/20 13:30:01.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: RandomAirports, size: 308
2020/08/20 13:30:01.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: RandomAirports with cardinality: 77, max length in bytes: 4, range: ABI to null
2020/08/20 13:30:01.303 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: TotalAddGTime with cardinality: 4, range: -2147483648 to 31
2020/08/20 13:30:01.303 INFO [CrcUtils] [Executor task launch worker for task 24] Computed crc = 324435894, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25/v3/metadata.properties]
2020/08/20 13:30:01.303 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Driver, record read time : 11
2020/08/20 13:30:01.304 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Driver, stats collector time : 0
2020/08/20 13:30:01.304 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: CRSDepTime with cardinality: 214, range: 600 to 2352
2020/08/20 13:30:01.314 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 24] Driver, indexing time : 6
2020/08/20 13:30:01.314 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 24] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25.tar.gz
2020/08/20 13:30:01.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 7 to 7
2020/08/20 13:30:01.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:30:01.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:30:01.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: Dest, size: 333
2020/08/20 13:30:01.323 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 24] Size for segment: airlineStats_batch_2014-01-25_2014-01-25, uncompressed: 106.5K, compressed: 28.92K
2020/08/20 13:30:01.332 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 24] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_batch_2014-01-25_2014-01-25.tar.gz]
2020/08/20 13:30:01.332 INFO [S3PinotFS] [Executor task launch worker for task 24] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-59602b56-2b09-400d-9d56-2486c5c04df3/output/airlineStats_batch_2014-01-25_2014-01-25.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_batch_2014-01-25_2014-01-25.tar.gz
2020/08/20 13:30:01.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: Dest with cardinality: 111, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:30:01.333 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: FirstDepTime with cardinality: 4, range: -2147483648 to 2041
2020/08/20 13:30:01.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: DivTailNums, size: 126
2020/08/20 13:30:01.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: DivTailNums with cardinality: 21, max length in bytes: 6, range: N11164 to null
2020/08/20 13:30:01.335 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DepDelayMinutes with cardinality: 68, range: -2147483648 to 333
2020/08/20 13:30:01.336 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DepDelay with cardinality: 81, range: -2147483648 to 333
2020/08/20 13:30:01.338 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: TaxiIn with cardinality: 24, range: -2147483648 to 93
2020/08/20 13:30:01.339 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: OriginAirportSeqID with cardinality: 96, range: 1015703 to 1599102
2020/08/20 13:30:01.340 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DestStateFips with cardinality: 43, range: 1 to 78
2020/08/20 13:30:01.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: ArrDelay with cardinality: 92, range: -2147483648 to 327
2020/08/20 13:30:01.342 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:30:01.343 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivAirportIDs with cardinality: 28, range: -2147483648 to 15991
2020/08/20 13:30:01.344 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: TaxiOut with cardinality: 44, range: -2147483648 to 97
2020/08/20 13:30:01.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: CarrierDelay with cardinality: 23, range: -2147483648 to 268
2020/08/20 13:30:01.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:01.346 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivLongestGTimes with cardinality: 17, range: -2147483648 to 116
2020/08/20 13:30:01.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: DivAirports, size: 112
2020/08/20 13:30:01.381 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: DivAirports with cardinality: 28, max length in bytes: 4, range: ANC to null
2020/08/20 13:30:01.382 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: DivDistance with cardinality: 12, range: -2147483648 to 909
2020/08/20 13:30:01.383 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:30:01.384 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: ArrDelayMinutes with cardinality: 62, range: -2147483648 to 327
2020/08/20 13:30:01.384 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for INT column: CRSArrTime with cardinality: 246, range: 15 to 2358
2020/08/20 13:30:01.385 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: TailNum, size: 1818
2020/08/20 13:30:01.386 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: TailNum with cardinality: 303, max length in bytes: 6, range: N011AA to N999DN
2020/08/20 13:30:01.386 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Using fixed bytes value dictionary for column: DestCityName, size: 3210
2020/08/20 13:30:01.387 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 25] Created dictionary for STRING column: DestCityName with cardinality: 107, max length in bytes: 30, range: Albuquerque, NM to Yuma, AZ
2020/08/20 13:30:01.387 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Start building IndexCreator!
2020/08/20 13:30:01.411 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Finished records indexing in IndexCreator!
2020/08/20 13:30:01.430 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Finished segment seal!
2020/08/20 13:30:01.431 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 25] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26 to v3 format
2020/08/20 13:30:01.551 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 25] v3 segment location for segment: airlineStats_batch_2014-01-26_2014-01-26 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26/v3
2020/08/20 13:30:01.552 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 25] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26
2020/08/20 13:30:01.588 INFO [CrcUtils] [Executor task launch worker for task 25] Computed crc = 3389422994, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26/v3/metadata.properties]
2020/08/20 13:30:01.588 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Driver, record read time : 14
2020/08/20 13:30:01.588 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Driver, stats collector time : 0
2020/08/20 13:30:01.588 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 25] Driver, indexing time : 10
2020/08/20 13:30:01.588 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 25] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26.tar.gz
2020/08/20 13:30:01.599 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 25] Size for segment: airlineStats_batch_2014-01-26_2014-01-26, uncompressed: 118.29K, compressed: 35.17K
2020/08/20 13:30:01.599 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 25] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_batch_2014-01-26_2014-01-26.tar.gz]
2020/08/20 13:30:01.599 INFO [S3PinotFS] [Executor task launch worker for task 25] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-294b6b24-8730-4cb6-8c0f-aa66bd58091e/output/airlineStats_batch_2014-01-26_2014-01-26.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_batch_2014-01-26_2014-01-26.tar.gz
2020/08/20 13:30:01.877 INFO [Executor] [Executor task launch worker for task 24] Finished task 24.0 in stage 0.0 (TID 24). 665 bytes result sent to driver
2020/08/20 13:30:01.878 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 26.0 in stage 0.0 (TID 26, localhost, executor driver, partition 26, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:30:01.878 INFO [Executor] [Executor task launch worker for task 26] Running task 26.0 in stage 0.0 (TID 26)
2020/08/20 13:30:01.879 INFO [TaskSetManager] [task-result-getter-0] Finished task 24.0 in stage 0.0 (TID 24) in 2598 ms on localhost (executor driver) (25/31)
2020/08/20 13:30:01.880 INFO [PinotFSFactory] [Executor task launch worker for task 26] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:30:01.881 WARN [HadoopPinotFS] [Executor task launch worker for task 26] no hadoop conf path is provided, will rely on default config
2020/08/20 13:30:01.896 INFO [HadoopPinotFS] [Executor task launch worker for task 26] successfully initialized HadoopPinotFS
2020/08/20 13:30:01.896 INFO [PinotFSFactory] [Executor task launch worker for task 26] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:30:02.027 INFO [Executor] [Executor task launch worker for task 25] Finished task 25.0 in stage 0.0 (TID 25). 708 bytes result sent to driver
2020/08/20 13:30:02.028 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 27.0 in stage 0.0 (TID 27, localhost, executor driver, partition 27, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:30:02.029 INFO [Executor] [Executor task launch worker for task 27] Running task 27.0 in stage 0.0 (TID 27)
2020/08/20 13:30:02.029 INFO [TaskSetManager] [task-result-getter-1] Finished task 25.0 in stage 0.0 (TID 25) in 2366 ms on localhost (executor driver) (26/31)
2020/08/20 13:30:02.031 INFO [PinotFSFactory] [Executor task launch worker for task 27] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:30:02.032 WARN [HadoopPinotFS] [Executor task launch worker for task 27] no hadoop conf path is provided, will rely on default config
2020/08/20 13:30:02.054 INFO [HadoopPinotFS] [Executor task launch worker for task 27] successfully initialized HadoopPinotFS
2020/08/20 13:30:02.054 INFO [PinotFSFactory] [Executor task launch worker for task 27] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:30:03.895 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 26] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-26]
2020/08/20 13:30:03.895 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 26] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-26], plugins includes [null]
2020/08/20 13:30:03.896 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 26] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/27/airlineStats_data_2014-01-27.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/input/airlineStats_data_2014-01-27.avro
2020/08/20 13:30:03.896 INFO [S3PinotFS] [Executor task launch worker for task 26] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/27/airlineStats_data_2014-01-27.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/input/airlineStats_data_2014-01-27.avro
2020/08/20 13:30:04.064 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 27] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-27]
2020/08/20 13:30:04.064 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 27] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-27], plugins includes [null]
2020/08/20 13:30:04.065 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 27] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/28/airlineStats_data_2014-01-28.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/input/airlineStats_data_2014-01-28.avro
2020/08/20 13:30:04.065 INFO [S3PinotFS] [Executor task launch worker for task 27] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/28/airlineStats_data_2014-01-28.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/input/airlineStats_data_2014-01-28.avro
2020/08/20 13:30:04.256 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:30:04.278 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Finished building StatsCollector!
2020/08/20 13:30:04.278 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Collected stats for 296 documents
2020/08/20 13:30:04.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: FlightNum with cardinality: 291, range: 25 to 7409
2020/08/20 13:30:04.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: Origin, size: 258
2020/08/20 13:30:04.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: Origin with cardinality: 86, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:30:04.281 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:30:04.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: LateAircraftDelay with cardinality: 22, range: -2147483648 to 88
2020/08/20 13:30:04.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivActualElapsedTime with cardinality: 9, range: -2147483648 to 751
2020/08/20 13:30:04.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivWheelsOns with cardinality: 29, range: -2147483648 to 2359
2020/08/20 13:30:04.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivWheelsOffs with cardinality: 11, range: -2147483648 to 2243
2020/08/20 13:30:04.285 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: AirTime with cardinality: 158, range: -2147483648 to 379
2020/08/20 13:30:04.286 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:04.294 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivTotalGTimes with cardinality: 21, range: -2147483648 to 56
2020/08/20 13:30:04.295 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:30:04.295 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:04.296 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DestCityMarketID with cardinality: 70, range: 30189 to 35389
2020/08/20 13:30:04.297 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 13, range: -2147483648 to 1486903
2020/08/20 13:30:04.298 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16097 to 16097
2020/08/20 13:30:04.299 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DepTime with cardinality: 249, range: -2147483648 to 2334
2020/08/20 13:30:04.300 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:30:04.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: CRSElapsedTime with cardinality: 151, range: 36 to 411
2020/08/20 13:30:04.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: DestStateName, size: 703
2020/08/20 13:30:04.301 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: DestStateName with cardinality: 37, max length in bytes: 19, range: Alaska to Wyoming
2020/08/20 13:30:04.302 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:30:04.302 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:04.303 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DestAirportID with cardinality: 86, range: 10257 to 15389
2020/08/20 13:30:04.304 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: Distance with cardinality: 229, range: 67 to 2640
2020/08/20 13:30:04.305 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:30:04.305 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:04.306 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivArrDelay with cardinality: 10, range: -2147483648 to 626
2020/08/20 13:30:04.307 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:30:04.308 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 37
2020/08/20 13:30:04.309 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: OriginWac with cardinality: 39, range: 1 to 93
2020/08/20 13:30:04.310 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: WheelsOff with cardinality: 245, range: -2147483648 to 2348
2020/08/20 13:30:04.311 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DestAirportSeqID with cardinality: 86, range: 1025702 to 1538902
2020/08/20 13:30:04.311 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:30:04.312 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:04.312 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:04.313 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:30:04.314 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: ActualElapsedTime with cardinality: 164, range: -2147483648 to 405
2020/08/20 13:30:04.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:30:04.315 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: OriginStateName, size: 546
2020/08/20 13:30:04.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: OriginStateName with cardinality: 39, max length in bytes: 14, range: Alabama to Wisconsin
2020/08/20 13:30:04.316 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:30:04.317 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:30:04.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:30:04.318 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-27 to 2014-01-27
2020/08/20 13:30:04.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: OriginCityName, size: 1722
2020/08/20 13:30:04.319 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: OriginCityName with cardinality: 82, max length in bytes: 21, range: Aguadilla, PR to Yuma, AZ
2020/08/20 13:30:04.320 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: OriginStateFips with cardinality: 39, range: 1 to 72
2020/08/20 13:30:04.321 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: OriginState, size: 78
2020/08/20 13:30:04.322 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: OriginState with cardinality: 39, max length in bytes: 2, range: AK to WI
2020/08/20 13:30:04.323 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:30:04.326 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: WeatherDelay with cardinality: 5, range: -2147483648 to 100
2020/08/20 13:30:04.328 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DestWac with cardinality: 37, range: 1 to 93
2020/08/20 13:30:04.329 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: WheelsOn with cardinality: 232, range: -2147483648 to 2336
2020/08/20 13:30:04.330 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: OriginAirportID with cardinality: 86, range: 10140 to 16218
2020/08/20 13:30:04.331 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: OriginCityMarketID with cardinality: 69, range: 30107 to 34819
2020/08/20 13:30:04.332 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: NASDelay with cardinality: 26, range: -2147483648 to 57
2020/08/20 13:30:04.333 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: ArrTime with cardinality: 241, range: -2147483648 to 2342
2020/08/20 13:30:04.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: DestState, size: 74
2020/08/20 13:30:04.334 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: DestState with cardinality: 37, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:04.335 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 13, range: -2147483648 to 11
2020/08/20 13:30:04.336 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:30:04.337 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 27 to 27
2020/08/20 13:30:04.337 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: RandomAirports, size: 292
2020/08/20 13:30:04.338 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: RandomAirports with cardinality: 73, max length in bytes: 4, range: ABI to null
2020/08/20 13:30:04.339 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 37
2020/08/20 13:30:04.340 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: CRSDepTime with cardinality: 197, range: 542 to 2329
2020/08/20 13:30:04.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 1 to 1
2020/08/20 13:30:04.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:30:04.341 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:30:04.342 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: Dest, size: 258
2020/08/20 13:30:04.342 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: Dest with cardinality: 86, max length in bytes: 3, range: ALB to TWF
2020/08/20 13:30:04.343 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 921
2020/08/20 13:30:04.344 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: DivTailNums, size: 66
2020/08/20 13:30:04.344 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: DivTailNums with cardinality: 11, max length in bytes: 6, range: N3773D to null
2020/08/20 13:30:04.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DepDelayMinutes with cardinality: 60, range: -2147483648 to 197
2020/08/20 13:30:04.345 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DepDelay with cardinality: 74, range: -2147483648 to 197
2020/08/20 13:30:04.346 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: TaxiIn with cardinality: 22, range: -2147483648 to 36
2020/08/20 13:30:04.347 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: OriginAirportSeqID with cardinality: 86, range: 1014002 to 1621801
2020/08/20 13:30:04.348 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DestStateFips with cardinality: 37, range: 2 to 78
2020/08/20 13:30:04.349 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: ArrDelay with cardinality: 82, range: -2147483648 to 171
2020/08/20 13:30:04.350 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:30:04.351 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivAirportIDs with cardinality: 13, range: -2147483648 to 14869
2020/08/20 13:30:04.351 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: TaxiOut with cardinality: 43, range: -2147483648 to 55
2020/08/20 13:30:04.352 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: CarrierDelay with cardinality: 24, range: -2147483648 to 171
2020/08/20 13:30:04.353 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:04.354 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivLongestGTimes with cardinality: 18, range: -2147483648 to 42
2020/08/20 13:30:04.355 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: DivAirports, size: 52
2020/08/20 13:30:04.355 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: DivAirports with cardinality: 13, max length in bytes: 4, range: ATL to null
2020/08/20 13:30:04.356 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: DivDistance with cardinality: 9, range: -2147483648 to 420
2020/08/20 13:30:04.357 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:30:04.358 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: ArrDelayMinutes with cardinality: 52, range: -2147483648 to 171
2020/08/20 13:30:04.359 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for INT column: CRSArrTime with cardinality: 230, range: 23 to 2354
2020/08/20 13:30:04.360 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: TailNum, size: 1728
2020/08/20 13:30:04.361 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: TailNum with cardinality: 288, max length in bytes: 6, range: N009AA to null
2020/08/20 13:30:04.362 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Using fixed bytes value dictionary for column: DestCityName, size: 1722
2020/08/20 13:30:04.362 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 26] Created dictionary for STRING column: DestCityName with cardinality: 82, max length in bytes: 21, range: Akron, OH to Williston, ND
2020/08/20 13:30:04.363 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Start building IndexCreator!
2020/08/20 13:30:04.381 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Finished records indexing in IndexCreator!
2020/08/20 13:30:04.402 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Finished segment seal!
2020/08/20 13:30:04.403 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 26] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27 to v3 format
2020/08/20 13:30:04.429 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:30:04.451 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Finished building StatsCollector!
2020/08/20 13:30:04.451 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Collected stats for 305 documents
2020/08/20 13:30:04.452 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: FlightNum with cardinality: 294, range: 1 to 6531
2020/08/20 13:30:04.453 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: Origin, size: 309
2020/08/20 13:30:04.453 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: Origin with cardinality: 103, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:30:04.454 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:30:04.456 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: LateAircraftDelay with cardinality: 14, range: -2147483648 to 364
2020/08/20 13:30:04.457 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivActualElapsedTime with cardinality: 17, range: -2147483648 to 529
2020/08/20 13:30:04.459 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivWheelsOns with cardinality: 56, range: -2147483648 to 2302
2020/08/20 13:30:04.460 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivWheelsOffs with cardinality: 19, range: -2147483648 to 2350
2020/08/20 13:30:04.461 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: AirTime with cardinality: 132, range: -2147483648 to 410
2020/08/20 13:30:04.480 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:04.481 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivTotalGTimes with cardinality: 27, range: -2147483648 to 77
2020/08/20 13:30:04.482 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:30:04.482 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:04.483 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DestCityMarketID with cardinality: 78, range: 30140 to 35411
2020/08/20 13:30:04.484 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 37, range: -2147483648 to 1627102
2020/08/20 13:30:04.485 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16098 to 16098
2020/08/20 13:30:04.487 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DepTime with cardinality: 220, range: -2147483648 to 2336
2020/08/20 13:30:04.488 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:30:04.489 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: CRSElapsedTime with cardinality: 146, range: 39 to 406
2020/08/20 13:30:04.490 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: DestStateName, size: 546
2020/08/20 13:30:04.491 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: DestStateName with cardinality: 39, max length in bytes: 14, range: Alabama to Washington
2020/08/20 13:30:04.493 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:30:04.493 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:04.495 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DestAirportID with cardinality: 93, range: 10140 to 15411
2020/08/20 13:30:04.496 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: Distance with cardinality: 243, range: 83 to 2704
2020/08/20 13:30:04.497 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 162
2020/08/20 13:30:04.497 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: ArrTimeBlk with cardinality: 18, max length in bytes: 9, range: 0600-0659 to 2300-2359
2020/08/20 13:30:04.498 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivArrDelay with cardinality: 15, range: -2147483648 to 428
2020/08/20 13:30:04.541 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:30:04.542 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: LongestAddGTime with cardinality: 2, range: -2147483648 to 30
2020/08/20 13:30:04.542 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 26] v3 segment location for segment: airlineStats_batch_2014-01-27_2014-01-27 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27/v3
2020/08/20 13:30:04.543 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 26] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27
2020/08/20 13:30:04.543 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: OriginWac with cardinality: 43, range: 1 to 93
2020/08/20 13:30:04.544 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: WheelsOff with cardinality: 234, range: -2147483648 to 2343
2020/08/20 13:30:04.545 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DestAirportSeqID with cardinality: 93, range: 1014002 to 1541103
2020/08/20 13:30:04.551 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:30:04.552 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:04.553 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:04.555 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:30:04.556 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: ActualElapsedTime with cardinality: 132, range: -2147483648 to 432
2020/08/20 13:30:04.559 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:30:04.560 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: OriginStateName, size: 602
2020/08/20 13:30:04.560 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: OriginStateName with cardinality: 43, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:30:04.561 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DepartureDelayGroups with cardinality: 13, range: -2147483648 to 12
2020/08/20 13:30:04.562 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:30:04.563 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:30:04.563 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-28 to 2014-01-28
2020/08/20 13:30:04.564 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: OriginCityName, size: 2970
2020/08/20 13:30:04.564 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: OriginCityName with cardinality: 99, max length in bytes: 30, range: Albuquerque, NM to West Palm Beach/Palm Beach, FL
2020/08/20 13:30:04.565 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: OriginStateFips with cardinality: 43, range: 1 to 72
2020/08/20 13:30:04.566 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: OriginState, size: 86
2020/08/20 13:30:04.566 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: OriginState with cardinality: 43, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:04.567 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:30:04.568 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: WeatherDelay with cardinality: 7, range: -2147483648 to 316
2020/08/20 13:30:04.569 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DestWac with cardinality: 39, range: 1 to 93
2020/08/20 13:30:04.570 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: WheelsOn with cardinality: 199, range: -2147483648 to 2354
2020/08/20 13:30:04.571 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: OriginAirportID with cardinality: 103, range: 10140 to 15919
2020/08/20 13:30:04.572 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: OriginCityMarketID with cardinality: 90, range: 30140 to 34986
2020/08/20 13:30:04.573 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: NASDelay with cardinality: 20, range: -2147483648 to 111
2020/08/20 13:30:04.575 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: ArrTime with cardinality: 194, range: -2147483648 to 2351
2020/08/20 13:30:04.575 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: DestState, size: 78
2020/08/20 13:30:04.576 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: DestState with cardinality: 39, max length in bytes: 2, range: AK to WA
2020/08/20 13:30:04.577 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 12, range: -2147483648 to 12
2020/08/20 13:30:04.578 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:30:04.579 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 28 to 28
2020/08/20 13:30:04.580 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: RandomAirports, size: 328
2020/08/20 13:30:04.580 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: RandomAirports with cardinality: 82, max length in bytes: 4, range: ABI to null
2020/08/20 13:30:04.581 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: TotalAddGTime with cardinality: 2, range: -2147483648 to 30
2020/08/20 13:30:04.582 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: CRSDepTime with cardinality: 209, range: 45 to 2315
2020/08/20 13:30:04.583 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 2 to 2
2020/08/20 13:30:04.584 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:30:04.584 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:30:04.585 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: Dest, size: 279
2020/08/20 13:30:04.585 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: Dest with cardinality: 93, max length in bytes: 3, range: ABQ to TYR
2020/08/20 13:30:04.586 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: FirstDepTime with cardinality: 2, range: -2147483648 to 903
2020/08/20 13:30:04.587 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: DivTailNums, size: 114
2020/08/20 13:30:04.587 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: DivTailNums with cardinality: 19, max length in bytes: 6, range: N229SW to null
2020/08/20 13:30:04.589 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DepDelayMinutes with cardinality: 52, range: -2147483648 to 375
2020/08/20 13:30:04.590 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DepDelay with cardinality: 72, range: -2147483648 to 375
2020/08/20 13:30:04.592 INFO [CrcUtils] [Executor task launch worker for task 26] Computed crc = 4051890346, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27/v3/metadata.properties]
2020/08/20 13:30:04.593 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: TaxiIn with cardinality: 17, range: -2147483648 to 19
2020/08/20 13:30:04.593 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Driver, record read time : 9
2020/08/20 13:30:04.593 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Driver, stats collector time : 0
2020/08/20 13:30:04.593 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 26] Driver, indexing time : 9
2020/08/20 13:30:04.593 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 26] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27.tar.gz
2020/08/20 13:30:04.595 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: OriginAirportSeqID with cardinality: 103, range: 1014002 to 1591902
2020/08/20 13:30:04.596 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DestStateFips with cardinality: 39, range: 1 to 72
2020/08/20 13:30:04.597 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: ArrDelay with cardinality: 77, range: -2147483648 to 427
2020/08/20 13:30:04.598 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:30:04.599 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivAirportIDs with cardinality: 37, range: -2147483648 to 16271
2020/08/20 13:30:04.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: TaxiOut with cardinality: 40, range: -2147483648 to 155
2020/08/20 13:30:04.600 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: CarrierDelay with cardinality: 14, range: -2147483648 to 173
2020/08/20 13:30:04.601 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:04.602 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivLongestGTimes with cardinality: 23, range: -2147483648 to 77
2020/08/20 13:30:04.602 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: DivAirports, size: 148
2020/08/20 13:30:04.603 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: DivAirports with cardinality: 37, max length in bytes: 4, range: ATL to null
2020/08/20 13:30:04.604 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: DivDistance with cardinality: 31, range: -2147483648 to 912
2020/08/20 13:30:04.605 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:30:04.606 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: ArrDelayMinutes with cardinality: 44, range: -2147483648 to 427
2020/08/20 13:30:04.607 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for INT column: CRSArrTime with cardinality: 239, range: 616 to 2359
2020/08/20 13:30:04.608 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: TailNum, size: 1752
2020/08/20 13:30:04.608 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 26] Size for segment: airlineStats_batch_2014-01-27_2014-01-27, uncompressed: 110.79K, compressed: 31.81K
2020/08/20 13:30:04.608 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: TailNum with cardinality: 292, max length in bytes: 6, range: N11150 to null
2020/08/20 13:30:04.608 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 26] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_batch_2014-01-27_2014-01-27.tar.gz]
2020/08/20 13:30:04.608 INFO [S3PinotFS] [Executor task launch worker for task 26] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-87e83b62-0425-416e-a815-5679ca0b40f0/output/airlineStats_batch_2014-01-27_2014-01-27.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_batch_2014-01-27_2014-01-27.tar.gz
2020/08/20 13:30:04.608 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Using fixed bytes value dictionary for column: DestCityName, size: 2670
2020/08/20 13:30:04.609 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 27] Created dictionary for STRING column: DestCityName with cardinality: 89, max length in bytes: 30, range: Albuquerque, NM to White Plains, NY
2020/08/20 13:30:04.609 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Start building IndexCreator!
2020/08/20 13:30:04.631 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Finished records indexing in IndexCreator!
2020/08/20 13:30:04.652 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Finished segment seal!
2020/08/20 13:30:04.652 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 27] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28 to v3 format
2020/08/20 13:30:04.770 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 27] v3 segment location for segment: airlineStats_batch_2014-01-28_2014-01-28 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28/v3
2020/08/20 13:30:04.771 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 27] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28
2020/08/20 13:30:04.805 INFO [CrcUtils] [Executor task launch worker for task 27] Computed crc = 1728584652, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28/v3/metadata.properties]
2020/08/20 13:30:04.805 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Driver, record read time : 15
2020/08/20 13:30:04.805 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Driver, stats collector time : 0
2020/08/20 13:30:04.806 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 27] Driver, indexing time : 6
2020/08/20 13:30:04.806 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 27] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28.tar.gz
2020/08/20 13:30:04.816 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 27] Size for segment: airlineStats_batch_2014-01-28_2014-01-28, uncompressed: 114.81K, compressed: 32.9K
2020/08/20 13:30:04.816 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 27] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_batch_2014-01-28_2014-01-28.tar.gz]
2020/08/20 13:30:04.816 INFO [S3PinotFS] [Executor task launch worker for task 27] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-1322317c-8a6f-4cae-b919-639231db3021/output/airlineStats_batch_2014-01-28_2014-01-28.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_batch_2014-01-28_2014-01-28.tar.gz
2020/08/20 13:30:05.216 INFO [Executor] [Executor task launch worker for task 26] Finished task 26.0 in stage 0.0 (TID 26). 708 bytes result sent to driver
2020/08/20 13:30:05.216 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 28.0 in stage 0.0 (TID 28, localhost, executor driver, partition 28, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:30:05.217 INFO [Executor] [Executor task launch worker for task 28] Running task 28.0 in stage 0.0 (TID 28)
2020/08/20 13:30:05.217 INFO [TaskSetManager] [task-result-getter-2] Finished task 26.0 in stage 0.0 (TID 26) in 3339 ms on localhost (executor driver) (27/31)
2020/08/20 13:30:05.219 INFO [PinotFSFactory] [Executor task launch worker for task 28] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:30:05.219 WARN [HadoopPinotFS] [Executor task launch worker for task 28] no hadoop conf path is provided, will rely on default config
2020/08/20 13:30:05.238 INFO [HadoopPinotFS] [Executor task launch worker for task 28] successfully initialized HadoopPinotFS
2020/08/20 13:30:05.238 INFO [PinotFSFactory] [Executor task launch worker for task 28] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:30:05.390 INFO [Executor] [Executor task launch worker for task 27] Finished task 27.0 in stage 0.0 (TID 27). 708 bytes result sent to driver
2020/08/20 13:30:05.392 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 29.0 in stage 0.0 (TID 29, localhost, executor driver, partition 29, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:30:05.392 INFO [Executor] [Executor task launch worker for task 29] Running task 29.0 in stage 0.0 (TID 29)
2020/08/20 13:30:05.392 INFO [TaskSetManager] [task-result-getter-3] Finished task 27.0 in stage 0.0 (TID 27) in 3364 ms on localhost (executor driver) (28/31)
2020/08/20 13:30:05.394 INFO [PinotFSFactory] [Executor task launch worker for task 29] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:30:05.394 WARN [HadoopPinotFS] [Executor task launch worker for task 29] no hadoop conf path is provided, will rely on default config
2020/08/20 13:30:05.413 INFO [HadoopPinotFS] [Executor task launch worker for task 29] successfully initialized HadoopPinotFS
2020/08/20 13:30:05.413 INFO [PinotFSFactory] [Executor task launch worker for task 29] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:30:06.679 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 28] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-28]
2020/08/20 13:30:06.679 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 28] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-28], plugins includes [null]
2020/08/20 13:30:06.680 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 28] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/29/airlineStats_data_2014-01-29.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/input/airlineStats_data_2014-01-29.avro
2020/08/20 13:30:06.680 INFO [S3PinotFS] [Executor task launch worker for task 28] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/29/airlineStats_data_2014-01-29.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/input/airlineStats_data_2014-01-29.avro
2020/08/20 13:30:06.818 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 29] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-29]
2020/08/20 13:30:06.818 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 29] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-29], plugins includes [null]
2020/08/20 13:30:06.819 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 29] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/30/airlineStats_data_2014-01-30.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/input/airlineStats_data_2014-01-30.avro
2020/08/20 13:30:06.819 INFO [S3PinotFS] [Executor task launch worker for task 29] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/30/airlineStats_data_2014-01-30.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/input/airlineStats_data_2014-01-30.avro
2020/08/20 13:30:07.087 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:30:07.113 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Finished building StatsCollector!
2020/08/20 13:30:07.113 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Collected stats for 322 documents
2020/08/20 13:30:07.114 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: FlightNum with cardinality: 310, range: 4 to 6529
2020/08/20 13:30:07.115 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: Origin, size: 288
2020/08/20 13:30:07.115 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: Origin with cardinality: 96, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:30:07.116 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:30:07.117 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: LateAircraftDelay with cardinality: 29, range: -2147483648 to 278
2020/08/20 13:30:07.118 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivActualElapsedTime with cardinality: 28, range: -2147483648 to 1308
2020/08/20 13:30:07.119 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivWheelsOns with cardinality: 47, range: -2147483648 to 2248
2020/08/20 13:30:07.120 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivWheelsOffs with cardinality: 30, range: -2147483648 to 2357
2020/08/20 13:30:07.121 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: AirTime with cardinality: 143, range: -2147483648 to 442
2020/08/20 13:30:07.122 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:07.125 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivTotalGTimes with cardinality: 27, range: -2147483648 to 201
2020/08/20 13:30:07.126 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:30:07.126 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:07.128 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DestCityMarketID with cardinality: 81, range: 30107 to 35041
2020/08/20 13:30:07.128 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 28, range: -2147483648 to 1541202
2020/08/20 13:30:07.130 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16099 to 16099
2020/08/20 13:30:07.131 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DepTime with cardinality: 244, range: -2147483648 to 2344
2020/08/20 13:30:07.132 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:30:07.133 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: CRSElapsedTime with cardinality: 146, range: 37 to 455
2020/08/20 13:30:07.133 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:30:07.133 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: DestStateName, size: 798
2020/08/20 13:30:07.134 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:30:07.134 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:30:07.134 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:07.135 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DestAirportID with cardinality: 97, range: 10140 to 15919
2020/08/20 13:30:07.136 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: Distance with cardinality: 251, range: 77 to 3365
2020/08/20 13:30:07.137 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:30:07.137 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:07.138 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivArrDelay with cardinality: 28, range: -2147483648 to 933
2020/08/20 13:30:07.139 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:30:07.140 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: LongestAddGTime with cardinality: 5, range: -2147483648 to 74
2020/08/20 13:30:07.141 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: OriginWac with cardinality: 41, range: 1 to 93
2020/08/20 13:30:07.142 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: WheelsOff with cardinality: 239, range: -2147483648 to 2355
2020/08/20 13:30:07.143 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DestAirportSeqID with cardinality: 97, range: 1014002 to 1591902
2020/08/20 13:30:07.144 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:30:07.144 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:07.145 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:07.146 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:30:07.147 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: ActualElapsedTime with cardinality: 140, range: -2147483648 to 460
2020/08/20 13:30:07.148 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:30:07.150 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: OriginStateName, size: 574
2020/08/20 13:30:07.150 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: OriginStateName with cardinality: 41, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:30:07.151 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DepartureDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:30:07.152 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:30:07.153 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:30:07.154 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-29 to 2014-01-29
2020/08/20 13:30:07.155 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: OriginCityName, size: 2760
2020/08/20 13:30:07.155 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: OriginCityName with cardinality: 92, max length in bytes: 30, range: Albuquerque, NM to Yuma, AZ
2020/08/20 13:30:07.156 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: OriginStateFips with cardinality: 41, range: 1 to 72
2020/08/20 13:30:07.157 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: OriginState, size: 82
2020/08/20 13:30:07.157 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: OriginState with cardinality: 41, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:07.159 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Finished building StatsCollector!
2020/08/20 13:30:07.159 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Collected stats for 333 documents
2020/08/20 13:30:07.159 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:30:07.161 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: FlightNum with cardinality: 325, range: 2 to 7411
2020/08/20 13:30:07.161 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: WeatherDelay with cardinality: 10, range: -2147483648 to 271
2020/08/20 13:30:07.162 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: Origin, size: 312
2020/08/20 13:30:07.162 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: Origin with cardinality: 104, max length in bytes: 3, range: ABQ to YUM
2020/08/20 13:30:07.162 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:30:07.163 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:30:07.164 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: WheelsOn with cardinality: 226, range: -2147483648 to 2350
2020/08/20 13:30:07.168 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: OriginAirportID with cardinality: 96, range: 10140 to 16218
2020/08/20 13:30:07.168 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: LateAircraftDelay with cardinality: 43, range: -2147483648 to 203
2020/08/20 13:30:07.169 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: OriginCityMarketID with cardinality: 82, range: 30070 to 35412
2020/08/20 13:30:07.170 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivActualElapsedTime with cardinality: 25, range: -2147483648 to 834
2020/08/20 13:30:07.171 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: NASDelay with cardinality: 29, range: -2147483648 to 185
2020/08/20 13:30:07.171 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivWheelsOns with cardinality: 55, range: -2147483648 to 2243
2020/08/20 13:30:07.172 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: ArrTime with cardinality: 228, range: -2147483648 to 2352
2020/08/20 13:30:07.172 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivWheelsOffs with cardinality: 25, range: -2147483648 to 2234
2020/08/20 13:30:07.172 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:30:07.173 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:07.173 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: AirTime with cardinality: 153, range: -2147483648 to 461
2020/08/20 13:30:07.174 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:07.174 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:30:07.175 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivTotalGTimes with cardinality: 30, range: -2147483648 to 96
2020/08/20 13:30:07.175 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:30:07.176 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: DepTimeBlk, size: 162
2020/08/20 13:30:07.176 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: DepTimeBlk with cardinality: 18, max length in bytes: 9, range: 0001-0559 to 2200-2259
2020/08/20 13:30:07.177 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 29 to 29
2020/08/20 13:30:07.178 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: RandomAirports, size: 328
2020/08/20 13:30:07.178 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DestCityMarketID with cardinality: 87, range: 30073 to 35412
2020/08/20 13:30:07.178 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: RandomAirports with cardinality: 82, max length in bytes: 4, range: ABI to null
2020/08/20 13:30:07.179 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 36, range: -2147483648 to 1599102
2020/08/20 13:30:07.179 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: TotalAddGTime with cardinality: 5, range: -2147483648 to 74
2020/08/20 13:30:07.180 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16100 to 16100
2020/08/20 13:30:07.180 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: CRSDepTime with cardinality: 200, range: 545 to 2350
2020/08/20 13:30:07.181 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DepTime with cardinality: 262, range: -2147483648 to 2337
2020/08/20 13:30:07.181 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 3 to 3
2020/08/20 13:30:07.182 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:30:07.182 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: CancellationCode, size: 12
2020/08/20 13:30:07.183 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: CancellationCode with cardinality: 3, max length in bytes: 4, range: A to null
2020/08/20 13:30:07.183 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: CRSElapsedTime with cardinality: 152, range: 31 to 667
2020/08/20 13:30:07.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: Dest, size: 291
2020/08/20 13:30:07.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: Dest with cardinality: 97, max length in bytes: 3, range: ABQ to XNA
2020/08/20 13:30:07.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: DestStateName, size: 560
2020/08/20 13:30:07.184 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: DestStateName with cardinality: 40, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:30:07.185 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: FirstDepTime with cardinality: 5, range: -2147483648 to 1621
2020/08/20 13:30:07.186 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:30:07.186 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:07.187 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: DivTailNums, size: 180
2020/08/20 13:30:07.187 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: DivTailNums with cardinality: 30, max length in bytes: 6, range: N001AA to null
2020/08/20 13:30:07.187 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DestAirportID with cardinality: 101, range: 10135 to 15412
2020/08/20 13:30:07.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DepDelayMinutes with cardinality: 63, range: -2147483648 to 303
2020/08/20 13:30:07.188 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: Distance with cardinality: 275, range: 74 to 4963
2020/08/20 13:30:07.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:30:07.189 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:07.190 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DepDelay with cardinality: 79, range: -2147483648 to 303
2020/08/20 13:30:07.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivArrDelay with cardinality: 25, range: -2147483648 to 467
2020/08/20 13:30:07.192 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: TaxiIn with cardinality: 28, range: -2147483648 to 43
2020/08/20 13:30:07.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: OriginAirportSeqID with cardinality: 96, range: 1014002 to 1621801
2020/08/20 13:30:07.193 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: SecurityDelay with cardinality: 2, range: -2147483648 to 0
2020/08/20 13:30:07.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 78
2020/08/20 13:30:07.194 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: LongestAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:30:07.196 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: ArrDelay with cardinality: 89, range: -2147483648 to 320
2020/08/20 13:30:07.196 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: OriginWac with cardinality: 43, range: 1 to 93
2020/08/20 13:30:07.197 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:30:07.197 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: WheelsOff with cardinality: 269, range: -2147483648 to 2355
2020/08/20 13:30:07.211 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivAirportIDs with cardinality: 28, range: -2147483648 to 15412
2020/08/20 13:30:07.211 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DestAirportSeqID with cardinality: 101, range: 1013503 to 1541202
2020/08/20 13:30:07.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: TaxiOut with cardinality: 43, range: -2147483648 to 124
2020/08/20 13:30:07.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:30:07.212 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:07.213 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: CarrierDelay with cardinality: 22, range: -2147483648 to 149
2020/08/20 13:30:07.214 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:07.215 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:07.215 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:30:07.216 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivLongestGTimes with cardinality: 25, range: -2147483648 to 112
2020/08/20 13:30:07.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: ActualElapsedTime with cardinality: 161, range: -2147483648 to 487
2020/08/20 13:30:07.217 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: DivAirports, size: 112
2020/08/20 13:30:07.218 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: DivAirports with cardinality: 28, max length in bytes: 4, range: BNA to null
2020/08/20 13:30:07.218 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:30:07.219 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: DivDistance with cardinality: 17, range: -2147483648 to 696
2020/08/20 13:30:07.219 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: OriginStateName, size: 817
2020/08/20 13:30:07.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: OriginStateName with cardinality: 43, max length in bytes: 19, range: Alabama to Wyoming
2020/08/20 13:30:07.220 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:30:07.221 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DepartureDelayGroups with cardinality: 16, range: -2147483648 to 12
2020/08/20 13:30:07.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: ArrDelayMinutes with cardinality: 60, range: -2147483648 to 320
2020/08/20 13:30:07.222 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivAirportLandings with cardinality: 3, range: 0 to 9
2020/08/20 13:30:07.223 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for INT column: CRSArrTime with cardinality: 246, range: 30 to 2355
2020/08/20 13:30:07.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:30:07.224 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-30 to 2014-01-30
2020/08/20 13:30:07.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: TailNum, size: 1854
2020/08/20 13:30:07.225 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: TailNum with cardinality: 309, max length in bytes: 6, range: N001AA to null
2020/08/20 13:30:07.226 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: OriginCityName, size: 3000
2020/08/20 13:30:07.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: OriginCityName with cardinality: 100, max length in bytes: 30, range: Akron, OH to Yuma, AZ
2020/08/20 13:30:07.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Using fixed bytes value dictionary for column: DestCityName, size: 2697
2020/08/20 13:30:07.227 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 28] Created dictionary for STRING column: DestCityName with cardinality: 93, max length in bytes: 29, range: Akron, OH to Wilmington, DE
2020/08/20 13:30:07.228 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Start building IndexCreator!
2020/08/20 13:30:07.228 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: OriginStateFips with cardinality: 43, range: 1 to 78
2020/08/20 13:30:07.240 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: OriginState, size: 86
2020/08/20 13:30:07.240 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: OriginState with cardinality: 43, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:07.241 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:30:07.242 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: WeatherDelay with cardinality: 10, range: -2147483648 to 207
2020/08/20 13:30:07.243 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DestWac with cardinality: 40, range: 1 to 93
2020/08/20 13:30:07.244 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: WheelsOn with cardinality: 246, range: -2147483648 to 2354
2020/08/20 13:30:07.245 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: OriginAirportID with cardinality: 104, range: 10140 to 16218
2020/08/20 13:30:07.246 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: OriginCityMarketID with cardinality: 86, range: 30140 to 35991
2020/08/20 13:30:07.247 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: NASDelay with cardinality: 34, range: -2147483648 to 305
2020/08/20 13:30:07.248 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: ArrTime with cardinality: 245, range: -2147483648 to 2400
2020/08/20 13:30:07.249 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: DestState, size: 80
2020/08/20 13:30:07.250 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: DestState with cardinality: 40, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:07.251 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 15, range: -2147483648 to 12
2020/08/20 13:30:07.252 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Finished records indexing in IndexCreator!
2020/08/20 13:30:07.252 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:30:07.253 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 30 to 30
2020/08/20 13:30:07.254 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: RandomAirports, size: 280
2020/08/20 13:30:07.254 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: RandomAirports with cardinality: 70, max length in bytes: 4, range: ABI to null
2020/08/20 13:30:07.256 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: TotalAddGTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:30:07.257 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: CRSDepTime with cardinality: 223, range: 525 to 2250
2020/08/20 13:30:07.259 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 4 to 4
2020/08/20 13:30:07.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: CancellationCode, size: 16
2020/08/20 13:30:07.261 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: CancellationCode with cardinality: 4, max length in bytes: 4, range: A to null
2020/08/20 13:30:07.262 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: Dest, size: 303
2020/08/20 13:30:07.262 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: Dest with cardinality: 101, max length in bytes: 3, range: ABE to TYS
2020/08/20 13:30:07.263 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: FirstDepTime with cardinality: 1, range: -2147483648 to -2147483648
2020/08/20 13:30:07.264 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: DivTailNums, size: 150
2020/08/20 13:30:07.265 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: DivTailNums with cardinality: 25, max length in bytes: 6, range: N010AA to null
2020/08/20 13:30:07.266 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DepDelayMinutes with cardinality: 84, range: -2147483648 to 359
2020/08/20 13:30:07.267 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DepDelay with cardinality: 100, range: -2147483648 to 359
2020/08/20 13:30:07.268 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: TaxiIn with cardinality: 29, range: -2147483648 to 50
2020/08/20 13:30:07.269 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: OriginAirportSeqID with cardinality: 104, range: 1014002 to 1621801
2020/08/20 13:30:07.270 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DestStateFips with cardinality: 40, range: 1 to 72
2020/08/20 13:30:07.271 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: ArrDelay with cardinality: 104, range: -2147483648 to 355
2020/08/20 13:30:07.272 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:30:07.273 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivAirportIDs with cardinality: 36, range: -2147483648 to 15991
2020/08/20 13:30:07.274 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: TaxiOut with cardinality: 42, range: -2147483648 to 112
2020/08/20 13:30:07.275 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: CarrierDelay with cardinality: 37, range: -2147483648 to 196
2020/08/20 13:30:07.276 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:07.277 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivLongestGTimes with cardinality: 27, range: -2147483648 to 96
2020/08/20 13:30:07.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: DivAirports, size: 144
2020/08/20 13:30:07.278 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Finished segment seal!
2020/08/20 13:30:07.278 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: DivAirports with cardinality: 36, max length in bytes: 4, range: ANC to null
2020/08/20 13:30:07.279 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 28] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29 to v3 format
2020/08/20 13:30:07.279 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: DivDistance with cardinality: 19, range: -2147483648 to 997
2020/08/20 13:30:07.280 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:30:07.281 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: ArrDelayMinutes with cardinality: 76, range: -2147483648 to 355
2020/08/20 13:30:07.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for INT column: CRSArrTime with cardinality: 249, range: 1 to 2359
2020/08/20 13:30:07.282 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: TailNum, size: 1932
2020/08/20 13:30:07.283 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: TailNum with cardinality: 322, max length in bytes: 6, range: N008AA to N986DL
2020/08/20 13:30:07.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Using fixed bytes value dictionary for column: DestCityName, size: 2910
2020/08/20 13:30:07.284 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 29] Created dictionary for STRING column: DestCityName with cardinality: 97, max length in bytes: 30, range: Albany, NY to Wichita, KS
2020/08/20 13:30:07.284 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Start building IndexCreator!
2020/08/20 13:30:07.307 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Finished records indexing in IndexCreator!
2020/08/20 13:30:07.331 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Finished segment seal!
2020/08/20 13:30:07.332 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 29] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30 to v3 format
2020/08/20 13:30:07.412 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 28] v3 segment location for segment: airlineStats_batch_2014-01-29_2014-01-29 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29/v3
2020/08/20 13:30:07.413 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 28] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29
2020/08/20 13:30:07.455 INFO [CrcUtils] [Executor task launch worker for task 28] Computed crc = 3433721519, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29/v3/metadata.properties]
2020/08/20 13:30:07.455 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Driver, record read time : 15
2020/08/20 13:30:07.455 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Driver, stats collector time : 0
2020/08/20 13:30:07.455 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 28] Driver, indexing time : 8
2020/08/20 13:30:07.455 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 28] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29.tar.gz
2020/08/20 13:30:07.468 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 29] v3 segment location for segment: airlineStats_batch_2014-01-30_2014-01-30 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30/v3
2020/08/20 13:30:07.468 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 29] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30
2020/08/20 13:30:07.469 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 28] Size for segment: airlineStats_batch_2014-01-29_2014-01-29, uncompressed: 116.89K, compressed: 34.35K
2020/08/20 13:30:07.469 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 28] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_batch_2014-01-29_2014-01-29.tar.gz]
2020/08/20 13:30:07.469 INFO [S3PinotFS] [Executor task launch worker for task 28] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-c5789eac-1f45-4f86-87c0-aabef5f86263/output/airlineStats_batch_2014-01-29_2014-01-29.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_batch_2014-01-29_2014-01-29.tar.gz
2020/08/20 13:30:07.506 INFO [CrcUtils] [Executor task launch worker for task 29] Computed crc = 3693622185, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30/v3/metadata.properties]
2020/08/20 13:30:07.507 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Driver, record read time : 17
2020/08/20 13:30:07.507 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Driver, stats collector time : 0
2020/08/20 13:30:07.507 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 29] Driver, indexing time : 4
2020/08/20 13:30:07.507 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 29] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30.tar.gz
2020/08/20 13:30:07.518 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 29] Size for segment: airlineStats_batch_2014-01-30_2014-01-30, uncompressed: 119.61K, compressed: 36.12K
2020/08/20 13:30:07.518 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 29] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_batch_2014-01-30_2014-01-30.tar.gz]
2020/08/20 13:30:07.518 INFO [S3PinotFS] [Executor task launch worker for task 29] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-78859a92-c623-44b4-b591-a21a44677816/output/airlineStats_batch_2014-01-30_2014-01-30.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_batch_2014-01-30_2014-01-30.tar.gz
2020/08/20 13:30:07.968 INFO [Executor] [Executor task launch worker for task 29] Finished task 29.0 in stage 0.0 (TID 29). 751 bytes result sent to driver
2020/08/20 13:30:07.969 INFO [TaskSetManager] [dispatcher-event-loop-1] Starting task 30.0 in stage 0.0 (TID 30, localhost, executor driver, partition 30, PROCESS_LOCAL, 7969 bytes)
2020/08/20 13:30:07.970 INFO [Executor] [Executor task launch worker for task 30] Running task 30.0 in stage 0.0 (TID 30)
2020/08/20 13:30:07.970 INFO [TaskSetManager] [task-result-getter-0] Finished task 29.0 in stage 0.0 (TID 29) in 2579 ms on localhost (executor driver) (29/31)
2020/08/20 13:30:07.971 INFO [PinotFSFactory] [Executor task launch worker for task 30] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:30:07.971 WARN [HadoopPinotFS] [Executor task launch worker for task 30] no hadoop conf path is provided, will rely on default config
2020/08/20 13:30:07.991 INFO [HadoopPinotFS] [Executor task launch worker for task 30] successfully initialized HadoopPinotFS
2020/08/20 13:30:07.991 INFO [PinotFSFactory] [Executor task launch worker for task 30] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:30:08.151 INFO [Executor] [Executor task launch worker for task 28] Finished task 28.0 in stage 0.0 (TID 28). 751 bytes result sent to driver
2020/08/20 13:30:08.159 INFO [TaskSetManager] [task-result-getter-1] Finished task 28.0 in stage 0.0 (TID 28) in 2943 ms on localhost (executor driver) (30/31)
2020/08/20 13:30:09.280 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 30] Trying to set System Property: [plugins.dir=/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-30]
2020/08/20 13:30:09.280 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 30] Pinot plugins System Properties are set at [/Users/xiangfu/workspace/pinot-master/pinot-distribution/target/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/apache-pinot-incubating-0.5.0-SNAPSHOT-bin/pinot-plugins-dir-30], plugins includes [null]
2020/08/20 13:30:09.281 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 30] Trying to copy input file from s3://my.bucket/batch/airlineStats/rawdata/2014/01/31/airlineStats_data_2014-01-31.avro to /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/input/airlineStats_data_2014-01-31.avro
2020/08/20 13:30:09.281 INFO [S3PinotFS] [Executor task launch worker for task 30] Copy s3://my.bucket/batch/airlineStats/rawdata/2014/01/31/airlineStats_data_2014-01-31.avro to local /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/input/airlineStats_data_2014-01-31.avro
2020/08/20 13:30:09.605 WARN [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Using class: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader to read segment, ignoring configured file format: AVRO
2020/08/20 13:30:09.626 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Finished building StatsCollector!
2020/08/20 13:30:09.626 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Collected stats for 354 documents
2020/08/20 13:30:09.627 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: FlightNum with cardinality: 344, range: 1 to 7391
2020/08/20 13:30:09.628 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: Origin, size: 306
2020/08/20 13:30:09.628 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: Origin with cardinality: 102, max length in bytes: 3, range: ABQ to YAK
2020/08/20 13:30:09.633 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
2020/08/20 13:30:09.655 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: LateAircraftDelay with cardinality: 36, range: -2147483648 to 127
2020/08/20 13:30:09.658 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivActualElapsedTime with cardinality: 22, range: -2147483648 to 1126
2020/08/20 13:30:09.659 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivWheelsOns with cardinality: 63, range: -2147483648 to 2327
2020/08/20 13:30:09.660 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivWheelsOffs with cardinality: 23, range: -2147483648 to 2339
2020/08/20 13:30:09.661 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: AirTime with cardinality: 155, range: -2147483648 to 380
2020/08/20 13:30:09.662 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: ArrDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:09.663 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivTotalGTimes with cardinality: 28, range: -2147483648 to 95
2020/08/20 13:30:09.663 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: DepTimeBlk, size: 171
2020/08/20 13:30:09.664 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: DepTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:09.665 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DestCityMarketID with cardinality: 89, range: 30070 to 35323
2020/08/20 13:30:09.665 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivAirportSeqIDs with cardinality: 34, range: -2147483648 to 1591902
2020/08/20 13:30:09.666 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DaysSinceEpoch with cardinality: 1, range: 16101 to 16101
2020/08/20 13:30:09.667 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DepTime with cardinality: 291, range: -2147483648 to 2357
2020/08/20 13:30:09.668 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: Month with cardinality: 1, range: 1 to 1
2020/08/20 13:30:09.669 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: CRSElapsedTime with cardinality: 160, range: 37 to 405
2020/08/20 13:30:09.669 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: DestStateName, size: 588
2020/08/20 13:30:09.670 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: DestStateName with cardinality: 42, max length in bytes: 14, range: Alabama to Wyoming
2020/08/20 13:30:09.670 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: Carrier, size: 28
2020/08/20 13:30:09.671 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: Carrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:09.671 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DestAirportID with cardinality: 104, range: 10140 to 15624
2020/08/20 13:30:09.672 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: Distance with cardinality: 269, range: 95 to 2724
2020/08/20 13:30:09.673 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: ArrTimeBlk, size: 171
2020/08/20 13:30:09.673 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: ArrTimeBlk with cardinality: 19, max length in bytes: 9, range: 0001-0559 to 2300-2359
2020/08/20 13:30:09.674 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivArrDelay with cardinality: 21, range: -2147483648 to 1045
2020/08/20 13:30:09.676 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: SecurityDelay with cardinality: 4, range: -2147483648 to 27
2020/08/20 13:30:09.676 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: LongestAddGTime with cardinality: 3, range: -2147483648 to 38
2020/08/20 13:30:09.677 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: OriginWac with cardinality: 41, range: 1 to 93
2020/08/20 13:30:09.678 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: WheelsOff with cardinality: 296, range: -2147483648 to 2331
2020/08/20 13:30:09.679 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DestAirportSeqID with cardinality: 104, range: 1014002 to 1562401
2020/08/20 13:30:09.680 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: UniqueCarrier, size: 28
2020/08/20 13:30:09.680 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: UniqueCarrier with cardinality: 14, max length in bytes: 2, range: AA to WN
2020/08/20 13:30:09.681 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivReachedDest with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:09.682 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: Diverted with cardinality: 2, range: 0 to 1
2020/08/20 13:30:09.683 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: ActualElapsedTime with cardinality: 163, range: -2147483648 to 411
2020/08/20 13:30:09.684 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: AirlineID with cardinality: 14, range: 19393 to 21171
2020/08/20 13:30:09.685 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: OriginStateName, size: 779
2020/08/20 13:30:09.685 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: OriginStateName with cardinality: 41, max length in bytes: 19, range: Alabama to Wisconsin
2020/08/20 13:30:09.686 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DepartureDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:30:09.687 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivAirportLandings with cardinality: 4, range: 0 to 9
2020/08/20 13:30:09.688 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: FlightDate, size: 10
2020/08/20 13:30:09.689 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: FlightDate with cardinality: 1, max length in bytes: 10, range: 2014-01-31 to 2014-01-31
2020/08/20 13:30:09.689 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: OriginCityName, size: 2940
2020/08/20 13:30:09.690 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: OriginCityName with cardinality: 98, max length in bytes: 30, range: Aguadilla, PR to Yakutat, AK
2020/08/20 13:30:09.692 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: OriginStateFips with cardinality: 41, range: 1 to 78
2020/08/20 13:30:09.693 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: OriginState, size: 82
2020/08/20 13:30:09.693 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: OriginState with cardinality: 41, max length in bytes: 2, range: AK to WV
2020/08/20 13:30:09.694 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DistanceGroup with cardinality: 11, range: 1 to 11
2020/08/20 13:30:09.695 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: WeatherDelay with cardinality: 4, range: -2147483648 to 62
2020/08/20 13:30:09.696 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DestWac with cardinality: 42, range: 1 to 93
2020/08/20 13:30:09.697 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: WheelsOn with cardinality: 265, range: -2147483648 to 2355
2020/08/20 13:30:09.698 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: OriginAirportID with cardinality: 102, range: 10140 to 15991
2020/08/20 13:30:09.699 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: OriginCityMarketID with cardinality: 87, range: 30140 to 35991
2020/08/20 13:30:09.700 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: NASDelay with cardinality: 22, range: -2147483648 to 418
2020/08/20 13:30:09.700 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: ArrTime with cardinality: 256, range: -2147483648 to 2400
2020/08/20 13:30:09.701 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: DestState, size: 84
2020/08/20 13:30:09.701 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: DestState with cardinality: 42, max length in bytes: 2, range: AK to WY
2020/08/20 13:30:09.702 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: ArrivalDelayGroups with cardinality: 14, range: -2147483648 to 12
2020/08/20 13:30:09.703 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: Flights with cardinality: 1, range: 1 to 1
2020/08/20 13:30:09.704 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DayofMonth with cardinality: 1, range: 31 to 31
2020/08/20 13:30:09.705 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: RandomAirports, size: 320
2020/08/20 13:30:09.705 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: RandomAirports with cardinality: 80, max length in bytes: 4, range: ABI to null
2020/08/20 13:30:09.706 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: TotalAddGTime with cardinality: 3, range: -2147483648 to 38
2020/08/20 13:30:09.707 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: CRSDepTime with cardinality: 236, range: 514 to 2355
2020/08/20 13:30:09.708 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DayOfWeek with cardinality: 1, range: 5 to 5
2020/08/20 13:30:09.708 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: CancellationCode, size: 12
2020/08/20 13:30:09.709 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: CancellationCode with cardinality: 3, max length in bytes: 4, range: A to null
2020/08/20 13:30:09.709 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: Dest, size: 312
2020/08/20 13:30:09.709 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: Dest with cardinality: 104, max length in bytes: 3, range: ABQ to VPS
2020/08/20 13:30:09.710 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: FirstDepTime with cardinality: 3, range: -2147483648 to 1032
2020/08/20 13:30:09.711 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: DivTailNums, size: 138
2020/08/20 13:30:09.711 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: DivTailNums with cardinality: 23, max length in bytes: 6, range: N109UW to null
2020/08/20 13:30:09.712 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DepDelayMinutes with cardinality: 76, range: -2147483648 to 926
2020/08/20 13:30:09.716 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DepDelay with cardinality: 91, range: -2147483648 to 926
2020/08/20 13:30:09.717 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: TaxiIn with cardinality: 29, range: -2147483648 to 35
2020/08/20 13:30:09.717 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: OriginAirportSeqID with cardinality: 102, range: 1014002 to 1599102
2020/08/20 13:30:09.718 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DestStateFips with cardinality: 42, range: 1 to 56
2020/08/20 13:30:09.719 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: ArrDelay with cardinality: 94, range: -2147483648 to 418
2020/08/20 13:30:09.720 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: Cancelled with cardinality: 2, range: 0 to 1
2020/08/20 13:30:09.721 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivAirportIDs with cardinality: 34, range: -2147483648 to 15919
2020/08/20 13:30:09.722 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: TaxiOut with cardinality: 35, range: -2147483648 to 44
2020/08/20 13:30:09.724 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: CarrierDelay with cardinality: 31, range: -2147483648 to 149
2020/08/20 13:30:09.726 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DepDel15 with cardinality: 3, range: -2147483648 to 1
2020/08/20 13:30:09.727 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivLongestGTimes with cardinality: 25, range: -2147483648 to 77
2020/08/20 13:30:09.728 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: DivAirports, size: 136
2020/08/20 13:30:09.728 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: DivAirports with cardinality: 34, max length in bytes: 4, range: ABQ to null
2020/08/20 13:30:09.729 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: DivDistance with cardinality: 22, range: -2147483648 to 1590
2020/08/20 13:30:09.729 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: Year with cardinality: 1, range: 2014 to 2014
2020/08/20 13:30:09.731 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: ArrDelayMinutes with cardinality: 60, range: -2147483648 to 418
2020/08/20 13:30:09.731 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for INT column: CRSArrTime with cardinality: 272, range: 28 to 2359
2020/08/20 13:30:09.732 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: TailNum, size: 2016
2020/08/20 13:30:09.732 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: TailNum with cardinality: 336, max length in bytes: 6, range: N002AA to null
2020/08/20 13:30:09.733 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Using fixed bytes value dictionary for column: DestCityName, size: 3400
2020/08/20 13:30:09.733 INFO [SegmentDictionaryCreator] [Executor task launch worker for task 30] Created dictionary for STRING column: DestCityName with cardinality: 100, max length in bytes: 34, range: Aberdeen, SD to Wilmington, NC
2020/08/20 13:30:09.734 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Start building IndexCreator!
2020/08/20 13:30:09.759 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Finished records indexing in IndexCreator!
2020/08/20 13:30:09.828 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Finished segment seal!
2020/08/20 13:30:09.829 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 30] Converting segment: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31 to v3 format
2020/08/20 13:30:09.980 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 30] v3 segment location for segment: airlineStats_batch_2014-01-31_2014-01-31 is /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31/v3
2020/08/20 13:30:09.980 INFO [SegmentV1V2ToV3FormatConverter] [Executor task launch worker for task 30] Deleting files in v1 segment directory: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31
2020/08/20 13:30:10.019 INFO [CrcUtils] [Executor task launch worker for task 30] Computed crc = 2349304884, based on files [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31/v3/columns.psf, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31/v3/index_map, /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31/v3/metadata.properties]
2020/08/20 13:30:10.019 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Driver, record read time : 16
2020/08/20 13:30:10.019 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Driver, stats collector time : 0
2020/08/20 13:30:10.019 INFO [SegmentIndexCreationDriverImpl] [Executor task launch worker for task 30] Driver, indexing time : 9
2020/08/20 13:30:10.020 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 30] Tarring segment from: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31 to: /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31.tar.gz
2020/08/20 13:30:10.032 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 30] Size for segment: airlineStats_batch_2014-01-31_2014-01-31, uncompressed: 121.48K, compressed: 37.2K
2020/08/20 13:30:10.032 INFO [SparkSegmentGenerationJobRunner] [Executor task launch worker for task 30] Trying to move segment tar file from: [/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31.tar.gz] to [s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_batch_2014-01-31_2014-01-31.tar.gz]
2020/08/20 13:30:10.032 INFO [S3PinotFS] [Executor task launch worker for task 30] Copy /var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/pinot-be336d98-0b97-4aba-8696-e615544b2d35/output/airlineStats_batch_2014-01-31_2014-01-31.tar.gz from local to s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_batch_2014-01-31_2014-01-31.tar.gz
2020/08/20 13:30:10.526 INFO [Executor] [Executor task launch worker for task 30] Finished task 30.0 in stage 0.0 (TID 30). 665 bytes result sent to driver
2020/08/20 13:30:10.527 INFO [TaskSetManager] [task-result-getter-2] Finished task 30.0 in stage 0.0 (TID 30) in 2558 ms on localhost (executor driver) (31/31)
2020/08/20 13:30:10.529 INFO [TaskSchedulerImpl] [task-result-getter-2] Removed TaskSet 0.0, whose tasks have all completed, from pool
2020/08/20 13:30:10.530 INFO [DAGScheduler] [dag-scheduler-event-loop] ResultStage 0 (foreach at SparkSegmentGenerationJobRunner.java:214) finished in 46.373 s
2020/08/20 13:30:10.538 INFO [DAGScheduler] [main] Job 0 finished: foreach at SparkSegmentGenerationJobRunner.java:214, took 46.667974 s
2020/08/20 13:30:10.540 INFO [IngestionJobLauncher] [main] Trying to create instance for class org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentUriPushJobRunner
2020/08/20 13:30:10.541 INFO [PinotFSFactory] [main] Initializing PinotFS for scheme file, classname org.apache.pinot.plugin.filesystem.HadoopPinotFS
2020/08/20 13:30:10.541 WARN [HadoopPinotFS] [main] no hadoop conf path is provided, will rely on default config
2020/08/20 13:30:10.561 INFO [HadoopPinotFS] [main] successfully initialized HadoopPinotFS
2020/08/20 13:30:10.561 INFO [PinotFSFactory] [main] Initializing PinotFS for scheme s3, classname org.apache.pinot.plugin.filesystem.S3PinotFS
2020/08/20 13:30:10.814 INFO [SparkContext] [main] Starting job: foreach at SparkSegmentUriPushJobRunner.java:117
2020/08/20 13:30:10.816 INFO [DAGScheduler] [dag-scheduler-event-loop] Got job 1 (foreach at SparkSegmentUriPushJobRunner.java:117) with 2 output partitions
2020/08/20 13:30:10.816 INFO [DAGScheduler] [dag-scheduler-event-loop] Final stage: ResultStage 1 (foreach at SparkSegmentUriPushJobRunner.java:117)
2020/08/20 13:30:10.816 INFO [DAGScheduler] [dag-scheduler-event-loop] Parents of final stage: List()
2020/08/20 13:30:10.816 INFO [DAGScheduler] [dag-scheduler-event-loop] Missing parents: List()
2020/08/20 13:30:10.816 INFO [DAGScheduler] [dag-scheduler-event-loop] Submitting ResultStage 1 (ParallelCollectionRDD[1] at parallelize at SparkSegmentUriPushJobRunner.java:115), which has no missing parents
2020/08/20 13:30:10.820 INFO [MemoryStore] [dag-scheduler-event-loop] Block broadcast_1 stored as values in memory (estimated size 5.2 KB, free 366.3 MB)
2020/08/20 13:30:10.822 INFO [MemoryStore] [dag-scheduler-event-loop] Block broadcast_1_piece0 stored as bytes in memory (estimated size 2.8 KB, free 366.3 MB)
2020/08/20 13:30:10.824 INFO [BlockManagerInfo] [dispatcher-event-loop-1] Added broadcast_1_piece0 in memory on 192.168.1.139:55914 (size: 2.8 KB, free: 366.3 MB)
2020/08/20 13:30:10.825 INFO [SparkContext] [dag-scheduler-event-loop] Created broadcast 1 from broadcast at DAGScheduler.scala:1163
2020/08/20 13:30:10.826 INFO [DAGScheduler] [dag-scheduler-event-loop] Submitting 2 missing tasks from ResultStage 1 (ParallelCollectionRDD[1] at parallelize at SparkSegmentUriPushJobRunner.java:115) (first 15 tasks are for partitions Vector(0, 1))
2020/08/20 13:30:10.826 INFO [TaskSchedulerImpl] [dag-scheduler-event-loop] Adding task set 1.0 with 2 tasks
2020/08/20 13:30:10.828 INFO [TaskSetManager] [dispatcher-event-loop-0] Starting task 0.0 in stage 1.0 (TID 31, localhost, executor driver, partition 0, PROCESS_LOCAL, 11591 bytes)
2020/08/20 13:30:10.829 INFO [TaskSetManager] [dispatcher-event-loop-0] Starting task 1.0 in stage 1.0 (TID 32, localhost, executor driver, partition 1, PROCESS_LOCAL, 11606 bytes)
2020/08/20 13:30:10.829 INFO [Executor] [Executor task launch worker for task 31] Running task 0.0 in stage 1.0 (TID 31)
2020/08/20 13:30:10.829 INFO [Executor] [Executor task launch worker for task 32] Running task 1.0 in stage 1.0 (TID 32)
2020/08/20 13:30:10.834 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_batch_2014-01-16_2014-01-16.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:10.834 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_OFFLINE_16071_16071_0.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:10.834 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_batch_2014-01-16_2014-01-16.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:10.834 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_OFFLINE_16071_16071_0.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:11.307 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:11.309 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_batch_2014-01-16_2014-01-16.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-16_2014-01-16 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:11.309 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_OFFLINE_16087_16087_16.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:11.309 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_OFFLINE_16087_16087_16.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:11.557 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:11.557 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_OFFLINE_16087_16087_16.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16087_16087_16 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:11.557 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_batch_2014-01-17_2014-01-17.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:11.558 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_batch_2014-01-17_2014-01-17.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:11.810 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:11.810 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/17/airlineStats_batch_2014-01-17_2014-01-17.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-17_2014-01-17 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:11.810 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_OFFLINE_16088_16088_17.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:11.810 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_OFFLINE_16088_16088_17.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:12.043 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:12.043 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_OFFLINE_16088_16088_17.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16088_16088_17 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:12.043 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_batch_2014-01-18_2014-01-18.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:12.043 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_batch_2014-01-18_2014-01-18.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:12.297 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:12.298 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/18/airlineStats_batch_2014-01-18_2014-01-18.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-18_2014-01-18 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:12.298 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_OFFLINE_16089_16089_18.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:12.298 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_OFFLINE_16089_16089_18.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:12.397 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:12.397 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_OFFLINE_16071_16071_0.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16071_16071_0 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:12.397 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_batch_2014-01-01_2014-01-01.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:12.397 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_batch_2014-01-01_2014-01-01.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:12.628 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:12.628 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_OFFLINE_16089_16089_18.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16089_16089_18 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:12.628 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_batch_2014-01-19_2014-01-19.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:12.628 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_batch_2014-01-19_2014-01-19.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:12.648 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:12.649 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/01/airlineStats_batch_2014-01-01_2014-01-01.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-01_2014-01-01 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:12.649 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_OFFLINE_16072_16072_1.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:12.649 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_OFFLINE_16072_16072_1.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:12.863 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:12.863 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/19/airlineStats_batch_2014-01-19_2014-01-19.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-19_2014-01-19 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:12.863 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_OFFLINE_16090_16090_19.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:12.863 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_OFFLINE_16090_16090_19.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:12.907 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:12.907 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_OFFLINE_16072_16072_1.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16072_16072_1 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:12.907 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_batch_2014-01-02_2014-01-02.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:12.907 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_batch_2014-01-02_2014-01-02.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:13.174 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:13.174 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_OFFLINE_16090_16090_19.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16090_16090_19 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:13.175 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_batch_2014-01-20_2014-01-20.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:13.175 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_batch_2014-01-20_2014-01-20.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:13.425 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:13.425 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/20/airlineStats_batch_2014-01-20_2014-01-20.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-20_2014-01-20 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:13.425 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_OFFLINE_16091_16091_20.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:13.425 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_OFFLINE_16091_16091_20.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:13.698 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:13.698 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_OFFLINE_16091_16091_20.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16091_16091_20 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:13.698 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_batch_2014-01-21_2014-01-21.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:13.698 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_batch_2014-01-21_2014-01-21.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:14.015 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:14.016 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/21/airlineStats_batch_2014-01-21_2014-01-21.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-21_2014-01-21 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:14.016 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_OFFLINE_16092_16092_21.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:14.016 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_OFFLINE_16092_16092_21.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:14.358 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:14.358 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_OFFLINE_16092_16092_21.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16092_16092_21 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:14.358 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_batch_2014-01-22_2014-01-22.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:14.358 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_batch_2014-01-22_2014-01-22.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:14.457 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:14.457 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/02/airlineStats_batch_2014-01-02_2014-01-02.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-02_2014-01-02 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:14.458 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_OFFLINE_16073_16073_2.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:14.458 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_OFFLINE_16073_16073_2.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:14.778 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:14.778 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/22/airlineStats_batch_2014-01-22_2014-01-22.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-22_2014-01-22 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:14.778 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_OFFLINE_16093_16093_22.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:14.778 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_OFFLINE_16093_16093_22.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:14.845 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:14.846 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_OFFLINE_16073_16073_2.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16073_16073_2 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:14.846 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_batch_2014-01-03_2014-01-03.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:14.846 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_batch_2014-01-03_2014-01-03.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:15.020 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:15.021 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_OFFLINE_16093_16093_22.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16093_16093_22 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:15.021 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_batch_2014-01-23_2014-01-23.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:15.021 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_batch_2014-01-23_2014-01-23.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:15.048 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:15.048 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/03/airlineStats_batch_2014-01-03_2014-01-03.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-03_2014-01-03 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:15.048 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_OFFLINE_16074_16074_3.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:15.048 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_OFFLINE_16074_16074_3.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:15.233 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:15.233 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/23/airlineStats_batch_2014-01-23_2014-01-23.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-23_2014-01-23 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:15.233 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_OFFLINE_16094_16094_23.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:15.233 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_OFFLINE_16094_16094_23.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:15.518 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:15.518 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_OFFLINE_16094_16094_23.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16094_16094_23 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:15.518 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_batch_2014-01-24_2014-01-24.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:15.518 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_batch_2014-01-24_2014-01-24.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:15.934 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:15.935 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/24/airlineStats_batch_2014-01-24_2014-01-24.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-24_2014-01-24 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:15.935 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_OFFLINE_16095_16095_24.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:15.935 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_OFFLINE_16095_16095_24.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:16.262 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:16.262 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_OFFLINE_16095_16095_24.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16095_16095_24 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:16.262 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_batch_2014-01-25_2014-01-25.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:16.263 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_batch_2014-01-25_2014-01-25.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:16.674 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:16.675 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/25/airlineStats_batch_2014-01-25_2014-01-25.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-25_2014-01-25 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:16.675 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_OFFLINE_16096_16096_25.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:16.675 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_OFFLINE_16096_16096_25.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:16.994 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:16.994 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_OFFLINE_16074_16074_3.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16074_16074_3 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:16.994 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_batch_2014-01-04_2014-01-04.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:16.994 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_batch_2014-01-04_2014-01-04.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:17.217 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:17.218 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/04/airlineStats_batch_2014-01-04_2014-01-04.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-04_2014-01-04 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:17.218 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_OFFLINE_16075_16075_4.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:17.218 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_OFFLINE_16075_16075_4.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:17.414 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:17.414 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_OFFLINE_16075_16075_4.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16075_16075_4 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:17.414 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_batch_2014-01-05_2014-01-05.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:17.414 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_batch_2014-01-05_2014-01-05.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:17.614 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:17.614 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/05/airlineStats_batch_2014-01-05_2014-01-05.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-05_2014-01-05 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:17.614 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_OFFLINE_16076_16076_5.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:17.614 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_OFFLINE_16076_16076_5.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:17.877 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:17.877 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_OFFLINE_16076_16076_5.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16076_16076_5 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:17.877 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_batch_2014-01-06_2014-01-06.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:17.877 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_batch_2014-01-06_2014-01-06.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.078 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.079 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/06/airlineStats_batch_2014-01-06_2014-01-06.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-06_2014-01-06 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.079 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_OFFLINE_16077_16077_6.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:18.079 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_OFFLINE_16077_16077_6.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.221 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.222 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_OFFLINE_16096_16096_25.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16096_16096_25 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.222 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_batch_2014-01-26_2014-01-26.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:18.222 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_batch_2014-01-26_2014-01-26.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.325 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.325 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_OFFLINE_16077_16077_6.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16077_16077_6 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.325 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_batch_2014-01-07_2014-01-07.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:18.325 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_batch_2014-01-07_2014-01-07.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.454 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.454 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/26/airlineStats_batch_2014-01-26_2014-01-26.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-26_2014-01-26 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.454 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_OFFLINE_16097_16097_26.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:18.454 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_OFFLINE_16097_16097_26.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.540 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.541 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/07/airlineStats_batch_2014-01-07_2014-01-07.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-07_2014-01-07 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.541 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_OFFLINE_16078_16078_7.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:18.541 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_OFFLINE_16078_16078_7.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.676 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.676 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_OFFLINE_16097_16097_26.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16097_16097_26 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.676 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_batch_2014-01-27_2014-01-27.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:18.676 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_batch_2014-01-27_2014-01-27.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.783 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.784 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_OFFLINE_16078_16078_7.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16078_16078_7 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.784 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_batch_2014-01-08_2014-01-08.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:18.784 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_batch_2014-01-08_2014-01-08.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.911 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.911 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/27/airlineStats_batch_2014-01-27_2014-01-27.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-27_2014-01-27 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.911 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_OFFLINE_16098_16098_27.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:18.911 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_OFFLINE_16098_16098_27.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:18.996 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:18.996 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/08/airlineStats_batch_2014-01-08_2014-01-08.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-08_2014-01-08 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:18.996 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_OFFLINE_16079_16079_8.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:18.996 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_OFFLINE_16079_16079_8.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:19.198 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:19.198 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_OFFLINE_16098_16098_27.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16098_16098_27 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:19.198 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_batch_2014-01-28_2014-01-28.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:19.198 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_batch_2014-01-28_2014-01-28.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:19.302 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:19.302 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_OFFLINE_16079_16079_8.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16079_16079_8 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:19.302 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_batch_2014-01-09_2014-01-09.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:19.302 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_batch_2014-01-09_2014-01-09.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:19.457 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:19.457 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/28/airlineStats_batch_2014-01-28_2014-01-28.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-28_2014-01-28 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:19.457 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_OFFLINE_16099_16099_28.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:19.457 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_OFFLINE_16099_16099_28.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:19.569 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:19.570 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/09/airlineStats_batch_2014-01-09_2014-01-09.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-09_2014-01-09 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:19.570 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_OFFLINE_16080_16080_9.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:19.570 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_OFFLINE_16080_16080_9.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:19.705 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:19.705 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_OFFLINE_16099_16099_28.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16099_16099_28 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:19.705 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_batch_2014-01-29_2014-01-29.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:19.705 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_batch_2014-01-29_2014-01-29.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:19.926 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:19.927 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/29/airlineStats_batch_2014-01-29_2014-01-29.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-29_2014-01-29 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:19.927 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_OFFLINE_16100_16100_29.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:19.927 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_OFFLINE_16100_16100_29.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:20.139 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:20.139 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_OFFLINE_16080_16080_9.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16080_16080_9 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:20.139 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_batch_2014-01-10_2014-01-10.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:20.139 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_batch_2014-01-10_2014-01-10.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:20.212 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:20.212 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_OFFLINE_16100_16100_29.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16100_16100_29 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:20.212 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_batch_2014-01-30_2014-01-30.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:20.212 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_batch_2014-01-30_2014-01-30.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:20.397 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:20.397 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/10/airlineStats_batch_2014-01-10_2014-01-10.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-10_2014-01-10 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:20.397 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_OFFLINE_16081_16081_10.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:20.397 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_OFFLINE_16081_16081_10.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:20.474 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:20.474 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/30/airlineStats_batch_2014-01-30_2014-01-30.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-30_2014-01-30 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:20.474 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_OFFLINE_16101_16101_30.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:20.474 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_OFFLINE_16101_16101_30.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:20.638 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:20.638 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_OFFLINE_16081_16081_10.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16081_16081_10 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:20.638 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_batch_2014-01-11_2014-01-11.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:20.638 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_batch_2014-01-11_2014-01-11.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:20.800 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:20.800 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_OFFLINE_16101_16101_30.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16101_16101_30 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:20.800 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_batch_2014-01-31_2014-01-31.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@24b2299c]
2020/08/20 13:30:20.800 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_batch_2014-01-31_2014-01-31.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:21.009 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:21.010 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/11/airlineStats_batch_2014-01-11_2014-01-11.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-11_2014-01-11 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:21.010 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_OFFLINE_16082_16082_11.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:21.010 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_OFFLINE_16082_16082_11.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:21.117 INFO [FileUploadDownloadClient] [Executor task launch worker for task 32] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:21.117 INFO [SegmentPushUtils] [Executor task launch worker for task 32] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/31/airlineStats_batch_2014-01-31_2014-01-31.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-31_2014-01-31 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:21.118 INFO [Executor] [Executor task launch worker for task 32] Finished task 1.0 in stage 1.0 (TID 32). 708 bytes result sent to driver
2020/08/20 13:30:21.119 INFO [TaskSetManager] [task-result-getter-3] Finished task 1.0 in stage 1.0 (TID 32) in 10291 ms on localhost (executor driver) (1/2)
2020/08/20 13:30:21.249 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:21.250 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_OFFLINE_16082_16082_11.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16082_16082_11 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:21.250 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_batch_2014-01-12_2014-01-12.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:21.250 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_batch_2014-01-12_2014-01-12.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:21.462 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:21.462 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/12/airlineStats_batch_2014-01-12_2014-01-12.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-12_2014-01-12 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:21.462 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_OFFLINE_16083_16083_12.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:21.462 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_OFFLINE_16083_16083_12.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:21.727 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:21.728 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_OFFLINE_16083_16083_12.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16083_16083_12 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:21.728 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_batch_2014-01-13_2014-01-13.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:21.728 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_batch_2014-01-13_2014-01-13.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:22.040 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:22.041 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/13/airlineStats_batch_2014-01-13_2014-01-13.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-13_2014-01-13 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:22.041 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_OFFLINE_16084_16084_13.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:22.041 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_OFFLINE_16084_16084_13.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:22.267 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:22.267 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_OFFLINE_16084_16084_13.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16084_16084_13 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:22.267 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_batch_2014-01-14_2014-01-14.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:22.267 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_batch_2014-01-14_2014-01-14.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:22.501 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:22.501 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/14/airlineStats_batch_2014-01-14_2014-01-14.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-14_2014-01-14 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:22.501 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_OFFLINE_16085_16085_14.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:22.501 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_OFFLINE_16085_16085_14.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:22.758 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:22.758 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_OFFLINE_16085_16085_14.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16085_16085_14 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:22.759 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_batch_2014-01-15_2014-01-15.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:22.759 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_batch_2014-01-15_2014-01-15.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:22.961 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:22.961 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/15/airlineStats_batch_2014-01-15_2014-01-15.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_batch_2014-01-15_2014-01-15 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:22.961 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Start sending table airlineStats segment URIs: [s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_OFFLINE_16086_16086_15.tar.gz] to locations: [org.apache.pinot.spi.ingestion.batch.spec.PinotClusterSpec@6295061f]
2020/08/20 13:30:22.961 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Sending table airlineStats segment URI: s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_OFFLINE_16086_16086_15.tar.gz to location: http://localhost:9000 for
2020/08/20 13:30:23.288 INFO [FileUploadDownloadClient] [Executor task launch worker for task 31] Sending request: http://localhost:9000/v2/segments to controller: localhost, version: Unknown
2020/08/20 13:30:23.288 INFO [SegmentPushUtils] [Executor task launch worker for task 31] Response for pushing table airlineStats segment uri s3://my.bucket/examples/output/airlineStats/segments/2014/01/16/airlineStats_OFFLINE_16086_16086_15.tar.gz to location http://localhost:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16086_16086_15 of table: airlineStats_OFFLINE"}
2020/08/20 13:30:23.290 INFO [Executor] [Executor task launch worker for task 31] Finished task 0.0 in stage 1.0 (TID 31). 708 bytes result sent to driver
2020/08/20 13:30:23.291 INFO [TaskSetManager] [task-result-getter-0] Finished task 0.0 in stage 1.0 (TID 31) in 12463 ms on localhost (executor driver) (2/2)
2020/08/20 13:30:23.292 INFO [TaskSchedulerImpl] [task-result-getter-0] Removed TaskSet 1.0, whose tasks have all completed, from pool
2020/08/20 13:30:23.292 INFO [DAGScheduler] [dag-scheduler-event-loop] ResultStage 1 (foreach at SparkSegmentUriPushJobRunner.java:117) finished in 12.475 s
2020/08/20 13:30:23.293 INFO [DAGScheduler] [main] Job 1 finished: foreach at SparkSegmentUriPushJobRunner.java:117, took 12.478071 s
2020/08/20 13:30:23.298 INFO [SparkContext] [Thread-1] Invoking stop() from shutdown hook
2020/08/20 13:30:23.312 INFO [AbstractConnector] [Thread-1] Stopped Spark@be164d8{HTTP/1.1,[http/1.1]}{0.0.0.0:4041}
2020/08/20 13:30:23.317 INFO [SparkUI] [Thread-1] Stopped Spark web UI at http://192.168.1.139:4041
2020/08/20 13:30:23.348 INFO [MapOutputTrackerMasterEndpoint] [dispatcher-event-loop-0] MapOutputTrackerMasterEndpoint stopped!
2020/08/20 13:30:23.382 INFO [MemoryStore] [Thread-1] MemoryStore cleared
2020/08/20 13:30:23.383 INFO [BlockManager] [Thread-1] BlockManager stopped
2020/08/20 13:30:23.385 INFO [BlockManagerMaster] [Thread-1] BlockManagerMaster stopped
2020/08/20 13:30:23.393 INFO [OutputCommitCoordinator$OutputCommitCoordinatorEndpoint] [dispatcher-event-loop-0] OutputCommitCoordinator stopped!
2020/08/20 13:30:23.500 INFO [SparkContext] [Thread-1] Successfully stopped SparkContext
2020/08/20 13:30:23.501 INFO [ShutdownHookManager] [Thread-1] Shutdown hook called
2020/08/20 13:30:23.503 INFO [ShutdownHookManager] [Thread-1] Deleting directory /private/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/spark-ff222c7f-209d-4101-b950-53b197974543
2020/08/20 13:30:23.534 INFO [ShutdownHookManager] [Thread-1] Deleting directory /private/var/folders/kp/v8smb2f11tg6q2grpwkq7qnh0000gn/T/spark-8e799266-782b-4069-b12a-4c1012c54954

```

## Sample Output

Below is the sample snapshot of s3 location for controller:

![Sample S3 Controller Storage](../../.gitbook/assets/image%20%2832%29.png)

Below is a sample download URI in PropertyStore

![Sample segment download URI in PropertyStore](../../.gitbook/assets/image%20%2833%29.png)







