---
description: >-
  This section contains a collection of guides that will show you how to import
  data from a Pinot supported input format.
---

# Input formats

Pinot offers support for various popular input formats during ingestion. By changing the input format, you can reduce the time spent doing serialization-deserialization and speed up the ingestion.

## Configuring input formats

The input format can be changed using the `recordReaderSpec` config in the ingestion job spec.

```yaml
recordReaderSpec:
  dataFormat: 'csv'
  className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
  configs: 
    key1 : 'value1'
    key2 : 'value2'
```

The config consists of the following keys:

* `dataFormat` - Name of the data format to consume.
* `className` - name of the class that implements the `RecordReader` interface. This class is used for parsing the data.
* `configClassName` - name of the class that implements the `RecordReaderConfig` interface. This class is used the parse the values mentioned in `configs`
* `configs` - Key value pair for format specific configs. This field can be left out.



To configure input format for realtime ingestion, you can add the following to the table config json

```json
"streamConfigs": {
    "streamType": "foo_bar",
    "stream.foo_bar.decoder.class.name": "org.apache.pinot.plugin.inputformat.csv.CSVMessageDecoder"
    "stream.foo_bar.decoder.prop.key1": "value1" ,
    "stream.foo_bar.decoder.prop.key2" : "value2"
}
```

## Supported input formats

Pinot supports the multiple input formats out of the box. You just need to specify the corresponding readers and the associated custom configs to switch between the formats.

### CSV

{% tabs %}
{% tab title="Batch" %}
```yaml
dataFormat: 'csv'
className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
configs:
	fileFormat: 'default' #should be one of default, rfc4180, excel, tdf, mysql
	header: 'columnName seperated by delimiter'
  delimiter: ','
  multiValueDelimiter: '-'
```
{% endtab %}

{% tab title="Realtime" %}
```json
"streamType": "kafka",
"stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.csv.CSVMessageDecoder"
"stream.kafka.decoder.prop.delimiter": "," ,
"stream.kafka.decoder.prop.multiValueDelimiter" : "-"
```
{% endtab %}
{% endtabs %}

#### Supported Configs

`fileFormat` - can be one of default, rfc4180, excel, tdf, mysql

`header` - header of the file. The columnNames should be seperated by the delimiter mentioned in the config

`delimiter` - The character seperating the columns

`multiValueDelimiter` - The character seperating multiple values in a single column. This can be used to split a column into a list.

`nullValueString` - use this to specify how NULL values are represented in your csv files. Default is empty string interpreted as NULL.

{% hint style="info" %}
Your CSV file may have raw text fields that cannot be reliably delimited using any character. In this case, explicitly set the **multiValueDelimeter** field to empty in the ingestion config. \
\
`multiValueDelimiter: ''`&#x20;
{% endhint %}

### AVRO

{% tabs %}
{% tab title="Batch" %}
```yaml
dataFormat: 'avro'
className: 'org.apache.pinot.plugin.inputformat.avro.AvroRecordReader'
```
{% endtab %}

{% tab title="Realtime" %}
```json
"streamType": "kafka",
"stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaAvroMessageDecoder",
"stream.kafka.decoder.prop.schema.registry.rest.url": "http://localhost:2222/schemaRegistry",
```
{% endtab %}
{% endtabs %}

The Avro record reader converts the data in file to a `GenericRecord`. A java class or `.avro` file is not required.&#x20;

You can also specify Kafka schema registry for avro records in stream.

### JSON

{% tabs %}
{% tab title="Batch" %}
```yaml
dataFormat: 'json'
className: 'org.apache.pinot.plugin.inputformat.json.JSONRecordReader'
```
{% endtab %}

{% tab title="Realtime" %}
```json
"streamType": "kafka",
"stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
```
{% endtab %}
{% endtabs %}

### Thrift

{% tabs %}
{% tab title="Batch" %}
```yaml
dataFormat: 'thrift'
className: 'org.apache.pinot.plugin.inputformat.thrift.ThriftRecordReader'
configs:
    thriftClass: 'ParserClassName'
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Thrift requires the generated class using `.thrift` file to parse the data. The .class file should be available in the Pinot's classpath. You can put the files in the `lib/` folder of pinot distribution directory.
{% endhint %}

### Parquet

{% tabs %}
{% tab title="Batch" %}
```yaml
dataFormat: 'parquet'
className: 'org.apache.pinot.plugin.inputformat.parquet.ParquetRecordReader'
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
The above class doesn't read the Parquet `INT96` and `Decimal`type.
{% endhint %}

