---
description: Ingestion job specification reference.
---

# Ingestion Job Specification

This page keeps the job-spec overview and the full property matrix on a single page.

The ingestion job spec is used while generating, running, and pushing segments from the input files.

The Job spec can be in either YAML or JSON format (0.5.0 onwards). Property names remain the same in both formats.

To use the JSON format, add the property`job-spec-format=json`in the properties file while launching the ingestion job. The properties file can be passed as follows

```
pinot-admin.sh LaunchDataIngestionJob \
-jobSpecFile /path/to/job_spec.json \
-propertyFile /path/to/job.properties
```

## Template your job spec file

Users are allowed to define some variables in the job spec file to make it a template then passing the variables at runtime.

Templating is based on [Groovy SimpleTemplateEngine](https://docs.groovy-lang.org/docs/next/html/documentation/template-engines.html).

E.g. users can specify below in the job spec file:

```
inputDirURI: 'file:///path/to/input/${year}/${month}/${day}/${hour}'
```

The values for the template strings in the jobSpecFile can be passed in one of the following three ways mentioned in their order of precedence, for same key, 1 will override 2 will override 3.

1. Values from the `-values` array passed from the Cmd Line. See [Launch Data Ingestion Job](../../operate-pinot/cli.md#launch-data-ingestion-job)
2. Values from the environment variables
3. Values from the propertyFile

Still take above `inputDirURI` as example,

We can define a `job.config` file with below content:

```
year=2020
month=05
day=01
hour=00
```

Above properties can be override by environment variables

```
export month=06
export day=02
export hour=03
```

From the command line, user can further override those keys using flag `-values`,

```bash
pinot-admin.sh LaunchDataIngestionJob \
-jobSpecFile /path/to/job_spec.json \
-propertyFile job.confg \
-values day=03 hour=04
```

After that the real ingestion spec passed to ingestion job will have `inputDirURI` as `'file:///path/to/input/2020/06/03/04'`

## Ingestion Job Spec

The following configurations are supported by Pinot

### Top-Level Spec

| Property                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| executionFrameworkSpec   | Contains config related to the executor to use to ingest data. See [Execution Framework Spec](job-specification.md#execution-framework-spec)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| jobType | Type of job to execute. The following types are supported - `SegmentCreation` - `SegmentMetadataPush` - `SegmentTarPush` - `SegmentUriPush` - `SegmentCreationAndMetadataPush`: (Recommended for production environments where Pinot deep store is configured): Use this job to bypass the controller, and send the segment payload directly to the data store. - `SegmentCreationAndUriPush`: (Alternative option if Pinot deep store is configured) Use this job to create the segment on the deep store, push the URI to the controller to download the segment, extract metadata from the URI, and copy the data to deep store. - `SegmentCreationAndTarPush`: If you use Network File System (NFS) or something that sits behind a controller, and are unable to externally copy segments to the data store, use this job to push the segment payload. **Note:** For production environments where Pinot Deep Store is configured, it's recommended to use **SegmentCreationAndMetadataPush** |
| inputDirURI              | Absolute Path along with scheme of the directory containing all the files to be ingested, e.g. `s3://bucket/path/to/input`, `/path/to/local/input`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| includeFileNamePattern | Only Files matching this pattern will be included from `inputDirURI`. Both `glob` and `regex` patterns are supported. Examples: Use `'glob:`*`.avro'`or `'regex:^.`*`.(avro)$'` to include all avro files one level deep in the `inputDirURI`. Alternatively, use `'glob:*`*`/`*`.avro'` to include all the avro files in `inputDirURI` as well as its subdirectories - bear in mind that, with this approach, the pattern needs to match the absolute path. You can use [Glob tool](https://www.digitalocean.com/community/tools/glob) or [Regex Tool ](https://www.regextester.com)to test out your patterns. |
| excludeFileNamePattern   | Exclude file name pattern, supported glob pattern. Similar usage as `includeFilePatternName`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| searchRecursively        | Set to `true` to explicitly search input files recursively from inputDirURI. It is set to `true` by default for now.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| outputDirURI             | Absolute Path along with scheme of the directory where to output all the segments.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| overwriteOutput          | Set to `true` to overwrite segments if already present in the output directory. Or set to`false`to raise exceptions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| pinotFSSpecs             | List of all the filesystems to be used for ingestions. You can mention multiple values in case input and output directories are present in different filesystems. For more details, scroll down to [Pinot FS Spec](job-specification.md#pinot-fs-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| tableSpec                | Defines table name and where to fetch corresponding table config and table schema. For more details, scroll down to [Table Spec](job-specification.md#table-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| recordReaderSpec         | Parser to use to read and decode input data. For more details, scroll down to [Record Reader Spec](job-specification.md#record-reader-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| segmentNameGeneratorSpec | Defines how the names of the segments will be. For more details, scroll down to [Segment Name Generator Spec](job-specification.md#segment-name-generator-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| pinotClusterSpecs        | Defines the Pinot Cluster Access Point. For more details, scroll down to [Pinot Cluster Spec](job-specification.md#pinot-cluster-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| pushJobSpec              | Defines segment push job-related configuration. For more details, scroll down to [Push Job Spec](job-specification.md#push-job-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

#### Example

```
executionFrameworkSpec:
  name: 'spark'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentUriPushJobRunner'
  segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentMetadataPushJobRunner'
  extraConfigs:
    stagingDir: hdfs://examples/batch/airlineStats/staging

# Recommended to set jobType to SegmentCreationAndMetadataPush for production environments where Pinot Deep Store is configured
jobType: SegmentCreationAndTarPush

inputDirURI: 'examples/batch/airlineStats/rawdata'
includeFileNamePattern: 'glob:**/*.avro'
searchRecursively: true
outputDirURI: 'hdfs:///examples/batch/airlineStats/segments'
overwriteOutput: true
pinotFSSpecs:
  - scheme: hdfs
    className: org.apache.pinot.plugin.filesystem.HadoopPinotFS
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS
recordReaderSpec:
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

### Execution Framework Spec

The configs specify the execution framework to use to ingest data. Check out [Batch Ingestion](../../build-with-pinot/ingestion/batch-ingestion) for configs related to all the supported frameworks

| Property                              | Description                                                                                                                          |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| name                                  | name of the execution framework. can be one of `spark,hadoop or standalone`                                                          |
| segmentGenerationJobRunnerClassName   | The class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface to run the segment generation job |
| segmentTarPushJobRunnerClassName      | The class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface to push the segment TAR file      |
| segmentUriPushJobRunnerClassName      | The class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface to send segment URI               |
| segmentMetadataPushJobRunnerClassName | The class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface to send segment Metadata          |
| extraConfigs                          | Key-value pairs of configs related to the framework of the executions                                                                |

#### Example

```
executionFrameworkSpec:
    name: 'standalone'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
    segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentMetadataPushJobRunner'
```

### Pinot FS Spec

| field     | description                                                                                                                                                                                                                                   |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| schema    | used to identify a PinotFS. E.g. local, hdfs, dbfs, etc                                                                                                                                                                                       |
| className | Class name used to create the PinotFS instance. E.g. `org.apache.pinot.spi.filesystem.LocalPinotFS` is used for local filesystem `org.apache.pinot.plugin.filesystem.HadoopPinotFS` is used for HDFS |
| configs   | configs used to init PinotFS instance                                                                                                                                                                                                         |

### Table Spec

Table spec is used to specify the table in which data should be populated along with schema.

| Property       | Description                                                                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tableName      | name of the table in which to populate the data                                                                                                           |
| schemaURI      | location from which to read the schema for the table. Supports both [File systems](../../build-with-pinot/ingestion/file-systems/) as well as `HTTP` URI |
| tableConfigURI | location from which to read the config for the table. Supports both [File systems](../../build-with-pinot/ingestion/file-systems/) as well as `HTTP` URI |

#### Example

```
tableSpec:
  tableName: 'airlineStats'
  schemaURI: 'http://localhost:9000/tables/airlineStats/schema'
  tableConfigURI: 'http://localhost:9000/tables/airlineStats'
```

### Record Reader Spec

| field           | description                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dataFormat      | Record data format, e.g. 'avro', 'parquet', 'orc', 'csv', 'json', 'thrift' etc.                                                                                                                                                                                                                                                                                                                                                                          |
| className | Corresponding RecordReader class name. E.g. org.apache.pinot.plugin.inputformat.avro.AvroRecordReader org.apache.pinot.plugin.inputformat.csv.CSVRecordReader org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader org.apache.pinot.plugin.inputformat.json.JSONRecordReader org.apache.pinot.plugin.inputformat.orc.ORCRecordReader org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReader |
| configClassName | Corresponding RecordReaderConfig class name, it's mandatory for CSV and Thrift file format. E.g. org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReaderConfig |
| configs         | Used to init RecordReaderConfig class name, this config is required for CSV and Thrift data format.                                                                                                                                                                                                                                                                                                                                                      |

### Segment Name Generator Spec

| Property                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **type** | The type of name generator to use. If not specified, Pinot infers an appropriate type from the segment generator config. Supported values are `simple`, `normalizedDate`, `fixed`, `inputFile`, and `uploadedRealtime`. Use `uploadedRealtime` when you are generating externally partitioned segments that will be uploaded into a realtime upsert table. |
| **configs**                      | Configs to init SegmentNameGenerator                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| segment.name                     | For `fixed` SegmentNameGenerator. Explicitly set the segment name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| segment.name.postfix | For `simple` SegmentNameGenerator. Postfix will be appended to all the segment names. For `uploadedRealtime`, this is an optional suffix override; if omitted, Pinot uses the segment sequence id. |
| segment.name.prefix | For `normalizedDate` and `uploadedRealtime` SegmentNameGenerator. The prefix will be prepended to generated segment names. `uploadedRealtime` requires a non-empty prefix. |
| exclude.sequence.id | Whether to include sequence ids in segment name. Needed when there are multiple segments for the same time range. |
| use.global.directory.sequence.id | Assign sequence ids to input files based on all input files under the directory. Set to `false` to use local directory sequence id. This is useful when generating multiple segments for multiple days. In that case, each of the days will start from sequence id 0. |
| append.uuid.to.segment.name      | If the input data doesn't contain a time column, set this to `true` to generate unique segment names. Can be used with any name generator type.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| file.path.pattern                | For `inputFile`, a Java regular expression used to match against the input file URI. e.g. `'.+/(.+).gz'` to extract file name from a .gz file without the extension                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| segment.name.template | For `inputFile` , the string template that should be used to substitute extracted fileName. Currently only supports `${filePathPattern:<match group>}` |
| segment.partitionId | For `uploadedRealtime`, the external partition id to encode in the generated segment name. This value is required. |
| segment.uploadTimeMs | For `uploadedRealtime`, the upload timestamp to encode in the generated segment name. If omitted, Pinot uses the segment creation time. |

#### Example

```
segmentNameGeneratorSpec:
  type: normalizedDate
  configs:
    segment.name.prefix: 'airlineStats_batch'
    exclude.sequence.id: true
```

To set the segment name to be the same as the input file name (without the trailing `.gz`), use:

```
segmentNameGeneratorSpec:
  type: inputFile
  configs:
    file.path.pattern: '.+/(.+)\.gz'
    segment.name.template: '\${filePathPattern:\1}'
```

Note that `$` in the yaml file must be escaped, since Pinot uses Groovy's SimpleTemplateEngine to process the yaml file, and a raw `$` is treated as a template specifier.

To generate externally partitioned uploaded-realtime segments for a realtime upsert table, use:

```
segmentNameGeneratorSpec:
  type: uploadedRealtime
  configs:
    segment.name.prefix: 'spark'
    segment.partitionId: 1
    segment.uploadTimeMs: 1717701199455
```

Pinot encodes uploaded realtime segments as `{prefix}__{tableName}__{partitionId}__{uploadTimeMs}__{suffixOrSequenceId}` so the uploaded segment can be assigned consistently with the external partitioning scheme.

### Pinot Cluster Spec

| Property      | Description                                                |
| ------------- | ---------------------------------------------------------- |
| controllerURI | URI to use to fetch table/schema information and push data |

#### Example

```
pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'
```

### Push Job Spec

| Property                | Description                                                                                                                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pushAttempts            | Number of attempts for push job. Default is 1, which means no retry                                                                                                                                                                         |
| pushParallelism         | Workers to use for push job. Default is 1                                                                                                                                                                                                   |
| pushRetryIntervalMillis | Time in milliseconds to wait for between retry attempts Default is 1 second.                                                                                                                                                                |
| segmentUriPrefix        | append this string before the path of the push destination. Generally, it is the scheme of the filesystem e.g. `s3://` , `file://` etc.                                                                                                     |
| segmentUriSuffix        | append this string after the path of the push destination.                                                                                                                                                                                  |
| pushFileNamePattern     | segment name pattern for which segments to push, supported glob and regex patterns. E.g. 'glob:\*\*2023-01\*' will push all the segment files under the outputDirURI whose names contain '2023-01'.                                         |
| batchSegmentUpload      | Boolean field for which the default value is `false`. When the value is set to `true` segments are uploaded in batch mode which is faster than uploading segments one after the other. Works when the jobType is set to SegmentMetadataPush |

#### Example

```
pushJobSpec:
  pushParallelism: 2
  pushAttempts: 2
  pushRetryIntervalMillis: 1000
  segmentUriPrefix : 'file://'
  segmentUriSuffix : my-dir/
  pushFileNamePattern : glob:\*\*2023-01\*
```
