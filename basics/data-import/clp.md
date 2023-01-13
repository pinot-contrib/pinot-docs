---
description: Support for encoding fields with CLP during ingestion.
---

# Stream Ingestion with CLP

{% hint style="warning" %}
This is an experimental feature. Configuration options and usage may change frequently until it is stabilized.
{% endhint %}

When performing stream ingestion of JSON records using [Kafka](pinot-stream-ingestion/import-from-apache-kafka.md), users can encode specific fields with [CLP](https://github.com/y-scope/clp) by using a CLP-specific StreamMessageDecoder.

CLP is a compressor designed to encode unstructured log messages in a way that makes them more compressible while retaining the ability to search them. It does this by decomposing the message into three fields:

* the message's static text, called a log type;
* repetitive variable values, called dictionary variables; and
* non-repetitive variable values (called encoded variables since we encode them specially if possible).

Searches are similarly decomposed into queries on the individual fields.

{% hint style="info" %}
Although CLP is designed for log messages, other unstructured text like file paths may also benefit from its encoding.
{% endhint %}

For example, consider this JSON record:

```json
{
  "timestamp": 1672531200000,
  "message": "INFO Task task_12 assigned to container: [ContainerID:container_15], operation took 0.335 seconds. 8 tasks remaining.",
  "logPath": "/mnt/data/application_123/container_15/stdout"
}
```

If the user specifies the fields `message` and `logPath` should be encoded with CLP, then the StreamMessageDecoder will output:

```json
{
  "timestamp": 1672531200000,
  "message_logtype": "INFO Task \\x12 assigned to container: [ContainerID:\\x12], operation took \\x13 seconds. \\x11 tasks remaining.",
  "message_dictionaryVars": [
    "task_12",
    "container_15"
  ],
  "message_encodedVars": [
    1801439850948198735,
    8
  ],
  "logPath_logtype": "/mnt/data/\\x12/\\x12/stdout",
  "logPath_dictionaryVars": [
    "application_123",
    "container_15"
  ],
  "logPath_encodedVars": []
}
```

_In the fields with the `_logtype` suffix, \x11 is a placeholder for an integer variable, \x12 is a placeholder for a dictionary variable, and \x13 is a placeholder for a float variable. In `message_encoedVars`, the float variable `0.335` is encoded as an integer using CLP's custom encoding._

All remaining fields are processed in the same way as they are in `org.apache.pinot.plugin.inputformat.json.JSONRecordExtractor`. Specifically, fields in the table's schema are extracted from each record and any remaining fields are dropped.

## Configuration

### Table Index

Assuming the user wants to encode `message` and `logPath` as in the example, they should change/add the following settings to their `tableIndexConfig` (we omit irrelevant settings for brevity):

```json
{
  "tableIndexConfig": {
    "streamConfigs": {
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.inputformat.clplog.CLPLogMessageDecoder",
      "stream.kafka.decoder.prop.fieldsForClpEncoding": "message,logPath"
    },
    "varLengthDictionaryColumns": [
      "message_logtype",
      "message_dictionaryVars",
      "logPath_logtype",
      "logPath_dictionaryVars"
    ]
  }
}
```

* `stream.kafka.decoder.prop.fieldsForClpEncoding` is a comma-separated list of names for fields that should be encoded with CLP.
* We use [variable-length dictionaries](../../configuration-reference/table#table-index-config) for the logtype and dictionary variables since their length can vary significantly.
* Ideally, we would disable the dictionaries for the encoded variable columns (since they are likely to be random), but currently, a bug prevents us from doing that for multi-valued number-type columns.

### Schema

For the table's schema, users should configure the CLP-encoded fields as follows  (we omit irrelevant settings for brevity):

```json
{
  "dimensionFieldSpecs": [
    {
      "name": "message_logtype",
      "dataType": "STRING",
      "maxLength": 2147483647
    },
    {
      "name": "message_encodedVars",
      "dataType": "LONG",
      "singleValueField": false
    },
    {
      "name": "message_dictionaryVars",
      "dataType": "STRING",
      "maxLength": 2147483647,
      "singleValueField": false
    },
    {
      "name": "message_logtype",
      "dataType": "STRING",
      "maxLength": 2147483647
    },
    {
      "name": "message_encodedVars",
      "dataType": "LONG",
      "singleValueField": false
    },
    {
      "name": "message_dictionaryVars",
      "dataType": "STRING",
      "maxLength": 2147483647,
      "singleValueField": false
    }
  ]
}
```

* We use the maximum possible length for the logtype and dictionary variable columns.
* The dictionary and encoded variable columns are multi-valued columns.

## Searching and decoding CLP-encoded fields

There is currently no built-in support within Pinot for searching and decoding CLP-encoded fields. This will be added in future commits, potentially as a set of UDFs. The development of these features is being tracked in this [design doc](https://docs.google.com/document/d/1nHZb37re4mUwEA258x3a2pgX13EWLWMJ0uLEDk1dUyU/edit).
