---
description: >-
  This section contains a collection of guides that will show you how to import
  data from a Pinot-supported input format.
---

# Supported Data Formats

Pinot offers support for various popular input formats during ingestion. By changing the input format, you can reduce the time spent doing serialization-deserialization and speed up the ingestion.

## Configuring input formats

To change the input format, adjust the `recordReaderSpec` config in the ingestion job specification.

```
recordReaderSpec:
  dataFormat: 'csv'
  className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
  configs: 
			key1 : 'value1'
			key2 : 'value2'
```

The configuration consists of the following keys:

* **`dataFormat`**: Name of the data format to consume.
* **`className`**: Name of the class that implements the `RecordReader` interface. This class is used for parsing the data.
* **`configClassName`**: Name of the class that implements the `RecordReaderConfig` interface. This class is used the parse the values mentioned in `configs`
* **`configs`**: Key-value pair for format-specific configurations. This field is optional.

## Supported input formats

Pinot supports multiple input formats out of the box. Specify the corresponding readers and the associated custom configurations to switch between formats.

### CSV

```
dataFormat: 'csv'
className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
configs:
	fileFormat: 'default' #should be one of default, rfc4180, excel, tdf, mysql
	header: 'columnName separated by delimiter'
  delimiter: ','
  multiValueDelimiter: '-'
```

CSV Record Reader supports the following configs:

* **`fileFormat`**: `default`, `rfc4180`, `excel`, `tdf`, `mysql`
* **`header`**: Header of the file. The `columnNames` should be separated by the delimiter mentioned in the configuration.
* **`delimiter`**: The character seperating the columns.
* **`multiValueDelimiter`**: The character separating multiple values in a single column. This can be used to split a column into a list.
* **`skipHeader`**: Skip header record in the file. Boolean.
* **`ignoreEmptyLines`**: Ignore empty lines (instead of filling them with default values). Boolean.
* **`ignoreSurroundingSpaces`**: ignore spaces around column names and values. Boolean
* **`quoteCharacter`**: Single character used for quotes in CSV files.
* **`recordSeparator`**: Character used to separate records in the input file. Default is  or `\r` depending on the platform.
* **`nullStringValue`**: String value that represents null in CSV files. Default is empty string.

{% hint style="info" %}
Your CSV file may have raw text fields that cannot be reliably delimited using any character. In this case, explicitly set the **multiValueDelimeter** field to empty in the ingestion config.\
\
`multiValueDelimiter: ''`
{% endhint %}

### Avro

```
dataFormat: 'avro'
className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'
configs:
    enableLogicalTypes: true
```

The Avro record reader converts the data in file to a `GenericRecord`. A Java class or `.avro` file is not required. By default, the Avro record reader only supports primitive types. To enable support for rest of the Avro data types, set `enableLogicalTypes` to `true` .

We use the following conversion table to translate between Avro and Pinot data types. The conversions are done using the offical Avro methods present in `org.apache.avro.Conversions`.

