# SegmentGenerationAndPushTask

The SegmentGenerationAndPushTask is a Minion task that performs batch ingestion by reading raw data files from an input directory, converting each file into a Pinot segment, and pushing the segment to the cluster. This is the primary mechanism for ingesting batch data into offline tables using the Minion framework.

## Overview

The task reads files from a configured input directory (local filesystem, S3, GCS, HDFS, or other supported filesystems), generates one Pinot segment per input file, and pushes the resulting segments to the Pinot cluster. It tracks which files have already been ingested by storing the input file URI in segment metadata, preventing duplicate ingestion across scheduling runs.

## Key Features

- **Multi-filesystem support**: Read input data from local disk, S3, GCS, HDFS, ADLS, or any PinotFS-compatible filesystem
- **Multiple input formats**: Supports Avro, Parquet, CSV, JSON, ORC, Thrift, and other formats via the RecordReader plugin architecture
- **Duplicate prevention**: Tracks ingested files in segment metadata to skip already-processed files in APPEND mode
- **Configurable push modes**: Push segments via TAR upload, URI reference, or metadata-only push
- **File pattern filtering**: Include or exclude files using glob patterns
- **Automatic retry**: Built-in retry logic for segment push operations (5 attempts by default)
- **Parallel task execution**: Configure the maximum number of concurrent tasks per table

## Configuration

### Table Configuration

To enable SegmentGenerationAndPushTask, configure both `ingestionConfig` and `task` in the table config:

```json
{
  "tableName": "events_OFFLINE",
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "DAILY",
      "batchConfigMaps": [
        {
          "inputDirURI": "s3://my-bucket/rawdata/events/",
          "includeFileNamePattern": "glob:**/*.avro",
          "excludeFileNamePattern": "glob:**/*.tmp",
          "inputFormat": "avro",
          "input.fs.className": "org.apache.pinot.plugin.filesystem.S3PinotFS",
          "input.fs.prop.region": "us-west-2"
        }
      ]
    }
  },
  "task": {
    "taskTypeConfigsMap": {
      "SegmentGenerationAndPushTask": {
        "schedule": "0 */10 * * * ?",
        "tableMaxNumTasks": "10"
      }
    }
  }
}
```

### Batch Config Properties

These properties are specified inside each entry of `batchConfigMaps`:

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
      <th>Required</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`inputDirURI`</td>
      <td>URI of the directory containing input data files</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>`inputFormat`</td>
      <td>Input file format (e.g., `avro`, `parquet`, `csv`, `json`, `orc`)</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>`includeFileNamePattern`</td>
      <td>Glob pattern for files to include (e.g., `glob:**/*.avro`)</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`excludeFileNamePattern`</td>
      <td>Glob pattern for files to exclude (e.g., `glob:**/*.tmp`)</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`input.fs.className`</td>
      <td>Fully qualified class name of the input filesystem</td>
      <td>No (inferred from URI)</td>
    </tr>
    <tr>
      <td>`input.fs.prop.<key>`</td>
      <td>Properties to initialize the input filesystem</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`outputDirURI`</td>
      <td>URI for writing output segments before push</td>
      <td>No (uses local temp dir)</td>
    </tr>
    <tr>
      <td>`output.fs.className`</td>
      <td>Fully qualified class name of the output filesystem</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`output.fs.prop.<key>`</td>
      <td>Properties to initialize the output filesystem</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`overwriteOutput`</td>
      <td>Delete existing output segment directory if `true`</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`recordReader.className`</td>
      <td>Fully qualified class name of the RecordReader</td>
      <td>No (inferred from inputFormat)</td>
    </tr>
    <tr>
      <td>`recordReader.configClassName`</td>
      <td>Fully qualified class name of the RecordReaderConfig</td>
      <td>No (inferred from inputFormat)</td>
    </tr>
    <tr>
      <td>`recordReader.prop.<key>`</td>
      <td>Properties to initialize RecordReaderConfig</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`schema`</td>
      <td>Pinot schema as a JSON string</td>
      <td>No (fetched from controller)</td>
    </tr>
    <tr>
      <td>`schemaURI`</td>
      <td>URI to fetch the Pinot schema</td>
      <td>No (fetched from controller)</td>
    </tr>
    <tr>
      <td>`segmentNameGenerator.type`</td>
      <td>Segment name generator type (`simple` or `fixed`)</td>
      <td>No (defaults to `simple`)</td>
    </tr>
    <tr>
      <td>`segmentNameGenerator.configs.<key>`</td>
      <td>Segment name generator configuration properties</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`push.mode`</td>
      <td>Segment push mode: `TAR`, `URI`, or `METADATA`</td>
      <td>No (defaults to `TAR`)</td>
    </tr>
    <tr>
      <td>`push.controllerUri`</td>
      <td>Controller URI for push requests</td>
      <td>No (defaults to controller VIP)</td>
    </tr>
    <tr>
      <td>`push.segmentUriPrefix`</td>
      <td>URI prefix for segment download (used with `URI` push mode)</td>
      <td>No</td>
    </tr>
    <tr>
      <td>`push.segmentUriSuffix`</td>
      <td>URI suffix for segment download (used with `URI` push mode)</td>
      <td>No</td>
    </tr>
  </tbody>
