---
description: >-
  This guide shows you how to ingest a stream of records from an Apache Pulsar
  topic into a Pinot table.
---

# Ingest streaming data from Apache Pulsar

Pinot supports consuming data from [Apache Pulsar](https://pulsar.apache.org) via the `pinot-pulsar` plugin. You need to enable this plugin so that Pulsar specific libraries are present in the classpath.

Enable the Pulsar plugin with the following config at the time of Pinot setup: `-Dplugins.include=pinot-pulsar`

{% hint style="info" %}
The `pinot-pulsar` plugin is included in the official binary distribution since Pinot 0.11.0. If you are running an older version, you can download the plugin from [the Apache Pinot external repository](https://repo.startreedata.io/artifactory/external-snapshots/org/apache/pinot/pinot-pulsar/) and add it to the `plugins` directory.
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

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`streamType`</td>
      <td>This should be set to "pulsar"</td>
    </tr>
    <tr>
      <td>`stream.pulsar.topic.name`</td>
      <td>Your pulsar topic name</td>
    </tr>
    <tr>
      <td>`stream.pulsar.bootstrap.servers`</td>
      <td>Comma-separated broker list for Apache Pulsar</td>
    </tr>
    <tr>
      <td>`stream.pulsar.metadata.populate`</td>
      <td>set to `true` to populate metadata</td>
    </tr>
    <tr>
      <td>`stream.pulsar.metadata.fields`</td>
      <td>set to comma separated list of metadata fields</td>
    </tr>
  </tbody>
</table>

### Authentication

The Pinot-Pulsar connector supports authentication using security tokens. To generate a token, follow the instructions in [Pulsar documentation](https://pulsar.apache.org/docs/en/security-jwt). Once generated, add the following property to `streamConfigs` to add an authentication token for each request:

```
"stream.pulsar.authenticationToken":"your-auth-token"
```

### OAuth2 Authentication

The Pinot-Pulsar connector supports authentication using OAuth2, for example, if connecting to a StreamNative Pulsar cluster. For more information, see how to [Configure OAuth2 authentication in Pulsar clients](https://pulsar.apache.org/docs/en/security-oauth2/#configure-oauth2-authentication-in-pulsar-clients). Once configured, you can add the following properties to `streamConfigs`:

```
"stream.pulsar.issuerUrl": "https://auth.streamnative.cloud"
"stream.pulsar.credsFilePath": "file:///path/to/private_creds_file
"stream.pulsar.audience": "urn:sn:pulsar:test:test-cluster"
```

### TLS support

The Pinot-pulsar connector also supports TLS for encrypted connections. You can follow [the official pulsar documentation](https://pulsar.apache.org/docs/en/security-tls-transport/) to enable TLS on your pulsar cluster. Once done, you can enable TLS in pulsar connector by providing the trust certificate file location generated in the previous step.

```
"stream.pulsar.tlsTrustCertsFilePath": "/path/to/ca.cert.pem"
```

Also, make sure to change the brokers url from `pulsar://localhost:6650` to `pulsar+ssl://localhost:6650` so that secure connections are used.

For other table and stream configurations, you can headover to [Table configuration Reference](../../../configuration-reference/table.md)

### Supported Pulsar versions

Pinot currently relies on Pulsar client version 4.0.x. Make sure the Pulsar broker is compatible with this client version.

#### Extract record headers as Pinot table columns

Pinot's Pulsar connector supports automatically extracting record headers and metadata into the Pinot table columns. Pulsar supports a large amount of per-record metadata. Reference the [official Pulsar documentation](https://pulsar.apache.org/docs/en/concepts-messaging/#message-properties) for the meaning of the metadata fields.

The following table shows the mapping for record header/metadata to Pinot table column names:

<table>
  <thead>
    <tr>
      <th>Pulsar Message</th>
      <th>Pinot table Column</th>
      <th>Comments</th>
      <th>Available By Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>key : String</td>
      <td>`__key` : String</td>
      <td></td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>properties : Map\<String, String></td>
      <td>Each header key is listed as a separate column: `__header$HeaderKeyName` : String</td>
      <td></td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>publishTime : Long</td>
      <td>`__metadata$publishTime` : String</td>
      <td>publish time as determined by the producer</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>brokerPublishTime: Optional</td>
      <td>`__metadata$brokerPublishTime` : String</td>
      <td>publish time as determined by the broker</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>eventTime : Long</td>
      <td>`__metadata$eventTime` : String</td>
      <td></td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>messageId : MessageId -> String</td>
      <td>`__metadata$messageId` : String</td>
      <td>String representation of the MessagId field. The format is ledgerId:entryId:partitionIndex</td>
      <td></td>
    </tr>
    <tr>
      <td>messageId : MessageId -> bytes</td>
      <td>`__metadata$messageBytes` : String</td>
      <td>Base64 encoded version of the bytes returned from calling MessageId.toByteArray()</td>
      <td></td>
    </tr>
    <tr>
      <td>producerName : String</td>
      <td>`__metadata$producerName` : String</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>schemaVersion : byte\[]</td>
      <td>`__metadata$schemaVersion` : String</td>
      <td>Base64 encoded value</td>
      <td></td>
    </tr>
    <tr>
      <td>sequenceId : Long</td>
      <td>`__metadata$sequenceId` : String</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>orderingKey : byte\[]</td>
      <td>`__metadata$orderingKey` : String</td>
      <td>Base64 encoded value</td>
      <td></td>
    </tr>
    <tr>
      <td>size : Integer</td>
      <td>`__metadata$size` : String</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>topicName : String</td>
      <td>`__metadata$topicName` : String</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>index : String</td>
      <td>`__metadata$index` : String</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>redeliveryCount : Integer</td>
      <td>`__metadata$redeliveryCount` : String</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

In order to enable the metadata extraction in a Pulsar table, set the stream config `metadata.populate` to `true`. The fields `eventTime`, `publishTime`, `brokerPublishTime`, and `key` are populated by default. If you would like to extract additional fields from the Pulsar Message, populate the `metadataFields` config with a comma separated list of fields to populate. The fields are referenced by the field name in the Pulsar Message. For example, setting:

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

Once the schema is updated, these columns are similar to any other pinot column. You can apply ingestion transforms and / or define indexes on them.

{% hint style="info" %}
Remember to follow the [schema evolution guidelines](../../../tutorials/data-ingestion/schema-evolution.md) when updating schema of an existing table!
{% endhint %}
