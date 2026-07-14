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
* **`stopOnError`**: Stop processing the file when Pinot encounters a malformed CSV record. Boolean. Default is `false`.

By default, Pinot attempts to recover from malformed data rows and continue reading the rest of the file. Set `stopOnError: true` if you want batch ingestion to stop at the first malformed record instead. Pinot still validates the CSV header during initialization, so an invalid header or first record fails fast.

{% hint style="info" %}
Your CSV file may have raw text fields that cannot be reliably delimited using any character. In this case, explicitly set the **multiValueDelimeter** field to empty in the ingestion config.\
\
`multiValueDelimiter: ''`
{% endhint %}

### Avro

Use `extractRawTimeValues` when you need raw Avro temporal logical-type values instead of Pinot's default converted values.

```
dataFormat: 'avro'
className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'
configs:
    extractRawTimeValues: true
```

The Avro record reader converts the data in file to a `GenericRecord`. A Java class or `.avro` file is not required. By default, `extractRawTimeValues` is `false`, so Pinot converts Avro temporal logical types during extraction. Set `extractRawTimeValues` to `true` to keep the raw Avro integer values for `date`, `time-millis`, `time-micros`, `timestamp-millis`, `timestamp-micros`, and `timestamp-nanos`. `decimal` and `uuid` always convert.

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

For batch ingestion, `dataFormat: 'json'` uses `JSONRecordReader` and reads newline-delimited UTF-8 text JSON files only.

For stream ingestion, use `org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder`. When `stream.<type>.decoder.prop.jsonFormat` is unset, the decoder keeps the same UTF-8 text JSON behavior. You can also pin the stream payload format to `TEXT`, `POSTGRES_JSONB`, `SQLITE_JSONB`, `SMILE`, or `CBOR`, or set `AUTO` to opt into per-message detection for mixed streams.

`AUTO` is opt-in and only detects CBOR when the payload includes the self-describe tag. If you already know the wire format, pin it explicitly instead of using `AUTO`. For a Kafka example and the config key details, see [Ingest streaming data from Apache Kafka](stream-ingestion/import-from-apache-kafka.md) and [Ingestion Configuration](../../reference/configuration-reference/ingestion.md).

### BSON

```
dataFormat: 'bson'
className: 'org.apache.pinot.plugin.inputformat.bson.BSONRecordReader'
```

Use the BSON record reader for `mongodump`-style files that store BSON documents back to back with the standard BSON length prefix. Pinot also detects and reads gzip-compressed BSON files automatically.

For batch ingestion, `dataFormat: bson` resolves to `BSONRecordReader` without any extra `configClassName`. For stream ingestion, configure your stream decoder as `org.apache.pinot.plugin.inputformat.bson.BSONMessageDecoder`; each stream message must contain exactly one BSON document.

`BSONRecordExtractor` converts decoded BSON values into Pinot-compatible Java values before schema coercion:

| BSON type | Pinot-side Java value | Notes |
| --- | --- | --- |
| `ObjectId` | `String` | 24-character hex string |
| `DateTime` | `java.sql.Timestamp` | Millisecond precision |
| `BsonTimestamp` | `java.sql.Timestamp` | Second precision; the intra-second ordinal is dropped |
| `Decimal128` | `BigDecimal` | `NaN` and `Infinity` become `null`; negative zero becomes `BigDecimal.ZERO` |
| `Binary` | `byte[]` | Includes UUID binary subtypes |
| Embedded document | `Map<String, Object>` | Converted recursively |
| Array | `Object[]` | Converted recursively |

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

To keep Parquet temporal values in their raw integer form instead of Pinot's default converted values, set `extractRawTimeValues` on `ParquetRecordReader`.

```
dataFormat: 'parquet'
className: 'org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader'
configs:
  extractRawTimeValues: true
```

When `extractRawTimeValues` is `false` (the default), Pinot converts Parquet `DATE`, `TIME_*`, and `TIMESTAMP_*` values during extraction. Set it to `true` to keep their raw integer values instead. When you use `ParquetRecordReader`, Pinot forwards this config to whichever underlying reader it selects (`ParquetAvroRecordReader` or `ParquetNativeRecordReader`). `DECIMAL` and `UUID` always convert.

`ParquetNativeRecordReader` preserves primitive values in their native Pinot-compatible form during extraction. For example, a Parquet `BOOLEAN` stays a Pinot `BOOLEAN` instead of being stringified.

| Parquet Data Type | Pinot Data Type | Comment |
| ----------------- | --------------- | ------- |
| BOOLEAN           | BOOLEAN         | Preserved as a native boolean value. |
| INT96 | LONG | Parquet`INT96` type converts **nanoseconds** to Pinot `INT64` type of **milliseconds** |
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
#### LIST and MAP wrapper extraction

Parquet LIST and MAP wrapper structs are now properly unwrapped when ingesting via `ParquetNativeRecordReader` and `ParquetAvroRecordReader`. Previously, schema-identified LIST and MAP columns had their wrapper elements exposed in the data:

