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
| `stream.pulsar.bootstrap.servers` | Comma-seperated broker list for Apache Pulsar |

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
