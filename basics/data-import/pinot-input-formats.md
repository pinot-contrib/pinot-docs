---
description: >-
  This section contains a collection of guides that will show you how to import
  data from a Pinot-supported input format.
---

# Input formats

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

| Avro Data Type    | Pinot Data Type | Comment                  |
| ----------------- | --------------- | ------------------------ |
| INT               | INT             |                          |
| LONG              | LONG            |                          |
| FLOAT             | FLOAT           |                          |
| DOUBLE            | DOUBLE          |                          |
| BOOLEAN           | BOOLEAN         |                          |
| STRING            | STRING          |                          |
| ENUM              | STRING          |                          |
| BYTES             | BYTES           |                          |
| FIXED             | BYTES           |                          |
| MAP               | JSON            |                          |
| ARRAY             | JSON            |                          |
| RECORD            | JSON            |                          |
| UNION             | JSON            |                          |
| DECIMAL           | BYTES           |                          |
| UUID              | STRING          |                          |
| DATE              | STRING          | `yyyy-MM-dd` format      |
| TIME\_MILLIS      | STRING          | `HH:mm:ss.SSS` format    |
| TIME\_MICROS      | STRING          | `HH:mm:ss.SSSSSS` format |
| TIMESTAMP\_MILLIS | TIMESTAMP       |                          |
| TIMESTAMP\_MICROS | TIMESTAMP       |                          |

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

| INT96                | LONG                              | <p>Parquet<code>INT96</code> type converts <strong>nanoseconds</strong></p><p>to Pinot <code>INT64</code> type of <strong>milliseconds</strong></p> |
| -------------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| INT64                | LONG                              |                                                                                                                                                     |
| INT32                | INT                               |                                                                                                                                                     |
| FLOAT                | FLOAT                             |                                                                                                                                                     |
| DOUBLE               | DOUBLE                            |                                                                                                                                                     |
| BINARY               | BYTES                             |                                                                                                                                                     |
| FIXED-LEN-BYTE-ARRAY | BYTES                             |                                                                                                                                                     |
| DECIMAL              | DOUBLE                            |                                                                                                                                                     |
| ENUM                 | STRING                            |                                                                                                                                                     |
| UTF8                 | STRING                            |                                                                                                                                                     |
| REPEATED             | MULTIVALUE/MAP (represented as MV | if parquet original type is LIST, then it is converted to MULTIVALUE column otherwise a MAP column.                                                 |

For `ParquetAvroRecordReader` , you can refer to the [Avro section above](pinot-input-formats.md#avro) for the type conversions.

### ORC

```
dataFormat: 'orc'
className: 'org.apache.pinot.plugin.inputformat.orc.ORCRecordReader'
```

ORC record reader supports the following data types -

| ORC Data Type | Java Data Type       |
| ------------- | -------------------- |
| BOOLEAN       | String               |
| SHORT         | Integer              |
| INT           | Integer              |
| LONG          | Integer              |
| FLOAT         | Float                |
| DOUBLE        | Double               |
| STRING        | String               |
| VARCHAR       | String               |
| CHAR          | String               |
| LIST          | Object\[]            |
| MAP           | Map\<Object, Object> |
| DATE          | Long                 |
| TIMESTAMP     | Long                 |
| BINARY        | byte\[]              |
| BYTE          | Integer              |

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
