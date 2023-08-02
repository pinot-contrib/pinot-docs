---
description: >-
  This guide shows you how to ingest a stream of records from an Apache Pulsar
  topic into a Pinot table.
---

# Import from Apache Pulsar

Pinot supports consuming data from [Apache Pulsar](https://pulsar.apache.org) via the `pinot-pulsar` plugin. You need to enable this plugin so that Pulsar specific libraries are present in the classpath.

Enable the Pulsar plugin with the following config at the time of Pinot setup:
`-Dplugins.include=pinot-pulsar`

{% hint style="info" %}
The `pinot-pulsar` plugin is not part of official 0.10.0 binary. You can download the plugin from [our external repository](https://repo.startreedata.io/artifactory/external-snapshots/org/apache/pinot/pinot-pulsar/0.11.0-SNAPSHOT/) and add it to the `libs` or `plugins` directory in pinot.
{% endhint %}

## Set up Pulsar table

Here is a sample Pulsar stream config. You can use the `streamConfigs` section from this sample and make changes for your corresponding table.

```json
{
  "tableName": "pulsarTable",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "timestamp",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "pulsar",
      "stream.pulsar.topic.name": "<your pulsar topic name>",
      "stream.pulsar.bootstrap.servers": "pulsar://localhost:6650,pulsar://localhost:6651",
      "stream.pulsar.consumer.prop.auto.offset.reset" : "smallest",
      "stream.pulsar.consumer.type": "lowlevel",
      "stream.pulsar.fetch.timeout.millis": "30000",
      "stream.pulsar.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
      "stream.pulsar.consumer.factory.class.name": "org.apache.pinot.plugin.stream.pulsar.PulsarConsumerFactory",
      "realtime.segment.flush.threshold.rows": "1000000",
      "realtime.segment.flush.threshold.time": "6h"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

## Pulsar configuration options

You can change the following Pulsar specifc configurations for your tables

| Property                          | Description                                   |
| --------------------------------- | --------------------------------------------- |
| `streamType`                      | This should be set to "pulsar"                |
| `stream.pulsar.topic.name`        | Your pulsar topic name                        |
| `stream.pulsar.bootstrap.servers` | Comma-separated broker list for Apache Pulsar |
| `stream.pulsar.metadata.populate` | set to `true` to populate metadata            |
| `stream.pulsar.metadata.fields`    | set to comma separated list of metadata fields|

### Authentication

The Pinot-Pulsar connector supports authentication using the security tokens. You can generate the token by following the [official Pulsar documentaton](https://pulsar.apache.org/docs/en/security-token-client/). Once generated, you can add the following property to `streamConfigs` to add auth token for each request

```
"stream.pulsar.authenticationToken":"your-auth-token"
```

### TLS support

The Pinot-pulsar connector also supports TLS for encrypted connections. You can follow [the official pulsar documentation](https://pulsar.apache.org/docs/en/security-tls-transport/) to enable TLS on your pulsar cluster. Once done, you can enable TLS in pulsar connector by providing the trust certificate file location generated in the previous step.

```
"stream.pulsar.tlsTrustCertsFilePath": "/path/to/ca.cert.pem"
```

Also, make sure to change the brokers url from `pulsar://localhost:6650` to `pulsar+ssl://localhost:6650` so that secure connections are used.



For other table and stream configurations, you can headover to [Table configuration Reference](../../../configuration-reference/table.md)

### Supported Pulsar versions

Pinot currently relies on Pulsar client version 2.7.2. Make sure the Pulsar broker is compatible with the this client version.

#### Extract record headers as Pinot table columns

Pinot's Pulsar connector supports automatically extracting record headers and metadata into the Pinot table columns. Pulsar supports a large amount of per-record metadata. Please reference the [official Pulsar documentation](https://pulsar.apache.org/docs/en/concepts-messaging/#message-properties) for the meaning of the metadata fields.

The following table shows the mapping for record header/metadata to Pinot table column names:


| Pulsar Message                    | Pinot table Column                            | Comments                            | Available By Default |
| ----------------------------------| --------------------------------------------- | ----------------------------------- | ---- |
| key : String                      | `__key` : String                              |                                     | Yes  |
| properties : Map<String, String>  | Each header key is listed as a separate column: `__header$HeaderKeyName` : String | | Yes  |
| publishTime : Long                | `__metadata$publishTime` : String             | publish time as determined by the producer |  Yes  |
| brokerPublishTime: Optional<Long> | `__metadata$brokerPublishTime` : String       | publish time as determined by the broker | Yes  |
| eventTime : Long                  | `__metadata$eventTime` : String               |                                     | Yes  |
| messageId : MessageId -> String   | `__metadata$messageId` : String               | String representation of the MessagId field. The format is ledgerId:entryId:partitionIndex |      |
| messageId :  MessageId -> bytes   | `__metadata$messageBytes` : String            | Base64 encoded version of the bytes returned from calling MessageId.toByteArray() |      |
| producerName : String             | `__metadata$producerName` : String            |                                     |      |
| schemaVersion : byte[]            | `__metadata$schemaVersion` : String           | Base64 encoded value                |      |
| sequenceId : Long                 | `__metadata$sequenceId` : String              |                                     |      |
| orderingKey : byte[]              | `__metadata$orderingKey` : String             | Base64 encoded value                |      |
| size : Integer                    | `__metadata$size` : String                    |                                     |      |
| topicName : String                | `__metadata$topicName` : String               |                                     |      |
| index : String                    | `__metadata$index` : String                   |                                     |      |
| redeliveryCount : Integer         | `__metadata$redeliveryCount` : String         |                                     |      |


In order to enable the metadata extraction in a Pulsar table, set the stream config `metadata.populate` to `true`. 
The fields `eventTime`, `publishTime`, `brokerPublishTime`, and `key` are populated by default. If you would like to extract additional fields from the Pulsar Message, populate the `metadataFields` config with a comma separated list of fields to populate. The fields are referenced by the field name in the Pulsar Message.  For example, setting:

```json

"streamConfigs": {
  ...
        "stream.pulsar.metadata.populate": "true",
        "stream.pulsar.metadata.fields": "messageId,messageIdBytes,eventTime,topicName",
  ...
}
```

 Will make the `__metadata$messageId`, `__metadata$messageBytes`, `__metadata$eventTime`, and `__metadata$topicName`, fields available for mapping to columns in the Pinot schema.



In addition to this, if you want to use any of these columns in your table, you have to list them explicitly in your table's schema.

For example, if you want to add only the offset and key as dimension columns in your Pinot table, it can listed in the schema as follows:

```json
  "dimensionFieldSpecs": [
    {
      "name": "__key",
      "dataType": "STRING"
    },
    {
      "name": "__metadata$messageId",
      "dataType": "STRING"
    },
    ...
  ],
```

Once the schema is updated, these columns are similar to any other pinot column. You can apply  ingestion transforms and / or define indexes on them.

{% hint style="info" %}
Remember to follow the [schema evolution guidelines](../../../users/tutorials/schema-evolution.md) when updating schema of an existing table!
{% endhint %}