<table>
  <thead>
    <tr>
      <th>Avro Data Type</th>
      <th>Pinot Data Type</th>
      <th>Comment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>INT</td>
      <td></td>
    </tr>
    <tr>
      <td>LONG</td>
      <td>LONG</td>
      <td></td>
    </tr>
    <tr>
      <td>FLOAT</td>
      <td>FLOAT</td>
      <td></td>
    </tr>
    <tr>
      <td>DOUBLE</td>
      <td>DOUBLE</td>
      <td></td>
    </tr>
    <tr>
      <td>BOOLEAN</td>
      <td>BOOLEAN</td>
      <td></td>
    </tr>
    <tr>
      <td>STRING</td>
      <td>STRING</td>
      <td></td>
    </tr>
    <tr>
      <td>ENUM</td>
      <td>STRING</td>
      <td></td>
    </tr>
    <tr>
      <td>BYTES</td>
      <td>BYTES</td>
      <td></td>
    </tr>
    <tr>
      <td>FIXED</td>
      <td>BYTES</td>
      <td></td>
    </tr>
    <tr>
      <td>MAP</td>
      <td>JSON</td>
      <td></td>
    </tr>
    <tr>
      <td>ARRAY</td>
      <td>JSON</td>
      <td></td>
    </tr>
    <tr>
      <td>RECORD</td>
      <td>JSON</td>
      <td></td>
    </tr>
    <tr>
      <td>UNION</td>
      <td>JSON</td>
      <td></td>
    </tr>
    <tr>
      <td>DECIMAL</td>
      <td>BYTES</td>
      <td></td>
    </tr>
    <tr>
      <td>UUID</td>
      <td>STRING</td>
      <td></td>
    </tr>
    <tr>
      <td>DATE</td>
      <td>STRING</td>
      <td>`yyyy-MM-dd` format</td>
    </tr>
    <tr>
      <td>TIME\_MILLIS</td>
      <td>STRING</td>
      <td>`HH:mm:ss.SSS` format</td>
    </tr>
    <tr>
      <td>TIME\_MICROS</td>
      <td>STRING</td>
      <td>`HH:mm:ss.SSSSSS` format</td>
    </tr>
    <tr>
      <td>TIMESTAMP\_MILLIS</td>
      <td>TIMESTAMP</td>
      <td></td>
    </tr>
    <tr>
      <td>TIMESTAMP\_MICROS</td>
      <td>TIMESTAMP</td>
      <td></td>
    </tr>
  </tbody>
</table>

### JSON

```
dataFormat: 'json'
className: 'org.apache.pinot.plugin.inputformat.json.JSONRecordReader'
```

### Thrift

```
dataFormat: 'thrift'
className: 'org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReader'
configs:
	thriftClass: 'ParserClassName'
```

{% hint style="info" %}
Thrift requires the generated class using `.thrift` file to parse the data. The `.class` file should be available in the Pinot's `classpath`. You can put the files in the `lib/` folder of Pinot distribution directory.
{% endhint %}

### Parquet

```
dataFormat: 'parquet'
className: 'org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader'
```

Since 0.11.0 release, the Parquet record reader determines whether to use `ParquetAvroRecordReader` or `ParquetNativeRecordReader` to read records. The reader looks for the `parquet.avro.schema` or `avro.schema` key in the parquet file footer, and if present, uses the Avro reader.

You can change the record reader manually in case of a misconfiguration.

```
dataFormat: 'parquet'
className: 'org.apache.pinot.plugin.inputformat.parquet.ParquetNativeRecordReader'
```

{% hint style="warning" %}
For the support of DECIMAL and other parquet native data types, always use `ParquetNativeRecordReader`.
{% endhint %}

