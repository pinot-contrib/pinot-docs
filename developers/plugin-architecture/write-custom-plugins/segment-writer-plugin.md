# Segment Writer Plugin

## Overview

The Segment Writer plugin provides an API for programmatically collecting `GenericRow` records and building Pinot segments without running a full batch ingestion job. This is particularly useful when you need to generate segments from application code, such as in a Minion task or a custom ingestion pipeline.

The built-in file-based implementation (`FileBasedSegmentWriter`) buffers incoming rows as Avro records on local disk and creates a Pinot segment when `flush()` is called.

## SPI Interface

To write a custom segment writer, implement the [SegmentWriter](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/ingestion/segment/writer/SegmentWriter.java) interface:

```java
public interface SegmentWriter extends Closeable {

  void init(TableConfig tableConfig, Schema schema) throws Exception;

  void init(TableConfig tableConfig, Schema schema, Map<String, String> batchConfigOverride)
      throws Exception;

  void collect(GenericRow row) throws Exception;

  default void collect(GenericRow[] rowBatch) throws Exception;

  URI flush() throws Exception;
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
      <td>`init(TableConfig, Schema)`</td>
      <td>Initializes the writer with table config and Pinot schema.</td>
    </tr>
    <tr>
      <td>`init(TableConfig, Schema, Map)`</td>
      <td>Initializes with additional batch config overrides.</td>
    </tr>
    <tr>
      <td>`collect(GenericRow)`</td>
      <td>Buffers a single row. The row is not written to a segment until `flush()` is called.</td>
    </tr>
    <tr>
      <td>`collect(GenericRow[])`</td>
      <td>Buffers a batch of rows.</td>
    </tr>
    <tr>
      <td>`flush()`</td>
      <td>Builds a Pinot segment from buffered rows and returns the URI of the generated segment tar file. Resets the buffer on success.</td>
    </tr>
    <tr>
      <td>`close()`</td>
      <td>Releases resources.</td>
    </tr>
  </tbody>
</table>

## File-Based Implementation

The `FileBasedSegmentWriter` works as follows:

1. **Initialization** -- Reads `batchConfigMaps` from the table config. Requires exactly one `BatchConfig` entry with an `outputDirURI`.
2. **Buffering** -- Each `collect()` call applies the table's transform pipeline and appends the result as an Avro record to a local buffer file.
3. **Flushing** -- The `flush()` method builds a Pinot segment from the buffer file, compresses it as a `.tar.gz`, writes it to the configured `outputDirURI`, and resets the buffer. If flush fails, the buffer is preserved so `flush()` can be retried.
4. **Closing** -- The `close()` method releases resources and cleans up staging directories.

## Configuration

The segment writer is configured through `batchConfigMaps` in the table config:

```json
{
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "batchConfigMaps": [
        {
          "outputDirURI": "/path/to/segment/output",
          "overwrite": "false"
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
      <td>`outputDirURI`</td>
      <td>Yes</td>
      <td>Directory where generated segment tar files are written.</td>
    </tr>
    <tr>
      <td>`overwrite`</td>
      <td>No</td>
      <td>Whether to overwrite segments with duplicate names. Defaults to `false`.</td>
    </tr>
  </tbody>
</table>

## Usage Example

```java
SegmentWriter writer = new FileBasedSegmentWriter();
writer.init(tableConfig, schema);

for (GenericRow row : rows) {
  writer.collect(row);
}

URI segmentURI = writer.flush();
// segmentURI points to the generated .tar.gz file

writer.close();
```

## Writing a Custom Segment Writer

To implement a custom segment writer:

1. Create a class that implements `SegmentWriter`.
2. Package it as a Pinot plugin (see [Write Custom Plugins](./)).
3. Place the plugin JAR in the Pinot `/plugins` directory.

Custom implementations could use different buffering strategies (for example, in-memory buffering for smaller datasets) or write to remote storage directly.
