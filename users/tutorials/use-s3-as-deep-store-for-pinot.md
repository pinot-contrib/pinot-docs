# Use S3 as Deep Storage for Pinot

{% hint style="info" %}
Below commands are based on pinot distribution binary.
{% endhint %}

## Setup Pinot Cluster

In order to set up Pinot to use S3 as deep store, we need to put extra configs for Controller and Server.

### Start Controller

Below is a sample `controller.conf` file.

{% hint style="info" %}
Configure `controller.data.dir`to your s3 bucket. All the uploaded segments will be stored there.
{% endhint %}

{% hint style="info" %}
And add s3 as a pinot storage with configs:

```bash
pinot.controller.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.controller.storage.factory.s3.region=us-west-2
```

Regarding AWS Credential, we also follow the convention of [DefaultAWSCredentialsProviderChain](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/auth/DefaultAWSCredentialsProviderChain.html).

You can specify AccessKey and Secret using:

* Environment Variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (RECOMMENDED since they are recognized by all the AWS SDKs and CLI except for .NET), or `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` (only recognized by Java SDK)
* Java System Properties - `aws.accessKeyId` and `aws.secretKey`
* Credential profiles file at the default location (`~/.aws/credentials`) shared by all AWS SDKs and the AWS CLI
* Configure AWS credential in pinot config files, e.g. set `pinot.controller.storage.factory.s3.accessKey` and `pinot.controller.storage.factory.s3.secretKey` in the config file. (Not recommended)

```bash
pinot.controller.storage.factory.s3.accessKey=****************LFVX
pinot.controller.storage.factory.s3.secretKey=****************gfhz
```
{% endhint %}

{% hint style="info" %}
Add `s3` to `pinot.controller.segment.fetcher.protocols`

and set `pinot.controller.segment.fetcher.s3.class` to`org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher`
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

If you to grant full control to bucket owner, then add this to the config:

```bash
pinot.controller.storage.factory.s3.disableAcl=false
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

{% hint style="info" %}
Similar to controller config, also set s3 configs in pinot server.
{% endhint %}

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

If you to grant full control to bucket owner, then add this to the config:

```bash
pinot.controller.storage.factory.s3.disableAcl=false
```

Then start pinot controller with:

```
bin/pinot-admin.sh StartServer -configFileName conf/server.conf -zkAddress localhost:2181 -clusterName pinot-s3-example
```

## Setup Table

In this demo, we just use `airlineStats` table as an example.

Create table with below command:

```
bin/pinot-admin.sh AddTable  -schemaFile examples/batch/airlineStats/airlineStats_schema.json -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -exec
```

## Set up Ingestion Jobs

### Standalone Job

Below is a sample standalone ingestion job spec with certain notable changes:

* **jobType** is **SegmentCreationAndUriPush**
* **inputDirURI** is set to a s3 location **s3://my.bucket/batch/airlineStats/rawdata/**
* **outputDirURI** is set to a s3 location **s3://my.bucket/output/airlineStats/segments**
*   Add a new PinotFs under **pinotFSSpecs**

    ```
    - scheme: s3
      className: org.apache.pinot.plugin.filesystem.S3PinotFS
      configs:
        region: 'us-west-2'
    ```
* For library version < **0.6.0**, set `segmentUriPrefix` to `[scheme]://[bucket.name]`, e.g. `s3://my.bucket` , from version **0.6.0**, you can put empty string or just ignore `segmentUriPrefix`.

Sample `ingestionJobSpec.yaml`

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

```bash
bin/pinot-admin.sh LaunchDataIngestionJob -jobSpecFile  ~/temp/pinot/pinot-s3-test/ingestionJobSpec.yaml
```

```
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

#### Set up Spark Cluster (Skip if you already have one)

Follow this [page](https://app.gitbook.com/@apache-pinot/s/apache-pinot-cookbook/operators/tutorials/batch-data-ingestion-in-practice#executing-the-job-using-spark) to setup a local spark cluster.

#### Submit Spark Job

Below is a sample Spark Ingestion job

```
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

```
${SPARK_HOME}/bin/spark-submit \
  --class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \
  --master "local[2]" \
  --deploy-mode client \
  --conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml" \
  --conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" \
  local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar \
  -jobSpecFile ${PINOT_DISTRIBUTION_DIR}/examples/sparkIngestionJobSpec.yaml
```

## Sample Results/Snapshots

Below is the sample snapshot of s3 location for controller:

![Sample S3 Controller Storage](<../../.gitbook/assets/image (37).png>)

Below is a sample download URI in PropertyStore, we expect the segment download uri is started with `s3://`

![Sample segment download URI in PropertyStore](<../../.gitbook/assets/image (7).png>)
