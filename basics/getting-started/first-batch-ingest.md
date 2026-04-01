---
description: Import your first batch of data into Pinot and see it appear in the query console.
---

# First batch ingest

## Outcome

By the end of this page you will have imported CSV data into your `transcript` offline table and confirmed the rows are queryable.

## Prerequisites

* Completed [First table and schema](first-table-and-schema.md) -- the `transcript_OFFLINE` table must already exist.
* The sample CSV file at `/tmp/pinot-quick-start/rawdata/transcript.csv` from the previous step.
* For Docker users: set the `PINOT_VERSION` environment variable. See the [Version reference](pinot-versions.md) page.

## Steps

### 1. Understand batch ingestion

Batch ingestion reads data from files (CSV, JSON, Avro, Parquet, and others), converts them into Pinot segments, and pushes those segments to the cluster. A job specification YAML file tells Pinot where to find the input data, what format it is in, and where to send the finished segments.

### 2. Create the ingestion job spec

{% tabs %}
{% tab title="Local" %}
Create the file `/tmp/pinot-quick-start/batch-job-spec.yml`:

{% code title="/tmp/pinot-quick-start/batch-job-spec.yml" %}
```yaml
executionFrameworkSpec:
  name: 'standalone'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
jobType: SegmentCreationAndTarPush
inputDirURI: '/tmp/pinot-quick-start/rawdata/'
includeFileNamePattern: 'glob:**/*.csv'
outputDirURI: '/tmp/pinot-quick-start/segments/'
overwriteOutput: true
pinotFSSpecs:
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS
recordReaderSpec:
  dataFormat: 'csv'
  className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
  tableName: 'transcript'
  schemaURI: 'http://localhost:9000/tables/transcript/schema'
  tableConfigURI: 'http://localhost:9000/tables/transcript'
pinotClusterSpecs:
  - controllerURI: 'http://localhost:9000'
```
{% endcode %}
{% endtab %}

{% tab title="Docker" %}
When running inside Docker, the ingestion job container must reach the controller by its Docker network hostname, not `localhost`. Create the file `/tmp/pinot-quick-start/batch-job-spec.yml`:

{% code title="/tmp/pinot-quick-start/batch-job-spec.yml" %}
```yaml
executionFrameworkSpec:
  name: 'standalone'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
jobType: SegmentCreationAndTarPush
inputDirURI: '/tmp/pinot-quick-start/rawdata/'
includeFileNamePattern: 'glob:**/*.csv'
outputDirURI: '/tmp/pinot-quick-start/segments/'
overwriteOutput: true
pinotFSSpecs:
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS
recordReaderSpec:
  dataFormat: 'csv'
  className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
  tableName: 'transcript'
  schemaURI: 'http://pinot-controller:9000/tables/transcript/schema'
  tableConfigURI: 'http://pinot-controller:9000/tables/transcript'
pinotClusterSpecs:
  - controllerURI: 'http://pinot-controller:9000'
```
{% endcode %}

{% hint style="info" %}
Replace `pinot-controller` with the actual container name of your Pinot controller if you used a different name during setup.
{% endhint %}
{% endtab %}
{% endtabs %}

### 3. Run the ingestion job

{% tabs %}
{% tab title="Local" %}
```bash
bin/pinot-admin.sh LaunchDataIngestionJob \
    -jobSpecFile /tmp/pinot-quick-start/batch-job-spec.yml
```
{% endtab %}

{% tab title="Docker" %}
```bash
docker run --rm -ti \
    --network=pinot-demo \
    -v /tmp/pinot-quick-start:/tmp/pinot-quick-start \
    --name pinot-data-ingestion-job \
    apachepinot/pinot:${PINOT_VERSION} LaunchDataIngestionJob \
    -jobSpecFile /tmp/pinot-quick-start/batch-job-spec.yml
```
{% endtab %}
{% endtabs %}

The job reads the CSV file, builds a segment, and pushes it to the controller. You should see log output ending with a success message.

## Verify

1. Open the [Query Console](http://localhost:9000/query) in your browser.
2. Run the following query:

```sql
SELECT * FROM transcript
```

3. You should see **4 rows** returned, matching the CSV data you loaded:

<table>
  <thead>
    <tr>
      <th>studentID</th>
      <th>firstName</th>
      <th>lastName</th>
      <th>gender</th>
      <th>subject</th>
      <th>score</th>
      <th>timestampInEpoch</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>200</td>
      <td>Lucy</td>
      <td>Smith</td>
      <td>Female</td>
      <td>Maths</td>
      <td>3.8</td>
      <td>1570863600000</td>
    </tr>
    <tr>
      <td>200</td>
      <td>Lucy</td>
      <td>Smith</td>
      <td>Female</td>
      <td>English</td>
      <td>3.5</td>
      <td>1571036400000</td>
    </tr>
    <tr>
      <td>201</td>
      <td>Bob</td>
      <td>King</td>
      <td>Male</td>
      <td>Maths</td>
      <td>3.2</td>
      <td>1571900400000</td>
    </tr>
    <tr>
      <td>202</td>
      <td>Nick</td>
      <td>Young</td>
      <td>Male</td>
      <td>Physics</td>
      <td>3.6</td>
      <td>1572418800000</td>
    </tr>
  </tbody>
</table>

## Next step

Continue to [First stream ingest](first-stream-ingest.md) to learn how to set up real-time ingestion from Kafka.
