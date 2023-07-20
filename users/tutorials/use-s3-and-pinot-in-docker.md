# Use S3 and Pinot in Docker

## Set up Pinot Cluster

In order to setup Pinot in Docker to use S3 as deep store, we need to put extra configs for Controller and Server.

### Create a docker network

```
docker network create -d bridge pinot-demo
```

### Start Zookeeper

```
docker run \
    --name zookeeper \
    --restart always \
    --network=pinot-demo \
    -d zookeeper:3.5.6
```

### Prepare Pinot configuration files

Below sections will prepare 3 config files under `/tmp/pinot-s3-docker` to mount to the container.

```
/tmp/pinot-s3-docker/
                     controller.conf
                     server.conf
                     ingestionJobSpec.yaml
```

### Start Controller

Below is a sample `controller.conf` file.

{% hint style="info" %}
Configure `controller.data.dir`to your s3 bucket. All the uploaded segments will be stored there.&#x20;
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
Add `s3` to `pinot.controller.segment.fetcher.protocols`&#x20;

and set `pinot.controller.segment.fetcher.s3.class` to`org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher`
{% endhint %}

```bash
pinot.role=controller
pinot.controller.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.controller.storage.factory.s3.region=us-west-2
controller.data.dir=s3://<my-bucket>/pinot-data/pinot-s3-example-docker/controller-data/
controller.local.temp.dir=/tmp/pinot-tmp-data/
controller.helix.cluster.name=pinot-s3-example-docker
controller.zk.str=zookeeper:2181
controller.port=9000
controller.enable.split.commit=true
pinot.controller.segment.fetcher.protocols=file,http,s3
pinot.controller.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

Then start pinot controller with:

```
docker run --rm -ti \
    --name pinot-controller \
    --network=pinot-demo \
    -p 9000:9000 \
    --env AWS_ACCESS_KEY_ID=<aws-access-key-id> \
    --env AWS_SECRET_ACCESS_KEY=<aws-secret-access-key> \
    --mount type=bind,source=/tmp/pinot-s3-docker,target=/tmp \
    apachepinot/pinot:0.6.0-SNAPSHOT-ca8545b29-20201105-jdk11 StartController \
    -configFileName /tmp/controller.conf
```

### Start Broker

Broker is a simple one you can just start it with default:

```
docker run --rm -ti \
    --name pinot-broker \
    --network=pinot-demo \
    --env AWS_ACCESS_KEY_ID=<aws-access-key-id> \
    --env AWS_SECRET_ACCESS_KEY=<aws-secret-access-key> \
    apachepinot/pinot:0.6.0-SNAPSHOT-ca8545b29-20201105-jdk11 StartBroker \
    -zkAddress zookeeper:2181 -clusterName pinot-s3-example-docker
```

### Start Server

Below is a sample `server.conf` file

{% hint style="info" %}
Similar to controller config, also set s3 configs in pinot server.&#x20;
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

Then start pinot server with:

```
docker run --rm -ti \
    --name pinot-server \
    --network=pinot-demo \
    --env AWS_ACCESS_KEY_ID=<aws-access-key-id> \
    --env AWS_SECRET_ACCESS_KEY=<aws-secret-access-key> \
    --mount type=bind,source=/tmp/pinot-s3-docker,target=/tmp \
    apachepinot/pinot:0.6.0-SNAPSHOT-ca8545b29-20201105-jdk11 StartServer \
    -zkAddress zookeeper:2181 -clusterName pinot-s3-example-docker \
    -configFileName /tmp/server.conf
```

## Set up Table

In this demo, we just use `airlineStats` table as an example which is already packaged inside the docker image.

You can also mount your table conf and schema files to the container and run it.

```
docker run --rm -ti \
    --name pinot-ingestion-job \
    --network=pinot-demo \
    apachepinot/pinot:0.6.0-SNAPSHOT-ca8545b29-20201105-jdk11 AddTable \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -schemaFile examples/batch/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json \
    -exec
```

## Set up Ingestion Jobs

### Standalone Job

Below is a sample standalone ingestion job spec with certain notable changes:

* **jobType** is **SegmentCreationAndMetadataPush** (this job will bypass controller download segment )
* **inputDirURI** is set to a s3 location  **s3://my.bucket/batch/airlineStats/rawdata/**
* **outputDirURI** is set to a s3 location  **s3://my.bucket/output/airlineStats/segments**
*   Add a new PinotFs under **pinotFSSpecs**

    ```
    - scheme: s3
      className: org.apache.pinot.plugin.filesystem.S3PinotFS
      configs:
        region: 'us-west-2'
    ```

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

  # segmentMetadataPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.IngestionJobRunner interface.
  segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentMetadataPushJobRunner'

# jobType: Pinot ingestion job type.
# Supported job types are:
#   'SegmentCreation'
#   'SegmentTarPush'
#   'SegmentUriPush'
#   'SegmentCreationAndTarPush'
#   'SegmentCreationAndUriPush'
jobType: SegmentCreationAndMetadataPush

# inputDirURI: Root directory of input data, expected to have scheme configured in PinotFS.
inputDirURI: 's3://<my-bucket>/pinot-data/rawdata/airlineStats/rawdata/'

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
outputDirURI: 's3://<my-bucket>/pinot-data/pinot-s3-docker/segments/airlineStats'

# segmentCreationJobParallelism: The parallelism to create egments.
segmentCreationJobParallelism: 5

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
  schemaURI: 'http://pinot-controller:9000/tables/airlineStats/schema'

  # tableConfigURI: defines where to reade the table config.
  # Supports using PinotFS or HTTP.
  # E.g.
  #   hdfs://path/to/table_config.json
  #   http://localhost:9000/tables/myTable
  # Note that the API to read Pinot table config directly from pinot controller contains a JSON wrapper.
  # The real table config is the object under the field 'OFFLINE'.
  tableConfigURI: 'http://pinot-controller:9000/tables/airlineStats'

# pinotClusterSpecs: defines the Pinot Cluster Access Point.
pinotClusterSpecs:
  - # controllerURI: used to fetch table/schema information and data push.
    # E.g. http://localhost:9000
    controllerURI: 'http://pinot-controller:9000'

# pushJobSpec: defines segment push job related configuration.
pushJobSpec:

  # pushAttempts: number of attempts for push job, default is 1, which means no retry.
  pushAttempts: 2

  # pushRetryIntervalMillis: retry wait Ms, default to 1 second.
  pushRetryIntervalMillis: 1000

```

Launch the data ingestion job:

```
docker run --rm -ti \
    --name pinot-ingestion-job \
    --network=pinot-demo \
    --env AWS_ACCESS_KEY_ID=<aws-access-key-id> \
    --env AWS_SECRET_ACCESS_KEY=<aws-secret-access-key> \
    --mount type=bind,source=/tmp/pinot-s3-docker,target=/tmp \
    apachepinot/pinot:0.6.0-SNAPSHOT-ca8545b29-20201105-jdk11 LaunchDataIngestionJob \
    -jobSpecFile /tmp/ingestionJobSpec.yaml
```

