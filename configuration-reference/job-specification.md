# Ingestion Job Spec

The ingestion job spec is used while generating, running, and pushing segments from the input files. 

The Job spec can be in either YAML or JSON format \(0.5.0 onwards\). Property names remain the same in both formats.

To use the JSON format, add the property`job-spec-format=json`in the properties file while launching the ingestion job.  The properties file can be passed as follows 

```text
pinot-admin.sh LaunchDataIngestionJob -jobSpecFile /path/to/job_spec.json -propertyFile /path/to/job.properties
```

The following configurations are supported by Pinot

### Top Level Spec

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">executionFrameworkSpec</td>
      <td style="text-align:left">Contains config related to the executor to use to ingest data. See <a href="job-specification.md#execution-framework-spec">Execution Framework Spec</a>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">jobType</td>
      <td style="text-align:left">
        <p>Type of job to execute. The following types are supported</p>
        <ul>
          <li><code>SegmentCreation - </code>
          </li>
          <li><code>SegmentTarPush</code>
          </li>
          <li><code>SegmentUriPush</code>
          </li>
          <li><code>SegmentMetadataPush</code>
          </li>
          <li><code>SegmentCreationAndTarPush</code>
          </li>
          <li><code>SegmentCreationAndUriPush</code>
          </li>
          <li><code>SegmentCreationAndMetadataPush</code>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">inputDirURI</td>
      <td style="text-align:left">Absolute Path along with scheme of the directory containing all the files
        to be ingested, e.g. <code>s3://bucket/path/to/input</code>, <code>/path/to/local/input </code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">includeFileNamePattern</td>
      <td style="text-align:left">
        <p>Include file name pattern, supported glob and regex patterns. E.g.</p>
        <p><code>&apos;glob:*.avro&apos;</code>or <code>&apos;regex:^.*\.(avro)$&apos;</code> will
          include all avro files just under the inputDirURI, not sub directories</p>
        <p><code>&apos;glob:**/*.avro&apos;</code> will include all the avro files
          under inputDirURI recursively.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">excludeFileNamePattern</td>
      <td style="text-align:left">Exclude file name pattern, supported glob pattern. Similar usage as <code>includeFilePatternName</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">outputDirURI</td>
      <td style="text-align:left">Absolute Path along with scheme of the directory where to output all the
        segments.</td>
    </tr>
    <tr>
      <td style="text-align:left">overwriteOutput</td>
      <td style="text-align:left">Set to <code>true</code> to overwrite segments if already present in the
        output directory. Or set to<code>false</code>to raise exceptions.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinotFSSpecs</td>
      <td style="text-align:left">List of all the filesystems to be used for ingestions. You can mention
        multiple values in case input and output directories are present in different
        filesystems. For more details, scroll down to <a href="job-specification.md#pinot-fs-spec">Pinot FS Spec</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">tableSpec</td>
      <td style="text-align:left">Defines table name and where to fetch corresponding table config and table
        schema. For more details, scroll down to <a href="job-specification.md#table-spec">Table Spec</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">recordReaderSpec</td>
      <td style="text-align:left">Parser to use to read and decode input data. For more details, scroll
        down to <a href="job-specification.md#record-reader-spec">Record Reader Spec</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">segmentNameGeneratorSpec</td>
      <td style="text-align:left">Defines how the names of the segments will be. For more details, scroll
        down to <a href="job-specification.md#segment-name-generator-spec">Segment Name Generator Spec</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinotClusterSpecs</td>
      <td style="text-align:left">Defines the Pinot Cluster Access Point. For more details, scroll down
        to <a href="job-specification.md#pinot-cluster-spec">Pinot Cluster Spec</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">pushJobSpec</td>
      <td style="text-align:left">Defines segment push job-related configuration. For more details, scroll
        down to <a href="job-specification.md#push-job-spec">Push Job Spec</a>.</td>
    </tr>
  </tbody>
</table>

#### Example

```text
executionFrameworkSpec:
  name: 'spark'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentUriPushJobRunner'
  extraConfigs:
    stagingDir: hdfs://examples/batch/airlineStats/staging
jobType: SegmentCreationAndTarPush
inputDirURI: 'examples/batch/airlineStats/rawdata'
includeFileNamePattern: 'glob:**/*.avro'
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



| Property | Description |
| :--- | :--- |
| name | name of the execution framework. can be one of `spark,hadoop or standalone` |
| segmentGenerationJobRunnerClassName | The class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentGenerationJobRunner interface to run the segment generation job |
| segmentTarPushJobRunnerClassName | The class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentTarPushJobRunner interface to push the segment TAR file |
| segmentUriPushJobRunnerClassName | The class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentUriPushJobRunner interface to send segment URI |
| segmentMetadataPushJobRunnerClassName | The class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentMetadataPushJobRunner interface to send segment Metadata |
| extraConfigs | Key-value pairs of configs related to the framework of the executions |

#### Example

```text
executionFrameworkSpec:
    name: 'standalone'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
```

### Pinot FS Spec

<table>
  <thead>
    <tr>
      <th style="text-align:left">field</th>
      <th style="text-align:left">description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">schema</td>
      <td style="text-align:left">used to identify a PinotFS. E.g. local, hdfs, dbfs, etc</td>
    </tr>
    <tr>
      <td style="text-align:left">className</td>
      <td style="text-align:left">
        <p>Class name used to create the PinotFS instance. E.g.</p>
        <p> <code>org.apache.pinot.spi.filesystem.LocalPinotFS</code> is used for local
          filesystem</p>
        <p><code>org.apache.pinot.plugin.filesystem.HadoopPinotFS</code> is used for
          HDFS</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">configs</td>
      <td style="text-align:left">configs used to init PinotFS instance</td>
    </tr>
  </tbody>