- An `array<string>` field previously came back as `[{"element": "abc"}, {"element": "xyz"}]` — now it correctly comes back as `["abc", "xyz"]`.
- A `map<string,string>` field previously came back as `{"key_value":[{"key":"k","value":"v"}]}` — now it correctly comes back as `{"k":"v"}`.

Real struct fields named `element` are preserved; only schema-identified LIST and MAP wrappers are normalized. The readers support both the standard 3-level Parquet LIST encoding and legacy 2-level encodings (repeated primitive, repeated multi-field group, or repeated single-field group not named `element`).

**Backward incompatibility:** If you have ingestion pipelines or transform expressions that worked around the previous broken shape (for example, selecting `data.element` instead of `data` for an array column), you will need to update those queries and transforms.

**MAP ordering:** Parquet itself does not preserve source MAP entry order. Pinot canonicalizes ingested MAP and JSON output by sorting map keys when it serializes the value, so query results are deterministic but do not preserve the original insertion order. If the original pair order matters, model the field as `LIST<STRUCT<key, value>>` instead.


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
| MAP | Map\<Object, Object> |
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

### Apache Arrow

The Arrow input format plugin supports reading data in [Apache Arrow IPC format](https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format). This is useful for ingesting data from systems that produce Arrow-formatted output.

{% hint style="success" %}
The `pinot-arrow` plugin is included in the standard Pinot binary distribution (tarball and Docker image). No additional installation steps are required to use Apache Arrow format for data ingestion.
{% endhint %}

#### Batch ingestion

For batch ingestion from Arrow IPC files:

```
dataFormat: 'arrow'
className: 'org.apache.pinot.plugin.inputformat.arrow.ArrowRecordReader'
```

The `ArrowRecordReader` reads Arrow IPC files for batch ingestion. Note that Arrow IPC files require seekable channels, so **gzip compression is not supported**.

To preserve raw Arrow temporal values instead of Pinot's default converted values, set `extractRawTimeValues` on `ArrowRecordReader`:

```yaml
dataFormat: 'arrow'
className: 'org.apache.pinot.plugin.inputformat.arrow.ArrowRecordReader'
configs:
  extractRawTimeValues: true
```

When `extractRawTimeValues` is `false` (the default), Pinot converts Arrow `Date`, `Time`, and `Timestamp` values during extraction. Set it to `true` to keep raw integers instead: `Date` stays as days since epoch, while `Time` and `Timestamp` stay in the schema's declared Arrow unit.

#### Direct segment generation

Standard batch ingestion job specs continue to use `ArrowRecordReader`. If you build segments directly in application code, Pinot also exposes an optional Arrow column-major path through `SegmentIndexCreationDriverImpl.init(config, columnReaderFactory)`.

Use `ArrowFileColumnReaderFactory` for Arrow IPC files on disk:

```java
SegmentIndexCreationDriverImpl driver = new SegmentIndexCreationDriverImpl();
try (ArrowFileColumnReaderFactory factory = new ArrowFileColumnReaderFactory(arrowFile)) {
  driver.init(config, factory);
  driver.build();
}
```

The file-backed factory reads one Arrow record batch at a time during segment build. For direct integrations, it also exposes these config keys:

* **`arrowAllocatorLimit`**: Maximum Arrow off-heap allocator size in bytes for the file-backed column-major path. The default is `268435456` (256 MB).
* **`extractRawTimeValues`**: Keeps Arrow `Date`, `Time`, and `Timestamp` values as raw integers instead of Pinot's default converted values. The default is `false`.

If you already manage an `ArrowReader` and allocator in process, use `ArrowColumnReaderFactory` instead. That path supports the same `extractRawTimeValues` behavior, but allocator sizing remains caller-managed.

#### Stream ingestion

For stream ingestion, the Arrow decoder converts Arrow columnar batches to Pinot rows:

```
stream.kafka.decoder.class.name=org.apache.pinot.plugin.inputformat.arrow.ArrowMessageDecoder
```

**Configuration properties:**

| Property | Default | Description |
|----------|---------|-------------|
| `arrow.allocator.limit` | 268435456 (256 MB) | Memory limit for Arrow's off-heap allocator in bytes |
| `extractRawTimeValues` | `false` | Keep Arrow `Date`, `Time`, and `Timestamp` values as raw integers instead of Pinot's default converted values |

Arrow type conversions are handled automatically: UTF-8 text becomes `String`, `Date` becomes `LocalDate`, `Time` becomes `LocalTime`, `Timestamp` becomes `Timestamp`, Arrow Maps become flattened `Map<String, Object>`, and Arrow Lists become `Object[]`. Dictionary-encoded columns are decoded against their logical type before extraction.

Each Arrow Kafka message should contain a complete IPC stream. Empty batches are skipped, single-row batches ingest as one Pinot row, and multi-row batches fan out into multiple Pinot rows.