Please use the below class to handle  `INT96` and `Decimal`type.

```yaml
dataFormat: 'parquet'
className: 'org.apache.pinot.plugin.inputformat.parquet.ParquetNativeRecordReader'
```

| Parquet Data Type | Java Data Type | Comment                                                                                                                                              |
| ----------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| INT96             | INT64          | <p>Parquet<code>INT96</code> type converts <strong>nanoseconds</strong></p><p> to Pinot <code>INT64</code> type of <strong>milliseconds</strong></p> |
| DECIMAL           | DOUBLE         |                                                                                                                                                      |

### ORC

{% tabs %}
{% tab title="Batch" %}
```yaml
dataFormat: 'orc'
className: 'org.apache.pinot.plugin.inputformat.orc.ORCRecordReader'
```
{% endtab %}
{% endtabs %}



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

{% tabs %}
{% tab title="Batch" %}
```yaml
dataFormat: 'proto'
className: 'org.apache.pinot.plugin.inputformat.protobuf.ProtoBufRecordReader'
configs:
    descriptorFile: 'file:///path/to/sample.desc'
    protoClassName: 'Metrics'
```
{% endtab %}

{% tab title="Realtime" %}
```json
"streamType": "kafka",
"stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder",
"stream.kafka.decoder.prop.descriptorFile": "file:///tmp/Workspace/protobuf/metrics.desc",
"stream.kafka.decoder.prop.protoClassName": "Metrics"
```
{% endtab %}
{% endtabs %}

The reader requires a descriptor file to deserialize the data present in the files. You can generate the descriptor file (`.desc`) from the `.proto` file using the command -

```
protoc --include_imports --descriptor_set_out=/absolute/path/to/output.desc /absolute/path/to/input.proto
```

#### Descriptor file in DFS

The descriptorFile needs to be present on all pinot server machines for ingestion to work. You can also upload the descriptor file to a DFS such as S3, GCS etc. and mention that path in the configs. Do note that you'll also need to specify [filesystem config](pinot-file-system/) for the directory in the pinot configuration  or ingestion spec as well.&#x20;

{% tabs %}
{% tab title="Batch" %}
<pre class="language-yaml"><code class="lang-yaml">recordReaderSpec:
<strong>  dataFormat: 'proto'
</strong>  className: 'org.apache.pinot.plugin.inputformat.protobuf.ProtoBufRecordReader'
  configs:
  	descriptorFile: 's3://path/to/sample.desc'
pinotFSSpecs:
  - scheme: s3
    className: org.apache.pinot.plugin.filesystem.S3PinotFS
    configs:
      region: 'us-west-1'</code></pre>
{% endtab %}

{% tab title="Realtime" %}
```json
"streamType": "kafka",
"stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.protobuf.ProtoBufMessageDecoder",
"stream.kafka.decoder.prop.descriptorFile": "s3://tmp/Workspace/protobuf/metrics.desc",
"stream.kafka.decoder.prop.protoClassName": "Metrics"
```
{% endtab %}
{% endtabs %}

Both `proto2` and `proto3` formats are supported by the reader.

#### Schema Registry

Protobuf reader also supports Confluent schema registry. Using schema registry allows you to not create and upload any descriptor file. The schema is fetched from the registry itself using the metadata present in the Kafka message. The only pre-requisite for it to work is that your messages should be serialized using `io.confluent.kafka.serializers.protobuf.KafkaProtobufSerializer` in producer.

{% tabs %}
{% tab title="Realtime" %}
<pre class="language-json"><code class="lang-json">"streamType": "kafka",
<strong>"stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.protobuf.KafkaConfluentSchemaRegistryProtoBufMessageDecoder",
</strong>"stream.kafka.decoder.prop.schema.registry.rest.url": "http://localhost:2222/schemaRegistry",
"stream.kafka.decoder.prop.cached.schema.map.capacity": 1000</code></pre>
{% endtab %}
{% endtabs %}
