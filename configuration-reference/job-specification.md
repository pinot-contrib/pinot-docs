# Ingestion Job Spec

The ingestion job spec is used while generating, running, and pushing segments from the input files.

The Job spec can be in either YAML or JSON format (0.5.0 onwards). Property names remain the same in both formats.

To use the JSON format, add the property`job-spec-format=json`in the properties file while launching the ingestion job. The properties file can be passed as follows

```
pinot-admin.sh LaunchDataIngestionJob -jobSpecFile /path/to/job_spec.json -propertyFile /path/to/job.properties
```

The values for the template strings in the jobSpecFile can be passed in one of the following three ways mentioned in their order of precedence,

1. Values from the -values array passed See [Launch Data Ingestion Job](../operators/cli.md#launch-data-ingestion-job)
2. Values from the environment variable
3. Values from the propertyFile

The following configurations are supported by Pinot

### Top-Level Spec

| Property                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| executionFrameworkSpec   | Contains config related to the executor to use to ingest data. See [Execution Framework Spec](job-specification.md#execution-framework-spec)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| jobType                  | <p>Type of job to execute. The following types are supported</p><ul><li><code>SegmentCreation</code></li><li><code>SegmentTarPush</code></li><li><code>SegmentUriPush</code></li><li><code>SegmentMetadataPush</code></li><li><code>SegmentCreationAndTarPush</code></li><li><code>SegmentCreationAndUriPush</code></li><li><code>SegmentCreationAndMetadataPush</code></li></ul><p><strong>Note:</strong> For production environments where Pinot Deep Store is configured, it's recommended to use <strong>SegmentCreationAndMetadataPush</strong></p>                                                                                                                                                                                                                                                         |
| inputDirURI              | Absolute Path along with scheme of the directory containing all the files to be ingested, e.g. `s3://bucket/path/to/input`, `/path/to/local/input`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| includeFileNamePattern   | <p>Only Files matching this pattern will be included from <code>inputDirURI</code>. Both <code>glob</code> and <code>regex</code> patterns are supported.</p><p>Examples:</p><p>Use <code>'glob:</code><em><code>.avro'</code>or <code>'regex:^.</code></em><code>.(avro)$'</code> to include all avro files one level deep in the <code>inputDirURI</code>.</p><p>Alternatively, use <code>'glob:*</code><em><code>/</code></em><code>.avro'</code> to include all the avro files in <code>inputDirURI</code> as well as its subdirectories - bear in mind that, with this approach, the pattern needs to match the absolute path. You can use <a href="https://www.digitalocean.com/community/tools/glob">Glob tool</a> or <a href="https://www.regextester.com">Regex Tool </a>to test out your patterns.</p> |
| excludeFileNamePattern   | Exclude file name pattern, supported glob pattern. Similar usage as `includeFilePatternName`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| searchRecursively        | Set to `true` to explicitly search input files recursively from inputDirURI. It is set to `true` by default for now.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| outputDirURI             | Absolute Path along with scheme of the directory where to output all the segments.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| overwriteOutput          | Set to `true` to overwrite segments if already present in the output directory. Or set to`false`to raise exceptions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| pinotFSSpecs             | List of all the filesystems to be used for ingestions. You can mention multiple values in case input and output directories are present in different filesystems. For more details, scroll down to [Pinot FS Spec](job-specification.md#pinot-fs-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| tableSpec                | Defines table name and where to fetch corresponding table config and table schema. For more details, scroll down to [Table Spec](job-specification.md#table-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| recordReaderSpec         | Parser to use to read and decode input data. For more details, scroll down to [Record Reader Spec](job-specification.md#record-reader-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| segmentNameGeneratorSpec | Defines how the names of the segments will be. For more details, scroll down to [Segment Name Generator Spec](job-specification.md#segment-name-generator-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| pinotClusterSpecs        | Defines the Pinot Cluster Access Point. For more details, scroll down to [Pinot Cluster Spec](job-specification.md#pinot-cluster-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| pushJobSpec              | Defines segment push job-related configuration. For more details, scroll down to [Push Job Spec](job-specification.md#push-job-spec).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

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

The configs specify the execution framework to use to ingest data. Check out [Batch Ingestion](../basics/data-import/batch-ingestion/) for configs related to all the supported frameworks

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
| className | <p>Class name used to create the PinotFS instance. E.g.</p><p><code>org.apache.pinot.spi.filesystem.LocalPinotFS</code> is used for local filesystem</p><p><code>org.apache.pinot.plugin.filesystem.HadoopPinotFS</code> is used for HDFS</p> |
| configs   | configs used to init PinotFS instance                                                                                                                                                                                                         |

### Table Spec

Table spec is used to specify the table in which data should be populated along with schema.

| Property       | Description                                                                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| tableName      | name of the table in which to populate the data                                                                                                    |
| schemaURI      | location from which to read the schema for the table. Supports both [File systems](../basics/data-import/pinot-file-system/) as well as `HTTP` URI |
| tableConfigURI | location from which to read the config for the table. Supports both [File systems](../basics/data-import/pinot-file-system/) as well as `HTTP` URI |

#### Example

```
tableSpec:
  tableName: 'airlineStats'
  schemaURI: 'http://localhost:9000/tables/airlineStats/schema'
  tableConfigURI: 'http://localhost:9000/tables/airlineStats'
​
```

### Record Reader Spec

| field           | description                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dataFormat      | Record data format, e.g. 'avro', 'parquet', 'orc', 'csv', 'json', 'thrift' etc.                                                                                                                                                                                                                                                                                                                                                                          |
| className       | <p>Corresponding RecordReader class name. E.g.</p><p>org.apache.pinot.plugin.inputformat.avro.AvroRecordReader</p><p>org.apache.pinot.plugin.inputformat.csv.CSVRecordReader</p><p>org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader</p><p>org.apache.pinot.plugin.inputformat.json.JSONRecordReader</p><p>org.apache.pinot.plugin.inputformat.orc.ORCRecordReader</p><p>org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReader</p> |
| configClassName | <p>Corresponding RecordReaderConfig class name, it's mandatory for CSV and Thrift file format. E.g.</p><p>org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig</p><p>org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReaderConfig</p>                                                                                                                                                                                                    |
| configs         | Used to init RecordReaderConfig class name, this config is required for CSV and Thrift data format.                                                                                                                                                                                                                                                                                                                                                      |

### Segment Name Generator Spec

| Property                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **type**                         | <p>The type of name generator to use. If not specified, an appropriate type will be inferred based on segment generator config properties. The following values are supported -</p><ul><li><code>simple</code> - this is the default spec.</li><li><code>normalizedDate</code> - use this type when the time column in your data is in the String format instead of epoch time.</li><li><code>fixed</code> - configure the segment name by the user.</li><li><code>inputFile</code> - supports naming the resulting segment file based on the input file name &#x26; path. Use this if your table doesn't have a time column. Ensure that input file names are unique though otherwise will lead to several issues.</li></ul> |
| **configs**                      | Configs to init SegmentNameGenerator                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| segment.name                     | For `fixed` SegmentNameGenerator. Explicitly set the segment name.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| segment.name.postfix             | <p>For <code>simple</code> SegmentNameGenerator.<br>Postfix will be appended to all the segment names.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| segment.name.prefix              | <p>For <code>normalizedDate</code> SegmentNameGenerator.<br>The Prefix will be prepended to all the segment names.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| exclude.sequence.id              | <p>Whether to include sequence ids in segment name.</p><p>Needed when there are multiple segments for the same time range.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| use.global.directory.sequence.id | <p>Assign sequence ids to input files based on all input files under the directory.</p><p>Set to <code>false</code> to use local directory sequence id. This is useful when generating multiple segments for multiple days. In that case, each of the days will start from sequence id 0.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| append.uuid.to.segment.name      | If the input data doesn't contain a time column, set this to `true` to generate unique segment names. Can be used with any name generator type.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| file.path.pattern                | For `inputFile`, a Java regular expression used to match against the input file URI. e.g. `'.+/(.+).gz'` to extract file name from a .gz file without the extension                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| segment.name.template            | For `inputFile` , the string template that should be used to substitute extracted fileName. Currently only supports `${filePathPattern:<match group>}`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

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

| Property                | Description                                                                                                                                                                                         |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pushAttempts            | Number of attempts for push job. Default is 1, which means no retry                                                                                                                                 |
| pushParallelism         | Workers to use for push job. Default is 1                                                                                                                                                           |
| pushRetryIntervalMillis | Time in milliseconds to wait for between retry attempts Default is 1 second.                                                                                                                        |
| segmentUriPrefix        | append this string before the path of the push destination. Generally, it is the scheme of the filesystem e.g. `s3://` , `file://` etc.                                                             |
| segmentUriSuffix        | append this string after the path of the push destination.                                                                                                                                          |
| pushFileNamePattern     | segment name pattern for which segments to push, supported glob and regex patterns. E.g. 'glob:\*\*2023-01\*' will push all the segment files under the outputDirURI whose names contain '2023-01'. |

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