</table>

### Task Config Properties

These properties go under `taskTypeConfigsMap.SegmentGenerationAndPushTask`:

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`schedule`</td>
      <td>Cron expression for automatic task scheduling</td>
      <td>None (manual only)</td>
    </tr>
    <tr>
      <td>`tableMaxNumTasks`</td>
      <td>Maximum number of concurrent tasks per table per run</td>
      <td>`Integer.MAX_VALUE`</td>
    </tr>
  </tbody>
</table>

## How It Works

1. **Task Generation**: The SegmentGenerationAndPushTaskGenerator:
   - Lists all files in the configured `inputDirURI`
   - Applies include/exclude file patterns to filter the file list
   - In APPEND mode, skips files that have already been ingested (tracked via segment metadata)
   - Skips files that are being processed by currently running tasks
   - Creates one task config per input file, up to `tableMaxNumTasks`

2. **Task Execution**: The SegmentGenerationAndPushTaskExecutor:
   - Copies the input file from the remote filesystem to local disk
   - Generates a Pinot segment from the input file using the configured RecordReader
   - Compresses the segment into a tar.gz archive
   - Moves the segment to the output filesystem (if `outputDirURI` is configured)
   - Pushes the segment to the Pinot cluster using the configured push mode

3. **Push Modes**:
   - **TAR**: Uploads the compressed segment tar file directly to the controller
   - **URI**: Sends the segment URI to the controller, which downloads from the specified location
   - **METADATA**: Sends only the segment metadata and URI to the controller (segment remains on deep store)

## Example Usage

### Ingesting from S3

```json
{
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "DAILY",
      "batchConfigMaps": [
        {
          "inputDirURI": "s3://my-bucket/data/events/",
          "includeFileNamePattern": "glob:**/*.parquet",
          "inputFormat": "parquet",
          "input.fs.className": "org.apache.pinot.plugin.filesystem.S3PinotFS",
          "input.fs.prop.region": "us-east-1",
          "outputDirURI": "s3://my-bucket/segments/events/",
          "output.fs.className": "org.apache.pinot.plugin.filesystem.S3PinotFS",
          "output.fs.prop.region": "us-east-1",
          "push.mode": "METADATA"
        }
      ]
    }
  },
  "task": {
    "taskTypeConfigsMap": {
      "SegmentGenerationAndPushTask": {
        "schedule": "0 */10 * * * ?",
        "tableMaxNumTasks": "10"
      }
    }
  }
}
```

### Ingesting from GCS

```json
{
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "batchConfigMaps": [
        {
          "inputDirURI": "gs://my-bucket/data/",
          "inputFormat": "json",
          "input.fs.className": "org.apache.pinot.plugin.filesystem.GcsPinotFS",
          "input.fs.prop.projectId": "my-gcp-project"
        }
      ]
    }
  },
  "task": {
    "taskTypeConfigsMap": {
      "SegmentGenerationAndPushTask": {
        "schedule": "0 0 * * * ?"
      }
    }
  }
}
```

## Scheduling

### Manual Scheduling

Use the Controller REST API to manually trigger SegmentGenerationAndPushTask:

```bash

# Schedule SegmentGenerationAndPushTask for all enabled tables

POST /tasks/schedule?taskType=SegmentGenerationAndPushTask

# Schedule SegmentGenerationAndPushTask for a specific table

POST /tasks/schedule?taskType=SegmentGenerationAndPushTask&tableName=myTable_OFFLINE
```

### Automatic Scheduling

Configure automatic scheduling using cron expressions:

```json
{
  "task": {
    "taskTypeConfigsMap": {
      "SegmentGenerationAndPushTask": {
        "schedule": "0 */10 * * * ?"
      }
    }
  }
}
```

## Important Considerations

- **One file per segment**: Each input file produces exactly one segment. Plan your input file sizes accordingly.
- **Segment name collisions**: In APPEND mode, a UUID is appended to segment names to prevent collisions across scheduling runs. Alternatively, omit `tableMaxNumTasks` to ingest all files in a single batch, which uses a sequence number suffix.
- **Input directory listing overhead**: The task lists all files in `inputDirURI` on every scheduling run. For cloud buckets with many files, keep `inputDirURI` pointing to the smallest possible set of files.
- **File tracking**: In APPEND mode, the input file URI is stored in the segment's ZK metadata custom map. This prevents re-ingestion of the same file. In non-APPEND modes, this deduplication does not apply.
- **Push mode selection**: Use `TAR` for simple setups, `URI` when the controller can access the deep store directly, and `METADATA` for the most efficient large-scale ingestion (segment data stays on deep store).

## Monitoring

SegmentGenerationAndPushTask generates standard Minion metrics for monitoring:

- Task execution time and success/failure rates
- Number of tasks in progress and queued
- Segment generation and push progress notifications

Use the Pinot UI Task Manager to monitor SegmentGenerationAndPushTask execution and troubleshoot issues.