</table>

### Table Spec

Table spec is used to specify the table in which  data should be populated along with schema.

| Property | Description |
| :--- | :--- |
| tableName | name of the table in which to populate the data |
| schemaURI | location from which to read the schema for the table. Supports both [File systems](../basics/data-import/pinot-file-system/) as well as `HTTP` URI  |
| tableConfigURI | location from which to read the config for the table. Supports both [File systems](../basics/data-import/pinot-file-system/) as well as `HTTP` URI  |

#### Example

```text
tableSpec:
  tableName: 'airlineStats'
  schemaURI: 'http://localhost:9000/tables/airlineStats/schema'
  tableConfigURI: 'http://localhost:9000/tables/airlineStats'
​
```

### Record Reader Spec

<table>
  <thead>
    <tr>
      <th style="text-align:left">field</th>
      <th style="text-align:left">description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">dataFormat</td>
      <td style="text-align:left">Record data format, e.g. &apos;avro&apos;, &apos;parquet&apos;, &apos;orc&apos;,
        &apos;csv&apos;, &apos;json&apos;, &apos;thrift&apos; etc.</td>
    </tr>
    <tr>
      <td style="text-align:left">className</td>
      <td style="text-align:left">
        <p>Corresponding RecordReader class name. E.g.</p>
        <p>org.apache.pinot.plugin.inputformat.avro.AvroRecordReader</p>
        <p>org.apache.pinot.plugin.inputformat.csv.CSVRecordReader</p>
        <p>org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader</p>
        <p>org.apache.pinot.plugin.inputformat.json.JSONRecordReader</p>
        <p>org.apache.pinot.plugin.inputformat.orc.ORCRecordReader</p>
        <p>org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReader</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">configClassName</td>
      <td style="text-align:left">
        <p>Corresponding RecordReaderConfig class name, it&apos;s mandatory for CSV
          and Thrift file format. E.g.</p>
        <p>org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig</p>
        <p>org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReaderConfig</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">configs</td>
      <td style="text-align:left">Used to init RecordReaderConfig class name, this config is required for
        CSV and Thrift data format.</td>
    </tr>
  </tbody>
</table>

### Segment Name Generator Spec

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><b>type</b>
      </td>
      <td style="text-align:left">
        <p>the type of name generator to use. Following values are supported -</p>
        <ul>
          <li><code>simple</code> - this is the default spec.</li>
          <li><code>normalizedDate</code> - use this type when the time column in your
            data is in the String format instead of epoch time.</li>
          <li><code>fixed</code> - configure the segment name by the user.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>configs</b>
      </td>
      <td style="text-align:left">Configs to init SegmentNameGenerator</td>
    </tr>
    <tr>
      <td style="text-align:left">segment.name</td>
      <td style="text-align:left">For <code>fixed</code> SegmentNameGenerator. Explicitly set the segment
        name.</td>
    </tr>
    <tr>
      <td style="text-align:left">segment.name.postfix</td>
      <td style="text-align:left">For <code>simple</code> SegmentNameGenerator.
        <br />Postfix will be appended to all the segment names.</td>
    </tr>
    <tr>
      <td style="text-align:left">segment.name.prefix</td>
      <td style="text-align:left">For <code>normalizedDate</code> SegmentNameGenerator.
        <br />The Prefix will be prepended to all the segment names.</td>
    </tr>
    <tr>
      <td style="text-align:left">exclude.sequence.id</td>
      <td style="text-align:left">
        <p>Whether to include sequence ids in segment name.</p>
        <p>Needed when there are multiple segments for the same time range.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">use.local.directory.sequence.id</td>
      <td style="text-align:left">
        <p>Assign sequence ids to input files based on each local directory level.</p>
        <p>This is useful when generating multiple segments for multiple days.</p>
        <p>In that case, each of the days will start from sequence id 0.</p>
      </td>
    </tr>
  </tbody>
</table>

#### Example

```text
segmentNameGeneratorSpec:
  type: normalizedDate
  configs:
    segment.name.prefix: 'airlineStats_batch'
    exclude.sequence.id: true
```

### Pinot Cluster Spec

| Property | Description |
| :--- | :--- |
| controllerURI | URI to use to fetch table/schema information and push data |

#### Example

```text
pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'
```

### Push Job Spec

| Property | Description |
| :--- | :--- |
| pushAttempts | Number of attempts for push job. Default is 1, which means no retry |
| pushParallelism | Workers to use for push job. Default is 1 |
| pushRetryIntervalMillis | Time in milliseconds to wait for between retry attempts Default is 1 second.  |
| segmentUriPrefix | append this string before the path of the push destination. Generally, it is the scheme of the filesystem e.g. `s3://` , `file://` etc. |
| segmentUriSuffix | append this string after the path of the push destination.  |

#### Example

```text
pushJobSpec:
  pushParallelism: 2
  pushAttempts: 2
  pushRetryIntervalMillis: 1000
  segmentUriPrefix : 'file://'
  segmentUriSuffix : my-dir/

```

