---
description: Upload existing Pinot segments to a controller.
---

# Upload segments to a Pinot controller

This guide explains how to upload already-built Pinot segments to a Pinot controller, which REST endpoint to call, and when to use tar push, URI push, or metadata push.

Use this flow when your segment `.tar.gz` files already exist outside Pinot, for example when migrating from an old cluster, backfilling from another system, or re-registering segments that already live in deep storage.

Before you upload, do the following:

1. [Create a schema configuration](../../basics/getting-started/first-table-and-schema.md#4-save-the-schema) or confirm one exists that matches the segment you want to upload.

2. [Create a table configuration](../../reference/configuration-reference/table.md) or confirm one exists that matches the segment you want to upload.

3. If needed, upload the schema and table configs.

```bash
pinot-admin.sh AddTable \\
  -tableConfigFile /path/to/table-config.json \\
  -schemaFile /path/to/table-schema.json -exec
```

4. Make sure the controller can read the segment source:

   * For tar push, the client must be able to stream the segment tar file to the controller.
   * For URI push and metadata push, the controller must be able to access the URI scheme you use. For PinotFS-backed schemes such as HDFS, S3, GCS, and ADLS, configure the matching [Pinot file system](../../manage-data/data-import/pinot-file-system). For custom schemes, implement a [segment fetcher](../../developers/developers-and-contributors/extending-pinot/segment-fetchers.md).

## Controller upload endpoints

The controller exposes three upload endpoints:

| Endpoint | Use case | Content type | Notes |
| --- | --- | --- | --- |
| `POST /v2/segments` | Preferred single-segment upload endpoint | `multipart/form-data` or `application/json` | Recommended for tar push, URI push, and metadata push |
| `POST /segments` | Legacy single-segment upload endpoint | `multipart/form-data` or `application/json` | Still supported, but prefer `/v2/segments` |
| `POST /segments/batchUpload` | Batch metadata push | `multipart/form-data` | Only supports metadata push for multiple segments |

`/v2/segments` is the endpoint to document and use by default. The legacy `/segments` endpoint is still present for backward compatibility. Its JSON-based URI push path keeps the original `DOWNLOAD_URI` instead of moving the segment into a Pinot-chosen final location, so new integrations should use `/v2/segments`.

## Common request options

### Query parameters

All three upload modes use the same query parameters:

| Query parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `tableName` | Recommended for single upload, required for batch upload | None | Table name to upload into. Pinot can sometimes derive it from the segment metadata, but you should pass it explicitly. |
| `tableType` | No | `OFFLINE` | `OFFLINE` or `REALTIME` |
| `enableParallelPushProtection` | No | `false` | Reject concurrent uploads for the same segment |
| `allowRefresh` | No | `true` | Allow an existing segment to be refreshed instead of failing the upload |

Example:

```text
POST /v2/segments?tableName=myTable&tableType=OFFLINE&enableParallelPushProtection=false&allowRefresh=true
```

### Headers

| Header | Required | Applies to | Description |
| --- | --- | --- | --- |
| `UPLOAD_TYPE` | No for tar push, yes for URI and metadata push | All uploads | `SEGMENT` (default), `URI`, or `METADATA` |
| `DOWNLOAD_URI` | Yes for URI push and metadata push | URI push, metadata push | Source URI of the segment tar file |
| `COPY_SEGMENT_TO_DEEP_STORE` | No | Metadata push | If `true`, controller copies the segment from the source URI into Pinot deep store and rewrites the stored download URI |
| `CRYPTER` | No | All uploads | Crypter class name if the uploaded payload is encrypted |

## Push modes

### Tar push

Tar push is the original and default upload mode. Use it when the client can stream the full segment tar file to the controller.

**Request shape**

* Endpoint: `POST /v2/segments`
* Content type: `multipart/form-data`
* Headers: `UPLOAD_TYPE` omitted or set to `SEGMENT`
* Body: one multipart file part containing the segment `.tar.gz`

**What the controller does**

1. Stores the uploaded segment in the controller's segment directory or deep store.
2. Extracts segment metadata.
3. Adds or refreshes the segment in the target table.

Example:

```bash
curl -X POST "http://localhost:9000/v2/segments?tableName=myTable&tableType=OFFLINE" \\
  -F "file=@/path/to/myTable_2024-01-01_2024-01-02_0.tar.gz"
```

If you prefer the Pinot CLI, `pinot-admin.sh UploadSegment` uses tar push for local segment directories:

```bash
pinot-admin.sh UploadSegment \\
  -controllerHost localhost \\
  -controllerPort 9000 \\
  -segmentDir /path/to/local/dir \\
  -tableName myTable
```

### URI push

URI push is best when the segment tar file already exists in deep storage or another controller-readable remote system.

**Request shape**

* Endpoint: `POST /v2/segments`
* Content type: `application/json`
* Headers:
  * `UPLOAD_TYPE: URI`
  * `DOWNLOAD_URI: <segment-tar-uri>`
* Body: empty JSON payload is fine; the controller uses the headers

**What the controller does**

1. Downloads the segment tar from `DOWNLOAD_URI`.
2. Stores it in the controller's segment directory or deep store.
3. Extracts metadata.
4. Adds or refreshes the segment in the table.

Example:

```bash
curl -X POST "http://localhost:9000/v2/segments?tableName=myTable&tableType=OFFLINE" \\
  -H "Content-Type: application/json" \\
  -H "UPLOAD_TYPE: URI" \\
  -H "DOWNLOAD_URI: s3://bucket/pinot-segments/myTable_2024-01-01_2024-01-02_0.tar.gz" \\
  -d '{}'
```

Use URI push only when the controller can resolve the URI scheme. If the source is on HDFS, S3, GCS, ADLS, or a custom system, configure Pinot with the appropriate [Pinot file system](../../manage-data/data-import/pinot-file-system) or [segment fetcher](../../developers/developers-and-contributors/extending-pinot/segment-fetchers.md).

### Metadata push

Metadata push is the most controller-efficient option when the segment tar already exists in a reachable storage system.

Instead of uploading the full segment tar, the client uploads segment metadata and tells the controller where the tar already lives.

**Request shape**

* Endpoint: `POST /v2/segments`
* Content type: `multipart/form-data`
* Headers:
  * `UPLOAD_TYPE: METADATA`
  * `DOWNLOAD_URI: <segment-tar-uri>`
  * Optional: `COPY_SEGMENT_TO_DEEP_STORE: true`
* Body: one multipart file part containing the metadata tarball for the segment

The metadata tarball contains the segment metadata files, typically `creation.meta` and `metadata.properties`.

**What the controller does**

1. Reads the uploaded metadata bundle.
2. Uses `DOWNLOAD_URI` as the segment download location.
3. Adds or refreshes the segment in the table without downloading the full tar just to inspect metadata.

If you set `COPY_SEGMENT_TO_DEEP_STORE: true`, the controller copies the segment from `DOWNLOAD_URI` into Pinot deep store and stores the final deep-store URI in segment metadata. This is useful when the ingestion job writes to a staging location instead of the final deep-store path.

Example:

```bash
curl -X POST "http://localhost:9000/v2/segments?tableName=myTable&tableType=OFFLINE" \\
  -H "UPLOAD_TYPE: METADATA" \\
  -H "DOWNLOAD_URI: s3://staging-bucket/segments/myTable_2024-01-01_2024-01-02_0.tar.gz" \\
  -H "COPY_SEGMENT_TO_DEEP_STORE: true" \\
  -F "file=@/path/to/myTable_2024-01-01_2024-01-02_0.metadata.tar.gz"
```

`COPY_SEGMENT_TO_DEEP_STORE` is only useful for metadata push. The staging URI and Pinot deep store should use the same storage scheme because the copy happens through PinotFS.

### Batch metadata push

If you need to metadata-push many segments in one call, use `POST /segments/batchUpload`.

**Request shape**

* Endpoint: `POST /segments/batchUpload`
* Content type: `multipart/form-data`
* Query parameters: `tableName` and `tableType` are required
* Header: `UPLOAD_TYPE: METADATA`
* Body: one multipart part containing an uber tarball with:
  * each segment's `creation.meta`
  * each segment's `metadata.properties`
  * an `all_segments_metadata` file mapping segment names to `DOWNLOAD_URI` values

This endpoint is only for metadata push.

## Job types and Pinot Admin mapping

If you are pushing from a batch ingestion job, the `jobType` maps to controller upload mode like this:

| Job type | Push mode | Controller endpoint |
| --- | --- | --- |
| `SegmentTarPush` or `SegmentCreationAndTarPush` | Tar push | `POST /v2/segments` |
| `SegmentUriPush` or `SegmentCreationAndUriPush` | URI push | `POST /v2/segments` |
| `SegmentMetadataPush` or `SegmentCreationAndMetadataPush` | Metadata push | `POST /v2/segments` |
| `SegmentMetadataPush` with `batchSegmentUpload: true` | Batch metadata push | `POST /segments/batchUpload` |

For ingestion jobs, define the push behavior in the [ingestion job spec](../../reference/configuration-reference/job-specification.md). Example:

```yaml
executionFrameworkSpec:
  name: standalone
  segmentGenerationJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner
  segmentTarPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner
  segmentUriPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner
  segmentMetadataPushJobRunnerClassName: org.apache.pinot.plugin.ingestion.batch.standalone.SegmentMetadataPushJobRunner

jobType: SegmentCreationAndMetadataPush

pinotClusterSpecs:
  - controllerURI: http://localhost:9000

pushJobSpec:
  pushAttempts: 2
  pushRetryIntervalMillis: 1000
  copyToDeepStoreForMetadataPush: true
```

Then launch it with:

```bash
pinot-admin.sh LaunchDataIngestionJob \\
  -jobSpecFile /path/to/job-spec.yaml
```

## Choosing the right mode

| Mode | Use it when | Tradeoff |
| --- | --- | --- |
| Tar push | The client has the segment tar locally and can upload it directly | Largest payload sent to controller |
| URI push | The segment tar already exists at a controller-readable URI | Controller still downloads the full segment tar |
| Metadata push | The segment tar already exists remotely and you want the lightest controller-side registration path | Requires a metadata bundle and a valid `DOWNLOAD_URI` |

For production clusters with deep store configured, `SegmentCreationAndMetadataPush` is generally the preferred ingestion-job mode.
