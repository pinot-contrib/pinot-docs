---
description: Upload a table segment in Apache Pinot.
---

# Upload a table segment from an external source

This procedure uploads one or more table segments that have been stored as Pinot segment binary files outside of Apache Pinot, such as if you had to close an original Pinot cluster and create a new one.

Choose one of the following:

* If your data is in a location that uses HDFS, create a segment fetcher.
* If your data is on a host where you have SSH access, use the Pinot Admin script.

Before you upload, do the following:

1. [Create a schema configuration](../../basics/getting-started/pushing-your-data-to-pinot#creating-a-schema) or confirm one exists that matches the segment you want to upload.

1. [Create a table configuration](../../configuration-reference/table.md) or confirm one exists that matches the segment you want to upload.

1. (If needed) Upload the schema and table configs.
```bash
pinot-admin.sh AddTable \\
  -tableConfigFile /path/to/table-config.json \\
  -schemaFile /path/to/table-schema.json -exec
```

## Create a segment fetcher

If the data is in a location using HDFS, you can create a [segment fetcher](../../developers/developers-and-contributors/extending-pinot/segment-fetchers.md), which will push segment files from external systems such as those running Hadoop or Spark. It is possible to [implement your own segment fetcher for other systems](../../developers/developers-and-contributors/extending-pinot/segment-fetchers.md) with an external jar by implementing a class that extends this interface.

## Use the Pinot Admin script to upload segments

To do this, you need to create a `JobSpec` configuration file. For details, see [Ingestion job spec](../../configuration-reference/job-specification.md). This file defines the job, including things like the job type, the input directory or URI, and the table name that the segments will be connected to.

You can upload a Pinot segment using several methods:
* Segment tar push
* Segment URI push
* Segment metadata push

### Segment tar push

This is the original and default push mechanism. It requires the segment to be stored locally, or that the segment can be opened as an InputStream on PinotFS, so we can stream the entire segment tar file to the controller.

The push job will upload the entire segment tar file to the Pinot controller.

The Pinot controller will save the segment into the controller segment directory (Local or any PinotFS), then extract segment metadata, and add the segment to the table.

While you can create a `JobSpec` for this job, in simple instances you can push without one.

Upload segment files to your Pinot server from controller using the Pinot Admin script as follows:

```bash
pinot-admin.sh UploadSegment -controllerHost localhost -controllerPort 9000 -segmentDir /path/to/local/dir -tableName myTable
```

All options should be prefixed with `-` (hyphen)

| Option         | Description                               |
| -------------- | ----------------------------------------- |
| controllerHost | Hostname or IP address of the controller  |
| controllerPort | Port of the controller                    |
| segmentDir     | Local directory containing segment files  |
| tableName      | Name of the table to push the segments into |

### Segment URI push

This push mechanism requires the segment tar file stored on a deep store with a globally accessible segment tar URI.

URI push is lightweight on the client-side, and the controller side requires equivalent work as the tar push.

The push job posts this segment tar URI to the Pinot controller.

The Pinot controller saves the segment into the controller segment directory (local or any PinotFS), then extracts segment metadata, and adds the segment to the table.


Upload segment files to your Pinot server using the `JobSpec` you create and the Pinot Admin script as follows:

```bash
pinot-admin.sh LaunchDataIngestionJob \\
    -jobSpecFile /file/location/my-job-spec.yaml
```

### Segment metadata push

This push mechanism also requires the segment tar file stored on a deep store with a globally accessible segment tar URI.

Metadata push is lightweight on the controller side. There is no deep store download involved from the controller side.

The push job downloads the segment based on URI, then extracts metadata, and upload metadata to the Pinot controller.

The Pinot controller adds the segment to the table based on the metadata.


Upload segment metadata to your Pinot server using the `JobSpec` you create and the Pinot Admin script as follows:

```bash
pinot-admin.sh LaunchDataIngestionJob \\
    -jobSpecFile /file/location/my-job-spec.yaml
```
