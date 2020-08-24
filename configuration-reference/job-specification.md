# Ingestion Job Spec

Ingestion job spec is used while generating, running and pushing segments from the input files. 

The Job spec can be in either YAML or JSON format \(0.5.0 onwards\) . Property names remain same in both the formats.

To use the JSON format, add `job-spec-format=json` property in the properties file while launching ingestions job.  The properties file can be passed as follows 

```text
pinot-admin.sh LaunchDataIngestionJob -jobSpecFile /path/to/job_spec.json -propertyFile /path/to/job.properties
```

The following configurations are supported by Pinot



<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">executionFrameworkSpec</td>
      <td style="text-align:left">Contains config related to the executor to use to ingest data. See <a href="job-specification.md#execution-config">Execution Config</a>
      </td>
      <td style="text-align:left"></td>
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
          <li><code>SegmentCreationAndTarPush</code>
          </li>
          <li><code>SegmentCreationAndUriPush</code>
          </li>
        </ul>
      </td>
      <td style="text-align:left"><code>jobType:  SegmentCreationAndTarPush</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">inputDirURI</td>
      <td style="text-align:left">Absolute Path along with scheme of the directory containing all the files
        to be ingested,</td>
      <td style="text-align:left">
        <p><code>inputDirURI: s3://bucket/path/to/input</code>
        </p>
        <p></p>
        <p><code>inputDirURI: /path/to/local/input</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">includeFileNamePattern</td>
      <td style="text-align:left">Files to include from the input dir. Supports both <code>glob</code> and <code>regex</code>
      </td>
      <td style="text-align:left">
        <p><code>includeFileNamePattern: glob:**/*.csv</code>
        </p>
        <p></p>
        <p><code>includeFileNamePattern: regex:^.*\.(csv)$</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">excludeFileNamePattern</td>
      <td style="text-align:left">Files to exclude from the input dir. Supports both <code>glob</code> and <code>regex</code>
      </td>
      <td style="text-align:left">
        <p><code>excludeFileNamePattern: glob:**/*.csv</code>
        </p>
        <p></p>
        <p><code>excludeFileNamePattern: regex:^.*\.(csv)$</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">outputDirURI</td>
      <td style="text-align:left">Absolute Path along with scheme of the directory where to output all the
        segments.</td>
      <td style="text-align:left">
        <p><code>ouputDirURI: s3://bucket/path/to/output</code>
        </p>
        <p></p>
        <p><code>ouputDirURI: /path/to/local/ouptut</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">overwriteOutput</td>
      <td style="text-align:left">Set to <code>true</code> to overwrite segments if already present in output
        directory, <code>false</code> otherwise</td>
      <td style="text-align:left"><code>overwriteOutput: true</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pinotFSSpecs</td>
      <td style="text-align:left">List of all the filesystems to be used for ingestions. You can mention
        multiple values in case input and output directories are present in different
        filesystems.</td>
      <td style="text-align:left">See <a href="../basics/data-import/pinot-file-system/">File systems</a> for
        all the supported filesystems along with their configs</td>
    </tr>
    <tr>
      <td style="text-align:left">tableSpec</td>
      <td style="text-align:left">Configs related to the table in which to populate data.</td>
      <td style="text-align:left">See <a href="job-specification.md#table-spec">Table Spec</a>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">recordReaderSpec</td>
      <td style="text-align:left">Parser to use to read and decode input data.</td>
      <td style="text-align:left">See <a href="../basics/data-import/pinot-input-formats.md">Input formats</a> for
        all the supported formats along with configurations</td>
    </tr>
    <tr>
      <td style="text-align:left">segmentNameGeneratorSpec</td>
      <td style="text-align:left">Configs to use while naming segment files.</td>
      <td style="text-align:left">See <a href="job-specification.md#segment-name-generator-spec">Segment Name Generator Spec</a> for
        details.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinotClusterSpecs</td>
      <td style="text-align:left">Cluster to which the job request are to be sent.</td>
      <td style="text-align:left">See <a href="job-specification.md#pinot-cluster-spec">Pinot Cluster Spec</a>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pushJobSpec</td>
      <td style="text-align:left">Configuration for the job that will push the segments to desired file
        systems.</td>
      <td style="text-align:left">See <a href="job-specification.md#push-job-spec">Push Job Spec</a>
      </td>
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

### Execution Config

The configs specifies the execution framework to use to ingest data. Check out [Batch Ingestion](../basics/data-import/batch-ingestion/) for configs related to all the supported frameworks



| Property | Description |
| :--- | :--- |
| name | name of the execution framework. can be one of `spark,hadoop or standalone` |
| segmentGenerationJobRunnerClassName | The name of class of the framework to run the job |
| segmentTarPushJobRunnerClassName | The name of class of the framework to push the TAR file |
| segmentUriPushJobRunnerClassName | The name of class of the framework to run the job |
| extraConfigs | Key-value pairs of configs related to the executions framework |

#### Example

```text
executionFrameworkSpec:
    name: 'standalone'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
```



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
      <td style="text-align:left">type</td>
      <td style="text-align:left">
        <p>the type of name generator to use. Following values are supported -</p>
        <ul>
          <li><code>simple</code> - this is the default spec.</li>
          <li><code>normalizedDate</code> - use this type when the time column in your
            data is in the String format instead of epoch time</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">configs</td>
      <td style="text-align:left">
        <p>Key-value pairs related to the name generator. Following configs are supported
          -</p>
        <ul>
          <li><code>segment.name.prefix</code>- prefix to use for segment name</li>
          <li><code>segment.name.postfix</code> - suffix to use for segment name</li>
          <li><code>exclude.sequence.id</code> - set to <code>true</code> to include the
            sequence id in segment name. <code>false</code> otherwise</li>
        </ul>
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

