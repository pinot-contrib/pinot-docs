# Advanced Pinot Setup

## Start Pinot components (scripts or docker images)

Set up Pinot by starting each component individually

{% tabs %}
{% tab title="Using docker images" %}
#### Start Pinot Components using docker

**Prerequisites**

{% hint style="info" %}
If running locally, ensure your docker cluster has enough resources, below is a sample config.
{% endhint %}

![Sample docker resources](<../../.gitbook/assets/image (4) (1).png>)

**Pull docker image**

You can try out pre-built Pinot all-in-one docker image.

```
export PINOT_VERSION=0.10.0
export PINOT_IMAGE=apachepinot/pinot:${PINOT_VERSION}
docker pull ${PINOT_IMAGE}
```

(Optional) You can also follow the instructions [here](../../operators/tutorials/build-docker-images.md) to build your own images.

**0. Create a Network**

Create an isolated bridge network in docker

```
docker network create -d bridge pinot-demo
```

**1. Start Zookeeper**

Start Zookeeper in daemon.

```
docker run \
    --network=pinot-demo \
    --name  pinot-zookeeper \
    --restart always \
    -p 2181:2181 \
    -d zookeeper:3.5.6
```

Start [ZKUI](https://github.com/DeemOpen/zkui) to browse Zookeeper data at [http://localhost:9090](http://localhost:9090).

```
docker run \
    --network pinot-demo --name=zkui \
    -p 9090:9090 \
    -e ZK_SERVER=pinot-zookeeper:2181 \
    -d qnib/plain-zkui:latest
```

**2. Start Pinot Controller**

Start Pinot Controller in daemon and connect to Zookeeper.

```
docker run \
    --network=pinot-demo \
    --name pinot-controller \
    -p 9000:9000 \
    -d ${PINOT_IMAGE} StartController \
    -zkAddress pinot-zookeeper:2181
```

**3. Start Pinot Broker**

Start Pinot Broker in daemon and connect to Zookeeper.

```
docker run \
    --network=pinot-demo \
    --name pinot-broker \
    -d ${PINOT_IMAGE} StartBroker \
    -zkAddress pinot-zookeeper:2181
```

**4. Start Pinot Server**

Start Pinot Server in daemon and connect to Zookeeper.

```
export PINOT_IMAGE=apachepinot/pinot:0.3.0-SNAPSHOT
docker run \
    --network=pinot-demo \
    --name pinot-server \
    -d ${PINOT_IMAGE} StartServer \
    -zkAddress pinot-zookeeper:2181
```

Now all Pinot related components are started as an empty cluster.

You can run below command to check container status.

```
docker container ls -a
```

**Sample Console Output**

```
CONTAINER ID        IMAGE                              COMMAND                  CREATED              STATUS                PORTS                                                  NAMES
9e80c3fcd29b        apachepinot/pinot:0.3.0-SNAPSHOT   "./bin/pinot-admin.s…"   18 seconds ago       Up 17 seconds         8096-8099/tcp, 9000/tcp                                pinot-server
f4c42a5865c7        apachepinot/pinot:0.3.0-SNAPSHOT   "./bin/pinot-admin.s…"   21 seconds ago       Up 21 seconds         8096-8099/tcp, 9000/tcp                                pinot-broker
a413b0013806        apachepinot/pinot:0.3.0-SNAPSHOT   "./bin/pinot-admin.s…"   26 seconds ago       Up 25 seconds         8096-8099/tcp, 0.0.0.0:9000->9000/tcp                  pinot-controller
9d3b9c4d454b        zookeeper:3.5.6                    "/docker-entrypoint.…"   About a minute ago   Up About a minute     2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp   pinot-zookeeper
```
{% endtab %}

{% tab title="Using launcher scripts" %}
Download Pinot Distribution from [http://pinot.apache.org/download/](http://pinot.apache.org/download/)

```
$ export PINOT_VERSION=0.10.0
$ tar -xvf apache-pinot-${PINOT_VERSION}-bin.tar.gz

$ cd apache-pinot-${PINOT_VERSION}-bin
$ ls
DISCLAIMER    LICENSE        NOTICE        bin        conf        lib        licenses    query_console    sample_data

$ PINOT_INSTALL_DIR=`pwd`
```

#### Start Pinot components via launcher scripts

**Start Zookeeper**

```
cd apache-pinot-${PINOT_VERSION}-bin
bin/pinot-admin.sh StartZookeeper
```

**Start Pinot Controller**

> See [controller page](advanced-pinot-setup.md) for more details .

```
bin/pinot-admin.sh StartController \
    -zkAddress localhost:2181
```

**Start Pinot Broker**

```
bin/pinot-admin.sh StartBroker \
    -zkAddress localhost:2181
```

**Start Pinot Controller**

```
bin/pinot-admin.sh StartServer \
    -zkAddress localhost:2181
```
{% endtab %}
{% endtabs %}

## Start Pinot Using Config Files

Often times we need to customized the setup of Pinot components. Hence user can compile a config file and use it to start Pinot components.

Below are the examples config files and sample command to start Pinot.

### Pinot Controller

Below is a sample `pinot-controller.conf` used in HelmChart setup.

```
controller.helix.cluster.name=pinot-quickstart
controller.port=9000
controller.vip.host=pinot-controller
controller.vip.port=9000
controller.data.dir=/var/pinot/controller/data
controller.zk.str=pinot-zookeeper:2181
pinot.set.instance.id.to.hostname=true
```

In order to run Pinot Controller, the command is:

```
bin/pinot-admin.sh StartController -configFileName config/pinot-controller.conf
```

#### Configure Controller

Below are some configurations you can set in Pinot Controller. You can head over to [Controller](../../configuration-reference/controller.md#primary-configuration) for complete list of available configs.

| Config Name                       | Description                                                    | Default Value                                                      |
| --------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------ |
| controller.helix.cluster.name     | Pinot Cluster name                                             | PinotCluster                                                       |
| controller.host                   | Pinot Controller Host                                          | Required if config **pinot.set.instance.id.to.hostname** is false. |
| pinot.set.instance.id.to.hostname | When enabled, use server hostname to infer **controller.host** | false                                                              |
| controller.port                   | Pinot Controller Port                                          | 9000                                                               |
| controller.vip.host               | The VIP hostname used to set the download URL for segments     | ${controller.host}                                                 |
| controller.vip.port               | The VIP port used to set the download URL for segments         | ${controller.port}                                                 |
| controller.data.dir               | Directory to host segment data                                 | ${java.io.tmpdir}/PinotController                                  |
| controller.zk.str                 | Zookeeper URL                                                  | localhost:2181                                                     |
| cluster.tenant.isolation.enable   | Enable Tenant Isolation, default is single tenant cluster      | true                                                               |

### Pinot Broker

Below is a sample `pinot-broker.conf` used in HelmChart setup.

```
pinot.broker.client.queryPort=8099
pinot.broker.routing.table.builder.class=random
pinot.set.instance.id.to.hostname=true
```

In order to run Pinot Broker, the command is:

```
bin/pinot-admin.sh StartBroker -clusterName pinot-quickstart -zkAddress pinot-zookeeper:2181 -configFileName config/pinot-broker.conf
```

#### Configure Broker

Below are some configurations you can set in Pinot Broker. You can head over to [Broker](../../configuration-reference/broker.md) for complete list of available configs.

| Config Name                              | Description                                                                                                                                                                                                                                   | Default Value                                             |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| instanceId                               | Unique id to register Pinot Broker in the cluster.                                                                                                                                                                                            | BROKER\_${BROKER\_HOST}\_${pinot.broker.client.queryPort} |
| pinot.set.instance.id.to.hostname        | When enabled, use server hostname to set ${BROKER\_HOST} in above config, else use IP address.                                                                                                                                                | false                                                     |
| pinot.broker.client.queryPort            | Port to query Pinot Broker                                                                                                                                                                                                                    | 8099                                                      |
| pinot.broker.timeoutMs                   | Timeout for Broker Query in Milliseconds                                                                                                                                                                                                      | 10000                                                     |
| pinot.broker.enable.query.limit.override | Configuration to enable Query LIMIT Override to protect Pinot Broker and Server from fetch too many records back.                                                                                                                             | false                                                     |
| pinot.broker.query.response.limit        | When config **pinot.broker.enable.query.limit.override** is enabled, reset limit for selection query if it exceeds this value.                                                                                                                | 2147483647                                                |
| pinot.broker.startup.minResourcePercent  | Configuration to consider the broker ServiceStatus as being STARTED if the percent of resources (tables) that are ONLINE for this this broker has crossed the threshold percentage of the total number of tables that it is expected to serve | 100.0                                                     |

### Pinot Server

Below is a sample `pinot-server.conf` used in HelmChart setup.

```
pinot.server.netty.port=8098
pinot.server.adminapi.port=8097
pinot.server.instance.dataDir=/var/pinot/server/data/index
pinot.server.instance.segmentTarDir=/var/pinot/server/data/segment
pinot.set.instance.id.to.hostname=true
```

In order to run Pinot Server, the command is:

```
bin/pinot-admin.sh StartServer -clusterName pinot-quickstart -zkAddress pinot-zookeeper:2181 -configFileName config/pinot-server.conf
```

#### Configure Server

Below are some outstanding configurations you can set in Pinot Server. You can head over to [Server](../../configuration-reference/server.md) for complete list of available configs.

| Config Name                         | Description                                                                                    | Default Value                                       |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| instanceId                          | Unique id to register Pinot Server in the cluster.                                             | Server\_${SERVER\_HOST}\_${pinot.server.netty.port} |
| pinot.set.instance.id.to.hostname   | When enabled, use server hostname to set ${SERVER\_HOST} in above config, else use IP address. | false                                               |
| pinot.server.netty.port             | Port to query Pinot Server                                                                     | 8098                                                |
| pinot.server.adminapi.port          | Port for Pinot Server Admin UI                                                                 | 8097                                                |
| pinot.server.instance.dataDir       | Directory to hold all the data                                                                 | ${java.io.tmpDir}/PinotServer/index                 |
| pinot.server.instance.segmentTarDir | Directory to hold temporary segments downloaded from Controller or Deep Store                  | ${java.io.tmpDir}/PinotServer/segmentTar            |
| pinot.server.query.executor.timeout | Timeout for Server to process Query in Milliseconds                                            | 15000                                               |

## Create and Configure table

A TABLE in regular database world is represented as \<TABLE>\_OFFLINE and/or \<TABLE>\_REALTIME in Pinot depending on the ingestion mode (batch, real-time, hybrid)

See [`examples`](https://github.com/apache/pinot/tree/master/pinot-tools/src/main/resources/examples) for all possible batch/streaming tables.

### Batch Table Creation

See [Batch Tables](advanced-pinot-setup.md) for table configuration details and how to customize it.

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    --network=pinot-demo \
    --name pinot-batch-table-creation \
    ${PINOT_IMAGE} AddTable \
    -schemaFile examples/batch/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
```

**Sample Console Output**

```
Executing command: AddTable -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -schemaFile examples/batch/airlineStats/airlineStats_schema.json -controllerHost pinot-controller -controllerPort 9000 -exec
Sending request: http://pinot-controller:9000/schemas to controller: a413b0013806, version: Unknown
{"status":"Table airlineStats_OFFLINE succesfully added"}
```
{% endtab %}

{% tab title="Using launcher scripts" %}
```
bin/pinot-admin.sh AddTable \
    -schemaFile examples/batch/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json \
    -exec
```
{% endtab %}
{% endtabs %}

### Streaming Table Creation

See [Streaming Tables](advanced-pinot-setup.md) for table configuration details and how to customize it.

{% tabs %}
{% tab title="Docker" %}
**Start Kafka**

```
docker run \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=pinot-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -d wurstmeister/kafka:latest
```

**Create a Kafka Topic**

```
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper pinot-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic flights-realtime
```

**Create a Streaming table**

```
docker run \
    --network=pinot-demo \
    --name pinot-streaming-table-creation \
    ${PINOT_IMAGE} AddTable \
    -schemaFile examples/stream/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/docker/table-configs/airlineStats_realtime_table_config.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
```

**Sample output**

```
Executing command: AddTable -tableConfigFile examples/docker/table-configs/airlineStats_realtime_table_config.json -schemaFile examples/stream/airlineStats/airlineStats_schema.json -controllerHost pinot-controller -controllerPort 9000 -exec
Sending request: http://pinot-controller:9000/schemas to controller: 8fbe601012f3, version: Unknown
{"status":"Table airlineStats_REALTIME succesfully added"}
```
{% endtab %}

{% tab title="Using launcher scripts" %}
**Start Kafka-Zookeeper**

```
bin/pinot-admin.sh StartZookeeper -zkPort 2191
```

**Start Kafka**

```
bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2191/kafka -port 19092
```

**Create stream table**

```
bin/pinot-admin.sh AddTable \
    -schemaFile examples/stream/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/stream/airlineStats/airlineStats_realtime_table_config.json \
    -exec
```
{% endtab %}
{% endtabs %}

## Load Data

Now that the table is configured, let's load some data. Data can be loaded in batch mode or streaming mode. See[ ingestion overview](data-ingestion.md) page for details. Loading data involves generating pinot segments from raw data and pushing them to the pinot cluster.

### Load Data in Batch

User can always generate and push segments to Pinot via standalone scripts or using frameworks such as Hadoop or Spark. See this [page](advanced-pinot-setup.md) for more details on setting up Data Ingestion Jobs.

Below example goes with the standalone mode.

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    --network=pinot-demo \
    --name pinot-data-ingestion-job \
    ${PINOT_IMAGE} LaunchDataIngestionJob \
    -jobSpecFile examples/docker/ingestion-job-specs/airlineStats.yaml
```

**Sample Console Output**

```
SegmentGenerationJobSpec:
!!org.apache.pinot.spi.ingestion.batch.spec.SegmentGenerationJobSpec
excludeFileNamePattern: null
executionFrameworkSpec: {extraConfigs: null, name: standalone, segmentGenerationJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner,
  segmentTarPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner,
  segmentUriPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner}
includeFileNamePattern: glob:**/*.avro
inputDirURI: examples/batch/airlineStats/rawdata
jobType: SegmentCreationAndTarPush
outputDirURI: examples/batch/airlineStats/segments
overwriteOutput: true
pinotClusterSpecs:
- {controllerURI: 'http://pinot-controller:9000'}
pinotFSSpecs:
- {className: org.apache.pinot.spi.filesystem.LocalPinotFS, configs: null, scheme: file}
pushJobSpec: {pushAttempts: 2, pushParallelism: 1, pushRetryIntervalMillis: 1000,
  segmentUriPrefix: null, segmentUriSuffix: null}
recordReaderSpec: {className: org.apache.pinot.plugin.inputformat.avro.AvroRecordReader,
  configClassName: null, configs: null, dataFormat: avro}
segmentNameGeneratorSpec: null
tableSpec: {schemaURI: 'http://pinot-controller:9000/tables/airlineStats/schema',
  tableConfigURI: 'http://pinot-controller:9000/tables/airlineStats', tableName: airlineStats}

Trying to create instance for class org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner
Initializing PinotFS for scheme file, classname org.apache.pinot.spi.filesystem.LocalPinotFS
Finished building StatsCollector!
Collected stats for 403 documents
Created dictionary for INT column: FlightNum with cardinality: 386, range: 14 to 7389
Using fixed bytes value dictionary for column: Origin, size: 294
Created dictionary for STRING column: Origin with cardinality: 98, max length in bytes: 3, range: ABQ to VPS
Created dictionary for INT column: Quarter with cardinality: 1, range: 1 to 1
Created dictionary for INT column: LateAircraftDelay with cardinality: 50, range: -2147483648 to 303
......
......
Pushing segment: airlineStats_OFFLINE_16085_16085_29 to location: http://pinot-controller:9000 for table airlineStats
Sending request: http://pinot-controller:9000/v2/segments?tableName=airlineStats to controller: a413b0013806, version: Unknown
Response for pushing table airlineStats segment airlineStats_OFFLINE_16085_16085_29 to location http://pinot-controller:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16085_16085_29 of table: airlineStats"}
Pushing segment: airlineStats_OFFLINE_16084_16084_30 to location: http://pinot-controller:9000 for table airlineStats
Sending request: http://pinot-controller:9000/v2/segments?tableName=airlineStats to controller: a413b0013806, version: Unknown
Response for pushing table airlineStats segment airlineStats_OFFLINE_16084_16084_30 to location http://pinot-controller:9000 - 200: {"status":"Successfully uploaded segment: airlineStats_OFFLINE_16084_16084_30 of table: airlineStats"}
```
{% endtab %}

{% tab title="Using launcher scripts" %}
```
bin/pinot-admin.sh LaunchDataIngestionJob \
    -jobSpecFile examples/batch/airlineStats/ingestionJobSpec.yaml
```
{% endtab %}
{% endtabs %}

JobSpec yaml file has all the information regarding data format, input data location and pinot cluster coordinates. Note that this assumes that the controller is **RUNNING** to fetch the table config and schema. If not, you will have to configure the spec to point at their location. See [Pinot Ingestion Job](../../basics/data-import/batch-ingestion/) for more details.

### Load Data in Streaming

#### Kafka

{% tabs %}
{% tab title="Docker" %}
Run below command to stream JSON data into Kafka topic: **flights-realtime**

```
docker run \
  --network pinot-demo \
  --name=loading-airlineStats-data-to-kafka \
  ${PINOT_IMAGE} StreamAvroIntoKafka \
  -avroFile examples/stream/airlineStats/sample_data/airlineStats_data.avro \
  -kafkaTopic flights-realtime -kafkaBrokerList kafka:9092 -zkAddress pinot-zookeeper:2181/kafka
```
{% endtab %}

{% tab title="Using launcher scripts" %}
Run below command to stream JSON data into Kafka topic: **flights-realtime**

```
bin/pinot-admin.sh StreamAvroIntoKafka \
  -avroFile examples/stream/airlineStats/sample_data/airlineStats_data.avro \
  -kafkaTopic flights-realtime -kafkaBrokerList localhost:19092 -zkAddress localhost:2191/kafka
```
{% endtab %}
{% endtabs %}
