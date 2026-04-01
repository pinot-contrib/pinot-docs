# Segment Uploader Plugin

## Overview

The Segment Uploader plugin is responsible for uploading completed segment tar files to the Pinot cluster. It abstracts the details of segment push so that different upload strategies (HTTP push, URI push, metadata push) can be supported through configuration.

The default implementation, `SegmentUploaderDefault`, reads push configuration from the table config's `batchConfigMaps` and delegates to `IngestionUtils` for the actual upload.

## SPI Interface

To write a custom segment uploader, implement the [SegmentUploader](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/ingestion/segment/uploader/SegmentUploader.java) interface:

```java
public interface SegmentUploader {

  void init(TableConfig tableConfig) throws Exception;

  void init(TableConfig tableConfig, Map<String, String> batchConfigOverride) throws Exception;

  void uploadSegment(URI segmentTarFile, AuthProvider authProvider) throws Exception;

  void uploadSegmentsFromDir(URI segmentDir, AuthProvider authProvider) throws Exception;
}
```

### Key Methods

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`init(TableConfig)`</td>
      <td>Initializes the uploader using batch config from the table config.</td>
    </tr>
    <tr>
      <td>`init(TableConfig, Map)`</td>
      <td>Initializes with additional config overrides on top of the table config.</td>
    </tr>
    <tr>
      <td>`uploadSegment(URI, AuthProvider)`</td>
      <td>Uploads a single segment tar file to the cluster.</td>
    </tr>
    <tr>
      <td>`uploadSegmentsFromDir(URI, AuthProvider)`</td>
      <td>Recursively finds and uploads all `.tar.gz` segment files from a directory.</td>
    </tr>
  </tbody>
</table>

## Default Implementation

The built-in `SegmentUploaderDefault` works as follows:

1. Reads the `batchConfigMaps` from `tableConfig.ingestionConfig.batchIngestionConfig`.
2. Requires exactly one `BatchConfig` entry in the list.
3. Uses the `push.controllerUri` property to determine the target controller.
4. Supports all push modes: `tar`, `uri`, and `metadata`.

## Configuration

The segment uploader is configured through `batchConfigMaps` in the table config. The following properties are relevant:

```json
{
  "ingestionConfig": {
    "batchIngestionConfig": {
      "batchConfigMaps": [
        {
          "push.controllerUri": "https://pinot-controller:9000",
          "push.mode": "tar"
        }
      ]
    }
  }
}
```

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`push.controllerUri`</td>
      <td>Yes</td>
      <td>URI of the Pinot controller for segment upload.</td>
    </tr>
    <tr>
      <td>`push.mode`</td>
      <td>No</td>
      <td>Push mode: `tar` (default), `uri`, or `metadata`.</td>
    </tr>
  </tbody>
</table>

## Writing a Custom Segment Uploader

To implement a custom segment uploader:

1. Create a class that implements `SegmentUploader`.
2. Package it as a Pinot plugin (see [Write Custom Plugins](./)).
3. Place the plugin JAR in the Pinot `/plugins` directory.

A custom uploader could be useful for scenarios such as:

* Uploading segments to a custom deep store before notifying the controller.
* Adding custom authentication or encryption during upload.
* Integrating with an external orchestration system that manages segment lifecycle.
