---
description: >-
  Discover the segment component in Apache Pinot for efficient data storage and
  querying within Pinot clusters, enabling optimized data processing and
  analysis.
---

# Segment

Pinot has the concept of a [**table**](../), which is a logical abstraction to refer to a collection of related data. Pinot has a distributed architecture and scales horizontally. Pinot expects the size of a table to grow infinitely over time. In order to achieve this, the entire data needs to be distributed across multiple nodes.

Pinot achieves this by breaking the data into smaller chunks known as **segments** (similar to **shards/partitions** in relational databases). Segments can be seen as **time-based partitions**.

A **segment is a horizontal shard representing a chunk of table data** with some number of rows. The segment stores data for all columns of the table. Each segment packs the data in a **columnar fashion**, along with the **dictionaries and indices** for the columns. The segment is laid out in a columnar format so that it can be directly mapped into memory for serving queries.

Columns can be **single or multi-valued** and the following types are supported: **STRING, BOOLEAN, INT, LONG, FLOAT, DOUBLE, TIMESTAMP or BYTES**. Only single-valued **BIG\_DECIMAL** data type is supported.

Columns may be declared to be **metric or dimension (or specifically as a time dimension)** in the schema. Columns can have default null values. For example, the default null value of a integer column can be 0. The default value for bytes columns must be hex-encoded before it's added to the schema.

Pinot uses **dictionary encoding** to store values as a dictionary ID. Columns may be configured to be “no-dictionary” column in which case raw values are stored. Dictionary IDs are encoded using minimum number of bits for efficient storage (_e.g._ a column with a cardinality of 3 will use only 2 bits for each dictionary ID).

A **forward index** is built for each column and compressed for efficient memory use. In addition, you can optionally configure **inverted indices** for any set of columns. Inverted indices take up more storage, but improve query performance. Specialized indexes like **Star-Tree index** are also supported. For more details, see [Indexing](../../../indexing/).

## Creating a segment

Once the table is configured, we can load some data. Loading data involves generating pinot segments from raw data and pushing them to the pinot cluster. Data can be loaded in batch mode or streaming mode. For more details, see the[ ingestion overview](../../../../developers/advanced/data-ingestion.md) page.

### Load data in batch

#### **Prerequisites**

1. [Set up a cluster](../../cluster/#setup-a-pinot-cluster)
2. [Create broker and server tenants](../../cluster/tenant.md#creating-a-tenant)
3. [Create an offline table](../#offline-table-creation)

Below are instructions to generate and push segments to Pinot via standalone scripts. For a production setup, you should use frameworks such as Hadoop or Spark. For more details on setting up data ingestion jobs, see [Import Data.](https://docs.pinot.apache.org/basics/data-import)

#### Job Spec YAML

To generate a segment, we need to first create a job spec YAML file. This file contains all the information regarding data format, input data location, and pinot cluster coordinates. Note that this assumes that the controller is **RUNNING** to fetch the table config and schema. If not, you will have to configure the spec to point at their location. For full configurations, see [Ingestion Job Spec](../../../../configuration-reference/job-specification.md).

{% code title="job-spec.yml" %}
```yaml
executionFrameworkSpec:
  name: 'standalone'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'

jobType: SegmentCreationAndTarPush
inputDirURI: 'examples/batch/baseballStats/rawdata'
includeFileNamePattern: 'glob:**/*.csv'
excludeFileNamePattern: 'glob:**/*.tmp'
outputDirURI: 'examples/batch/baseballStats/segments'
overwriteOutput: true

pinotFSSpecs:
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS

recordReaderSpec:
  dataFormat: 'csv'
  className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
  configs:

tableSpec:
  tableName: 'baseballStats'
  schemaURI: 'http://localhost:9000/tables/baseballStats/schema'
  tableConfigURI: 'http://localhost:9000/tables/baseballStats'
  
segmentNameGeneratorSpec:

pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'

pushJobSpec:
  pushParallelism: 2
  pushAttempts: 2
  pushRetryIntervalMillis: 1000
```
{% endcode %}

#### Create and push segment

To create and push the segment in one go, use the following:

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

Alternately, you can separately create and then push, by changing the jobType to `SegmentCreation` or `SegmenTarPush`.

#### Templating Ingestion Job Spec

The Ingestion job spec supports templating with Groovy Syntax.

This is convenient if you want to generate one ingestion job template file and schedule it on a daily basis with extra parameters updated daily.

e.g. you could set `inputDirURI` with parameters to indicate the date, so that the ingestion job only processes the data for a particular date. Below is an example that templates the date for input and output directories.

```yaml
inputDirURI: 'examples/batch/airlineStats/rawdata/${year}/${month}/${day}'
outputDirURI: 'examples/batch/airlineStats/segments/${year}/${month}/${day}'
```

You can pass in arguments containing values for `${year}, ${month}, ${day}` when kicking off the ingestion job: `-values $param=value1 $param2=value2`...

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    --network=pinot-demo \
    --name pinot-data-ingestion-job \
    ${PINOT_IMAGE} LaunchDataIngestionJob \
    -jobSpecFile examples/docker/ingestion-job-specs/airlineStats.yaml
    -values year=2014 month=01 day=03
```
{% endtab %}
{% endtabs %}

This ingestion job only generates segments for date `2014-01-03`

### Load data in streaming

**Prerequisites**

1. [Set up a cluster](../../cluster/#setup-a-pinot-cluster)
2. [Create broker and server tenants](../../cluster/tenant.md#creating-a-tenant)
3. [Create a real-time table and set up a real-time stream](../#streaming-table-creation)

Below is an example of how to publish sample data to your stream. As soon as data is available to the real-time stream, it starts getting consumed by the real-time servers.

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