<table>
  <thead>
    <tr>
      <th>INT96</th>
      <th>LONG</th>
      <th><p>Parquet<code>INT96</code> type converts <strong>nanoseconds</strong></p><p>to Pinot <code>INT64</code> type of <strong>milliseconds</strong></p></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT64</td>
      <td>LONG</td>
      <td></td>
    </tr>
    <tr>
      <td>INT32</td>
      <td>INT</td>
      <td></td>
    </tr>
    <tr>
      <td>FLOAT</td>
      <td>FLOAT</td>
      <td></td>
    </tr>
    <tr>
      <td>DOUBLE</td>
      <td>DOUBLE</td>
      <td></td>
    </tr>
    <tr>
      <td>BINARY</td>
      <td>BYTES</td>
      <td></td>
    </tr>
    <tr>
      <td>FIXED-LEN-BYTE-ARRAY</td>
      <td>BYTES</td>
      <td></td>
    </tr>
    <tr>
      <td>DECIMAL</td>
      <td>DOUBLE</td>
      <td></td>
    </tr>
    <tr>
      <td>ENUM</td>
      <td>STRING</td>
      <td></td>
    </tr>
    <tr>
      <td>UTF8</td>
      <td>STRING</td>
      <td></td>
    </tr>
    <tr>
      <td>REPEATED</td>
      <td>MULTIVALUE/MAP (represented as MV</td>
      <td>if parquet original type is LIST, then it is converted to MULTIVALUE column otherwise a MAP column.</td>
    </tr>
  </tbody>
</table>

For `ParquetAvroRecordReader` , you can refer to the [Avro section above](pinot-input-formats.md#avro) for the type conversions.

### ORC

```
dataFormat: 'orc'
className: 'org.apache.pinot.plugin.inputformat.orc.ORCRecordReader'
```

ORC record reader supports the following data types -

<table>
  <thead>
    <tr>
      <th>ORC Data Type</th>
      <th>Java Data Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BOOLEAN</td>
      <td>String</td>
    </tr>
    <tr>
      <td>SHORT</td>
      <td>Integer</td>
    </tr>
    <tr>
      <td>INT</td>
      <td>Integer</td>
    </tr>
    <tr>
      <td>LONG</td>
      <td>Integer</td>
    </tr>
    <tr>
      <td>FLOAT</td>
      <td>Float</td>
    </tr>
    <tr>
      <td>DOUBLE</td>
      <td>Double</td>
    </tr>
    <tr>
      <td>STRING</td>
      <td>String</td>
    </tr>
    <tr>
      <td>VARCHAR</td>
      <td>String</td>
    </tr>
    <tr>
      <td>CHAR</td>
      <td>String</td>
    </tr>
    <tr>
      <td>LIST</td>
      <td>Object\[]</td>
    </tr>
    <tr>
      <td>MAP</td>
      <td>Map\<Object, Object></td>
    </tr>
    <tr>
      <td>DATE</td>
      <td>Long</td>
    </tr>
    <tr>
      <td>TIMESTAMP</td>
      <td>Long</td>
    </tr>
    <tr>
      <td>BINARY</td>
      <td>byte\[]</td>
    </tr>
    <tr>
      <td>BYTE</td>
      <td>Integer</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
In LIST and MAP types, the object should only belong to one of the data types supported by Pinot.
{% endhint %}

### Protocol Buffers

```
dataFormat: 'proto'
className: 'org.apache.pinot.plugin.inputformat.protobuf.ProtoBufRecordReader'
configs:
	descriptorFile: 'file:///path/to/sample.desc'
```

The reader requires a descriptor file to deserialize the data present in the files. You can generate the descriptor file (`.desc`) from the `.proto` file using the command -

```
protoc --include_imports --descriptor_set_out=/absolute/path/to/output.desc /absolute/path/to/input.proto
```

### Apache Arrow

```
dataFormat: 'arrow'
```

The Arrow input format plugin supports reading data in [Apache Arrow IPC streaming format](https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format). This is useful for ingesting data from systems that produce Arrow-formatted output.

{% hint style="success" %}
The `pinot-arrow` plugin is included in the standard Pinot binary distribution (tarball and Docker image). The `ArrowMessageDecoder` is available out of the box, and no additional installation steps are required to use Apache Arrow format for data ingestion.
{% endhint %}

For stream ingestion, the Arrow decoder converts Arrow columnar batches to Pinot rows:

```
stream.kafka.decoder.class.name=org.apache.pinot.plugin.inputformat.arrow.ArrowMessageDecoder
```

**Configuration properties:**

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`arrow.allocator.limit`</td>
      <td>268435456 (256 MB)</td>
      <td>Memory limit for Arrow's off-heap allocator in bytes</td>
    </tr>
  </tbody>
</table>

The decoder handles Arrow type conversions automatically: `Text` → `String`, `LocalDateTime` → `Timestamp`, Arrow Maps → flattened `Map<String, Object>`, and Arrow Lists → `List<Object>`. Dictionary-encoded columns are also supported.
